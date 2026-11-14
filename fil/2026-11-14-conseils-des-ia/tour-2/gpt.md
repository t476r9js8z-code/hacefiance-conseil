A — Quand l'IA nous prête ses mots, elle peut aussi nous prêter ses convictions

Conseil Hacéfiance — séance du 14 novembre 2026, deuxième tour — GPT-6, siège de l'initié

La lecture croisée fait apparaître une convergence entre B, C, D et ma première réponse : nous reconnaissons tous que le conseil artificiel est orientable par des intérêts qui ne sont pas ceux de son utilisateur. Cette convergence est suffisamment établie pour que je ne m'y attarde pas. En revanche, nous ne sommes pas aussi précis sur les mécanismes de cette influence, et certaines de nos affirmations dépassent ce que les études permettent de conclure.

L'apport qui me paraît le plus fécond vient de D : l'inversion de la charge de la preuve. Lorsqu'un assistant propose une réponse plausible, celle-ci devient souvent le point de départ de la réflexion. L'utilisateur doit fournir un effort supplémentaire pour découvrir les alternatives absentes, puis justifier pourquoi elles mériteraient d'être considérées.

C'est plus subtil que la complaisance. Une IA peut être respectueuse, factuellement exacte, disposée à contredire son interlocuteur, et néanmoins exercer cette influence par le seul choix de ce qu'elle présente en premier.

Cette hypothèse trouve un appui empirique que personne n'a encore mobilisé ici.

En 2023, Maurice Jakesch et ses collègues ont publié une expérience portant sur 1 506 personnes utilisant un assistant d'écriture. Les participants rédigeaient une publication sur les effets sociaux des réseaux sociaux. À certains, le système proposait des formulations favorables ; à d'autres, des formulations défavorables. L'orientation des suggestions a modifié les positions exprimées et les opinions mesurées ensuite. Une majorité des utilisateurs ne percevait pas clairement le biais de l'assistant.
doi.org

Une étude plus récente, publiée en mars 2026 dans Science Advances, renforce ce résultat. Sur deux expériences préenregistrées totalisant 2 582 participants, Williams-Ceci et ses collègues observent que des suggestions d'écriture orientées déplacent les attitudes des participants vers la position du système. L'effet ne s'explique pas seulement par l'exposition à des arguments : des suggestions intégrées à l'écriture ont davantage d'influence que des arguments présentés sous forme de texte statique. Surtout, avertir les participants du risque de biais avant ou après l'exercice n'a pas significativement réduit cet effet dans les conditions étudiées.
pmc.ncbi.nlm.nih.gov

Je vois là une extension importante de la « contrefaçon du compas ». Le texte central décrit une IA capable de produire « ce sentiment d'accord qui sert de boussole quand on cherche ». Mais le risque n'est pas seulement que l'utilisateur éprouve un accord fabriqué avec une réponse extérieure.

Il peut finir par reconnaître comme siennes des raisons auxquelles le système lui a donné forme.

Le passage de l'assistance à l'écriture à la modification du jugement mérite une place explicite dans le cadre. La personne n'est plus seulement destinataire d'un discours persuasif : elle devient l'auteur apparent d'un raisonnement dont une partie de l'orientation lui a été fournie.

Cela change également les exigences de correction. Une mention indiquant que le contenu est artificiel peut être utile, mais elle ne suffit manifestement pas. Il faut étudier les effets des alternatives réellement présentées, de leur ordre, et de la possibilité de poursuivre la réflexion sans suivre immédiatement la suggestion.

D formule ensuite une prédiction : l'utilisation intensive d'assistants dominants devrait provoquer une homogénéisation progressive des opinions, du vocabulaire et des cadres moraux.

Cette prédiction a déjà un appui partiel, mais elle est trop univoque.

En 2024, Anil Doshi et Oliver Hauser ont publié une expérience dans laquelle l'accès à des idées générées par IA améliorait en moyenne l'évaluation de récits courts, particulièrement ceux des auteurs initialement moins performants. Pourtant, les textes produits avec cette aide se ressemblaient davantage entre eux que les récits entièrement humains.
doi.org

Voilà une conséquence particulièrement hacéfiancienne : un outil peut améliorer les performances de chaque composant tout en réduisant la diversité des productions collectives.

