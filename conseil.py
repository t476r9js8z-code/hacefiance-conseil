#!/usr/bin/env python3
"""Conseil Hacéfiance — orchestration d'un dialogue continu entre plusieurs IA.

Aucune dépendance hors de la bibliothèque standard (Python 3.11 ou plus récent).
Usage : python conseil.py --help
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ICI = Path(__file__).resolve().parent
SIEGES = {"proche", "initie", "etranger", "hors-table"}
NOM_SIEGE = {"proche": "proche", "initie": "initié", "etranger": "étranger", "hors-table": "hors table"}
TEXTE_SIEGE = {
    "proche": (
        "Ton siège : le proche. Tu connais l'auteur et l'historique de vos échanges. "
        "Dis-le quand cela oriente ta réponse, et méfie-toi d'en devenir l'écho."
    ),
    "initie": (
        "Ton siège : l'initié. Tu as reçu le corpus du cadre (texte central, sujets publiés, carnet de travail). "
        "Il est critiquable et extensible : discute-le, ne te contente pas de le répéter."
    ),
    "etranger": (
        "Ton siège : l'étranger. Tu ne reçois ni le corpus ni l'état du fil, seulement la question. "
        "Réponds à partir de ta propre pensée, sans chercher à deviner le cadre dont il est question."
    ),
}


# --------------------------------------------------------------------------- outils


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def ecrire(p: Path, texte: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texte, encoding="utf-8", newline="\n")


def empreinte(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def maintenant() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def slugifier(texte: str, maxi: int = 48) -> str:
    t = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    return (t[:maxi].rstrip("-")) or "seance"


def version_git(racine: Path) -> str:
    """Commit courant d'un dépôt, pour savoir exactement quel corpus a été lu."""
    git = shutil.which("git")
    if not git or not racine.exists():
        return "inconnue"
    try:
        r = subprocess.run([git, "-C", str(racine), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or "hors git"
    except Exception:  # noqa: BLE001
        return "inconnue"


def erreur(message: str) -> None:
    print(f"Erreur : {message}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- configuration


class Conseil:
    def __init__(self, chemin_config: Path, simulation: bool = False):
        self.chemin_config = chemin_config
        self.base = chemin_config.parent
        with open(chemin_config, "rb") as f:
            self.cfg = tomllib.load(f)
        c = self.cfg.get("conseil", {})
        self.fil = (self.base / c.get("fil", "fil")).resolve()
        self.longueur = c.get("longueur", "600 à 1200 mots")
        self.longueur_etat = c.get("longueur_etat", "1200 mots")
        self.cartographe_id = c.get("cartographe", "") or ""
        self.delai = int(c.get("delai_secondes", 900))
        self.simulation = simulation
        self.participants = []
        for p in self.cfg.get("participant", []):
            if p.get("siege") not in SIEGES:
                erreur(f"siège inconnu pour {p.get('id')} : {p.get('siege')}")
            self.participants.append(p)
        ids = [p["id"] for p in self.participants]
        if len(ids) != len(set(ids)):
            erreur("deux participants portent le même id")
        if self.cartographe_id and self.cartographe_id not in ids:
            erreur(f"cartographe « {self.cartographe_id} » absent des participants")
        self.consignes = self.base / "consignes"
        self.etat_fichier = self.fil / "etat-du-fil.md"
        self.journal_fichier = self.fil / "journal.md"
        self.memoire_fichier = self.fil / "memoire.json"

    # -- mémoire des fils persistants : version du corpus déjà reçue par chacun
    def memoire(self) -> dict:
        if self.memoire_fichier.exists():
            return json.loads(lire(self.memoire_fichier))
        return {}

    def memoriser(self, pid: str, version: str | None) -> None:
        m = self.memoire()
        if version is None:
            m.pop(pid, None)
        else:
            m[pid] = {"corpus": version, "date": maintenant()}
        ecrire(self.memoire_fichier, json.dumps(m, ensure_ascii=False, indent=2) + "\n")

    # -- participants
    def table(self) -> list[dict]:
        return [p for p in self.participants if p["siege"] != "hors-table"]

    def participant(self, pid: str) -> dict:
        for p in self.participants:
            if p["id"] == pid:
                return p
        erreur(f"participant inconnu : {pid}")

    def consigne(self, nom: str) -> str:
        return lire(self.consignes / f"{nom}.md")

    # -- état du fil
    def etat(self) -> str:
        if self.etat_fichier.exists():
            t = lire(self.etat_fichier).strip()
            if t:
                return t
        return "Le fil commence : il n'y a pas encore d'état. Cette séance est la première."

    # -- journal (en ajout seulement)
    def journaliser(self, ligne: str) -> None:
        self.fil.mkdir(parents=True, exist_ok=True)
        if not self.journal_fichier.exists():
            ecrire(self.journal_fichier, "# Journal du conseil\n\n*Registre en ajout seulement : chaque réponse versée au fil, avec son empreinte SHA-256.*\n\n")
        with open(self.journal_fichier, "a", encoding="utf-8", newline="\n") as f:
            f.write(f"- {maintenant()} · {ligne}\n")

    # -- corpus
    def dossier(self, p: dict) -> tuple[str, list[tuple[str, int, bool]]]:
        """Assemble le dossier d'initiation d'un participant. Renvoie le texte et un manifeste."""
        if p["siege"] == "etranger":
            return "", []
        corpus = self.cfg.get("corpus", {})
        budget = int(p.get("budget_caracteres", corpus.get("budget_caracteres", 400000)))
        morceaux, manifeste, total, vus = [], [], 0, set()
        for src in corpus.get("sources", []):
            racine = (self.base / src["chemin"]).resolve()
            if not racine.exists():
                manifeste.append((f"{src['chemin']} (introuvable)", 0, False))
                continue
            for motif in src.get("motifs", ["**/*.md"]):
                for f in sorted(racine.glob(motif)):
                    if not f.is_file() or f in vus:
                        continue
                    if any(fnmatch.fnmatch(f.name, e) for e in src.get("exclure", [])):
                        continue
                    vus.add(f)
                    rel = f"{Path(src['chemin']).name}/{f.relative_to(racine).as_posix()}"
                    contenu = lire(f)
                    if total + len(contenu) > budget:
                        manifeste.append((rel, len(contenu), False))
                        continue
                    morceaux.append(f"===== {rel} =====\n\n{contenu.strip()}\n")
                    manifeste.append((rel, len(contenu), True))
                    total += len(contenu)
        return "\n".join(morceaux), manifeste


# --------------------------------------------------------------------------- séances


class Seance:
    def __init__(self, conseil: Conseil, dossier: Path):
        self.c = conseil
        self.dir = dossier
        self.meta_fichier = dossier / "seance.json"
        if not self.meta_fichier.exists():
            erreur(f"pas de seance.json dans {dossier}")
        self.meta = json.loads(lire(self.meta_fichier))

    @property
    def nom(self) -> str:
        return self.dir.name

    def sauver(self) -> None:
        ecrire(self.meta_fichier, json.dumps(self.meta, ensure_ascii=False, indent=2) + "\n")

    def question(self) -> str:
        return lire(self.dir / "00-question.md").split("\n", 2)[-1].strip()

    def lettre(self, pid: str) -> str:
        return self.meta["lettres"][pid]

    def reponse_fichier(self, tour: int, pid: str) -> Path:
        return self.dir / f"tour-{tour}" / f"{pid}.md"

    def reponse(self, tour: int, pid: str) -> str | None:
        f = self.reponse_fichier(tour, pid)
        return lire(f) if f.exists() and lire(f).strip() else None

    def membres(self) -> list[dict]:
        return [self.c.participant(pid) for pid in self.meta["participants"]]

    def verser(self, tour: int, p: dict, texte: str, source: str) -> None:
        f = self.reponse_fichier(tour, p["id"])
        ecrire(f, texte.strip() + "\n")
        self.enregistrer(tour, p, source)

    def enregistrer(self, tour: int, p: dict, source: str) -> None:
        cle = f"{tour}/{p['id']}"
        if cle in self.meta.setdefault("journalise", []):
            return
        texte = lire(self.reponse_fichier(tour, p["id"]))
        self.c.journaliser(
            f"séance {self.nom} · tour {tour} · {p['id']} ({self.lettre(p['id'])}) · {source} · "
            f"tour-{tour}/{p['id']}.md · sha256:{empreinte(texte)[:16]}"
        )
        self.meta["journalise"].append(cle)
        envoye = self.meta.get("dossier_envoye", {}).get(f"{tour}/{p['id']}")
        if envoye and p.get("fil_persistant"):
            self.c.memoriser(p["id"], envoye)
        self.sauver()

    def cibles(self, tour: int) -> list[dict]:
        """Participants appelés à ce tour : tous aux tours 1 et 2, les destinataires de questions ensuite."""
        if tour in (1, 2):
            return self.membres()
        ids = {q["cible"] for q in questions_du_tour(self, tour - 1) if q["cible"] != "Fabien"}
        return [m for m in self.membres() if m["id"] in ids]

    def complet(self, tour: int) -> bool:
        return all(self.reponse(tour, p["id"]) for p in self.cibles(tour))

    def par_lettre(self, lettre: str) -> str | None:
        for pid, l in self.meta["lettres"].items():
            if l == lettre:
                return pid
        return None


def seances(conseil: Conseil) -> list[Path]:
    if not conseil.fil.exists():
        return []
    dossiers = [d for d in conseil.fil.iterdir() if d.is_dir() and (d / "seance.json").exists()]
    return sorted(dossiers, key=lambda d: json.loads(lire(d / "seance.json")).get("numero", 0))


def seance_courante(conseil: Conseil, nom: str | None) -> Seance:
    if nom:
        d = conseil.fil / nom
        if not d.exists():
            erreur(f"séance introuvable : {nom}")
        return Seance(conseil, d)
    toutes = seances(conseil)
    if not toutes:
        erreur("aucune séance : commence par « nouvelle »")
    return Seance(conseil, toutes[-1])


# --------------------------------------------------------------------------- adaptateurs


class EnAttente(Exception):
    """La réponse doit être relayée à la main (ou par Chrome)."""


def appeler(conseil: Conseil, p: dict, s: Seance, tour: int, systeme: str, consigne: str,
            dossier: str, contexte: dict) -> str:
    """Appelle un participant et renvoie sa réponse, ou lève EnAttente."""
    mode = "simulation" if conseil.simulation else p.get("adaptateur", "manuel")
    if p["siege"] == "etranger":
        systeme, consigne = neutraliser(systeme), neutraliser(consigne)
    complet = consigne.replace("{dossier}", corpus_integre(dossier) if dossier else contexte.get("note_dossier", ""))

    if mode == "simulation":
        return simuler(p, tour, contexte)

    if mode == "manuel":
        relais = s.dir / "relais"
        base = f"{p['id']}-tour-{tour}"
        if p.get("joindre_dossier") and dossier:
            ecrire(relais / f"{base}.dossier.md", dossier)
            texte = consigne.replace("{dossier}", "Le corpus du cadre est joint à ce message (fichier « dossier »).")
        else:
            texte = complet
        ecrire(relais / f"{base}.consigne.md", f"{systeme.strip()}\n\n---\n\n{texte.strip()}\n")
        raise EnAttente(
            f"à relayer : {relais / (base + '.consigne.md')}"
            + (f" (+ {base}.dossier.md en pièce jointe)" if p.get("joindre_dossier") and dossier else "")
            + f" → déposer la réponse dans {s.reponse_fichier(tour, p['id'])}"
            + (f" — {p['relais']}" if p.get("relais") else "")
        )

    if mode == "api":
        return appeler_api(conseil, p, systeme, complet)

    if mode == "commande":
        return appeler_commande(conseil, p, systeme, complet)

    erreur(f"adaptateur inconnu pour {p['id']} : {mode}")


def neutraliser(texte: str) -> str:
    """Retire des consignes le nom du cadre, pour que l'étranger ne puisse pas le retrouver."""
    texte = texte.replace("Conseil Hacéfiance", "Conseil de réflexion")
    texte = texte.replace(", auteur du cadre et seule instance de décision", ", seule instance de décision")
    return re.sub(r"(?i)hac[ée]fiance", "ce cadre", texte)


def corpus_integre(dossier: str) -> str:
    if not dossier:
        return ""
    return "## Corpus\n\n" + dossier


def appeler_api(conseil: Conseil, p: dict, systeme: str, consigne: str) -> str:
    cle = os.environ.get(p.get("cle_env", ""), "")
    if not cle:
        raise RuntimeError(f"variable d'environnement {p.get('cle_env')} absente pour {p['id']}")
    corps = {
        "model": p["modele"],
        "messages": [{"role": "system", "content": systeme}, {"role": "user", "content": consigne}],
    }
    if "temperature" in p:
        corps["temperature"] = p["temperature"]
    corps.update(p.get("extra", {}))  # options propres au fournisseur (ex. recherche web d'OpenRouter)
    req = urllib.request.Request(
        p["base"].rstrip("/") + "/chat/completions",
        data=json.dumps(corps).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {cle}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=conseil.delai) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API {p['id']} : HTTP {e.code} {e.read().decode('utf-8', 'replace')[:500]}")
    return data["choices"][0]["message"]["content"]


def appeler_commande(conseil: Conseil, p: dict, systeme: str, consigne: str) -> str:
    """Lance un outil en ligne de commande dans un dossier vide, consigne sur l'entrée standard."""
    gabarit = list(p["commande"])
    exe = shutil.which(gabarit[0])
    if not exe:
        raise RuntimeError(f"outil introuvable pour {p['id']} : {gabarit[0]}")
    with tempfile.TemporaryDirectory(prefix="conseil-") as bac:
        bac = Path(bac)
        sortie = bac / "reponse.md"
        fichier_systeme = bac / "systeme.md"
        ecrire(fichier_systeme, systeme)
        args = [exe] + [a.replace("{sortie}", str(sortie)).replace("{systeme}", str(fichier_systeme)) for a in gabarit[1:]]
        systeme_passe = any("{systeme}" in a for a in gabarit)
        entree = consigne if systeme_passe else f"{systeme.strip()}\n\n---\n\n{consigne}"
        r = subprocess.run(
            args, input=entree, capture_output=True, text=True, encoding="utf-8",
            errors="replace", cwd=bac, timeout=conseil.delai,
        )
        if r.returncode != 0:
            raise RuntimeError(f"{p['id']} a échoué (code {r.returncode}) : {(r.stderr or r.stdout)[-800:]}")
        if any("{sortie}" in a for a in gabarit):
            if not sortie.exists():
                raise RuntimeError(f"{p['id']} n'a pas écrit de réponse dans {{sortie}}")
            return lire(sortie)
        return r.stdout


def simuler(p: dict, tour, ctx: dict) -> str:
    rnd = random.Random(f"{p['id']}-{tour}-{ctx.get('seance')}")
    if tour == 1:
        return (
            f"[Réponse simulée de {p['nom']}, siège {p['siege']}.]\n\n"
            f"Sur la question posée, je soutiens que le compas naît du couplage et non d'une règle. "
            f"{'Je n’ai pas lu le corpus. ' if p['siege'] == 'etranger' else 'Le corpus le dit, mais trop vite. '}"
            f"Argument n° {rnd.randint(1, 99)}.\n\nQuestion ouverte : que vaut un compas sans canal de retour ?"
        )
    autres = ctx.get("autres_lettres", [])
    if tour in (3, 4):
        relance = []
        if tour == 3 and autres and rnd.random() < 0.5:
            relance = [{"cible": rnd.choice(autres), "question": "Peux-tu préciser ce que tu entends par canal ?"}]
        decl = {"repond_a": ctx.get("questions_de", []), "questions": relance}
        return (f"[Réponses simulées de {p['nom']} ({ctx.get('lettre')}) aux questions de "
                f"{', '.join(ctx.get('questions_de', []))}.]\n\n```json\n{json.dumps(decl, ensure_ascii=False)}\n```\n")
    cible_a = rnd.choice(autres) if autres else "?"
    cible_r = rnd.choice([x for x in autres if x != cible_a] or autres or ["?"])
    change = rnd.random() < 0.4
    questions = []
    if rnd.random() < 0.6 and autres:
        questions.append({"cible": rnd.choice(autres), "question": "Qu'est-ce qui, chez toi, distingue la place de l'expérience ?"})
    if rnd.random() < 0.3:
        questions.append({"cible": "Fabien", "question": "Le compas d'un collectif peut-il se tromper de tout ?"})
    decl = {
        "accepte": [{"cible": cible_a, "point": "l'idée que le canal précède la règle"}],
        "rejette": [{"cible": cible_r, "point": "la confusion entre place et expérience", "raison": "elle suppose ce qu'elle veut montrer"}],
        "revision": {"change": change, "avant": "le compas est une règle" if change else "", "apres": "le compas est un couplage" if change else "", "argument_decisif": cible_a if change else ""},
        "faits": [{"cible": cible_r, "affirmation": "date citée de mémoire", "doute": "non vérifiée"}] if ctx.get("verificateur") else [],
        "questions": questions,
        "question_ouverte": "ce qu'ajoute la révélation au ressenti",
    }
    return (
        f"[Lecture croisée simulée de {p['nom']} ({ctx.get('lettre')}).]\n\n"
        f"Je retiens chez {cible_a} l'antériorité du canal ; je refuse chez {cible_r} une confusion.\n\n"
        f"```json\n{json.dumps(decl, ensure_ascii=False, indent=2)}\n```\n"
    )


# --------------------------------------------------------------------------- tours

MAX_QUESTIONS = {2: 2, 3: 1}  # questions permises par participant : lecture croisée, puis relance unique


def questions_du_tour(s: Seance, tour: int) -> list[dict]:
    """Questions posées dans les déclarations d'un tour (2 = lecture croisée, 3 = relances)."""
    if tour not in MAX_QUESTIONS:
        return []
    sortie = []
    for m in s.membres():
        d = extraire_declaration(s.reponse(tour, m["id"]) or "") or {}
        qs = [q for q in (d.get("questions") or []) if isinstance(q, dict) and str(q.get("question", "")).strip()]
        for q in qs[: MAX_QUESTIONS[tour]]:
            cible = str(q.get("cible", "")).strip()
            texte = str(q["question"]).strip()
            if cible.lower() in ("fabien", "l'auteur", "auteur"):
                sortie.append({"de": m["id"], "cible": "Fabien", "question": texte, "tour": tour})
            elif cible.lower() in ("tous", "toutes", "*"):
                for autre in s.membres():
                    if autre["id"] != m["id"]:
                        sortie.append({"de": m["id"], "cible": autre["id"], "question": texte, "tour": tour})
            else:
                pid = s.par_lettre(cible.upper()[:1]) if cible else None
                if pid and pid != m["id"]:
                    sortie.append({"de": m["id"], "cible": pid, "question": texte, "tour": tour})
    return sortie


def executer_tour(conseil: Conseil, s: Seance, tour: int, seulement: list[str] | None = None) -> dict:
    if tour > 1 and not s.complet(tour - 1):
        manquants = [p["id"] for p in s.cibles(tour - 1) if not s.reponse(tour - 1, p["id"])]
        print(f"Le tour {tour - 1} n'est pas complet (manquent : {', '.join(manquants)}).")
        return {"attente": manquants}
    systeme = conseil.consigne("systeme")
    bilan = {"faits": [], "attente": [], "erreurs": []}
    for p in s.cibles(tour):
        if seulement and p["id"] not in seulement:
            continue
        if s.reponse(tour, p["id"]):
            s.enregistrer(tour, p, "relais" if p.get("adaptateur") == "manuel" else "existant")
            continue
        consigne, dossier, ctx = preparer(conseil, s, tour, p)
        try:
            texte = appeler(conseil, p, s, tour, systeme, consigne, dossier, ctx)
        except EnAttente as e:
            bilan["attente"].append(p["id"])
            print(f"  … {p['id']} : {e}")
            continue
        except Exception as e:  # noqa: BLE001 — on consigne et on continue avec les autres
            bilan["erreurs"].append(p["id"])
            ecrire(s.dir / "relais" / f"{p['id']}-tour-{tour}.erreur.txt", f"{maintenant()}\n{e}\n")
            print(f"  ✗ {p['id']} : {e}")
            continue
        s.verser(tour, p, texte, "simulation" if conseil.simulation else p.get("adaptateur", "?"))
        bilan["faits"].append(p["id"])
        print(f"  ✓ {p['id']} : tour {tour} versé")
    return bilan


def choisir_dossier(conseil: Conseil, s: Seance, tour: int, p: dict) -> tuple[str, str]:
    """Décide si le corpus part avec la consigne. Renvoie (dossier, note qui le remplace sinon)."""
    dossier, _ = conseil.dossier(p)
    if not dossier:
        return "", ""
    if p.get("dossier_dans_sources"):
        return "", ("Le corpus du cadre se trouve dans les sources de ce projet (dossier-hacefiance.md). "
                    "Lis-le en entier avant de répondre, pas seulement les passages qu'une recherche ferait remonter.")
    if p.get("fil_persistant"):
        version = empreinte(dossier)[:16]
        if tour != 1:
            return "", "Le corpus est celui que tu as reçu dans cette discussion."
        if conseil.memoire().get(p["id"], {}).get("corpus") == version:
            return "", "Tu as déjà reçu le corpus dans cette discussion, et il n'a pas changé depuis."
        s.meta.setdefault("dossier_envoye", {})[f"1/{p['id']}"] = version
        s.sauver()
    return dossier, ""


def preparer(conseil: Conseil, s: Seance, tour: int, p: dict) -> tuple[str, str, dict]:
    siege = TEXTE_SIEGE[p["siege"]]
    dossier, note = choisir_dossier(conseil, s, tour, p)
    ctx = {"seance": s.nom, "lettre": s.lettre(p["id"]), "note_dossier": note}
    if tour == 1:
        etat = conseil.etat() if p["siege"] != "etranger" else "(Tu ne reçois pas l'état du fil.)"
        consigne = conseil.consigne("tour1").format(
            seance=s.nom, siege=siege, etat=etat, question=s.question(),
            longueur=conseil.longueur, dossier="{dossier}",
        )
        return consigne, dossier, ctx
    if tour == 2:
        # lecture croisée, ordre des autres propre à chaque lecteur
        autres = [m for m in s.membres() if m["id"] != p["id"]]
        random.Random(f"{s.meta['graine']}-{p['id']}").shuffle(autres)
        blocs = "\n\n".join(f"### Participant {s.lettre(m['id'])}\n\n{masquer(s.reponse(1, m['id']).strip())}" for m in autres)
        verif = ""
        if s.meta.get("verificateur") == p["id"]:
            verif = (
                "\nTu es aussi le vérificateur de cette séance : si des affirmations factuelles des autres te paraissent "
                "douteuses, signale-les avec la raison du doute, et reporte-les dans le champ « faits » du bloc final.\n"
            )
            ctx["verificateur"] = True
        consigne = conseil.consigne("tour2").format(
            seance=s.nom, siege=siege, lettre=s.lettre(p["id"]), question=s.question(),
            propre=s.reponse(1, p["id"]).strip(), autres=blocs, longueur=conseil.longueur, verification=verif,
        )
        consigne += "\n{dossier}"
        ctx["autres_lettres"] = [s.lettre(m["id"]) for m in autres]
        return consigne, dossier, ctx
    # tours 3 et 4 : réponses aux questions reçues
    recues = [q for q in questions_du_tour(s, tour - 1) if q["cible"] == p["id"]]
    blocs = []
    for q in recues:
        de = s.lettre(q["de"])
        blocs.append(f"### Question de {de}\n\n> {q['question']}\n\n**Ce que {de} a écrit au tour précédent :**\n\n"
                     f"{masquer((s.reponse(tour - 1, q['de']) or '').strip())}")
    relance = ("Si une réponse appelle une précision, tu peux poser au plus une question de relance dans le champ "
               "« questions » ; elle recevra une réponse au tour suivant." if tour == 3 else
               "C'est le dernier tour de questions de cette séance : n'en pose pas de nouvelle.")
    consigne = conseil.consigne("reponses").format(
        seance=s.nom, siege=siege, lettre=s.lettre(p["id"]), question=s.question(),
        questions="\n\n".join(blocs), relance=relance, rang="premier tour" if tour == 3 else "relances",
    )
    consigne += "\n{dossier}"
    ctx["questions_de"] = sorted({s.lettre(q["de"]) for q in recues})
    ctx["autres_lettres"] = [s.lettre(m["id"]) for m in s.membres() if m["id"] != p["id"]]
    return consigne, dossier, ctx


MASQUES = [r"Chat ?GPT(?:-\d+(?:\.\d+)?)?", r"GPT-\d+(?:\.\d+)?(?: Astra)?", r"\bGPT\b", r"OpenAI",
           r"Gemini(?: \d+(?:\.\d+)?)?(?: Pro| Flash)?", r"Google DeepMind", r"Grok(?: \d+)?", r"\bxAI\b",
           r"Claude(?: (?:Opus|Sonnet|Haiku|Fable|Mythos))?(?: \d+(?:\.\d+)?)?", r"Anthropic"]


def masquer(texte: str) -> str:
    """Retire d'un texte relayé les noms des modèles assis à la table, pour préserver l'anonymat."""
    for motif in MASQUES:
        texte = re.sub(motif, "[modèle]", texte)
    return texte


def questions_pour_fabien(s: Seance) -> list[dict]:
    return [q for t in (2, 3) for q in questions_du_tour(s, t) if q["cible"] == "Fabien"]


def ecrire_questions_fabien(conseil: Conseil, s: Seance) -> None:
    qs = questions_pour_fabien(s)
    f = s.dir / "questions-pour-fabien.md"
    if not qs or f.exists():
        return
    lignes = [f"# Questions pour Fabien — séance {s.nom}", "",
              "*Posées par les participants pendant la séance. Tes réponses, si tu en donnes, vont dans "
              "`reponses-de-fabien.md` à côté de ce fichier : elles entreront dans la carte et l'état du fil.*", ""]
    for q in qs:
        lignes.append(f"- **{s.lettre(q['de'])}** (tour {q['tour']}) : {q['question']}")
    ecrire(f, "\n".join(lignes) + "\n")
    conseil.journaliser(f"séance {s.nom} · {len(qs)} question(s) pour Fabien")
    print(f"  ? {len(qs)} question(s) pour Fabien : {f}")


# --------------------------------------------------------------------------- carte


def extraire_declaration(texte: str) -> dict | None:
    blocs = re.findall(r"```json\s*(\{.*?\})\s*```", texte, flags=re.S)
    for b in reversed(blocs):
        try:
            d = json.loads(b)
            if isinstance(d, dict):
                return d
        except json.JSONDecodeError:
            continue
    return None


def carte_mecanique(s: Seance) -> tuple[str, dict]:
    membres = s.membres()
    membres = sorted(membres, key=lambda m: s.lettre(m["id"]))
    nom = {m["id"]: f"{s.lettre(m['id'])} — {m['nom']} ({NOM_SIEGE[m['siege']]})" for m in membres}
    par_lettre = {s.lettre(m["id"]): m for m in membres}
    decl = {m["id"]: extraire_declaration(s.reponse(2, m["id"]) or "") for m in membres}
    l = [f"## Carte mécanique", "",
         "*Assemblée à partir des déclarations des participants, sans interprétation.*", "",
         "| Participant | Accepte | Rejette | A changé de position | Déclaration |",
         "|---|---|---|---|---|"]
    rejets, accords, revisions, faits, questions = [], [], [], [], []
    for m in membres:
        d = decl[m["id"]]
        if d is None:
            l.append(f"| {nom[m['id']]} | – | – | – | illisible ou absente |")
            continue
        acc, rej = d.get("accepte") or [], d.get("rejette") or []
        rev = d.get("revision") or {}
        l.append(f"| {nom[m['id']]} | {len(acc)} | {len(rej)} | {'oui' if rev.get('change') else 'non'} | lue |")
        acc = [a if isinstance(a, dict) else {"point": str(a)} for a in acc]
        rej = [r if isinstance(r, dict) else {"point": str(r)} for r in rej]
        if not isinstance(rev, dict):
            rev = {}
        for a in acc:
            accords.append(f"- **{s.lettre(m['id'])}** retient de **{a.get('cible', '?')}** : {a.get('point', '')}")
        for r in rej:
            rejets.append(f"- **{s.lettre(m['id'])}** rejette chez **{r.get('cible', '?')}** : {r.get('point', '')} — *{r.get('raison', 'sans raison donnée')}*")
        if rev.get("change"):
            revisions.append(f"- **{s.lettre(m['id'])}** passe de « {rev.get('avant', '')} » à « {rev.get('apres', '')} » (argument décisif : {rev.get('argument_decisif', '?')})")
        for f in d.get("faits") or []:
            if not isinstance(f, dict):
                faits.append(f"- **{s.lettre(m['id'])}** signale : {f}")
                continue
            faits.append(f"- **{s.lettre(m['id'])}** met en doute chez **{f.get('cible', '?')}** : {f.get('affirmation', '')} — *{f.get('doute', '')}*")
        if d.get("question_ouverte"):
            questions.append(f"- **{s.lettre(m['id'])}** : {d['question_ouverte']}")
    lues = [d for d in decl.values() if d]
    n_rej = sum(len(d.get("rejette") or []) for d in lues)
    n_chg = sum(1 for d in lues if isinstance(d.get("revision"), dict) and d["revision"].get("change"))
    signaux = []
    if len(lues) >= 3 and n_rej == 0:
        signaux.append("**Convergence suspecte** : aucun rejet déclaré. Désigner un participant pour défendre la position abandonnée.")
    if lues and n_chg == len(lues):
        signaux.append("**Convergence suspecte** : tous les participants déclarent avoir changé de position.")
    if n_chg:
        signaux.append(f"**Tournant possible** : {n_chg} changement(s) de position déclaré(s).")
    if len(lues) < len(membres):
        signaux.append(f"{len(membres) - len(lues)} déclaration(s) illisible(s) ou absente(s) : lire les réponses brutes.")
    qr = []
    for t in (2, 3):
        for q in questions_du_tour(s, t):
            if q["cible"] == "Fabien":
                qr.append(f"- **{s.lettre(q['de'])}** → **Fabien** (tour {t}) : {q['question']}")
                continue
            rep_f = s.reponse_fichier(t + 1, q["cible"])
            statut = f"réponse : `tour-{t + 1}/{q['cible']}.md`" if rep_f.exists() else "*sans réponse*"
            qr.append(f"- **{s.lettre(q['de'])}** → **{s.lettre(q['cible'])}** (tour {t}) : {q['question']} — {statut}")
    fabien = s.dir / "reponses-de-fabien.md"
    if fabien.exists():
        qr.append(f"- Fabien a répondu : `reponses-de-fabien.md`")
    for titre, lignes in (("Rejets", rejets), ("Acceptations", accords), ("Changements de position", revisions),
                          ("Faits signalés", faits), ("Questions et réponses", qr), ("Questions ouvertes", questions),
                          ("Signaux", [f"- {x}" for x in signaux])):
        l += ["", f"### {titre}", ""] + (lignes or ["- aucun"])
    l += ["", "### Intégrité", "", "| Fichier | SHA-256 |", "|---|---|"]
    for t in (1, 2, 3, 4):
        for m in membres:
            texte = s.reponse(t, m["id"])
            if texte:
                l.append(f"| tour-{t}/{m['id']}.md | `{empreinte(lire(s.reponse_fichier(t, m['id'])))[:16]}` |")
    resume = {"rejets": n_rej, "changements": n_chg, "lues": len(lues), "membres": len(membres), "signaux": signaux,
              "questions": len(qr), "questions_fabien": [q["question"] for q in questions_pour_fabien(s)],
              "lettres": {k: v["id"] for k, v in par_lettre.items()}}
    return "\n".join(l) + "\n", resume


def faire_carte(conseil: Conseil, s: Seance, cartographe: str | None, nom_fichier: str = "carte.md") -> str | None:
    if not s.complet(2):
        manquants = [p["id"] for p in s.membres() if not s.reponse(2, p["id"])]
        print(f"La lecture croisée n'est pas complète (manquent : {', '.join(manquants)}).")
        return None
    mecanique, resume = carte_mecanique(s)
    narration = ""
    cid = cartographe if cartographe is not None else conseil.cartographe_id
    if cid:
        cp = conseil.participant(cid)
        if cp["id"] in s.meta["participants"]:
            print(f"  ! {cid} est assis à la table : sa carte n'est pas celle d'un tiers.")
        membres = s.membres()
        consigne = conseil.consigne("carte").format(
            seance=s.nom, question=s.question(),
            sieges="\n".join(f"- {s.lettre(m['id'])} : {NOM_SIEGE[m['siege']]}" for m in sorted(membres, key=lambda m: s.lettre(m['id']))),
            tour1="\n\n".join(f"### {s.lettre(m['id'])}\n\n{s.reponse(1, m['id']).strip()}" for m in sorted(membres, key=lambda m: s.lettre(m['id']))),
            tour2="\n\n".join(f"### {s.lettre(m['id'])}\n\n{s.reponse(2, m['id']).strip()}" for m in sorted(membres, key=lambda m: s.lettre(m['id']))),
            qr="\n\n".join(f"### {s.lettre(m['id'])}, tour {t}\n\n{s.reponse(t, m['id']).strip()}"
                            for t in (3, 4) for m in sorted(membres, key=lambda m: s.lettre(m['id'])) if s.reponse(t, m['id']))
               or "(Aucune question n'a été posée entre participants.)",
        )
        try:
            deja = s.reponse("carte", cid)
            if deja:
                narration = "## Carte du cartographe\n\n" + deja.strip() + "\n"
            elif conseil.simulation:
                narration = "## Carte du cartographe\n\n[Carte simulée.]\n\n7. **Tournant** — simulation : aucun.\n"
            else:
                narration = "## Carte du cartographe\n\n" + appeler(
                    conseil, cp, s, "carte", conseil.consigne("systeme"), consigne, "", {"seance": s.nom}).strip() + "\n"
        except EnAttente as e:
            print(f"  … cartographe : {e}")
            narration = f"## Carte du cartographe\n\n*En attente du relais ({cid}).*\n"
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ cartographe : {e}")
            narration = f"## Carte du cartographe\n\n*Échec : {e}*\n"
    entete = [f"# Carte des désaccords — séance {s.nom}", "", f"**Question** : {s.question()}", "",
              "**Participants** : " + " · ".join(f"{s.lettre(m['id'])} = {m['nom']} ({NOM_SIEGE[m['siege']]})" for m in sorted(s.membres(), key=lambda m: s.lettre(m["id"]))), "",
              f"*Cartographe : {cid or 'aucun (carte mécanique seulement)'} · générée le {maintenant()}*", ""]
    texte = "\n".join(entete) + ("\n" + narration if narration else "") + "\n" + mecanique
    ecrire(s.dir / nom_fichier, texte)
    s.meta.setdefault("cartes", {})[nom_fichier] = {"cartographe": cid, "date": maintenant(), "resume": resume}
    s.sauver()
    conseil.journaliser(f"séance {s.nom} · {nom_fichier} · cartographe {cid or 'mécanique'} · sha256:{empreinte(texte)[:16]}")
    print(f"  ✓ {nom_fichier} écrite")
    for sig in resume["signaux"]:
        print(f"    · {re.sub(r'[*]', '', sig)}")
    return texte


# --------------------------------------------------------------------------- état du fil


def mettre_a_jour_etat(conseil: Conseil, s: Seance) -> None:
    carte_f = s.dir / "carte.md"
    if not carte_f.exists():
        print("Pas encore de carte pour cette séance.")
        return
    carte = lire(carte_f)
    if conseil.cartographe_id and not conseil.simulation:
        cp = conseil.participant(conseil.cartographe_id)
        consigne = conseil.consigne("etat").format(seance=s.nom, etat=conseil.etat(), carte=carte, longueur_etat=conseil.longueur_etat)
        try:
            nouveau = (s.reponse("etat", cp["id"]) or appeler(
                conseil, cp, s, "etat", conseil.consigne("systeme"), consigne, "", {"seance": s.nom})).strip()
        except EnAttente as e:
            print(f"  … état du fil : {e}")
            return
    else:
        resume = s.meta.get("cartes", {}).get("carte.md", {}).get("resume", {})
        ancien = conseil.etat() if conseil.etat_fichier.exists() else ""
        sections = [x for x in re.split(r"(?m)^(?=## Séance )", ancien) if x.startswith("## Séance ")]
        bloc = (f"## Séance {s.nom}\n\n**Question** : {s.question()}\n\n"
                f"Déclarations lues : {resume.get('lues', '?')}/{resume.get('membres', '?')} · rejets : {resume.get('rejets', '?')} · "
                f"changements de position : {resume.get('changements', '?')}.\n"
                + "".join(f"\n- {re.sub(r'[*]', '', x)}" for x in resume.get("signaux", []))
                + "".join(f"\n- Question pour Fabien : {q}" for q in resume.get("questions_fabien", []))
                + f"\n\nCarte complète : `{s.nom}/carte.md`.\n")
        sections = (sections + [bloc])[-6:]
        nouveau = ("# État du fil\n\n*État mécanique : les six dernières séances. Un cartographe hors table "
                   "peut le remplacer par un état rédigé.*\n\n" + "\n".join(x.strip() + "\n" for x in sections))
    ecrire(conseil.etat_fichier, nouveau.strip() + "\n")
    conseil.journaliser(f"séance {s.nom} · état du fil mis à jour · sha256:{empreinte(nouveau)[:16]}")
    print("  ✓ état du fil mis à jour")


# --------------------------------------------------------------------------- commandes


def cmd_nouvelle(conseil: Conseil, a) -> None:
    question = lire(Path(a.fichier)) if a.fichier else (a.question or "")
    if not question.strip():
        erreur("question vide")
    date = dt.date.today().isoformat()
    slug = a.slug or slugifier(question.splitlines()[0])
    d = conseil.fil / f"{date}-{slug}"
    n = 2
    while d.exists():
        d = conseil.fil / f"{date}-{slug}-{n}"
        n += 1
    table = conseil.table()
    if len(table) < 2:
        erreur("il faut au moins deux participants à la table")
    graine = random.SystemRandom().randrange(1, 10**9)
    rnd = random.Random(graine)
    lettres = list(string.ascii_uppercase[: len(table)])
    rnd.shuffle(lettres)
    numero = len(seances(conseil)) + 1
    candidats = sorted(p["id"] for p in table if p["siege"] != "etranger") or [p["id"] for p in table]
    meta = {
        "numero": numero, "creee": maintenant(), "graine": graine,
        "participants": [p["id"] for p in table],
        "lettres": {p["id"]: l for p, l in zip(table, lettres)},
        "verificateur": candidats[(numero - 1) % len(candidats)],
        "journalise": [],
    }
    ecrire(d / "00-question.md", f"# Question\n\n{question.strip()}\n")
    ecrire(d / "seance.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    s = Seance(conseil, d)
    manif = ["# Dossiers d'initiation", "", "*Ce que chaque participant a reçu. Les fichiers non retenus ont dépassé le budget.*", ""]
    for src in conseil.cfg.get("corpus", {}).get("sources", []):
        manif.append(f"- Source `{src['chemin']}` : version {version_git((conseil.base / src['chemin']).resolve())}")
    manif.append("")
    for p in table:
        _, m = conseil.dossier(p)
        manif.append(f"## {p['nom']} ({NOM_SIEGE[p['siege']]})")
        manif.append("")
        if p["siege"] == "etranger":
            manif.append("- rien : la question seule")
        for rel, taille, ok in m:
            manif.append(f"- {'✓' if ok else '✗'} {rel} ({taille} car.)")
        manif.append("")
    ecrire(d / "01-dossiers.md", "\n".join(manif))
    conseil.journaliser(f"séance {s.nom} ouverte · vérificateur {meta['verificateur']}")
    print(f"Séance ouverte : {d}")
    print("Lettres : " + ", ".join(f"{pid}={l}" for pid, l in meta["lettres"].items()))


def cmd_tour(conseil: Conseil, a) -> None:
    s = seance_courante(conseil, a.seance)
    print(f"Séance {s.nom} — tour {a.numero}")
    executer_tour(conseil, s, a.numero, a.seulement.split(",") if a.seulement else None)


def cmd_carte(conseil: Conseil, a) -> None:
    s = seance_courante(conseil, a.seance)
    faire_carte(conseil, s, a.cartographe, a.sortie)


def cmd_etat(conseil: Conseil, a) -> None:
    mettre_a_jour_etat(conseil, seance_courante(conseil, a.seance))


def cmd_seance(conseil: Conseil, a) -> None:
    """Avance la séance aussi loin que possible ; s'arrête aux relais en attente."""
    s = seance_courante(conseil, a.seance)
    print(f"Séance {s.nom}")
    for t in (1, 2):
        if not s.complet(t):
            executer_tour(conseil, s, t)
            if not s.complet(t):
                print(f"Arrêt : tour {t} incomplet. Relaie les réponses en attente puis relance « seance ».")
                return
        else:
            executer_tour(conseil, s, t)  # journalise d'éventuels relais déposés
    for t in (3, 4):  # questions et réponses, seulement si des questions ont été posées
        if not s.cibles(t):
            break
        executer_tour(conseil, s, t)
        if not s.complet(t):
            print(f"Arrêt : tour {t} (réponses aux questions) incomplet. Relaie puis relance « seance ».")
            return
    ecrire_questions_fabien(conseil, s)
    if not (s.dir / "carte.md").exists():
        if faire_carte(conseil, s, None) is None:
            return
    if not s.meta.get("etat_fait"):
        mettre_a_jour_etat(conseil, s)
        s.meta["etat_fait"] = True
        s.sauver()
    print("Séance complète.")


def cmd_statut(conseil: Conseil, a) -> None:
    s = seance_courante(conseil, a.seance)
    print(f"Séance {s.nom} (n° {s.meta['numero']}) — {s.question()[:90]}")
    print(f"Vérificateur : {s.meta.get('verificateur')}")
    for t in (1, 2, 3, 4):
        if t > 2 and not s.cibles(t):
            continue
        print(f"Tour {t} :" + (" (réponses aux questions)" if t > 2 else ""))
        for p in s.cibles(t):
            if s.reponse(t, p["id"]):
                etat = "fait"
            elif (s.dir / "relais" / f"{p['id']}-tour-{t}.erreur.txt").exists():
                etat = "erreur (voir relais/)"
            elif (s.dir / "relais" / f"{p['id']}-tour-{t}.consigne.md").exists():
                etat = f"en attente de relais → tour-{t}/{p['id']}.md"
            else:
                etat = "à lancer"
            print(f"  {s.lettre(p['id'])} {p['id']:<12} {NOM_SIEGE[p['siege']]:<9} {etat}")
    for q in questions_pour_fabien(s):
        print(f"Question pour Fabien ({s.lettre(q['de'])}) : {q['question']}")
    for nom, info in s.meta.get("cartes", {}).items():
        print(f"{nom} : {info['cartographe'] or 'mécanique'} · {info['date']}")


def cmd_rafraichir(conseil: Conseil, a) -> None:
    conseil.participant(a.participant)
    conseil.memoriser(a.participant, None)
    conseil.journaliser(f"{a.participant} : corpus à renvoyer en entier à la prochaine séance")
    print(f"{a.participant} recevra le corpus complet à la prochaine séance.")


def cmd_dossier(conseil: Conseil, a) -> None:
    p = conseil.participant(a.participant)
    texte, manif = conseil.dossier(p)
    for rel, taille, ok in manif:
        print(f"{'✓' if ok else '✗'} {rel} ({taille} car.)", file=sys.stderr)
    print(f"Total : {len(texte)} caractères", file=sys.stderr)
    if a.sortie:
        ecrire(Path(a.sortie), texte)
    else:
        print(texte)


def principal(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="conseil", description="Conseil Hacéfiance : dialogue continu entre plusieurs IA.")
    ap.add_argument("--config", default=str(ICI / "conseil.toml"), help="fichier de configuration")
    ap.add_argument("--simulation", action="store_true", help="faux participants, aucun appel réel")
    sp = ap.add_subparsers(dest="cmd", required=True)

    x = sp.add_parser("nouvelle", help="ouvrir une séance")
    x.add_argument("question", nargs="?")
    x.add_argument("--fichier", help="lire la question dans un fichier")
    x.add_argument("--slug", help="nom court de la séance")
    x.set_defaults(f=cmd_nouvelle)

    x = sp.add_parser("tour", help="lancer un tour (1 = à l'aveugle, 2 = lecture croisée, 3-4 = questions et réponses)")
    x.add_argument("numero", type=int, choices=[1, 2, 3, 4])
    x.add_argument("--seance")
    x.add_argument("--seulement", help="ids séparés par des virgules")
    x.set_defaults(f=cmd_tour)

    x = sp.add_parser("carte", help="dresser la carte des désaccords")
    x.add_argument("--seance")
    x.add_argument("--cartographe", help="id du cartographe (contre-greffe) ; vide = mécanique")
    x.add_argument("--sortie", default="carte.md", help="nom du fichier (ex. carte-contre.md)")
    x.set_defaults(f=cmd_carte)

    x = sp.add_parser("etat", help="mettre à jour l'état du fil")
    x.add_argument("--seance")
    x.set_defaults(f=cmd_etat)

    x = sp.add_parser("seance", help="avancer la séance aussi loin que possible")
    x.add_argument("--seance")
    x.set_defaults(f=cmd_seance)

    x = sp.add_parser("statut", help="où en est la séance")
    x.add_argument("--seance")
    x.set_defaults(f=cmd_statut)

    x = sp.add_parser("rafraichir", help="renvoyer le corpus complet à un participant en fil persistant")
    x.add_argument("participant")
    x.set_defaults(f=cmd_rafraichir)

    x = sp.add_parser("dossier", help="voir le dossier d'initiation d'un participant")
    x.add_argument("participant")
    x.add_argument("--sortie")
    x.set_defaults(f=cmd_dossier)

    a = ap.parse_args(argv)
    conseil = Conseil(Path(a.config).resolve(), simulation=a.simulation)
    a.f(conseil, a)


if __name__ == "__main__":
    principal()
