# Kafka Expert — conservation intégrale confirmée (20 octobre 2026)

**Statut : 30/30 ORIGINAL_BLOBS_EXACT / MERGED_MAIN / SOURCE_DELETED_BY_OWNER_VERIFIED_404_2026-10-20**

## Provenance et intégrité

Source historique : [kafka-expert](https://github.com/zdmooc/kafka-expert), dépôt public archivé, branche originale `master`, commit `2e41ea86a53e2bc544b4f1b7644717307dd07da1`.

Cible : [kafka-data-engineer-kafkaops-topic-service-crc](https://github.com/zdmooc/kafka-data-engineer-kafkaops-topic-service-crc), sous `legacy/kafka-expert/`.

- **30/30 fichiers copiés à l'identique depuis la branche `master`** : 29 fichiers texte/source et un schéma PNG binaire.
- **0 fichier manquant, 0 divergence de SHA Git, modes originaux conservés**, y compris les deux scripts shell exécutables `100755`.
- **Schéma original** : [`architecture/hld_diagram.png`](kafka-expert/architecture/hld_diagram.png), taille 293873 octets, blob SHA `3b10458dd20368598016355ac17a1179a78d5d76`.
- [Manifeste complet : chemins, modes, SHA d'origine](kafka-expert-source-map.json).

## Preuves techniques

Le transfert binaire a été réalisé directement entre deux clones GitHub au sein d'un workflow public, sans tentative de décodage UTF-8 du PNG :

1. [Exécution GitHub Actions réussie](https://github.com/zdmooc/kafka-data-engineer-kafkaops-topic-service-crc/actions/runs/39484111012) : toutes les étapes en succès, dont contrôle du SHA original et de la taille du PNG.
2. [PR #2 fusionnée](https://github.com/zdmooc/kafka-data-engineer-kafkaops-topic-service-crc/pull/2), commit `baa6ca4036102871cde2bdc030869f927ebe21cb`.
3. **Arbre GitHub `main` revérifié : 30/30 SHA/modes concordants** entre la source archivée et le sous-arbre `legacy/kafka-expert/` du dépôt cible.

## Décision relative à l'ancien dépôt

Le propriétaire a **supprimé manuellement le dépôt `kafka-expert` le 20 octobre 2026**. Le contrôle GitHub `get_repo` a renvoyé **404**, et l'inventaire du portefeuille est passé à **73 dépôts dont 5 archivés**. Les **30/30 fichiers d'origine** sont toujours présents sur `main` du dépôt canonique, avec les empreintes SHA et modes identiques, dont le PNG de 293 873 octets. L'historique Git autonome, les éventuels tags, tickets, artefacts de release et paramètres de l'ancien dépôt n'ont pas été transférés.

**Aucune suppression n'a été effectuée par l'assistant : le propriétaire a supprimé la source.** Ne pas présenter les fichiers et manifestes archivés comme une validation runtime : aucun broker Kafka, service Topic-as-a-Service, Ansible, environnement CRC ou système Elastic/OpenSearch n'a été exécuté ou vérifié pendant cette consolidation.