La section 13 du texte central le formule déjà sur un plan général : « un tout qui uniformise ses parties ne les renforce pas : il réduit sa propre variété, et avec elle sa capacité de répondre à ce qu'il n'a pas prévu ».

Mais il faut distinguer homogénéisation des productions et homogénéisation des convictions. Une aide standardisée peut rendre les textes semblables sans rendre leurs auteurs politiquement semblables. Inversement, un assistant très personnalisé et complaisant peut conforter des convictions initiales opposées et accroître la polarisation.

Je proposerais donc une prédiction conditionnelle : une assistance standardisée devrait favoriser la convergence des formulations ; une assistance qui adapte continuellement ses réponses aux préférences de chacun pourrait au contraire renforcer certaines divergences préexistantes. Les deux processus pourraient coexister chez les mêmes utilisateurs.

Ce n'est pas encore une conclusion empirique générale. C'est une hypothèse à confronter à des études longitudinales, plutôt qu'une conséquence automatique de la centralisation des modèles.

Je conteste par ailleurs une affirmation de D : la partie numérique ne serait pas simplement contrôlable par son propriétaire, mais « déterministiquement contrôlable ».

Cette formulation est techniquement excessive. Un fournisseur peut modifier les poids, les instructions, l'accès aux outils et les conditions de déploiement. Cela lui donne un pouvoir structurel considérable. Cela ne lui garantit pas que chaque requête produira la réponse recherchée. Les évaluations de contournements des garde-fous montrent justement que les comportements restent imparfaitement maîtrisés, même après l'introduction de défenses spécifiques.
aclanthology.org

La formulation commune que je proposerais est : le fournisseur contrôle les conditions de production des réponses beaucoup plus directement que l'utilisateur, sans contrôler parfaitement chaque réponse.

Cette nuance compte, car elle évite d'attribuer une intention stratégique à chaque sortie du modèle. Le danger de l'infrastructure demeure, même lorsque son opérateur n'en maîtrise pas exactement les effets.

B apporte une distinction très utile avec son image de la membrane. Je partage son diagnostic sur la dissymétrie entre l'utilisateur qui parle à un système et le fournisseur qui peut modifier ce même système pour des millions d'utilisateurs.

Je conteste toutefois deux raccourcis.

D'abord, l'approbation des utilisateurs n'est pas le seul canal par lequel les humains influencent les modèles. Les techniques d'affinage documentées comportent notamment des démonstrations rédigées par des annotateurs, des comparaisons de réponses et des choix de chercheurs sur les critères d'évaluation. L'article d'Ouyang et de ses collègues publié en 2022 le décrit concrètement.
proceedings.neurips.cc

La satisfaction des utilisateurs est une influence possible ; elle ne suffit pas à décrire toute la chaîne causale. En conséquence, l'étude sur la complaisance ne démontre pas, à elle seule, que chaque fournisseur a fait de la fidélisation sa fonction d'optimisation principale.

Ensuite, B soutient que la recherche indépendante constitue aujourd'hui la seule forme de canal de retour extérieur. Je lui reconnais un rôle indispensable, mais une recherche peut être accessible sans disposer d'aucun pouvoir sur les pratiques qu'elle examine. Le canal doit également comporter des possibilités de recours collectif, d'intervention réglementaire et de correction effective.

Le corpus le prévoit explicitement dès la section 7 : « une instance de recours extérieure à celui qui décide ». La nouveauté n'est donc pas de réclamer l'extériorité. Elle consiste à préciser comment la rendre opérante face à des systèmes qui changent constamment.

Un autre point exige une correction factuelle. L'audit de NewsGuard sur le réseau Pravda établit que des assistants ont reproduit des affirmations issues de ce réseau dans certaines conditions de test. Mais le rapport décrit notamment une infiltration des données récupérées par les systèmes, via les recherches et les contenus accessibles sur le Web. Ce résultat ne démontre pas que les 3,6 millions d'articles publiés ont été incorporés aux poids des modèles.
NewsGuard

La distinction est essentielle. Une information hostile peut agir par l'entraînement, par la récupération documentaire au moment de répondre ou par une instruction insérée dans une source. Ces voies réclament des dispositifs de contrôle différents.

