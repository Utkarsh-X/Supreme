@echo off
cd /d E:\RofU\Supreme
set PYTHONUNBUFFERED=1

echo =======================================================
echo Starting CARB-v3 Supreme Pending Tasks (7 tasks)
echo =======================================================
python carb_benchmark/scripts/run_carb_v2_batch.py --configs supreme-v2.0 --task-list-file carb_benchmark/results/v3_supreme_pending_tasks.txt --progress carb_benchmark/results/v3_supreme_pending_progress.json

echo.
echo =======================================================
echo Starting CARB-v3 Superpowers Pending Tasks (10 tasks)
echo =======================================================
python carb_benchmark/scripts/run_carb_v2_batch.py --configs superpowers-v2.0 --task-list-file carb_benchmark/results/v3_superpowers_pending_tasks.txt --progress carb_benchmark/results/v3_superpowers_pending_progress.json

echo.
echo =======================================================
echo All V3 Pending Tasks Completed!
echo =======================================================
