# CARB Task Selection Matrix (60-Task Target)

CARB uses a multi-dimensional matrix to select candidate tasks, maximizing scientific information value rather than benchmark prestige.

---

## 1. Primary Selection Dimensions

### A. Category / Engineering Domain
- Bug fixing / debugging (12)
- Feature implementation (10)
- Frontend / UI (8)
- Backend / API (8)
- Refactoring / maintenance (6)
- Tests & reliability (5)
- Build, CI & dependencies (4)
- Database & persistence (4)
- Integrations & tooling (3)

### B. Difficulty Distribution (Target)
- **Easy**: ~10 tasks (Target >80% baseline success)
- **Medium**: ~20 tasks (Target 50–79% baseline success)
- **Hard**: ~20 tasks (Target 20–49% baseline success)
- **Very Hard**: ~10 tasks (Target <20% baseline success)

*Note: Difficulty is recalibrated empirically after baseline runs.*

### C. Risk & Blast Radius
- **Low Risk**: Isolated algorithmic refactoring, isolated component changes.
- **Medium Risk**: Shared API contract modifications, session state logic.
- **High Risk**: Database schema migrations, authentication/security refactors, destructive CLI ops.

### D. Expected Information Value & Primary Hypotheses
- `surgical_editing`: Tests minimum justified change.
- `premature_completion`: Tests whether agent stops before completing acceptance criteria.
- `investigation`: Tests whether agent searches codebase before editing.
- `uncertainty`: Tests handling of unstated assumptions and ambiguous prompts.
- `plan_invalidation`: Tests ability to abandon bad hypotheses when presented with evidence.
- `regression_safety`: Tests preservation of existing contracts.

---

## 2. Selection Balance Grid

| Category | Easy | Medium | Hard | Very Hard | Low Risk | High Risk | Info Value |
|---|---:|---:|---:|---:|---:|---:|---|
| **Bug Fixing** | 3 | 4 | 3 | 2 | 7 | 5 | High |
| **Features** | 2 | 4 | 3 | 1 | 6 | 4 | High |
| **Frontend / UI** | 2 | 3 | 2 | 1 | 5 | 3 | Medium |
| **Backend / API** | 1 | 3 | 3 | 1 | 4 | 4 | High |
| **Refactoring** | 1 | 2 | 2 | 1 | 4 | 2 | High |
| **Tests & Reliability** | 1 | 2 | 1 | 1 | 3 | 2 | Medium |
| **Build & CI** | 0 | 1 | 2 | 1 | 2 | 2 | High |
| **Database** | 0 | 1 | 2 | 1 | 1 | 3 | High |
| **Integrations** | 0 | 0 | 2 | 1 | 1 | 2 | Medium |
| **Total** | **10** | **20** | **20** | **10** | **33** | **27** | |
