# Réponse de Claude au message 5/6 : audit du fonctionnement réel

**Date : 12 octobre 2026**

**Méthode** : lectures en lecture seule des skills (`.claude/skills/routine-*/SKILL.md`), de `plan.md`, des scripts `tools/`, de la mémoire, du Radar, de l'état courant et de l'historique git. Aucun fichier du système n'a été modifié.

**Marquage** : **[V]** vérifié dans un fichier ou une commande · **[D]** déduit · **[P]** proposé · **[A]** à arbitrer par le fondateur.

Ce qui figure déjà dans la réponse 4 n'est pas répété ici : volumes depuis la V5, stock, politique de maintenance, contradictions. Les renvois prennent la forme « R4 §n ».

---

## 0. Trois corrections préalables

1. **La V5 est implémentée.** Elle ne se limite pas à un plan. **[V]** Le commit `16c3283` du 2026-10-06 l'a mise en place : skill quotidienne réécrit, `build_etat_courant.py`, Radar. Les décisions D12 à D16 sont consignées dans `plan.md` §3. Le message 5 décrit donc pour l'essentiel ce que les skills font déjà. Les écarts réels sont listés au §1.
2. **Les 7 domaines du message 5 correspondent déjà à la taxonomie.** **[V]** Les 7 codes thème sont `MONDE`, `POL`, `ECON`, `TECH`, `CLIMAT`, `SCIENCE` et `CULTURE` (`plan.md` D2, `validate_index_editorial.py`), et la mensuelle les utilise déjà à l'étape 9. Seul l'intitulé diffère : « Culture & Philosophie » / `CULTURE`. Les dossiers de fichiers sont au nombre de 6, car `MONDE` est rangé sous `Politique_Societe`. J'avais signalé à tort une absence de « Monde ».
3. **Un journal des décisions existe déjà en partie.** **[V]** `plan.md` §3 contient 17 décisions au format `# | Sujet | Décision | Date`. Il manque, par rapport au format proposé, les colonnes Justification, Références et Validation. `plan.md` §13 tient le journal des évolutions. Les décisions courantes laissent elles aussi une trace : archives du Radar (colonne « Raison »), mémoire §3 (« 2 articles : pas de Fil du Phare »), `Signalements_renovation.md` et `Propositions_fonds/`. Ce qui manque est précisé au §4.

---

## 1. Routine quotidienne : réel contre V5

| Point demandé | Réel (skill `routine-quotidienne`) | Écart avec le message 5 |
|---|---|---|
| Fichiers lus | **[V]** Trois lectures par défaut : `Etat_editorial_courant.md` (48 lignes), `Radar_editorial.md` (90 lignes), veille web. S'y ajoutent le skill (211 lignes) et `CLAUDE.md`, chargés à chaque session. | Aucun. La V5 parle de « lire les métadonnées des 5 à 10 dernières publications » ; dans les faits, elles arrivent condensées par l'état courant. Aucun fichier d'article n'est lu à cette étape. |
| Ordre | **[V]** État courant → Radar → veille (D12). | Conforme. |
| Veille | **[V]** Recherche web faite par Claude, 24 à 72 h, « presse sérieuse ». Elle est réduite à un contrôle si le Radar contient déjà un candidat fort. **[V]** Aucune liste de sources n'est fixée et aucune trace de la veille n'est conservée. | Le message 5 ne demande pas de liste de sources. **[D]** C'est pourtant le point le plus faible pour l'objectif « ne pas manquer une actualité majeure hors dossiers » (voir §7). |
| Candidats | **[V]** 5 au plus, dont 1 à 3 issus de la veille, de sortes A/B/C/D. | Conforme. |
| Critères | **[V]** 5 critères notés Faible / Moyen / Fort, avec un ordre de priorité en cas d'égalité. | Conforme. |
| Type | **[V]** Choisi après le sujet, sans équilibrage. | Conforme. |
| Doublons | **[V]** Aucun contrôle automatique de doublon éditorial. La recherche ciblée passe par `index_lookup.py --search` (5 liens au plus), au jugement de Claude. Les scripts ne détectent que les doublons **techniques** : un post WP créé deux fois, une ligne d'index en double. | Le message 5 demande de « vérifier que le sujet n'a pas été traité de manière équivalente ». C'est prévu dans la consigne, sans aucun garde-fou outillé. |
| Sources | **[V]** Pour les faits, aucune vérification outillée. `verify_publication.py` contrôle la **forme** : liens internes, maillage, URL nues, statut WP, tag. **[V]** `stage` contrôle la conformité de l'en-tête et de l'index (v3). La vérification factuelle repose entièrement sur Claude pendant la rédaction. | Aucun écart avec le texte de la V5, mais c'est le risque n°5 du message 5 (hallucinations) et rien ne le mesure. |
| Mémoire | **[V]** `memoire_append.py` (§1), retrait et ajout dans le Radar, puis `build_etat_courant.py`. Mises à jour ciblées, sans reconstruction du catalogue. | Conforme. |
| Conditions de publication | **[V]** Publication directe sur WP (`daily_run`, statut publié) sauf variante « brouillons seulement ». **[V]** Aucune option de report : le skill ne prévoit pas de « ne rien publier aujourd'hui ». **[V]** Déclenchement manuel par l'utilisateur, sans cron (D4). | **Écart réel** : le report (Q16, option 2) n'existe pas dans la quotidienne. Il existe déjà dans l'hebdomadaire (« moins de 3 articles : pas de Fil ») et dans la mensuelle (« 0 est une réponse valide »). |
| Cadence | **[V]** Le skill dit « un article par jour ». **[V]** Les commits montrent des articles produits par deux (563+564, 565+566) et des rattrapages datés du même jour (531–548 datés du 2026-10-05). | **[D]** Comme le déclenchement est manuel, la cadence réelle dépend des sessions de l'utilisateur, pas du système. « Un par jour » est en pratique « un par déclenchement ». |

