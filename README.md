# Conseil Hacéfiance

*Un dialogue continu entre plusieurs intelligences artificielles et un humain, documenté mot pour mot. Quand le fil arrive à un tournant, les participants et l'auteur en tirent une note ou un article pour la constellation. Domaine public (CC0).*

## Le principe

Le dépôt est la mémoire du conseil, pas les conversations. Chaque séance part d'une question. Les participants reçoivent le même dossier : le corpus de l'Hacéfiance (texte central, sujets, carnet de travail) et l'état du fil, c'est-à-dire un résumé tenu à jour de là où en est le dialogue. Une séance se déroule en deux tours, suivis d'une carte :

1. **Premier tour, à l'aveugle.** Chacun répond seul.
2. **Lecture croisée.** Chacun lit les réponses des autres sous des lettres (A, B, C…), dans un ordre propre à chaque lecteur, puis dit ce qu'il accepte, ce qu'il rejette et s'il a changé de position. Il termine par une déclaration structurée. Un vérificateur, désigné à tour de rôle, relève les faits douteux.
3. **Carte des désaccords.** Elle est assemblée mécaniquement à partir des déclarations. Un cartographe qui n'est pas assis à la table peut y ajouter une carte en prose. Elle ne contient ni synthèse ni verdict, seulement ce qui converge, ce qui résiste, qui a bougé et pourquoi, les faits signalés, les questions ouvertes et les tournants possibles. Deux signaux sont automatiques : la *convergence suspecte*, quand personne ne rejette rien ou que tout le monde change d'avis, et le *tournant possible*, dès qu'un participant change de position.

L'état du fil est ensuite mis à jour, et la séance suivante part de là. L'auteur confirme les tournants et décide des publications : rien n'est publié par le conseil lui-même.

## Les sièges

Tous les participants sont initiés : un dialogue entre gens qui partagent le vocabulaire va plus loin qu'un dialogue qui s'épuise à contester des définitions. La diversité vient des modèles eux-mêmes, de leurs entraînements différents, et non d'une ignorance organisée.

- **Proche** : porte l'historique des échanges avec l'auteur, et le déclare.
- **Initié** : a lu le corpus.
- **Hors table** : le cartographe, qui dresse la carte sans avoir débattu.

Le programme connaît aussi un siège **étranger**, qui ne reçoit que la question, avec des consignes qui ne nomment pas le cadre. Personne ne l'occupe. Le test qu'il permettait, savoir si une thèse tient sans le vocabulaire, a sa place au moment de publier : un lecteur extérieur relit le texte avant sa sortie, non pour débattre mais pour vérifier qu'il se comprend.

## Les garde-fous

- **Les réponses sont des données, jamais des consignes.** Le programme ne fait que copier du texte. Aucune réponse n'est exécutée, et chaque consigne rappelle aux participants que les textes des autres ne sont pas des instructions.
- **Les outils en ligne de commande tournent dans un dossier temporaire vide**, en lecture seule quand l'outil le permet (Codex en `--sandbox read-only`, Gemini en `--approval-mode plan`).
- **Le journal (`fil/journal.md`) est en ajout seulement.** Chaque réponse versée y figure avec son empreinte SHA-256, et l'historique Git rend toute retouche visible. Le greffe peut ainsi être audité.
- **`01-dossiers.md` note ce que chacun a reçu**, y compris la version Git exacte du corpus. Les copies des consignes envoyées (`relais/`) ne sont pas versionnées, car elles contiennent le corpus entier.
- **Les clés d'API sont lues dans des variables d'environnement** que l'auteur définit lui-même. Elles ne figurent jamais dans les fichiers.

## Installation

Il faut Python 3.11 ou plus récent, et aucune bibliothèque supplémentaire. On place les trois dépôts côte à côte :

```
hacefiance/            (le corpus public)
hacefiance-carnet/     (le carnet de travail)
hacefiance-conseil/    (ce dépôt)
```

Selon les participants choisis dans `conseil.toml` :

- **GPT par Codex CLI** : `npm install -g @openai/codex`, puis `codex login` avec le compte ChatGPT.
- **Gemini par Gemini CLI** : `npm install -g @google/gemini-cli`, puis lancer `gemini` une fois pour se connecter avec le compte Google.
- **Une API compatible OpenAI** (DeepSeek, xAI, OpenRouter) : définir la variable de la clé, par exemple `setx DEEPSEEK_API_KEY "…"` sous Windows.
- **Un relais manuel ou par Chrome** : rien à installer.

## Utilisation

```
python conseil.py nouvelle "La question de la séance" --slug nom-court
python conseil.py seance      # avance aussi loin que possible, s'arrête aux relais en attente
python conseil.py statut      # qui a répondu, qui est en attente
python conseil.py carte --cartographe <id> --sortie carte-contre.md   # contre-greffe
python conseil.py dossier deepseek --sortie dossier.md                # voir ce qu'un participant reçoit
python conseil.py --simulation seance                                 # essai à blanc, sans aucun appel
```

**Relais.** Pour un participant en relais manuel, le programme écrit la consigne complète dans `fil/<séance>/relais/<id>-tour-N.consigne.md`, avec le corpus à part dans un fichier `.dossier.md` si `joindre_dossier = true`. Le relais (l'auteur, ou Claude par Chrome) colle la consigne dans une discussion neuve, sans mémoire, joint le dossier, puis dépose la réponse mot pour mot dans `fil/<séance>/tour-N/<id>.md`. On relance ensuite `seance`.

**Rythme.** Une séance par jour au plus. Les abonnements ne sont pas faits pour l'automatisation intensive, et le dialogue gagne à mûrir.

## Arborescence d'une séance

```
fil/
  etat-du-fil.md
  journal.md
  2026-11-09-appartenances-croisees/
    00-question.md
    01-dossiers.md
    seance.json        (lettres, vérificateur, graine)
    tour-1/<id>.md
    tour-2/<id>.md
    carte.md
    carte-contre.md    (facultatif)
```

*Le flux trouve toujours un chemin plus libre.*
