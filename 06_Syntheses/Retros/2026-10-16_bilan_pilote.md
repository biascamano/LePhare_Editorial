# Bilan de pilote — 2026-10-16

## Activités

| Activité | ID | Statut journal | Tentatives | Durée | Décision de contrôle | Publié ensuite |
|---|---|---|---|---|---|---|
| fil (2026-S42) | 2026-571 | brouillon | 1 | 11 min (journal) | PUBLIER (retenu par le mode) | non (en attente du fondateur) |
| generale | — | non lancée | — | — | — | — |
| curiosite | — | non lancée | — | — | — | — |
| question | — | non lancée | — | — | — | — |

Une seule activité ce jour : le Fil du Phare de la semaine 42, désigné en priorité par `phare.py next`. Les trois activités quotidiennes restent à faire (`next` propose `generale`). L'échantillon est donc très réduit.

Publiés ensuite par le fondateur (toutes périodes) : 2026-567, 568, 569, 570, tous vus par `verify_publication` sans décalage avec l'index.

## 1. Sujets et complémentarité

- **2026-571** — « Le Fil du Phare - Qui a les moyens de vérifier ce qu'on nous affirme ? » (ECON, catégorie `cycle`). Il relie les huit articles 563 à 570 : fusion Paramount-Warner, Ebola au Kenya, opérations d'influence selon OpenAI, sanctions contre la CPI, 722 manuscrits mathématiques, Nobel et Fed, seconde intercalaire (CGPM), et la Question 570 sur les fusions.
- Fil conducteur : les trois conditions posées par 570 (voir, pouvoir agir, durer), appliquées à chaque cas. Penseur : Shapin et Schaffer, *Leviathan and the Air-Pump* (1985), sur la vérification comme dispositif social.
- La connexion est réelle, pas plaquée : 563, 565 et 566 se renvoyaient déjà la question du contrôleur (voir la conclusion de 566). Le Fil la formalise et l'étend aux sciences (722 manuscrits, seconde intercalaire).
- Pas de complémentarité à évaluer avec les autres activités du jour, puisqu'aucune n'a été faite.

## 2. Sources (nombre, nature, ouvertes ou non, sources faibles)

- **11 repères, tous ouverts.** Agences (AP via WSLS, Inquirer, KSAT, ADN ; Reuters via TimesLive), médias (NPR, Al Jazeera), source primaire (dépôt GitHub `openai/math`), reprises (Sinclair/ABC6, Access/Pollstar), Wikipédia EN. S'y ajoute la mention « autres sources dans les articles liés ».
- Sources faibles : les reprises (Sinclair, Access/Pollstar) et Wikipédia. C'est acceptable pour un Fil, qui s'appuie surtout sur les articles déjà contrôlés.
- Retraction Watch n'a pas été retenu, parce que son URL est en `?p=` et que la règle interne contre les liens `?p=` ne distingue pas les liens externes.
- Les repères externes ne sont pas venus dès la V1 : le relecteur a relevé un C1 au cycle 1, puis des C1/m ×4 au cycle 2. L'adaptation 5 du 13/10 (Repères complets dès la V1) n'est pas encore entrée dans la pratique pour le type Fil.

## 3. Contrôle : rédacteur et relecteur