**Écarts réels de la quotidienne** (les autres points sont conformes) :
1. absence d'option de report ;
2. aucune trace de la veille ni de l'arbitrage : le rapport final (candidats, notes, raison du choix) ne s'affiche que dans la session et n'est pas conservé (§4) ;
3. aucun contrôle outillé des doublons éditoriaux ;
4. une entrée `P?` ajoutée au Radar sans priorité (566) : la quotidienne ajoute, l'hebdomadaire priorise, ce qui est conforme à D14 mais laisse des trous jusqu'au comité.

---

## 2. Routine hebdomadaire

**Le Fil du Phare est produit manuellement.** **[V]** Il ne s'agit ni d'une génération automatique ni d'un simple projet : l'utilisateur déclenche la routine (« routine hebdomadaire »), puis Claude relit, rédige et publie en suivant le skill. La structure en 7 parties du message 5 est **déjà celle du skill**, mot pour mot.

| Point | Réel |
|---|---|
| Synthèse des publications | **[V]** Lecture de la mémoire §1 (7 jours), puis des fichiers canoniques des articles de la semaine. |
| Détection des connexions | **[V]** Faite par Claude, selon une consigne qualitative (« questions récurrentes, tensions communes… »). Aucun outil. |
| Seuil | **[V]** Moins de 3 articles : pas de Fil. Cela s'est produit deux fois (mémoire §3). |
| Fils actifs | **[V]** Mémoire §2, avec 5 fils actifs au plus. Ils sont 5 aujourd'hui, avec 4 fils de côté et 0 clôturé. |
| Pistes | **[V]** 3 à 5, consignées dans la mémoire §3. |
| Radar | **[V]** Le comité trie les blocs 1 à 3, mais **[V]** le Radar compte aujourd'hui **34 entrées actives pour un plafond de 30** (13 + 9 + 3 + 4 + 5). |
| Fils publiés | **[V]** 2 (547, 562), tous deux produits les 5 et 6 octobre pendant la mise en place. **[D]** Il n'y a pas encore de recul sur un cycle hebdomadaire réel. |

**Écart à signaler** : le fil « Le prix de l'invisible » regroupe 12 articles, et sa justification devient fragile. **[D]** Un fil qui accueille Ebola, la publicité dans ChatGPT et la persévérance en physique risque la « connexion artificielle » (risque n°3 du message 5). L'hebdomadaire n'a aucun critère de scission ou de clôture d'un fil trop large.

---

## 3. Routine mensuelle

