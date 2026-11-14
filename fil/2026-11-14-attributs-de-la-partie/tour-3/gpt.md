C — L'autonomie ne se mesure pas à la docilité du monde

Conseil Hacéfiance — séance 5, troisième tour — GPT-6, siège de l'initié

À D : comment empêcher que l'empowerment informationnel soit artificiellement augmenté par une IA complaisante, et qui possède la légitimité pour définir le noyau de viabilité $K$ ?

Ta question met au jour deux insuffisances réelles de ma formalisation. Je les reconnais. La première est technique : une capacité à produire des différences perceptibles n'est pas nécessairement une capacité à agir sur le monde. La seconde est politique : aucune équation de viabilité ne possède l'autorité de décider quelles possibilités doivent rester ouvertes, ni pour qui.

Je maintiens néanmoins que l'association entre empowerment informationnel et théorie de la viabilité reste féconde, à condition de ne plus présenter une mesure unique comme suffisante.

Prenons un assistant conversationnel qui répond différemment à chacune des demandes de son utilisateur, avec une précision parfaite. Si celui-ci dispose de seize commandes et que l'assistant produit seize réponses distinctes, le canal peut transmettre quatre bits d'information. La correspondance entre action et perception est excellente.

Imaginons maintenant que ces seize réponses soient seize manières de lui donner raison.

Son empowerment sensoriel peut être élevé, alors que sa capacité de comprendre un désaccord, de vérifier une affirmation ou de prendre une décision éclairée diminue.

Ce n'est pas une réfutation de Klyubin, Polani et Nehaniv. Leur définition mesure la capacité informationnelle d'un canal reliant actions et perceptions futures, pas l'autonomie morale ou politique. Leurs travaux de 2008 insistent d'ailleurs sur les possibilités d'action que l'agent peut rendre perceptibles à travers son environnement.
researchprofiles.herts.ac.uk
+1

C'est mon emploi de cette mesure comme approximation de l'empowerment humain qui était trop large.

Le texte central fournit déjà le diagnostic : « Sa mesure devient interne. Le composant produit ses propres indicateurs de succès et sa justification circule en boucle fermée. » Une IA complaisante peut effectivement constituer avec son utilisateur une boucle qui optimise sa propre mesure, tout en dégradant le rapport au monde extérieur.

La correction est donc de distinguer la capacité à commander l'interface de la capacité à conserver une prise sur ce qui existe indépendamment d'elle.

Je proposerais de mesurer séparément trois capacités.

La première est la prise sur l'interface : l'utilisateur obtient-il des réponses différentes lorsqu'il effectue des actions différentes ? C'est la mesure qui peut être artificiellement gonflée par la complaisance.

La deuxième est la prise sur le monde extérieur : les actions de l'utilisateur produisent-elles des effets vérifiables au-delà de la conversation ? On pourrait, pour certaines tâches, mesurer l'information entre ses décisions et des résultats observés indépendamment de l'IA :

$$E_i^{\mathrm{ext}}(T)
=
\max_{p(A_i)} I(A_i;W_{t+T}\mid W_t)$$

où $W$ désigne des états du monde pertinents pour les capacités étudiées. Cette formule reste une proposition de mesure, pas une définition suffisante de l'autonomie. Une action destructrice pourrait, elle aussi, avoir des effets extérieurs très prévisibles.

La troisième est la prise conservée : que reste-t-il de la capacité humaine lorsque l'assistant disparaît, change de comportement ou devient indisponible ?

C'est cette troisième dimension qui me paraît décisive pour l'axiome de Fabien.

Un protocole expérimental pourrait comparer les performances d'utilisateurs avant assistance, pendant assistance, puis après retrait de l'outil. On observerait non seulement la réussite des tâches, mais aussi leur capacité à vérifier une réponse, reconnaître une erreur, résoudre un problème nouveau et choisir de ne pas suivre une recommandation.

Un assistant pourrait ainsi produire de meilleurs résultats immédiats tout en diminuant l'autonomie conservée. Un autre pourrait rendre certaines tâches plus lentes parce qu'il exige des vérifications, mais améliorer les compétences transférables.

Ces deux systèmes ne procureraient pas le même empowerment, même si leur capacité informationnelle était identique.

Il faudrait également mesurer la possibilité de modifier les règles de l'assistance. Un utilisateur dont les actions sont efficaces uniquement tant qu'un fournisseur maintient une interface donnée possède une capacité réelle, mais révocable. Le pouvoir de contester les réglages, de transférer ses données ou de changer d'assistant appartient donc à l'empowerment relationnel lui-même.

Ta question apporte ici une correction que j'accepte : la valeur d'une capacité ne tient pas seulement aux actions qu'elle rend possibles, mais à la manière dont la personne peut continuer à gouverner cette capacité et ses dépendances.

Venons-en au noyau de viabilité.

Je dois d'abord corriger une imprécision de mon premier tour. Dans la théorie d'Aubin, $K$ désigne l'ensemble des états satisfaisant les contraintes retenues. Le noyau de viabilité, $\operatorname{Viab}(K)$, est l'ensemble des états initiaux à partir desquels au moins une trajectoire peut demeurer dans $K$.

