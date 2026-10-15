# Candidate brief and comparison — 15 October 2026

**User:** CI maintainers reviewing how literal matrix includes and excludes change job coverage.

**Pain and smallest capability:** An include can overwrite an earlier added value while being forbidden to overwrite original axes; appended jobs are not merged by later includes. Expand bounded literal axes and emit a provenance trace for exclusions, merges into originals and independent appended combinations.

**Acceptance criteria:** Earlier added values may be overwritten without changing original axes; appended rows stay independent; excluded combinations can be re-added as appended entries; include-only and256-job boundary work; expressions and product overflow fail.

**Demand evidence:** Inferred operator/developer need, not a verified customer request. Current upstream READMEs, relevant docs/code and accessible issues were inspected. Issue titles below provide context about maintenance and operational work; they are not presented as requests for this tool. No claimed competitor absence is inferred from a successful example here.

**Discovery path:** Accurate repository description/topics, a runnable captured-input example and this evidence file; discoverable by `github actions matrix; github actions local` and the task-specific terms. No unsolicited outreach or activity manipulation.

## Relevant established alternatives found

Live GitHub searches used Most stars ordering; exact queries/URLs/observations are in research-provenance.json. Highest-star relevant comparable found for this bounded workflow: `nektos/act`. Broader collections, tutorials, proxies or unrelated applications in broad results were excluded by relevance; this is not an exhaustive global ranking. Focused invoice-rounding and matrix queries were sparse and broader established tools were retained transparently.

| Comparable | Stars observed | Latest push observed | Archived | API license classification |
| --- | ---: | --- | --- | --- |
| [nektos/act](https://github.com/nektos/act) | 72334 | 2026-08-09T22:50:11Z | False | MIT |
| [actions/runner](https://github.com/actions/runner) | 6327 | 2026-10-14T15:52:02Z | False | MIT |
| [rhysd/actionlint](https://github.com/rhysd/actionlint) | 4326 | 2026-07-16T06:05:57Z | False | MIT |

Observations are dated in research-provenance.json, including README blob hashes and accessible issue links. NOASSERTION means the API did not classify the license; upstream terms must be read before reuse. No upstream source was incorporated.

act executes GitHub Actions locally, the official runner executes jobs, and actionlint checks workflow syntax/types/actions/security. This is a literal expansion explanation, not execution, lint replacement or a demonstrated feature absence in those projects. Official GitHub documentation supplies include/exclude semantics; no assertion is made about unsupported dynamic cases.

Installation and first-use paths were inspected in current documentation, not benchmarked. These alternatives provide broader workflows, operational reliability features, docs/examples and support communities. This tool offers a bounded file/JSON contract, explicit failure modes and runnable fixtures but lacks their broader product capabilities, adoption evidence and maintenance history. Our build/install example measures only our behavior. Competitor installs, time-to-first-result, reliability and technical performance were not measured; no superiority claim or numerical performance comparison is made. Stars inform discovery, not quality or speed.

## Portfolio and candidate distinctness

release-asset-matrix checks uploaded release assets against OS/architecture/archive filename coverage. This traces job expansion and sequential include behavior, with no release metadata, asset verification or shared product identity.

All 178 owned repository identities/descriptions and the current project index were compared. Related release-asset-matrix, table-reconcile, sqlite-rehearsal and traceweave READMEs were inspected. The five candidates have separate users/contracts: backup dependency preservation, Kafka recovery positions, tax allocation arithmetic, span ancestry/interval coverage and CI matrix inclusion provenance. They are independent tools, not renamed/forked/subdivided versions of one product. Shared JSON CLI and packaging scaffolding does not substitute for their distinct algorithms and tests.