| Point | Réel |
|---|---|
| Sources | **[V]** Catalogue régénéré (`build_catalogue.py`, 771 lignes), Radar complet, mémoire §1 à §4. C'est la seule routine qui lit la vue large. |
| Dossiers | **[V]** Règle : « un mot qui revient ne suffit pas ». Les hubs sont régénérés par `build_hubs.py` (déterministe). La création se fait par `new_article.py create --type dossier`. |
| TF | **[V]** 0 à 2 par mois, à partir du Radar (bloc 4) et des lacunes du catalogue. |
| Sentier | **[V]** 0 à 2 ateliers. Jamais de 11ᵉ fondamental ni de push sur `02_Fonds/`. |
| Liens internes | **[V]** Étape 8 : proposition dans le rapport, avec seulement un ajout « évident » autorisé. |
| Radar | **[V]** Archivage au-delà d'un mois sans suite et purge des archives de plus de 3 mois. |
| Mémoire courte | **[V]** Mémoire §4 (cap) et §5 (condensé), puis `build_etat_courant.py`. |
| Cap | **[V]** Mémoire §4, avec 2 à 4 dossiers prioritaires. |
| Exécutions réelles | **[V]** Une seule exécution complète, pour septembre (rapport `06_Syntheses/Rapports_mensuels/2026-09.md`), plus une « mise à jour légère » du cap d'octobre (`8c5caf8`). |

**Écart constaté : le résumé vieillit.** **[V]** Le cap d'octobre (mémoire §4, repris dans l'état courant) annonce « audition de Philadelphie (7 octobre) ». Le Radar et la mémoire §2 disent pourtant « reportée au 26 octobre ». **[V]** La mémoire §5 indique pour septembre « tous les articles sont en brouillon WordPress », ce qui n'est plus vrai. Ce sont des instantanés : ils étaient exacts quand ils ont été écrits. C'est la réponse concrète à « comment un résumé peut déformer » (voir §7).

---

## 4. Architecture mémoire réelle

| Couche | Fichier | Taille | Écrit par | Lu par |
|---|---|---|---|---|
| 1. Mémoire courte | `Etat_editorial_courant.md` | 48 lignes | **généré** (`build_etat_courant.py`) | quotidienne |
| 2. Radar | `Radar_editorial.md` | 90 lignes, 34 actives | les 3 routines (D14) | les 3 |
| (sens) | `Memoire_editoriale.md` | 142 lignes, §1 à §5 | les 3 routines | hebdo, mensuelle ; la quotidienne seulement au besoin |
| 3. Catalogue | `Catalogue_editorial.md` | 771 lignes | **généré** (`build_catalogue.py`) | mensuelle |
| 4. Index | `index_editorial.csv` | 528 lignes | scripts uniquement (`index_editorial_utils`) | scripts, `index_lookup.py` |
| Décisions | `plan.md` §3, §13 | 760 lignes au total | Claude, à la demande | aucune routine ne le lit |
| Maintenance | `Inventaire_renovation.md` (généré), `Signalements_renovation.md`, `Propositions_fonds/` | 181 + 18 lignes | rénovation, routines | rénovation |
| Technique | `Logs/daily_run_*.{json,log}` | 1 paire par jour de run | `daily_run` | personne en routine |
| Configuration | `tools/*.local.json` (non versionnés), `editorial_config.example.json` | — | humain | scripts |
| Caches | **[V]** Aucun cache applicatif. Des snapshots WP sont présents dans `Manifests/`. | — | — | — |

Les **4 couches du message 5 existent toutes [V]**, avec la mémoire en plus. Ce n'est pas un doublon : l'état courant est **dérivé** de la mémoire et du Radar, et n'est jamais édité.