| ID | Autocontrôle (codes) | Relecteur (codes B/m, verdict) | Trouvé par le relecteur seul | Cycles | Décision |
|---|---|---|---|---|---|
| 2026-571 | B1 (569 qualifié de « dossier »), B2 (attribution OpenAI), B3 (« gentlemen » sans source), B2 (échéance CPI), D (longueur ramenée d'environ 1 600 à environ 1 400 mots) | **C1** : B2/B et B1/B (CPI « coupée à terme » des banques et de la tech US, contredit par la licence GL14 ; dépendance non sourcée) ; m : B2 ×3, B3, B1, C1, D2 ; CORRIGER. **C2** (ciblé) : B4/m ×2, B2/m, C1/m ×4 ; PUBLIER | les 2 bloquants CPI ; tous les mineurs | 2 | PUBLIER (retenu par le mode : `wp_draft`) |

Détails :
- Cycle 1 : 24 affirmations vérifiées. Les mineurs portent sur trois B2 (« six mois », « Fed depuis juin », Live Nation « neuf ans » au lieu de près de dix), un B3 (« trois technologies », « ou la refaire »), un B1 (consignes), un C1 (sources externes manquantes) et un D2 (meta « 722 preuves »).
- Cycle 2 : relecture ciblée sur le chemin et les passages modifiés, 14 à 15 affirmations. Deux défauts viennent de la correction elle-même : B2/m (exemptions présentées trop largement) et B4/m (« la Fed a renoncé »). Le troisième, B4/m sur Ebola (hypothèse présentée comme un fait), existait déjà et avait échappé au cycle 1.
- Les mineurs du cycle 2 ont été corrigés à la source, sans 3e cycle, comme le veut la règle.
- **Premier PUBLIER du pilote** (contre 4 BROUILLON sur 4 le 13/10). La règle recalibrée et la relecture ciblée (adaptations 1 et 2 du 13/10) ont fait converger le contrôle en 2 cycles.
- L'autocontrôle et le relecteur ne se recoupent pas : le rédacteur a vu les approximations de formulation, mais pas l'erreur de fond sur la CPI. Cette erreur venait en partie de la formulation reprise de 566 (AP : « cut off from […] US tech companies »), sans la nuance de la licence GL14.

## 4. Corrections et maintiens en brouillon (motifs)

- 2026-571 : corrigé deux fois, aucun maintien en brouillon pour motif éditorial. Il reste en `wp_draft` uniquement à cause du mode brouillons. Note de clôture : « pilote ; contrôle : PUBLIER ».
- Point d'attention : 2 défauts sur 3 au cycle 2 viennent d'une reformulation faite en corrigeant, pas de la V1. C'est le même constat que l'adaptation 4 du 13/10 (vérifier à la source les ajouts faits en corrigeant) : il faut aller plus loin et reprendre la formulation de la source.
- 566 (publié) porte la même formulation que celle corrigée dans 571 (« coupent la Cour […] des entreprises technologiques américaines »), sans mention des exemptions de la licence GL14. Ce n'est pas faux, puisque c'est attribué à AP et suivi d'une mention des exemptions selon Al Jazeera. À examiner en rénovation, sans urgence.

## 5. Rattrapage

Aucun ce jour.

## 6. Journal (erreurs, incohérences avec l'index)

- Journal : 5 lignes (debut 14:33, redaction 14:35, controle_ok 14:43, wp 14:43, fin 14:44, statut `brouillon`). Pas d'erreur. Cohérent avec l'index (2026-571, `wp_draft`, ECON SYNTHESE).
- **Durée à vérifier** : 11 min (de 14:33 à 14:44) est trop court pour une séance qui a enchaîné deux relectures (176 s puis 107 s) et un compactage du contexte. Les horodatages `redaction` et `controle_ok` semblent avoir été posés en rafale, pas au fil de l'eau. La durée du journal sous-estime donc la séance réelle.
- Le Fil est compté sous la période `2026-S42`. Pour `next`, la journée du 16/10 reste donc « rien aujourd'hui » côté quotidien. C'est le comportement attendu, mais il peut surprendre en lisant `— état`.

## 7. Ressources (durée, lectures, recherches, appels à l'agent)

- Durée : 11 min selon le journal, en réalité nettement plus (voir section 6).
- Lectures : les 8 articles reliés, la mémoire éditoriale et l'état courant, le Radar.
- Agent `relecteur-prepublication` : 2 appels. Cycle 1 : environ 59 500 tokens, 176 s, 24 outils. Cycle 2 : environ 43 800 tokens, 107 s, 15 outils. Le cycle ciblé coûte environ 26 % de tokens en moins et 39 % de temps en moins.
- Scripts : `daily_run` (push en brouillon), `memoire_append`, `build_etat_courant`, `verify_publication` (7 articles, 0 erreur, 1 avertissement : 571 en draft).

## 8. Difficultés techniques

- Le contexte a été compacté en cours de séance. La séance a pu reprendre sans perte, mais c'est un risque pour un Fil, qui lit beaucoup.
- nobelprize.org a renvoyé une erreur 403 au relecteur. La vérification est passée par d'autres sources.
- Le résultat du vote de la CGPM du 15 octobre était introuvable. Le Fil reste au conditionnel.
- Radar : 34 entrées pour un plafond de 30. Il faut fusionner ou archiver à la prochaine rétro hebdomadaire.
- Relier en retour en attente de publication : 562 → 571 et 570 → 571. 570 étant publié, il faut aussi vérifier 563 → 570 : la Question suivante de 563 pointe déjà vers `question-du-phare-fusion-promesses-qui-verifie/`, ce lien semble donc fait.

## 9. Adaptations proposées

1. **Repères externes dès la V1 pour un Fil** : au moins un repère externe par article relié qui contient une affirmation reprise, avant l'autocontrôle. Cela rend effective l'adaptation 5 du 13/10, qui ne l'était pas encore.
2. **Correction à la lettre de la source** : en corrigeant un défaut B, reprendre la formulation de la source (ou la citer) plutôt que reformuler. 2 défauts sur 3 du cycle 2 en viennent.
3. **Héritage d'une formulation déjà publiée** : quand un Fil ou une Question reprend un fait d'un article lié, revérifier ce fait à la source primaire, même si l'article lié a été contrôlé (cas de la CPI repris de 566).
4. **URL externes en `?p=`** : la règle anti-`?p=` vise les liens internes. Préciser dans `Controle_prepublication.md` qu'une URL externe en `?p=` est acceptable si elle est stable (Retraction Watch).
5. **Horodatage des étapes** : poser `etape redaction` et `etape controle_ok` au moment réel, pour que la durée du journal mesure la séance.
6. **Bilan sur une journée complète** : ne tirer de conclusion sur le taux de PUBLIER qu'après une journée à quatre activités. Celui-ci repose sur un seul Fil.

## Recommandation

**Poursuivre le pilote.** Premier PUBLIER en 2 cycles, convergence obtenue grâce aux adaptations du 13/10 (règle bloquant / mineur, relecture ciblée). Mais l'échantillon se limite à un seul article, d'un type particulier (Fil), et deux faiblesses persistent : les repères externes tardifs et les défauts introduits en corrigeant (adaptations 1 et 2).

Ne pas passer en production avant une journée complète de quatre activités qui confirme ce taux. **Aucun passage en production sans validation du fondateur** (suppression de `00_Systeme/Mode_brouillons.md` par lui seul).

**Décision du fondateur (2026-10-16)** : poursuivre le pilote. Après 2 relectures, publier s'il ne reste aucun défaut bloquant. Les relectures doivent rester courtes et peu coûteuses : budget de 15 appels web au cycle 1 et 6 au cycle 2, sortie limitée aux écarts (`Controle_prepublication.md`, plan.md v5.13).
