#!/usr/bin/env bash
# Launch the CARB-v2 corrective reruns (baseline/supreme on the 7 fixed tasks
# + pytest-5262) and then the full superpowers-v2.0 batch (all 50 tasks).
# Both drivers are resumable: if this shell dies, re-run the same command.
set -u
cd "$(dirname "$0")/../.." || exit 1

STAMP=$(date +%Y%m%d-%H%M%S)
LOG=carb_benchmark/results/batch_launch_${STAMP}.log

{
  echo "===== launch ${STAMP} ====="
  echo "--- rerun batch (baseline + supreme, fixed tasks) ---"
  python carb_benchmark/scripts/run_carb_v2_batch.py \
      --configs baseline-v2.0,supreme-v2.0 \
      --task-list-file carb_benchmark/results/rerun_task_list.txt \
      --progress carb_benchmark/results/benchmark_v2_rerun_progress.json
  echo "--- superpowers batch (all 50 tasks) ---"
  python carb_benchmark/scripts/run_carb_v2_batch.py \
      --configs superpowers-v2.0 \
      --progress carb_benchmark/results/benchmark_v2_superpowers_progress.json
  echo "===== launch ${STAMP} complete ====="
} >> "$LOG" 2>&1

exit 0