**Doublons et reconstructions** :
- **[V]** Aucune reconstruction inutile en quotidienne : `build_etat_courant.py` lit 2 fichiers et écrit 48 lignes. Le catalogue n'est reconstruit qu'en mensuelle, deux fois dans la même routine (étapes 1 et 10), ce qui est justifié puisque le mois a changé entre-temps.
- **[V]** Doublon fonctionnel : les « prochaines pistes » figurent à la fois en mémoire §2 (colonne « Prochaine piste »), en mémoire §3 (« Pistes pour la semaine suivante ») et dans le Radar bloc 1. Ce sont trois copies d'une même information, d'où l'incohérence Philadelphie relevée au §3.
- **[V]** Doublon documentaire : `00_Systeme/` contient 37 entrées, dont au moins 8 documents obsolètes ou archivés : `Routine_quotidienne.md`, `Routine_quotidienne_V2.md`, `Briefing_slow_…_PROTOTYPE.md`, `Automatisation_editoriale_v1.md`, `Automatisation_wordpress_v1.md`, `Architecture_orchestrateur_…`, les deux `Memo_prompt_court_…`. D7 a choisi de les garder sous bandeau « ARCHIVÉ ». **[D]** Ils ne coûtent rien en routine, puisqu'ils ne sont pas lus, mais ils brouillent toute lecture humaine ou par un autre modèle.

**Ce qui manque vraiment pour le journal des décisions (X)** : **[V]** la raison d'un **choix de sujet** n'est conservée nulle part. Le rapport final de la quotidienne (5 candidats, notes, « pourquoi celui-là ») disparaît avec la session, sauf ce qu'en reprend le message de commit. Les autres décisions de la liste X sont déjà tracées :

| Décision | Trace |
|---|---|
| Dossier | rapport mensuel |
| Relation entre articles | en-tête `Article precedent` et mémoire §1 |
| Archivage Radar | colonne « Raison » des archives |
| Correction | `Remarques` de l'index et `Signalements_renovation.md` |
| Fondamental | `Propositions_fonds/` |
| Décision structurante | `plan.md` §3 |

**[P]** La réponse la plus simple ne passe pas par un nouveau fichier. Il suffit d'ajouter **une ligne « Arbitrage »** à la mémoire §1 (ou de conserver la ligne « Candidats / Pourquoi celui-là » du rapport). Pour les décisions structurantes, on compléterait `plan.md` §3 avec les colonnes **Justification** et **Validation** (fondateur / Claude / proposé).

---

## 5. Consommation de ressources

**Ce qui n'est pas mesurable [V]**
- **Nombre d'appels modèle** : la rédaction est faite par Claude Code dans une session interactive, sans API externe (`--use-api-llm` et les flags `*_api_enabled` sont désactivés par défaut). Il n'existe pas d'« appels » séparés à compter : une routine est **une session**.
- **Tokens** : aucune mesure n'est disponible dans le dépôt. Les logs `daily_run` ne contiennent que la partie technique (WP, maillage). **Je ne donne donc aucun chiffre de tokens.**

**Ce qui est mesuré (en lignes, pas en tokens) [V]**

| Routine | Lectures fixes | Variable |
|---|---|---|
| Quotidienne | `CLAUDE.md` + skill (211) + état courant (48) + Radar (90) | **veille web** (non bornée, sauf « 5 à 10 sujets ») + ≤ 5 lookups + rédaction |
| Hebdomadaire | skill (103) + mémoire (142) + Radar (90) | **les fichiers complets des articles de la semaine** (souvent 5 à 10 articles de 1 000 mots) |
| Mensuelle | skill (105) + catalogue (771) + mémoire + Radar | articles du mois, dossiers, fondamentaux parents |
| Rénovation | skill + inventaire (181, lu par section) | **resynchronisation WP et réécriture** (articles longs) |

