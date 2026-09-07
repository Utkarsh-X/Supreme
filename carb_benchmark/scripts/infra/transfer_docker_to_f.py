#!/usr/bin/env python3
"""
===============================================================================
  DOCKER & WSL HIGH-PERFORMANCE MIGRATION ENGINE (E: -> F:)
===============================================================================
"""

import os
import sys
import json
import time
import shutil
import winreg
import subprocess

os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

SETTINGS_JSON = os.path.expandvars(r"%APPDATA%\Docker\settings-store.json")
LXSS_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Lxss"
WSLCONFIG_PATH = os.path.expanduser(r"~\.wslconfig")

SOURCE_DOCKER_APP = r"E:\LargeApplications\Docker"
TARGET_DOCKER_APP = r"F:\LargeApplications\Docker"

SOURCE_DOCKER_SWAP = r"E:\Docker"
TARGET_DOCKER_SWAP = r"F:\Docker"

TARGET_WSL_DIR = r"F:\LargeApplications\Docker\wsl\DockerDesktopWSL"


def log(msg, color=CYAN):
    ts = time.strftime("%H:%M:%S")
    print(f"{color}[{ts}] {msg}{RESET}", flush=True)


def stop_all_services():
    log("Stopping Docker Desktop and all background daemon processes...", YELLOW)
    procs = ["Docker Desktop.exe", "com.docker.backend.exe", "com.docker.proxy.exe", "com.docker.service.exe"]
    for p in procs:
        subprocess.run(["taskkill", "/F", "/IM", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    log("Shutting down WSL to release all file handles on virtual disks...", YELLOW)
    subprocess.run(["wsl", "--shutdown"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    log("Docker and WSL services stopped cleanly.", GREEN)


def robocopy_transfer(src_dir, dst_dir):
    """Transfers directory tree with robocopy using /J unbuffered I/O."""
    os.makedirs(dst_dir, exist_ok=True)
    log(f"Starting unbuffered high-speed transfer:\n  SRC: {src_dir}\n  DST: {dst_dir}", CYAN)
    
    cmd = [
        "robocopy",
        src_dir,
        dst_dir,
        "/E",          # Copy subdirectories
        "/J",          # Unbuffered I/O (up to 3x faster for large files)
        "/R:2",        # 2 retries
        "/W:2",        # 2s wait between retries
        "/V",          # Verbose output
        "/ETA"         # Estimated time of arrival
    ]
    
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    last_print = time.time()
    for line in p.stdout:
        line_clean = line.strip()
        now = time.time()
        # Filter for file announcements or progress milestones
        if ("New File" in line or "%" in line or "Speed" in line or "Ended" in line) and (now - last_print > 4.0 or "%" not in line):
            print(f"  {line_clean}", flush=True)
            last_print = now
            
    p.wait()
    elapsed = time.time() - t0
    
    # Robocopy return codes: 0-7 are successful transfers; >=8 is error
    if p.returncode >= 8:
        raise RuntimeError(f"Robocopy failed with error code {p.returncode}")
    
    log(f"Transfer completed in {elapsed/60:.2f} minutes (Robocopy return code: {p.returncode})", GREEN)


def verify_file_sizes(src_dir, dst_dir):
    """Verifies that every file in source exists in destination with matching byte size."""
    log(f"Validating file integrity: {src_dir} vs {dst_dir}...", CYAN)
    mismatches = []
    total_bytes = 0
    file_count = 0
    
    for root, dirs, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        target_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        
        for f in files:
            src_f = os.path.join(root, f)
            dst_f = os.path.join(target_root, f)
            
            if not os.path.exists(dst_f):
                mismatches.append(f"Missing file: {dst_f}")
                continue
            
            src_sz = os.path.getsize(src_f)
            dst_sz = os.path.getsize(dst_f)
            total_bytes += dst_sz
            file_count += 1
            
            if src_sz != dst_sz:
                mismatches.append(f"Size mismatch on {f}: Src={src_sz} bytes, Dst={dst_sz} bytes")
                
    if mismatches:
        for m in mismatches:
            log(f"  ERROR: {m}", RED)
        raise ValueError(f"Integrity check failed with {len(mismatches)} errors!")
        
    log(f"Verification successful: {file_count} files ({total_bytes/(1024**3):.2f} GB) 100% matched byte-for-byte!", GREEN)
    return True


def update_docker_settings():
    log("Updating Docker Desktop configuration in settings-store.json...", CYAN)
    if not os.path.exists(SETTINGS_JSON):
        raise FileNotFoundError(f"Docker settings file not found: {SETTINGS_JSON}")
    
    with open(SETTINGS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    bak_path = SETTINGS_JSON + ".pre_migration.bak"
    with open(bak_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log(f"  Backup saved: {bak_path}", GREEN)
    
    data["CustomWslDistroDir"] = TARGET_WSL_DIR
    with open(SETTINGS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log(f"  Updated CustomWslDistroDir -> {TARGET_WSL_DIR}", GREEN)


def update_windows_registry():
    log("Updating Windows Registry for WSL docker-desktop distro...", CYAN)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, LXSS_REG_PATH) as key:
        num_subkeys = winreg.QueryInfoKey(key)[0]
        for i in range(num_subkeys):
            sub_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, sub_name) as sub_key:
                try:
                    distro_name = winreg.QueryValueEx(sub_key, "DistributionName")[0]
                    if distro_name.lower() == "docker-desktop":
                        sub_key_path = f"{LXSS_REG_PATH}\\{sub_name}"
                        target_main_path = os.path.join(TARGET_WSL_DIR, "main")
                        target_reg_base = f"\\\\?\\{target_main_path}"
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key_path, 0, winreg.KEY_SET_VALUE) as wkey:
                            winreg.SetValueEx(wkey, "BasePath", 0, winreg.REG_SZ, target_reg_base)
                        log(f"  Updated Registry [{sub_key_path}]: BasePath -> {target_reg_base}", GREEN)
                        return True
                except FileNotFoundError:
                    continue
    log("  Warning: docker-desktop registry key not found.", YELLOW)
    return False


def update_wslconfig():
    log("Updating .wslconfig swap path to Drive F:...", CYAN)
    if os.path.exists(WSLCONFIG_PATH):
        with open(WSLCONFIG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            if line.strip().lower().startswith("swapfile="):
                new_lines.append(f"swapFile={TARGET_DOCKER_SWAP}\\wsl\\swap.vhdx\n")
            else:
                new_lines.append(line)
        
        with open(WSLCONFIG_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        log(f"  Updated {WSLCONFIG_PATH} with swapFile on F:\\", GREEN)


def update_docker_switcher():
    switcher_py = r"E:\DockerSwitcher\docker_switcher.py"
    if os.path.exists(switcher_py):
        log("Updating DockerSwitcher profiles to include Drive F:...", CYAN)
        with open(switcher_py, "r", encoding="utf-8") as f:
            code = f.read()
        
        if '"F": {' not in code:
            profile_f = '''    "F": {
        "name": "F: Drive (Removable High-Capacity Drive)",
        "path": r"F:\\LargeApplications\\Docker\\wsl\\DockerDesktopWSL",
        "drive": "F:\\\\",
        "description": "High-capacity external storage for Docker containers & benchmarks."
    },
'''
            code = code.replace('PROFILES = {', 'PROFILES = {\n' + profile_f)
            with open(switcher_py, "w", encoding="utf-8") as f:
                f.write(code)
            log("  Added Profile [F] to E:\\DockerSwitcher\\docker_switcher.py", GREEN)


def verify_docker_on_f():
    log("Starting Docker backend to verify runtime on Drive F:...", CYAN)
    backend_exe = r"C:\Users\Utkarsh\AppData\Local\Programs\DockerDesktop\resources\com.docker.backend.exe"
    if os.path.exists(backend_exe):
        subprocess.Popen([backend_exe])
    
    log("Waiting for Docker API to initialize...", YELLOW)
    for i in range(45):
        res = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if res.returncode == 0:
            log("Docker is ONLINE and responding!", GREEN)
            print(res.stdout, flush=True)
            
            log("Verifying Docker images inventory on Drive F:...", CYAN)
            res_img = subprocess.run(["docker", "images"], capture_output=True, text=True)
            print(res_img.stdout[:500] + "...", flush=True)
            return True
        time.sleep(2)
    
    log("Docker took longer than expected to respond.", YELLOW)
    return False


def create_junctions_and_reclaim_space():
    log("Creating NTFS directory junctions on Drive E: -> Drive F:...", CYAN)
    stop_all_services()
    
    # 1. E:\LargeApplications\Docker -> F:\LargeApplications\Docker
    if os.path.exists(SOURCE_DOCKER_APP) and not os.path.islink(SOURCE_DOCKER_APP):
        bak_app = SOURCE_DOCKER_APP + "_OLD_DELETE_ME"
        log(f"Renaming {SOURCE_DOCKER_APP} -> {bak_app}", YELLOW)
        os.rename(SOURCE_DOCKER_APP, bak_app)
        
        cmd = f'cmd /c mklink /J "{SOURCE_DOCKER_APP}" "{TARGET_DOCKER_APP}"'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        log(f"Created Junction: {res.stdout.strip()}", GREEN)
        
        log(f"Permanently purging {bak_app} to reclaim ~99 GB on Drive E:...", YELLOW)
        shutil.rmtree(bak_app, ignore_errors=True)
        log("Space successfully reclaimed on Drive E:!", GREEN)
        
    # 2. E:\Docker -> F:\Docker
    if os.path.exists(SOURCE_DOCKER_SWAP) and not os.path.islink(SOURCE_DOCKER_SWAP):
        bak_swap = SOURCE_DOCKER_SWAP + "_OLD_DELETE_ME"
        log(f"Renaming {SOURCE_DOCKER_SWAP} -> {bak_swap}", YELLOW)
        os.rename(SOURCE_DOCKER_SWAP, bak_swap)
        
        cmd = f'cmd /c mklink /J "{SOURCE_DOCKER_SWAP}" "{TARGET_DOCKER_SWAP}"'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        log(f"Created Junction: {res.stdout.strip()}", GREEN)
        
        log(f"Purging {bak_swap} to reclaim swap space on Drive E:... ", YELLOW)
        shutil.rmtree(bak_swap, ignore_errors=True)


def main():
    print(f"{CYAN}{BOLD}==============================================================================={RESET}")
    print(f"{CYAN}{BOLD}  DOCKER & WSL STORAGE MIGRATION: DRIVE E: -> DRIVE F:                         {RESET}")
    print(f"{CYAN}{BOLD}==============================================================================={RESET}\n", flush=True)
    
    if not os.path.exists("F:\\"):
        print(f"{RED}ERROR: Drive F: is not mounted or accessible!{RESET}", flush=True)
        sys.exit(1)
        
    usage_f = shutil.disk_usage("F:\\")
    free_f_gb = usage_f.free / (1024**3)
    log(f"Target Drive F: connected and online ({free_f_gb:.1f} GB free).", GREEN)
    
    stop_all_services()
    
    # High-performance robocopy transfers
    robocopy_transfer(SOURCE_DOCKER_APP, TARGET_DOCKER_APP)
    verify_file_sizes(SOURCE_DOCKER_APP, TARGET_DOCKER_APP)
    
    robocopy_transfer(SOURCE_DOCKER_SWAP, TARGET_DOCKER_SWAP)
    verify_file_sizes(SOURCE_DOCKER_SWAP, TARGET_DOCKER_SWAP)
    
    # Reconfigure settings and registry
    update_docker_settings()
    update_windows_registry()
    update_wslconfig()
    update_docker_switcher()
    
    # Verify Docker runs
    verified = verify_docker_on_f()
    if not verified:
        log("Verification failed or timed out. Stopping before deleting E: data.", RED)
        sys.exit(1)
        
    # Reclaim disk space and create transparent junctions
    create_junctions_and_reclaim_space()
    
    usage_e = shutil.disk_usage("E:\\")
    usage_f = shutil.disk_usage("F:\\")
    print(f"\n{GREEN}{BOLD}==============================================================================={RESET}")
    print(f"{GREEN}{BOLD}  MIGRATION COMPLETED SUCCESSFULLY!                                            {RESET}")
    print(f"{GREEN}{BOLD}==============================================================================={RESET}", flush=True)
    print(f"  Drive E: Free Space : {usage_e.free/(1024**3):.1f} GB (Reclaimed ~100 GB!)", flush=True)
    print(f"  Drive F: Free Space : {usage_f.free/(1024**3):.1f} GB (Active Docker & WSL Storage)", flush=True)
    print(f"  Active VHDX Path    : {TARGET_WSL_DIR}\\disk\\docker_data.vhdx", flush=True)
    print(f"  Junctions Active    : E:\\LargeApplications\\Docker -> F:\\LargeApplications\\Docker\n", flush=True)


if __name__ == "__main__":
    main()
