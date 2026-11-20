#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Annote une transcription YouTube collee dans un fichier texte.

Usage :
    python annoter_transcription.py transcription.txt
    python annoter_transcription.py transcription.txt --mode retirer
    python annoter_transcription.py transcription.txt -o sortie.md

Ce que fait le script, sur VOTRE fichier :
  1. supprime l'horodatage double ("0:1515 secondes" -> "[0:15]") ;
  2. corrige les noms propres ecorches par le sous-titrage automatique ;
  3. repere les extraits inseres (voir la table EXTRAITS) et, selon le mode :
       etiqueter (defaut) : les encadre d'une mention avec locuteur et contexte ;
       retirer            : les remplace par une ligne de renvoi.

Les bornes sont appliquees a la ligne : la premiere ou la derniere ligne
d'un extrait peut contenir quelques mots de l'auteur.
"""
import argparse
import re
import sys
from pathlib import Path

# (debut, fin, nature, locuteur / source, certitude)
EXTRAITS = [
    ("0:15", "1:28", "Montage d'archives télé sur le climat et l'ozone, discours présidentiel",
     "Journaux télévisés anciens ; Jacques Chirac, Johannesburg, 2002", "probable"),
    ("3:20", "3:44", "Archive sur le goût et le jugement de préférence", "Pierre Bourdieu", "sûr"),
    ("4:22", "4:58", "Plateau télé : un invité interrogé sur l'achat d'un fourgon diesel", "non identifié", "inconnu"),
    ("6:01", "7:53", "Entretien : les ZFE décrites comme une ségrégation sociale",
     "Alexandre Jardin, mouvement « Les Gueux »", "probable"),
    ("7:53", "8:28", "Vidéo de garage : contrôle antipollution d'une Mazda MX-5 de 1996", "non identifié", "inconnu"),
    ("9:08", "10:18", "Intervention sur la crise du logement et le DPE", "professionnel de l'immobilier, non identifié", "inconnu"),
    ("13:25", "14:18", "Montage de plateaux : faire payer leurs soins aux non-vaccinés et aux malades jugés responsables",
     "plusieurs intervenants, non identifiés", "inconnu"),
    ("16:31", "17:30", "Définition du monopole radical (en anglais)", "Ivan Illich", "sûr"),
    ("18:18", "19:08", "Défense du diesel propre et de la norme Euro 5", "Arnaud Montebourg, ministre, vers 2013", "sûr"),
    ("20:11", "21:48", "Chronique sur la taxe carbone européenne de 2027, puis débat", "chroniqueurs télé, non identifiés", "inconnu"),
    ("26:36", "27:00", "Question sur les ultra-riches et le climat (en anglais), coupée", "non identifié", "inconnu"),
    ("27:35", "28:14", "Explication pédagogique du crédit carbone", "reportage, non identifié", "inconnu"),
    ("28:14", "28:47", "Critique des crédits carbone, étude des 94 %", "vidéaste, non identifié", "inconnu"),
    ("28:47", "29:52", "Critique de la « neutralité carbone » d'entreprise", "Jean-Marc Jancovici", "probable"),
    ("30:27", "31:20", "Chiffres de Tesla et des crédits carbone en 2024", "vidéaste finance", "probable"),
    ("31:20", "31:58", "Baisse des crédits réglementaires de Tesla (en anglais)", "reportage financier américain, 2025", "probable"),
    ("33:33", "35:42", "Montage sobriété : spots officiels, ministres, délestage des patients sous respirateur",
     "campagne gouvernementale de 2022, ministres, porte-parole du réseau électrique", "probable"),
    ("43:19", "44:04", "Mise en garde contre un « état d'urgence climatique » (en anglais)", "commentateur américain, non identifié", "inconnu"),
    ("44:36", "45:05", "Échange sur la taxation des jets privés et les biocarburants", "ministres français, dont Clément Beaune", "probable"),
    ("46:37", "47:40", "Bunkers de luxe pour milliardaires (en anglais)", "reportage télé et constructeur d'abris", "inconnu"),
    ("47:40", "48:26", "Visite d'un abri antiatomique américain", "reportage télé français", "inconnu"),
    ("50:34", "52:33", "Enfants dans les mines de cobalt en RDC (en anglais)", "enquête de Sky News, vers 2017", "probable"),
    ("54:35", "56:58", "Appel d'un auditeur rural en colère", "émission de libre antenne, non identifiée", "inconnu"),
    ("57:18", "57:51", "Réaction à l'accord UE-Mercosur", "représentant agricole, non identifié", "inconnu"),
    ("57:51", "1:01:11", "Chronique sur le Mercosur et les contrôles sanitaires", "autre vidéaste", "probable"),
    ("1:02:08", "1:03:19", "L'entraide dans les quartiers populaires", "Jean-Claude Michéa", "sûr"),
    ("1:03:33", "1:04:12", "Plaidoyer pour la décroissance", "Sandrine Rousseau", "probable"),
    ("1:05:36", "1:07:55", "Chronique ironique sur les jets de la COP26", "chroniqueur radio, non identifié", "inconnu"),
    ("1:09:33", "1:10:45", "La politique comme projet d'autonomie", "Cornelius Castoriadis", "sûr"),
    ("1:11:32", "1:12:21", "L'enracinement et la responsabilité", "non identifié", "inconnu"),
]

# Corrections des noms propres (expression reguliere -> remplacement)
CORRECTIONS = [
    (r"\bFou(?:co|o)\b", "Foucault"),
    (r"\bIvanic\b", "Ivan Illich"),
    (r"\bIlich\b", "Illich"),
    (r"\bSupio\b", "Supiot"),
    (r"\bHarvet\b", "Harvey"),
    (r"\bJean-Claude Micha\b", "Jean-Claude Michéa"),
    (r"\bJaul\b", "Jacques Ellul"),
    (r"\bHPS\b", "Hobbes"),
    (r"\bH Jonas\b", "Hans Jonas"),
    (r"\bThomson\b", "Thompson"),
    (r"\bBelamy\b", "Bellamy"),
    (r"\bSimon Veille\b", "Simone Weil"),
    (r"\bChristopher Lash\b", "Christopher Lasch"),
    (r"\bvidéo sur lâche\b", "vidéo sur Lasch"),
    (r"\bprolongé l'âche\b", "prolongé Lasch"),
    (r"\bcastoriadist\b", "Castoriadis"),
    (r"\b(?:Tonberg|Sunberg)\b", "Thunberg"),
    (r"\bBenoît Pulv\b", "Benoît Poelvoorde"),
    (r"\b(?:ces|les|des) aides (?:et|des) feu\b", "les ZFE"),
    (r"\bADFE\b", "ZFE"),
    (r"\bcritère ([0-5])\b", r"Crit'Air \1"),
    (r"\bMercossure\b", "Mercosur"),
    (r"\bdroit de glève\b", "droit de glaive"),
    (r"\bLeuristique\b", "L'heuristique"),
    (r"\bleuristique\b", "l'heuristique"),
    (r"\bcommon disency\b", "common decency"),
    (r"\bscientifiques du GC\b", "scientifiques du GIEC"),
    (r"\ble terrorisme et la Première Guerre\b", "le taylorisme et la Première Guerre"),
    (r"\bSilicone Valallet\b", "Silicon Valley"),
]

RE_LIGNE = re.compile(
    r"^(\d{1,2}:\d{2}(?::\d{2})?)"
    r"(?:\d+ heures?)?"
    r"(?:(?:, | et )?\d+ minutes?)?"
    r"(?:(?:, | et )?\d+ secondes?)?"
    r"(.*)$"
)
RE_CHAPITRE = re.compile(r"^Chapitre \d+ : (.*)$")


def en_secondes(horodatage):
    total = 0
    for partie in horodatage.split(":"):
        total = total * 60 + int(partie)
    return total


def corriger(texte):
    for motif, remplacement in CORRECTIONS:
        texte = re.sub(motif, remplacement, texte)
    return texte


def main():
    analyseur = argparse.ArgumentParser(description="Annote une transcription YouTube.")
    analyseur.add_argument("fichier", help="transcription collee depuis YouTube (.txt)")
    analyseur.add_argument("--mode", choices=["etiqueter", "retirer"], default="etiqueter")
    analyseur.add_argument("-o", "--sortie", help="fichier de sortie (.md)")
    options = analyseur.parse_args()

    source = Path(options.fichier)
    lignes = source.read_text(encoding="utf-8").splitlines()
    plages = [(en_secondes(d), en_secondes(f), d, f, n, s, c) for d, f, n, s, c in EXTRAITS]

    sortie = []
    courant = None      # extrait en cours
    non_reconnues = 0

    def fermer():
        nonlocal courant
        if courant is not None and options.mode == "etiqueter":
            sortie.append("> *— fin de l'extrait —*")
            sortie.append("")
        courant = None

    for brute in lignes:
        brute = brute.strip()
        if not brute or brute == "Synchroniser avec la vidéo":
            continue
        chapitre = RE_CHAPITRE.match(brute)
        if chapitre:
            fermer()
            sortie += ["", "## " + chapitre.group(1), ""]
            continue
        trouve = RE_LIGNE.match(brute)
        if not trouve:
            non_reconnues += 1
            sortie.append(corriger(brute))
            continue
        horodatage, texte = trouve.group(1), corriger(trouve.group(2).strip())
        instant = en_secondes(horodatage)
        plage = next((p for p in plages if p[0] <= instant < p[1]), None)

        if plage is not courant:
            fermer()
            if plage is not None:
                _, _, debut, fin, nature, locuteur, certitude = plage
                entete = f"EXTRAIT {debut} – {fin} · {nature} · {locuteur} · attribution : {certitude}"
                sortie.append("")
                if options.mode == "etiqueter":
                    sortie.append(f"> **[{entete}]**")
                else:
                    sortie.append(f"*[{entete} — retiré]*")
                    sortie.append("")
            courant = plage

        if plage is None:
            sortie.append(f"[{horodatage}] {texte}")
        elif options.mode == "etiqueter":
            sortie.append(f"> [{horodatage}] {texte}")
    fermer()

    cible = Path(options.sortie) if options.sortie else source.with_name(source.stem + "_annotee.md")
    cible.write_text("\n".join(sortie).strip() + "\n", encoding="utf-8")
    print(f"Ecrit : {cible}")
    print(f"Lignes lues : {len(lignes)} · extraits reperes : {len(plages)} · lignes non reconnues : {non_reconnues}")


if __name__ == "__main__":
    sys.exit(main())
