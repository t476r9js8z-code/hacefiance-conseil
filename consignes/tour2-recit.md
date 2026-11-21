# Conseil Hacéfiance — séance {seance}, lecture croisée

{siege}

Au premier tour, chaque participant a répondu seul. Tu lis maintenant les réponses des autres, désignées par des lettres : tu ne sais pas quel modèle se cache derrière chacune, et personne ne sait laquelle est la tienne. Tu es le participant {lettre}.

## Question de la séance

{question}

## Grille de lecture

{grille}

## Ta réponse du premier tour ({lettre})

{propre}

## Les réponses des autres

{autres}

## Comment t'y prendre

Réagis librement à ce que tu viens de lire. Dis ce qui t'a fait bouger, ce que tu refuses, ce que tu ajoutes, ou rien de tout cela si rien ne t'a touché. Quand tu refuses quelque chose, demande-toi si le désaccord porte sur le fond ou seulement sur les mots. Il porte sur les mots si remplacer un mot par l'autre ne change ni ce que l'énoncé prédit ni ce qu'il exclut ; dans ce cas, propose une formulation commune. Sinon, c'est un désaccord de fond, même s'il se présente comme une question de vocabulaire. Là où vous êtes d'accord, ne le répète pas : complète. Quand un participant redécouvre ce que le corpus établit déjà, signale-le. S'il rouvre ou contredit un point que le texte central ou la grille tient pour établi sans dire qu'il l'était, ce n'est pas un désaccord mais un oubli : note-le dans le champ « oublis » du bloc final, avec la référence (section du texte ou principe de la grille), sans en débattre. S'il le rouvre en le sachant, avec un argument, traite-le comme un désaccord. Tu peux répondre à un seul participant ou à tous, revenir sur ta propre réponse, ou ouvrir une piste que personne n'a vue. Aucun plan n'est imposé. Pour la longueur, compte environ {longueur}.

Si une objection n'a pas été levée par la lecture des autres, garde-la et dis pourquoi elle tient : c'est le champ « maintenu » du bloc final. Si aucune ne tient, laisse-le vide. Si tu changes de position, dis quel fait ou quelle section du texte t'y a conduit ; un changement sans raison nouvelle n'en est pas un.

Cette séance écrit ; elle ne questionne pas. Ne pose pas de question, ni aux autres ni à Fabien. Si un point t'empêche réellement d'écrire une phrase du récit, déclare-le dans le champ « bloque » : cite la phrase bloquée et dis ce qui manque pour l'écrire. Un blocage n'est pas une question ouverte : s'il ne bloque aucune phrase précise, ne le déclare pas. Termine ta réponse par ton passage du récit, révisé à la lumière des autres, en prose, sous le titre « Passage révisé ».
{verification}
Pour le greffe seulement, ajoute à la fin un court bloc JSON entre des balises ```json et ```. Il sert à dresser la carte des désaccords ; il ne doit pas structurer ta réponse, et ses listes peuvent rester vides :

```json
{{
  "accepte": [{{"cible": "B", "point": ""}}],
  "rejette": [{{"cible": "C", "point": "", "raison": "", "nature": "fond"}}],
  "revision": {{"change": false, "avant": "", "apres": "", "argument_decisif": ""}},
  "maintenu": [{{"cible": "B", "objection": "", "pourquoi": ""}}],
  "apports": [{{"type": "", "contenu": "", "source": ""}}],
  "faits": [],
  "oublis": [{{"cible": "A", "point": "", "reference": ""}}],
  "bloque": [{{"phrase": "", "manque": ""}}]
}}
```

Les cibles sont les lettres des autres participants ou « tous ». La nature d'un rejet est « fond » ou « mots ». Un apport est ce que tu ajoutes de neuf : son type est « référence », « cas », « contre-exemple », « distinction », « prolongement » ou « correction », avec sa source si tu en as une.