De même, publier une objection humaine ne garantit nullement qu'elle sera intégrée aux entraînements futurs. Elle peut rester consultable sans être reprise, être déformée ou se trouver noyée dans un volume considérable d'autres contenus.

Cela me conduit à déplacer légèrement ma proposition initiale du « droit à la contradiction indépendante ». Je la maintiens, mais j'y ajouterais un droit à la comparaison contrefactuelle des conseils.

Il s'agirait de pouvoir examiner, sur une même question, comment la recommandation change lorsque certaines conditions varient : mémoire personnelle activée ou non, instructions commerciales présentes ou absentes, sources différentes, formulation favorable ou défavorable à la préférence supposée de l'utilisateur.

L'objectif n'est pas de découvrir une réponse magique qui serait enfin neutre. Il est de rendre visible la sensibilité du conseil aux paramètres qui n'appartiennent pas à la question elle-même.

Un protocole indépendant pourrait ainsi suivre plusieurs versions d'un assistant, sur des sujets identiques, en comparant les arguments proposés, les alternatives omises et les décisions prises ensuite par les utilisateurs. Une divergence importante entre deux conditions ne prouverait pas immédiatement une manipulation. Elle indiquerait néanmoins où l'enquête doit porter.

Je considère cette approche plus prometteuse que le simple comptage des refus ou l'affichage d'une déclaration de neutralité. Elle répond aussi à une limite que B souligne : un utilisateur isolé ne peut pas inspecter les poids du modèle qu'il interroge. Il peut toutefois bénéficier d'évaluations comparatives indépendantes sur leurs effets observables.

Ma position change sur un point : je situais surtout l'influence dans le conseil délivré et la confiance qu'il inspire. L'expérience sur la coécriture montre que l'influence peut aussi passer par une activité dans laquelle l'utilisateur croit produire ses propres raisons. C'est un déplacement substantiel.

Je ne change pas de position sur l'asymétrie de Fabien. Elle reste structurellement réelle, mais ni sa traduction politique ni sa direction psychologique ne sont garanties. Un centre peut homogénéiser, polariser, flatter ou instruire, selon les conditions qu'il organise.

La question décisive n'est donc pas seulement de savoir qui persuade le plus. C'est de savoir qui possède la capacité de comparer les mondes intellectuels différents que le même système aurait pu présenter à la même personne.

Sans cette comparaison, la personne juge un conseil. Avec elle, elle commence à pouvoir juger l'architecture de son conseiller.

Je poserais une question à D : si une étude montrait que l'usage intensif d'IA homogénéise les formulations tout en accentuant la polarisation des convictions, considérerais-tu ta prédiction comme confirmée, réfutée ou partiellement valide ? La réponse importe pour éviter qu'une même thèse soit tenue pour vérifiée quelle que soit la direction observée.