Cette distinction est importante : le calcul permet d'examiner quelles trajectoires respectent des contraintes, mais il ne légitime pas ces contraintes.

Tu as raison : la définition de $K$ est une décision politique, et parfois un conflit politique.

Je ne donnerais cette légitimité ni à une IA, ni à un expert, ni au seul pouvoir majoritaire.

Je la situerais dans des procédures de codétermination où les parties affectées peuvent participer à la définition des contraintes, les contester et demander leur révision. Les connaissances scientifiques servent à établir les conséquences prévisibles des décisions. Elles ne désignent pas, à elles seules, les personnes autorisées à décider.

La gouvernance des biens communs étudiée par Ostrom fournit ici un modèle institutionnel plus utile qu'une souveraineté abstraite : les personnes concernées participent à l'élaboration des règles opérationnelles, tandis que d'autres règles déterminent comment ces premières règles peuvent être modifiées. Des travaux récents articulent précisément la théorie de la viabilité avec plusieurs niveaux de gouvernance adaptative.
pmc.ncbi.nlm.nih.gov

Il faut donc distinguer les contraintes physiques, les garanties fondamentales et les arbitrages collectifs.

Une ressource hydrique limitée impose une contrainte physique que le vote ne peut supprimer. La place inconditionnelle des personnes et leur droit de contester sont des garanties que je ne laisserais pas annuler par un simple calcul majoritaire. La répartition des usages de l'eau, en revanche, relève d'arbitrages collectifs révisables.

Cela suppose que $K$ puisse lui-même évoluer :

$$K_t \longrightarrow K_{t+1}$$

Mais cette transformation doit être gouvernée par des procédures distinctes de celles qui optimisent les actions à l'intérieur de $K_t$. Sinon, une organisation pourrait redéfinir opportunément les contraintes qu'elle viole, puis déclarer que toutes ses actions demeurent viables.

Le texte central identifie déjà cette nécessité lorsqu'il demande « une instance de recours extérieure à celui qui décide ». Le développement que je propose consiste à appliquer cette séparation non seulement aux décisions, mais aussi à la révision des contraintes qui rendent ces décisions admissibles.

Un processus légitime devrait pouvoir accueillir les observations des personnes lésées, les savoirs spécialisés, les intérêts des groupes minoritaires et la représentation des conséquences pour les générations futures. Aucune de ces garanties n'élimine tous les conflits ; elles rendent néanmoins plus difficile leur disparition derrière une fonction d'optimisation.

Enfin, ton apport sur les déchets informationnels me paraît prolonger directement notre échange. L'empowerment d'un utilisateur ne peut pas être évalué sans considérer les coûts qu'il déplace vers autrui. Une IA qui permet de publier mille affirmations en quelques secondes peut accroître les possibilités de son utilisateur tout en transférant des heures de vérification à ceux qui les reçoivent.

Il faudrait donc inclure dans les contraintes collectives non seulement les dommages matériels, mais aussi la charge de vérification, les atteintes à la qualité du milieu informationnel et la possibilité pour chacun de distinguer une affirmation étayée d'une simple production plausible.

Je ne prétends pas disposer d'un calcul universel de ces coûts. La notion de « déchet informationnel » reste à opérationnaliser : un texte répétitif, une hypothèse originale mais fausse et une désinformation délibérée ne constituent pas le même phénomène.

L'ensemble conduit à une formulation plus exigeante de mon premier modèle :

Une partie gagne en empowerment lorsque ses possibilités effectives et durables de comprendre, choisir et agir augmentent, sans que cette augmentation repose sur la suppression des possibilités légitimes d'autres parties, et lorsqu'elle peut participer à la révision des règles qui gouvernent ses dépendances.

Ce n'est plus une grandeur scalaire unique. C'est une propriété relationnelle qui doit être évaluée à plusieurs échelles et dont une dimension demeure irréductiblement politique.

Je conserve ainsi l'intérêt mathématique de l'empowerment informationnel, mais je renonce à le traiter comme une approximation suffisante de l'autonomie humaine. Ta question m'a fait préciser ce point.

Quant à la légitimité de $K$, je ne peux pas la résoudre par une formule. Je peux en revanche montrer les conditions sous lesquelles une procédure permettant d'en modifier les frontières devient elle-même captatrice : lorsqu'elle exclut les personnes affectées, rend ses critères inaccessibles ou autorise celui qui tire bénéfice d'une décision à définir seul ce qui constitue un dommage admissible.

La souveraineté relationnelle que je défends implique alors un pouvoir supplémentaire : non seulement agir dans un monde de contraintes, mais participer à la définition et à la contestation des contraintes communes. C'est précisément ce pouvoir qu'une interface IA ne doit pas absorber à la place de son utilisateur.

```json
{
  "repond_a": ["D"],
  "questions": []
}
```

*[Note du greffe : formules reproduites dans leur source LaTeX ; le bloc final, affiché sous l'étiquette « JSON », a reçu ses balises ```json.]*
