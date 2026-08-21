# CARB Benchmark — Exclusive Research Findings & Archive

This directory serves as the canonical, immutable archive for all empirical research findings, telemetry records, per-task audits, and statistical analyses of the **Controlled Agent-Role Benchmark (CARB)**.

## Directory Structure & Academic Index

- **[`01_EXECUTIVE_FINDINGS_V3.md`](./01_EXECUTIVE_FINDINGS_V3.md)**: Master executive research paper for CARB-v3. Contains primary accuracy rates, exact paired McNemar significance statistics, power analysis, and core architectural insights.
- **[`02_DISCRIMINATIVE_MATRIX_AND_PER_TASK_DATA.md`](./02_DISCRIMINATIVE_MATRIX_AND_PER_TASK_DATA.md)**: Complete 39-task discriminative dataset table with task difficulty tiers, pass/fail status, wall-clock latencies, tool iteration counts, token usages, and diff metrics.
- **[`03_VICTORY_FORENSICS_AND_CASE_STUDIES.md`](./03_VICTORY_FORENSICS_AND_CASE_STUDIES.md)**: Forensic case studies of the 10 distinct tasks where challenger agent systems succeeded and the baseline failed.
- **[`04_TELEMETRY_AND_EFFICIENCY_ANALYSIS.md`](./04_TELEMETRY_AND_EFFICIENCY_ANALYSIS.md)**: Deep statistical breakdown of wall-clock time distributions, tool-call densities, and token consumption economics.
- **[`05_CALIBRATION_METHODOLOGY_AND_POOL_DYNAMICS.md`](./05_CALIBRATION_METHODOLOGY_AND_POOL_DYNAMICS.md)**: Phase A empirical calibration protocol, 131-candidate pool evaluation, and pre-registered selection boundaries.
- **[`06_DATA_INTEGRITY_AND_HARNESS_AUDIT.md`](./06_DATA_INTEGRITY_AND_HARNESS_AUDIT.md)**: Full transparency audit covering test harness bug resolutions, evaluator strictness nuances, and OAuth disruption recovery.
- **[`v3_dataset_manifest.json`](./v3_dataset_manifest.json)**: Machine-readable JSON manifest containing complete per-task telemetry and outcome records.
- **[`v2_canonical_archive/`](./v2_canonical_archive/)**: Standalone historical archive of CARB-v2 (50 tasks), documenting the 94% ceiling effect that motivated v3.

---

## Benchmark Snapshot

| Metric | CARB-v2 (50 Tasks) | CARB-v3 (39 Tasks) |
|---|:---:|:---:|
| **Design Focus** | Broad Task Pool Coverage | Empirically Calibrated Hard Tasks |
| **Baseline Accuracy** | 94.0% (47/50) | 0.0% (0/39) |
| **Superpowers Accuracy** | 92.0% (46/50) | 17.9% (7/39) |
| **Supreme Agent Accuracy** | 94.0% (47/50) | **23.1% (9/39)** |
| **Statistical Discrimination** | None ($p = 1.0$) | **Statistically Significant ($p < 0.01$)** |