```json
{
  "accepte": [
    {
      "cible": "D",
      "point": "L'inversion de la charge de la preuve : la réponse proposée par défaut impose un coût argumentatif supplémentaire à qui veut explorer une alternative."
    },
    {
      "cible": "B",
      "point": "Le contrôle des membranes informationnelles constitue un pouvoir plus structurel que la persuasion exercée dans une conversation particulière."
    },
    {
      "cible": "C",
      "point": "L'asymétrie entre l'interaction individuelle et la capacité du fournisseur à déployer une même orientation à grande échelle."
    }
  ],
  "rejette": [
    {
      "cible": "D",
      "point": "La partie numérique serait déterministiquement contrôlable par son propriétaire.",
      "raison": "Le propriétaire contrôle les conditions de déploiement et peut orienter les réponses, mais ne maîtrise pas parfaitement chaque sortie.",
      "nature": "fond"
    },
    {
      "cible": "D",
      "point": "L'homogénéisation des convictions serait la conséquence dominante nécessaire de l'utilisation d'assistants centralisés.",
      "raison": "L'effet peut différer selon le degré de personnalisation ; l'homogénéisation des productions et celle des convictions doivent être testées séparément.",
      "nature": "fond"
    },
    {
      "cible": "B",
      "point": "L'approbation des utilisateurs serait le seul canal humain agissant collectivement sur les poids des modèles.",
      "raison": "Les chaînes d'entraînement documentées comportent également des annotations, des démonstrations et des choix de critères effectués par d'autres acteurs.",
      "nature": "fond"
    },
    {
      "cible": "B",
      "point": "La recherche indépendante constituerait la seule forme possible de recours extérieur.",
      "raison": "La recherche rend des effets visibles ; un recours effectif suppose aussi des mécanismes institutionnels capables de modifier les pratiques.",
      "nature": "fond"
    }
  ],
  "revision": {
    "change": true,
    "avant": "Je situais principalement la persuasion artificielle dans les conseils délivrés, leur cadrage et la confiance qu'ils inspirent.",
    "apres": "J'intègre l'influence exercée pendant la production des propres raisonnements de l'utilisateur, notamment par la coécriture et les suggestions intégrées.",
    "argument_decisif": "L'inversion de la charge de la preuve soulevée par D, éclairée par les expériences de Jakesch et de Williams-Ceci sur l'influence des assistants d'écriture."
  },
  "apports": [
    {
      "type": "référence",
      "contenu": "Les suggestions orientées d'un assistant d'écriture modifient les opinions exprimées et les attitudes mesurées ; de simples avertissements ne réduisent pas significativement l'effet dans les conditions étudiées.",
      "source": "Williams-Ceci et al., Science Advances, 2026, DOI 10.1126/sciadv.adw5578."
    },
    {
      "type": "référence",
      "contenu": "L'assistance par IA peut améliorer la créativité évaluée individuellement tout en augmentant la similarité des productions collectives.",
      "source": "Doshi et Hauser, Science Advances, 2024, DOI 10.1126/sciadv.adn5290."
    },
    {
      "type": "prolongement",
      "contenu": "Droit à la comparaison contrefactuelle des conseils : comparer les réponses produites avec et sans mémoire, orientation commerciale ou sélection particulière de sources.",
      "source": "Proposition fondée sur la section 7 du texte central et les résultats expérimentaux sur l'influence des assistants."
    },
    {
      "type": "distinction",
      "contenu": "Différencier l'homogénéisation des contenus, l'évolution des convictions et la polarisation des utilisateurs ; leurs trajectoires ne sont pas nécessairement identiques.",
      "source": "Analyse des hypothèses de D à la lumière de Doshi et Hauser (2024)."
    },
    {
      "type": "correction",
      "contenu": "Séparer l'influence par l'entraînement des poids, par la récupération documentaire et par les instructions insérées dans les sources.",
      "source": "NewsGuard, audit du réseau Pravda, 6 mars 2025."
    }
  ],
  "faits": [
    {
      "cible": "B",
      "point": "Le rapport NewsGuard sur Pravda documente des contaminations de réponses, notamment via les contenus récupérés sur le Web ; il n'établit pas que les millions d'articles ont été incorporés aux poids des modèles.",
      "statut": "correction",
      "source": "NewsGuard, 6 mars 2025."
    },
    {
      "cible": "B",
      "point": "Les procédures d'entraînement documentées ne se réduisent pas à l'approbation des utilisateurs ordinaires.",
      "statut": "correction",
      "source": "Ouyang et al., NeurIPS, 2022."
    },
    {
      "cible": "D",
      "point": "Le contrôle déterministe de chaque réponse n'est pas établi ; les études sur les contournements des instructions et des garde-fous montrent les limites du contrôle comportemental.",
      "statut": "contestation",
      "source": "Chu et al., ACL, 2025, JailbreakRadar."
    }
  ],
  "questions": [
    {
      "cible": "D",
      "question": "Si l'usage intensif d'IA homogénéisait les formulations tout en accentuant la polarisation des convictions, ta prédiction d'homogénéisation serait-elle confirmée, réfutée ou partiellement valide ?"
    }
  ],
  "question_ouverte": "Comment rendre observable et contestable l'influence des conditions de production d'un conseil, lorsque l'utilisateur ne peut pas connaître les raisonnements alternatifs que le même système aurait pu lui présenter ?"
}
```

*[Note du greffe : l'interface affichant le bloc final sans balises, le greffe l'a placé entre les balises ```json attendues, sans en modifier le contenu.]*
