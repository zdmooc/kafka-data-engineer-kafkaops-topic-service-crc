# Historical Kafka Expert — incomplete binary preservation (20 October 2026)

**PARTIAL_MIGRATION / 29_OF_30_EXACT / SOURCE_DELETION_BLOCKED**

Historical source: [kafka-expert](https://github.com/zdmooc/kafka-expert), archived public repository, branch `master`, commit `2e41ea86a53e2bc544b4f1b7644717307dd07da1`.

All **29 text/source files** were copied **byte-for-byte** to `legacy/kafka-expert/`, including Ansible, HLD/DDL, Topic-as-a-Service Python snippets, Filebeat, Logstash, Kafka operational scripts and the Mermaid architecture diagram. Two shell scripts retain their executable mode `100755`.

**ONE BINARY MISSING**: `architecture/hld_diagram.png` (293873 bytes), original Git SHA `3b10458dd20368598016355ac17a1179a78d5d76`. The available GitHub connector rejects the image as non-UTF-8 and cannot return bytes required for `create_blob`. The existing `architecture/hld_diagram.mmd` is preserved, but is **not** a substitute for exact PNG preservation. Do not generate a replacement and call it the same file. No workaround has been attempted.

Full original map: [source-to-target SHA manifest](kafka-expert-source-map.json). **Never delete** `kafka-expert` until the original PNG has been copied as binary and its SHA is checked on the target `main`. The archived source remains intact, including its independent Git history.

This is source preservation only. No Kafka broker, Strimzi, Ansible, Topic-as-a-Service API, CI/CD, performance or security behavior has been exercised in this work.

## Completing binary preservation (Git Bash)

From a trusted local checkout, the owner can copy `architecture/hld_diagram.png` into `legacy/kafka-expert/architecture/hld_diagram.png` of this repository and check `git hash-object` equals the original SHA above. Then update the manifest's `preserved` flag to `true`, commit and push; verify the resulting `main` Git tree. Keep the original repository until those checks pass. Do not expose credentials.