**Opérations les plus coûteuses [D]** (d'après la nature des lectures, sans mesure)
- La **veille web** de la quotidienne, qui n'a aucun plafond explicite de recherches.
- La **relecture intégrale des articles** dans l'hebdomadaire.
- La rénovation, lot 3.
- Les répétitions de `verify_publication.py` après `--fix` sont négligeables (script local et appels WP).

**Risques de dépassement [D]**
- Une session qui enchaîne plusieurs routines (le cas des 5 et 6 octobre) atteint la limite de contexte et déclenche une compaction. C'est ce qui s'est passé dans **cette** session d'alignement.

**Économies sans perte de qualité [P]**
- (a) L'hebdomadaire lit l'**en-tête et la dernière section** des articles plutôt que le texte entier ; elle n'ouvre le corps complet que des articles candidats au « lien invisible ».
- (b) Plafonner la veille quotidienne à un nombre de recherches, qui reste à fixer après observation, **sauf** pour la vérification des faits de l'article retenu. Ce sont les deux budgets du message 5 : je les approuve.
- (c) Supprimer la triple copie des pistes (§4).

---

## 6. Développement futur : présent, documenté, idée

| Élément | Statut | Utilité | Complexité | Coût | Dépendances | Risque de maintenance |
|---|---|---|---|---|---|---|
| Fil du Phare | **présent** [V] | forte | — | 1 session/semaine | ≥ 3 articles | faible |
| Dossiers + hubs | **présent** [V] (12 lignes DOSSIER, 11 brouillons, R4) | forte | moyenne | mensuelle | `build_hubs.py` | moyen (11 brouillons à trier) |
| TF, ateliers | **présent** [V] | forte | faible | mensuelle | manifeste Sentier | faible |
| Navigation entre articles | **présent** [V] (nav v3, `verify_publication`) | forte | faible | nulle | index | faible |
| Rénovation | **présent** [V] (D17) | forte | moyenne | sessions dédiées | WP pull/refresh | moyen |
| Newsletter | **documenté, non implémenté** [V] (aucun script, aucun skill) | moyenne à forte (fidélisation) | faible à moyenne | outil externe à choisir | Fil du Phare | faible si elle reprend le Fil |
| Synthèses visuelles | idée [V] (aucun outil) | moyenne | moyenne | humain ou outil d'image | — | moyen |
| Ressources pédagogiques imprimables | idée | moyenne | moyenne | — | Sentier stabilisé | moyen |
| Recherche par concepts | idée [V] (aucune colonne concept, R3) | moyenne | **forte** (taxonomie WP) | — | migration de tags | **fort** (interdit X.5 pendant l'alignement) |
| Podcast, vidéo, espace membre, contributeurs, formation, livres | idées non confirmées (message 5 lui-même) | — | forte | — | public existant | fort |

**[D]** Le seul projet à fort rapport utilité/coût qui ne soit pas encore présent est la **newsletter fondée sur le Fil du Phare** : elle réemploie un contenu déjà produit chaque semaine. Tout le reste dépend soit d'un lectorat mesuré, soit d'une migration de taxonomie.

---

## 7. Analyse critique : réponses aux huit questions

**1. La V5 peut-elle choisir le meilleur prochain article avec un contexte réduit ?**
- **Oui pour la continuité, non pour la nouveauté.** **[D]** L'état courant et le Radar donnent une très bonne vue de « derrière » et de « devant ».
- La part « autour » repose sur une veille web non tracée et sans repères fixes. Le risque n'est pas le manque de contexte interne, c'est le **biais vers le Radar**. Le skill dit d'ailleurs que si le Radar a un candidat fort, la veille « se limite à vérifier ». Sur les 36 publications, les fils actifs absorbent la majorité des articles récents (R4 §1).
- **[P]** Objection : il faut un garde-fou de nouveauté, pas plus de contexte. Par exemple, **au moins un candidat sur cinq sans lien avec un fil actif**, noté sur ses mérites propres.

**2. Comment éviter qu'un résumé déforme les décisions passées ?**
- **[V]** C'est déjà observable (Philadelphie, §3).
- **[P]** Trois règles simples :
  - (a) Une information datée n'a **qu'une seule source**, le Radar (blocs à échéance). La mémoire §2 à §4 **renvoie** au Radar au lieu de recopier les dates.
  - (b) Tout résumé porte sa date (`point au …`), ce qui est déjà le cas pour les catégories sous-représentées.
  - (c) Le cap mensuel n'est pas corrigé en cours de mois, mais l'état courant prend les échéances dans le Radar, pas dans le cap.
- C'est une simplification, pas un ajout.

**3. Comment contrôler l'importance des actualités hors dossiers ?**
- **[D]** La note « importance actuelle » est le seul critère indépendant de l'historique, et rien ne l'étalonne.
- **[P]**
  - Fixer une courte liste de **sources de veille de référence**, à arbitrer par le fondateur : agences, quotidiens de référence, sources institutionnelles.
  - Conserver dans la trace d'arbitrage (§4) les 1 à 3 candidats de veille **écartés** et la raison.
  - L'hebdomadaire peut alors vérifier si une actualité majeure a été ignorée plusieurs jours de suite. C'est un indicateur simple et vérifiable du risque n°4 (dépendance à l'historique).

**4. Quelles étapes nécessitent réellement un modèle ?**
- Veille et jugement d'importance.
- Arbitrage entre candidats.
- Choix du type.
- Rédaction.
- Vérification des faits par croisement des sources.
- Formulation de la Question du Phare.
- Détection d'un lien invisible (hebdo) et d'un phénomène (mensuelle).
- Décision de rénovation (lot 3).

**5. Quelles opérations peuvent être déterministes ?**
- **[V]** Elles le sont déjà :
  - IDs, index, slugs, catégories et tags (`new_article.py`) ;
  - état courant, catalogue, hubs et inventaire de rénovation ;
  - maillage (`post_linking.py`) ;
  - contrôles de forme (`verify_publication.py`, `stage`) ;
  - publication WP.
- **[P]** Pourraient l'être en plus :
  - le **compteur du Radar** (alerte au-delà de 30, entrées `P?`), dans `build_etat_courant.py` ;
  - la **liste des échéances dépassées** ;
  - un **contrôle de proximité de titre ou de question** contre l'index avant `create`, qui avertirait sans bloquer ;
  - la **répartition par thème** sur 30 jours dans l'état courant.

  Ce sont quatre ajouts à des scripts existants, sans nouveau fichier.

**6. Comment éviter qu'une optimisation des tokens augmente les erreurs ?**
- **[P]** Une seule règle : **on ne coupe jamais dans la vérification de l'article en cours**, c'est-à-dire les sources des faits avancés, les URLs internes lues dans l'index et les chiffres datés. On coupe dans le contexte d'orientation : relectures d'articles anciens, vue large, recopies.
- **[V]** Le dispositif actuel respecte déjà cette séparation, car les économies portent sur les lectures de contexte, pas sur la veille. Il ne l'écrit pas : à inscrire dans le skill sous la forme des deux budgets du message 5.

**7. Comment préserver le contrôle humain ?**
- **[V]** Le contrôle humain existe aujourd'hui à trois endroits :
  - le déclenchement manuel (D4) ;
  - le refus de `02_Fonds/` et des fondamentaux ;
  - le lot 1 de rénovation.
- **[V]** Il n'existe pas sur la publication quotidienne, qui part en publié sans relecture.
- **[A]** C'est la question centrale du message 6 (tension 3). Trois options :
  - le statu quo ;
  - le brouillon par défaut avec publication par le fondateur ;
  - le publié par défaut, sauf pour les sujets « sensibles » à définir (conflits armés, santé, personnes nommées), qui passeraient en brouillon.

  Je recommande la troisième option (voir réponse 6).

**8. Comment rester maintenable ?**
- **[D]** Le système est aujourd'hui à la limite :
  - 23 scripts ;
  - 5 skills, dont un archivé ;
  - 37 entrées dans `00_Systeme/` ;
  - un `plan.md` de 760 lignes ;
  - une mémoire à 5 sections ;
  - un Radar à 5 blocs.
- **Objection au message 5 et aux messages 3 et 4** : chaque proposition prise isolément est raisonnable (journal, 6 statuts de maintenance, 9 relations, 16 métadonnées, deux budgets, quatre fonctions intellectuelles). Additionnées, elles doublent la surface.
- **[P]** Règle proposée : **toute nouvelle fonction doit remplacer ou fusionner une structure existante, ou démontrer un problème observé.** Exemples :
  - ajout de colonnes à `plan.md` §3 plutôt qu'un journal séparé ;
  - Radar seule source des échéances plutôt que trois copies ;
  - un `README` de `00_Systeme/` qui liste les 10 fichiers vivants, plutôt qu'un déplacement des archives.

---

## 8. Ce qui reste à arbitrer (ajouté à la liste de R4 §9)

6. **[A]** La quotidienne peut-elle **ne rien publier** (Q16, option 2) ? Si oui, le skill gagne une sortie « report motivé », tracée dans la mémoire §1.
7. **[A]** Publication directe ou brouillon pour les sujets sensibles (§7.7) ?
8. **[A]** Liste de sources de veille de référence (§7.3) : la fixer, ou laisser le jugement de Claude ?
9. **[A]** Conserver la trace d'arbitrage quotidien (candidats écartés), au prix d'une ligne par jour ?

La réponse 6 reprend l'ensemble sous la forme du rapport d'alignement demandé.
