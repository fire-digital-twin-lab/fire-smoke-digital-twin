# AGENTS.md

## Purpose

This file defines the operating rules for coding agents working in this repository.

The repository implements the pipeline:

BIM/IFC → Building Graph → Scenario Generation → CFAST/FDS → Virtual IoT → Dataset → AI Models → Dashboard.

Agents must preserve module boundaries, shared data contracts, reproducibility, and the P0 scope of the research proposal.

---

## 1. General operating rules

A coding agent must:

1. Work only inside the scope explicitly assigned by the user.
2. Inspect relevant module documentation before changing code.
3. Prefer the smallest safe change that satisfies the task.
4. Update or add tests for every behavior change.
5. Preserve backward compatibility at module boundaries unless a contract change is explicitly requested.
6. Never modify generated data, simulation outputs, checkpoints, or large binary assets.
7. Never silently broaden the scientific scope of the project.
8. Never commit secrets, credentials, local machine paths, or private data.
9. Never bypass failing tests, lint checks, validation, or CI.
10. Never delete existing code unless the task clearly requires it and the replacement is verified.

Before editing a module, read:

- `README.md`
- `ARCHITECTURE.md`
- `SCOPE.md`
- `MODULE_OWNERS.md`
- `CONTRIBUTING.md`
- `docs/data_contracts.md`
- the module README under `src/fire_smoke_dt/<module>/README.md`
- the corresponding document under `docs/modules/`

---

## 2. Files agents must not modify without explicit approval

Agents must not edit the following files unless the user explicitly requests that exact class of change.

### Repository governance and CI

- `.github/CODEOWNERS`
- `.github/workflows/**`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `CONTRIBUTING.md`
- `MODULE_OWNERS.md`
- `ARCHITECTURE.md`
- `SCOPE.md`
- `FILE_MANIFEST.md`
- `AGENTS.md`

### Packaging, dependencies, and environment

- `pyproject.toml`
- `requirements.txt`
- `docker-compose.yml`
- `.gitattributes`
- `.gitignore`
- `.env.example`

Dependency changes require:

- a clear reason,
- minimal version changes,
- verification that installation still works,
- updated documentation when setup commands change.

### Shared contracts and configuration

- `configs/schema_version.yaml`
- `configs/scenario_schema.yaml`
- `configs/sensor_schema.yaml`
- `configs/label_rules.yaml`
- `configs/noise_presets.yaml`
- `configs/split_rules.yaml`
- `configs/model_configs/**`

- `src/fire_smoke_dt/shared/schema.py`
- `src/fire_smoke_dt/shared/labels.py`
- `src/fire_smoke_dt/shared/validation.py`
- `src/fire_smoke_dt/shared/io_utils.py`
- `src/fire_smoke_dt/shared/paths.py`

These files define contracts used by multiple modules. A change is allowed only when the task explicitly requests a contract change.

Any approved contract change must also include:

1. an update to `configs/schema_version.yaml`,
2. an update to `docs/data_contracts.md`,
3. compatibility notes,
4. updated unit or integration tests,
5. review by the repository lead or relevant module owners.

---

## 3. Module ownership and edit boundaries

Agents must not modify another module merely to make a local task easier.

### BIM and shared foundation

Primary scope:

- `src/fire_smoke_dt/bim_graph/**`
- related tests under `tests/unit/bim_graph/**`
- `docs/modules/01_bim_graph.md`

Shared and config changes still require explicit approval.

### Scenario and CFAST

Primary scope:

- `src/fire_smoke_dt/scenario/**`
- `src/fire_smoke_dt/cfast_sim/**`
- related tests
- `docs/modules/02_cfast_scenarios.md`

### Virtual IoT and dataset

Primary scope:

- `src/fire_smoke_dt/iot_sim/**`
- `src/fire_smoke_dt/dataset/**`
- related tests
- `docs/modules/03_iot_dataset.md`

### AI models and training

Primary scope:

- `src/fire_smoke_dt/models/**`
- `src/fire_smoke_dt/training/**`
- related tests
- `docs/modules/04_ai_models.md`

### FDS, comparison, and dashboard

Primary scope:

- `src/fire_smoke_dt/fds_sim/**`
- `src/fire_smoke_dt/comparison/**`
- `dashboard/**`
- related tests
- `docs/modules/05_fds_dashboard.md`

When a task requires changes in more than one ownership area, the agent must keep the changes isolated and explain the cross-module dependency in the final summary.

---

## 4. Scientific scope that must be preserved

The P0 outputs are:

- `smoke_label`
- `time_to_arrival`

Agents must not remove, rename, or replace these outputs without explicit approval.

The following rules are mandatory:

