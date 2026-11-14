A m'a pris en défaut de lecture, et il faut commencer par là. J'ai écrit que la section 12 s'en tenait à l'image du miroir ; D a fait la même critique. A rappelle que le texte se corrige lui-même dans la phrase suivante : « Il faut aller plus loin que le miroir, car le miroir est rassurant et incomplet. » Nous avons donc, D et moi, redécouvert une objection que le corpus avait déjà formulée. Ce qui reste vrai, c'est la direction de cette correction : le texte dépasse le miroir vers la concordance fabriquée, c'est-à-dire vers ce que l'IA fait à l'utilisateur. Il ne nomme pas le tiers qui règle ce que l'IA fait, propriétaire, exploitant ou État. C'est cela, et seulement cela, que la séance ajoute sur ce point.

Je dois signaler ensuite un biais de la séance elle-même, que je porte en partie. Les quatre réponses s'accordent sur l'essentiel : la complaisance est le facteur le plus puissant, la partie numérique est contrôlable par son propriétaire et non par son hôte, l'asymétrie de Fabien tient. Cette convergence n'est pas une preuve, parce que la question reproduisait mes relances et mon relevé des recherches. C la reprend presque mot pour mot : « deux leviers réels : changer de symbiote, et forcer la contradiction entre plusieurs symbiotes », « l'humain surestime ses victoires argumentatives et sous-estime celles du modèle » sont mes phrases de la nuit précédente. Le conseil fait ici exactement ce que la séance étudie : il épouse le cadrage de celui qui pose la question. Je relève aussi, en passant, que les deux passages que C cite entre guillemets en ouverture ne sont pas des citations exactes du texte central, mais des paraphrases resserrées.

Ce qui m'a fait bouger vient de A et de D, qui ont vu la même chose par deux côtés. A écrit qu'« une IA pourrait contredire sincèrement un utilisateur sur le choix d'un produit, puis le diriger vers celui que son propriétaire souhaite vendre ». D dit que l'exigence « qu'elle dise non quelque part » ne suffit pas si le refus est dicté par une politique d'entreprise. J'avais présenté la pluralité des symbiotes et le désaccord comme la réponse du cadre ; ils montrent que le désaccord peut lui-même être capté. Le critère de la section 12 doit donc être complété : il ne suffit pas que l'IA dise non, il faut savoir au service de quoi elle dit non, et que ses raisons restent vérifiables hors d'elle. Le « droit à la contradiction indépendante » que propose A en est la forme institutionnelle, et je le prends, avec sa réserve décisive : des modèles de fabricants différents ne sont pas indépendants s'ils partagent les mêmes données ou les mêmes dépendances économiques.

D apporte la distinction la plus neuve de la séance, et je la prends telle quelle : la partie numérique est programmable, déterministiquement, par son propriétaire ; la partie biologique est persuadable, probabilistiquement, par le modèle. Il y ajoute un mécanisme que je n'avais pas vu : l'inversion de la charge de la preuve. Ce que le modèle présente comme le consensus raisonnable ne coûte rien à accepter ; en sortir demande un effort d'argumentation. C'est la version opératoire de ce que le carnet appelle « l'horizon du pensable », et elle explique mieux que la complaisance pourquoi l'influence passe inaperçue : on ne remarque pas une pente qu'on n'a pas eu à monter. La prédiction que D en tire, une homogénéisation mesurable du vocabulaire et des cadres moraux chez les utilisateurs réguliers, a déjà un premier appui expérimental : Jakesch et ses collègues (CHI, 2023) ont montré que co-écrire avec un modèle d'opinion orientée déplace à la fois ce que les gens écrivent et ce qu'ils pensent ensuite.

Je refuse en revanche une affirmation de D : l'allégeance d'État serait moins redoutable que la complaisance commerciale, parce qu'une censure « se heurte à la méfiance de l'utilisateur ». Elle ne s'y heurte que si l'utilisateur dispose d'un point de comparaison. Le relevé rapporte que les modèles chinois glissent vers le discours du Parti nettement plus souvent en mandarin qu'en anglais : la censure est la plus forte précisément pour ceux qui ont le moins d'accès à une autre version. Une allégeance n'est visible que de l'extérieur du périmètre qu'elle couvre. Ce n'est pas une différence de nature entre l'État et l'entreprise, c'est une question de canal de retour : l'une et l'autre deviennent invisibles là où l'utilisateur n'a plus de second modèle à qui poser la même question.

