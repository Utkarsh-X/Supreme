@echo off
cd /d E:\RofU\Supreme
set PYTHONUNBUFFERED=1
python carb_benchmark/scripts/run_carb_v2_batch.py --configs superpowers-v2.0 --task-list-file carb_benchmark/results/v3_superpowers_pending_tasks.txt --progress carb_benchmark/results/v3_superpowers_pending_progress.json