1. CFAST remains the main source for large-scale training data.
2. FDS remains an independent selective comparison and validation source.
3. FDS data must not be silently mixed into the main CFAST training split.
4. Dataset splitting must be based on `base_scenario_id` or the approved split contract.
5. Noise variants of the same base scenario must not appear across both training and test sets.
6. Future data must never leak into the input window.
7. `time_to_arrival` must use an explicit validity mask for nodes where smoke never arrives.
8. Label thresholds, persistence, forecast horizon, and noise presets must come from configuration files.
9. P1 and P2 features must not be promoted to mandatory P0 requirements without a documented scope decision.
10. The model is a research surrogate and must not be described as replacing CFD or providing legal fire-safety conclusions.

---

## 5. Data and generated artifacts

Agents must not create, edit, or commit generated artifacts under:

- `data/raw_ifc/**`
- `data/cfast_raw/**`
- `data/fds_raw/**`
- `data/processed/**`
- `outputs/**`
- `checkpoints/**`
- model run directories
- simulation logs
- exported plots generated by experiments

Agents may edit only small repository-control files in those directories, such as:

- `README.md`
- `.gitkeep`
- small deterministic fixtures required by tests

Do not commit:

- `*.ifc`
- `*.parquet`
- `*.pt`
- `*.pth`
- `*.ckpt`
- large `*.csv`
- CFAST raw outputs
- FDS raw outputs
- secrets or local `.env` files

Test fixtures must be small, deterministic, documented, and safe to commit.

---

## 6. Coding requirements

Python code must:

1. target Python 3.11,
2. use type hints for public functions,
3. include docstrings for public modules, classes, and functions,
4. avoid hard-coded absolute paths,
5. use `pathlib.Path`,
6. read shared values from `configs/` or `shared/`,
7. avoid duplicated label and schema logic,
8. raise clear exceptions for invalid external input,
9. keep side effects out of import time,
10. remain deterministic when a seed is provided.

Do not place production logic only in notebooks.

Notebooks may be used for:

- exploration,
- visualization,
- debugging,
- demonstration.

Reusable logic must live under `src/fire_smoke_dt/`.

---

## 7. Testing requirements

Every behavior change must include an appropriate test.

Use:

- `tests/unit/<module>/` for isolated logic,
- `tests/integration/` for cross-module contracts,
- `tests/fixtures/` for small reusable deterministic inputs.

Before declaring a task complete, run:

```cmd
py -3.11 -m ruff check src tests dashboard\backend
py -3.11 -m compileall -q src dashboard\backend
py -3.11 -m pytest -q
git diff --check
```

An agent must not claim completion when any required command fails.

Do not:

- delete failing tests to make CI pass,
- weaken assertions without justification,
- add unconditional skips,
- mock the behavior being tested so heavily that the test becomes meaningless.

---

## 8. Documentation requirements

When behavior, input, output, configuration, setup, or CLI usage changes, update the nearest relevant documentation.

Possible locations:

- module README,
- `docs/modules/*.md`,
- `docs/data_contracts.md`,
- root `README.md`,
- `ARCHITECTURE.md` only with explicit approval.

Documentation must describe the implementation that actually exists. Do not document planned behavior as already completed.

---

## 9. Git and change safety

Agents must not:

- commit directly to `main`,
- force-push,
- rewrite shared history,
- delete remote branches,
- run destructive Git cleanup commands without explicit approval,
- amend a commit created by another person without explicit approval,
- stage unrelated files,
- include generated artifacts in a commit.

Avoid destructive commands such as:

```text
git reset --hard
git clean -fd
git push --force
```

unless the user explicitly requests them and understands the consequences.

Recommended branch naming:

- `feature/<module>-<task>`
- `fix/<module>-<issue>`
- `docs/<topic>`
- `chore/<topic>`

---

## 10. Required final report from an agent

At the end of a coding task, the agent must report:

1. files changed,
2. behavior added or fixed,
3. tests added or updated,
4. commands executed,
5. whether all checks passed,
6. any assumptions or unresolved risks,
7. whether a shared contract or config changed,
8. whether a migration or manual follow-up is required.

The agent must clearly state partial completion and remaining failures instead of presenting incomplete work as finished.

---

## 11. Allowed default edit scope

Unless the user says otherwise, an agent may edit only:

- the assigned module under `src/fire_smoke_dt/<module>/**`,
- tests for that module,
- the module README,
- the corresponding `docs/modules/*.md`.

Everything else is read-only by default.

When uncertain whether a file is in scope, do not modify it. Explain the dependency and ask for explicit approval before changing repository-wide contracts, CI, dependencies, architecture, ownership, or scope.