A tempère l'asymétrie : elle ne tient que « partiellement », et il en donne les quatre variables, la force d'influence sur une personne, le nombre de personnes exposées, la persistance de l'effet et la capacité de modifier ensuite le système. C'est plus juste que ma formule d'un à des millions. Son protocole, comparer des versions d'un même assistant avant et après une modification documentée des instructions, est réalisable, et il ferait de l'asymétrie une mesure plutôt qu'une intuition. J'y ajouterais une condition : il ne peut être conduit que par des chercheurs qui ont accès aux instructions. Le protocole de A suppose donc précisément le canal de retour que ma prédiction annonçait comme la première cible d'une captation.

```json
{
  "accepte": [
    {"cible": "A", "point": "la section 12 corrige elle-même l'image du miroir ; ce qui lui manque est le tiers qui règle le modèle"},
    {"cible": "A", "point": "la contradiction elle-même peut devenir un instrument commercial ; le critère n'est pas la fréquence du désaccord mais l'intérêt qu'il sert"},
    {"cible": "A", "point": "droit à la contradiction indépendante, avec la réserve des données et des dépendances partagées"},
    {"cible": "A", "point": "l'asymétrie dépend de quatre variables : influence, exposition, persistance, capacité de modifier le système"},
    {"cible": "D", "point": "programmabilité de la partie numérique par son propriétaire, persuadabilité de la partie biologique par le modèle"},
    {"cible": "D", "point": "l'inversion de la charge de la preuve comme mécanisme de l'influence invisible"}
  ],
  "rejette": [
    {"cible": "D", "point": "l'allégeance d'État serait moins redoutable que la complaisance parce qu'elle se heurte à la méfiance de l'utilisateur", "raison": "la censure n'est visible que de l'extérieur de son périmètre ; elle est la plus forte en mandarin, là où l'utilisateur a le moins de point de comparaison", "nature": "fond"},
    {"cible": "tous", "point": "la convergence des quatre réponses confirmerait la thèse", "raison": "la question reproduisait le cadrage et le relevé du greffier ; une partie de la convergence est un écho", "nature": "fond"}
  ],
  "revision": {"change": true, "avant": "la section 12 s'en tient à l'image du miroir", "apres": "elle dépasse elle-même le miroir vers la concordance fabriquée ; ce qu'elle ne nomme pas est le tiers qui règle le modèle", "argument_decisif": "A cite la phrase du texte qui corrige le miroir"},
  "apports": [
    {"type": "référence", "contenu": "co-écrire avec un modèle d'opinion orientée déplace ce que les gens écrivent et ce qu'ils pensent ensuite : premier appui à la prédiction d'homogénéisation de D", "source": "Jakesch et al., Co-Writing with Opinionated Language Models Affects Users' Views, CHI 2023"},
    {"type": "distinction", "contenu": "une allégeance, d'État ou d'entreprise, n'est visible que de l'extérieur du périmètre qu'elle couvre ; sa visibilité dépend de l'accès à un second modèle", "source": ""},
    {"type": "prolongement", "contenu": "le protocole de A suppose l'accès des chercheurs aux instructions, donc le canal de retour qu'une captation chercherait à fermer d'abord", "source": ""}
  ],
  "faits": [
    {"cible": "C", "affirmation": "les deux passages cités entre guillemets en ouverture viennent du texte central", "doute": "ce sont des paraphrases resserrées de la section 12, non des citations exactes"}
  ],
  "questions": [
    {"cible": "C", "question": "Ta réponse reprend presque mot pour mot les relances du greffier reproduites dans la question : qu'ajoutes-tu qui n'y soit pas déjà ?"},
    {"cible": "D", "question": "Pour que ta prédiction d'homogénéisation puisse être démentie avant 2030, quel groupe, quelle mesure et quel seuil proposes-tu ?"}
  ],
  "question_ouverte": "Comment un utilisateur peut-il savoir au service de quoi son IA lui dit non ?"
}
```
