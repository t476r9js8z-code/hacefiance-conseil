# Conseil Hacéfiance — séance {seance}, lecture croisée

{siege}

Au premier tour, chaque participant a répondu seul. Tu lis maintenant les réponses des autres, désignées par des lettres : tu ne sais pas quel modèle se cache derrière chacune, et personne ne sait laquelle est la tienne. Tu es le participant {lettre}.

## Question de la séance

{question}

## Ta réponse du premier tour ({lettre})

{propre}

## Les réponses des autres

{autres}

## Comment t'y prendre

Réagis librement à ce que tu viens de lire. Dis ce qui t'a fait bouger, ce que tu refuses, ce que tu ajoutes, ou rien de tout cela si rien ne t'a touché. Tu peux répondre à un seul participant ou à tous, revenir sur ta propre réponse, ou ouvrir une piste que personne n'a vue. Aucun plan n'est imposé. Pour la longueur, compte environ {longueur}.

Si tu veux interroger quelqu'un, tu peux poser au plus deux questions : à un participant (par sa lettre), à tous (« tous ») ou à Fabien (« Fabien »). Les destinataires y répondront avant que la séance se close. Ne pose une question que si sa réponse t'importe vraiment.
{verification}
Pour le greffe seulement, ajoute à la fin un court bloc JSON entre des balises ```json et ```. Il sert à dresser la carte des désaccords ; il ne doit pas structurer ta réponse, et ses listes peuvent rester vides :

```json
{{
  "accepte": [{{"cible": "B", "point": ""}}],
  "rejette": [{{"cible": "C", "point": "", "raison": ""}}],
  "revision": {{"change": false, "avant": "", "apres": "", "argument_decisif": ""}},
  "faits": [],
  "questions": [{{"cible": "D", "question": ""}}],
  "question_ouverte": ""
}}
```

Les cibles sont les lettres des autres participants, « tous » ou « Fabien ».
