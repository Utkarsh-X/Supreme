"""Validate SWE-bench v2 corpus tasks.

For each task: prove the bug is real (FAIL_TO_PASS tests fail on the buggy
base-commit state) and the fix is real (they pass with the gold patch applied).

Strategy (Windows, no Docker, no source builds):
  - era-appropriate Python venv per repo (via uv, auto-downloads Python)
  - wheel-only dependency install (never `pip install -e .`)
  - for repos with compiled extensions (matplotlib / scikit-learn / astropy):
    install the published wheel of the same minor version into the venv, then
    copy its compiled .pyd files into the workspace source tree (protected via
    .git/info/exclude so git-clean keeps them). Pure-Python code under test is
    always the repo's own at the exact base commit.
  - run tests with PYTHONPATH pointing at the workspace (or workspace/lib for
    matplotlib).

Usage:
  python validate_swe_tasks.py [--only <instance_id>] [--skip-setup] [--reset]
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"E:\RofU\Supreme")
REGISTRY = ROOT / "carb_benchmark" / "task_registry" / "swe_tasks_v2.json"
VERIFIED = ROOT / "carb_benchmark" / "sources" / "data" / "swebench_verified" / "verified.jsonl"
PRIVATE = ROOT / "carb_benchmark" / "private"
VENVS = ROOT / "carb_benchmark" / "venvs"
VALIDATION = ROOT / "carb_benchmark" / "validation"
WORKSPACES = ROOT / "carb_workspaces"

TEST_TIMEOUT = 900
PIP_TIMEOUT = 900

# ---------------------------------------------------------------------------
# Per-repo configuration
# ---------------------------------------------------------------------------

# pkg version prefix -> python version (Windows wheels must exist for the pair)
# python versions aligned to the official SWE-bench specs where uv can provide them
PY_MAP: dict[str, dict[str, str]] = {
    "sympy": {"1.1": "3.8", "1.4": "3.8", "1.5": "3.8", "1.7": "3.9", "1.12": "3.11"},
    "django": {"3.0": "3.8", "3.1": "3.8", "3.2": "3.8", "4.0": "3.8", "4.2": "3.9", "5.0": "3.11"},
    "pytest": {"4.5": "3.8", "6.0": "3.9"},
    "sphinx": {"3.5": "3.9", "4.1": "3.9", "4.3": "3.9", "5.0": "3.9"},
    "matplotlib": {"3.5": "3.10", "3.6": "3.10"},
    # 3.0 needs py3.7 (uv cannot provide); 0.21 has no py3.8 wheels
    "scikit-learn": {"0.22": "3.8"},
    "astropy": {"5.1": "3.10", "1.3": None},  # None => not runnable on this machine
}

# import root inside the workspace (matplotlib keeps its package under lib/)
IMPORT_ROOT = {"matplotlib": "lib"}

# dependency wheels per repo (pure deps only, nothing that builds from source)
DEPS: dict[str, list[str]] = {
    "sympy": ["mpmath"],
    "django": ["asgiref", "sqlparse", "tzdata", "pytz"],
    "pytest": ["iniconfig", "packaging", "pluggy<1.0", "pygments",
               "six", "py", "more-itertools", "attrs", "wcwidth",
               "atomicwrites", "setuptools==68.0.0", "toml"],
    "sphinx": [
        "docutils", "jinja2", "pygments==2.15.1", "babel", "requests",
        "snowballstemmer", "alabaster==0.7.12", "imagesize", "packaging",
        "sphinxcontrib-applehelp==1.0.7", "sphinxcontrib-devhelp==1.0.5",
        "sphinxcontrib-htmlhelp==2.0.4", "sphinxcontrib-jsmath",
        "sphinxcontrib-qthelp==1.0.6", "sphinxcontrib-serializinghtml==1.1.9",
        "Jinja2==3.0.3", "markupsafe==2.0.1", "setuptools==68.0.0", "html5lib",
    ],
    "matplotlib": ["numpy==1.25.2", "pillow==10.0.0", "cycler==0.11.0",
                   "kiwisolver==1.4.5", "contourpy==1.1.0", "fonttools==4.42.1",
                   "packaging==23.1", "pyparsing==3.0.9", "python-dateutil==2.8.2",
                   "setuptools-scm==7.1.0"],
    "scikit-learn": ["numpy", "scipy", "joblib", "threadpoolctl"],
    "astropy": ["numpy==1.25.2", "pyerfa", "PyYAML", "packaging",
               "hypothesis==6.82.6", "psutil", "sortedcontainers", "tomli",
               "setuptools==68.0.0", "attrs", "exceptiongroup", "execnet",
               "iniconfig", "pluggy", "pytest-astropy-header", "pytest-doctestplus",
               "pytest-openfiles", "pytest-remotedata", "pytest-filter-subpackage",
               "pytest-xdist", "pytest-arraydiff", "pytest-astropy", "pytest-mock",
               "pytest-cov"],
}

# published wheel version used only to obtain compiled .pyd for the overlay
WHEEL_VERSION: dict[str, dict[str, str]] = {
    "matplotlib": {"3.0": "3.0.3", "3.5": "3.5.3", "3.6": "3.6.3"},
    "scikit-learn": {"0.21": "0.21.3", "0.22": "0.22.2.post1"},
    "astropy": {"5.1": "5.1.1"},
}

# numpy pin per python version (keeps compiled-wheel ABI happy; era-aligned)
NUMPY_PIN = {"3.7": "numpy==1.19.5", "3.8": "numpy==1.19.5",
             "3.9": "numpy==1.26.4", "3.10": "numpy==1.25.2", "3.11": "numpy==2.0.2"}

# sphinx pins docutils per major version (newer docutils breaks old sphinx)
DOCUTILS_PIN = {"3.5": "docutils==0.16", "4.1": "docutils==0.17.1",
                "4.3": "docutils==0.17.1", "5.0": "docutils==0.18.1"}

RUNNER_PYTEST = {"3.7": "pytest==6.2.5", "3.8": "pytest==6.2.5",
                 "3.9": "pytest==7.4.4", "3.10": "pytest==7.4.4", "3.11": "pytest==8.2.1"}

# ---------------------------------------------------------------------------


def run(cmd, cwd=None, env=None, timeout=PIP_TIMEOUT, silent=False):
    e = os.environ.copy()
    if env:
        e.update(env)
    try:
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=e,
                           capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except Exception as ex:  # noqa: BLE001
        return -1, f"EXCEPTION: {ex}"


def venv_python(venv: Path) -> Path:
    return venv / "Scripts" / "python.exe"


def ensure_venv(repo: str, pkg_version: str) -> Path | None:
    pv = PY_MAP.get(repo, {}).get(pkg_version)
    if pv is None:
        return None
    venv = VENVS / f"{repo}_py{pv}"
    marker = venv / ".ready"
    if marker.exists():
        return venv
    print(f"  [setup] creating venv {venv.name}")
    venv.mkdir(parents=True, exist_ok=True)
    clear = ["--clear"] if any(venv.iterdir()) else []
    rc, out = run(["uv", "venv", "--python", pv] + clear + [str(venv)], timeout=300)
    if rc != 0:
        print(f"  [setup] FAILED venv create: {out[:800]}")
        return None
    py = venv_python(venv)
    # runner pytest
    rc, out = run(["uv", "pip", "install", "--python", str(py), RUNNER_PYTEST[pv]], timeout=PIP_TIMEOUT)
    if rc != 0:
        print(f"  [setup] FAILED pytest install: {out[:800]}")
        return None
    # deps
    deps = list(DEPS[repo])
    if repo == "sphinx" and pkg_version in DOCUTILS_PIN:
        deps = [DOCUTILS_PIN[pkg_version] if d == "docutils" else d for d in deps]
    if pv in NUMPY_PIN:
        deps = [NUMPY_PIN[pv] if d == "numpy" else d for d in deps]
        if not any(d.startswith("numpy") for d in deps):
            deps.insert(0, NUMPY_PIN[pv])
    if repo == "scikit-learn":
        deps = ["numpy==1.19.5" if d.startswith("numpy") else d for d in deps]
    # compiled repos: pin numpy to era wheel set
    rc, out = run(["uv", "pip", "install", "--python", str(py)] + deps, timeout=PIP_TIMEOUT)
    if rc != 0:
        print(f"  [setup] FAILED deps install: {out[:1500]}")
        return None
    marker.write_text(time.strftime("%Y-%m-%d %H:%M:%S"))
    return venv


def overlay_compiled(venv: Path, repo: str, pkg_version: str, workspace: Path):
    """Copy compiled .pyd from the published wheel into the workspace tree."""
    wheel_ver = WHEEL_VERSION.get(repo, {}).get(pkg_version)
    if wheel_ver is None:
        return
    py = venv_python(venv)
    pip_name = {
        "matplotlib": "matplotlib",
        "scikit-learn": "scikit-learn",  # PyPI name differs from the import dir
        "astropy": "astropy",
    }[repo]
    pkg_dir_name = {
        "matplotlib": "matplotlib",
        "scikit-learn": "sklearn",
        "astropy": "astropy",
    }[repo]
    install_root = IMPORT_ROOT.get(repo, ".")
    pkg_dir = (workspace / install_root / pkg_dir_name)
    # install the published wheel into the venv
    rc, out = run(["uv", "pip", "install", "--python", str(py),
                   f"{pip_name}=={wheel_ver}"], timeout=PIP_TIMEOUT)
    if rc != 0:
        print(f"  [setup] FAILED wheel install {pip_name}=={wheel_ver}: {out[:800]}")
        return
    site = subprocess.run(
        [str(py), "-c", "import sysconfig;print(sysconfig.get_paths()['purelib'])"],
        capture_output=True, text=True).stdout.strip()
    wheel_pkg = Path(site) / pkg_dir_name
    if not wheel_pkg.exists():
        print(f"  [setup] wheel pkg dir missing: {wheel_pkg}")
        return
    n = 0
    copied = []
    for f in wheel_pkg.rglob("*"):
        if f.suffix.lower() in (".pyd", ".so"):
            rel = f.relative_to(wheel_pkg)
            dst = pkg_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
            copied.append(rel)
            n += 1
        elif f.suffix == ".py" and f.name != "__init__.py":
            # pure-python shims that exist in the wheel but not in the source
            # tree (e.g. sklearn 0.22 neighbors/ball_tree.py) — needed so the
            # workspace source can import its own compiled modules
            rel = f.relative_to(wheel_pkg)
            dst = pkg_dir / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                copied.append(rel)
                n += 1
    # setuptools-scm generated _version.py (also copied from the wheel)
    verfile = wheel_pkg / "_version.py"
    if verfile.exists():
        shutil.copy2(verfile, pkg_dir / "_version.py")
        exclude = workspace / ".git" / "info" / "exclude"
        lines = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        if "_version.py" not in lines:
            exclude.write_text(lines + "\n_pytest/_version.py\nmatplotlib/_version.py\nastropy/_version.py\n",
                              encoding="utf-8")
    # protect from git clean via .git/info/exclude (always append: the *.pyd
    # rule may already be present while the copied .py shims are not).
    # patterns are repo-root-relative and need FORWARD slashes.
    exclude = workspace / ".git" / "info" / "exclude"
    lines = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    pkg_prefix = pkg_dir.relative_to(workspace).as_posix()
    shim_paths = [
        f"{pkg_prefix}/{str(c).replace(chr(92), '/')}"
        for c in copied if c.suffix != ".pyd"
    ]
    add = "\n*.pyd\n*.so\n" + "\n".join(shim_paths) + "\n"
    exclude.write_text(lines + add, encoding="utf-8")
    # uninstall the wheel so its site-packages copy cannot shadow the workspace
    # (namespace packages like mpl_toolkits would otherwise merge both copies)
    run(["uv", "pip", "uninstall", "--python", str(py), pip_name], timeout=PIP_TIMEOUT)
    print(f"  [setup] overlay: copied {n} compiled files from {pip_name}=={wheel_ver}")


def git_reset(workspace: Path):
    rc, out = run(["git", "reset", "--hard", "HEAD"], cwd=workspace, timeout=120)
    if rc != 0:
        print(f"  [reset] FAILED git reset: {out[:500]}")
    # remove untracked non-ignored files (keeps *.pyd / *.so via info/exclude)
    run(["git", "clean", "-fd"], cwd=workspace, timeout=120)


def apply_patch(workspace: Path, patch: Path) -> bool:
    # normalize patch to LF and guarantee a trailing newline (patches written
    # on Windows carry CRLF and sometimes drop the final line terminator)
    raw = patch.read_bytes().replace(b"\r\n", b"\n")
    if not raw.endswith(b"\n"):
        raw += b"\n"
    tmp = VALIDATION / f"{patch.stem}.lf.patch"
    tmp.write_bytes(raw)
    rc, out = run(["git", "apply", "--recount", "--whitespace=nowarn", str(tmp)],
                  cwd=workspace, timeout=120)
    if rc == 0:
        return True
    print(f"  [patch] git apply FAILED for {patch.name}: {out[:500]}")
    return False


def resolve_test_args(f2p: list[str], test_patch: Path, workspace: Path, repo: str) -> list[str]:
    """Turn F2P/P2P entries into runner args.

    django -> test labels for tests/runtests.py
    others -> pytest file paths / node ids.
    Handles the dataset's bare test names (e.g. "test_Vector") by locating the
    defining file case-insensitively in the workspace.
    """
    if repo == "django":
        out = []
        for entry in f2p:
            if " (" in entry and entry.rstrip().endswith(")"):
                name, content = entry.split(" (", 1)
                content = content.rstrip()[:-1]
                label = content if content.endswith(f".{name.strip()}") else f"{content}.{name.strip()}"
                out.append(label)
            else:
                # sentence/docstring-style entry: cannot map to a single label
                out.append(f"__UNRESOLVABLE__:{entry}")
        return out

    out = []
    touched = []
    try:
        txt = test_patch.read_text(encoding="utf-8")
        for m in re.finditer(r"^\+\+\+ b/(.+)$", txt, re.M):
            touched.append(m.group(1).strip())
    except Exception:  # noqa: BLE001
        pass

    def find_file_for(name: str) -> str | None:
        base = name.lower()
        for tf in touched:
            b = tf.split("/")[-1].lower().replace(".py", "")
            if base == b or (base.startswith("test_") and b.startswith(base)):
                return tf
        # fallback: search the workspace for the defining test file/function
        for tf in touched:
            if base in tf.lower():
                return tf
        # repo-wide function definition search (bounded)
        for p in workspace.rglob("test_*.py"):
            if "site-packages" in str(p) or "\\.venv" in str(p):
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:  # noqa: BLE001
                continue
            if re.search(rf"^\s*def\s+{re.escape(name)}\s*\(", txt, re.M):
                return str(p.relative_to(workspace)).replace("\\", "/")
        return None

    for entry in f2p:
        if entry == "[100%]":
            continue
        # dataset form: "test_name (module.path.ClassName)" -> file::Class::test_name
        if " (" in entry and entry.rstrip().endswith(")"):
            name_part, cls_part = entry.split(" (", 1)
            cls_part = cls_part.rstrip()[:-1]
            name = name_part.strip()
            mod_parts = cls_part.split(".")
            cls = mod_parts[-1]
            mod = ".".join(mod_parts[:-1])
            if mod:
                f = f"{mod.replace('.', '/')}.py"
                if not (workspace / f).exists() and (workspace / "tests" / f).exists():
                    f = f"tests/{f}"  # django-style tests/ layout
                out.append(f"{f}::{cls}::{name}")
                continue
        if "/" in entry or "::" in entry:
            out.append(entry)
            continue
        name = entry.split(" (")[0].strip()
        f = find_file_for(name)
        if f:
            out.append(f"{f}::{name}")
        else:
            out.append(entry)  # let pytest try (will report clearly)
    return out


def get_install_root(workspace: Path, repo: str) -> str:
    install_root = IMPORT_ROOT.get(repo, ".")
    src = workspace / "src"
    if (src / "pytest").exists() or (src / "pytest.py").exists() or (src / "_pytest").exists():
        install_root = "src"
    return install_root


def write_sklearn_compat(venv: Path):
    """The 0.22.2 wheel's compiled modules import a deprecation helper that was
    added to the workspace's source after this base commit. Patch it from the
    venv (outside the workspace) so the repo stays untouched."""
    py = venv_python(venv)
    site = subprocess.run(
        [str(py), "-c", "import sysconfig;print(sysconfig.get_paths()['purelib'])"],
        capture_output=True, text=True).stdout.strip()
    sc = Path(site) / "sitecustomize.py"
    if sc.exists():
        return
    sc.write_text(
        "def _carb_sklearn_compat():\n"
        "    try:\n"
        "        import sklearn.utils.deprecation as _d\n"
        "        if not hasattr(_d, '_raise_dep_warning_if_not_pytest'):\n"
        "            def _raise_dep_warning_if_not_pytest(*a, **k):\n"
        "                pass\n"
        "            _d._raise_dep_warning_if_not_pytest = _raise_dep_warning_if_not_pytest\n"
        "    except Exception:\n"
        "        pass\n"
        "\n"
        "try:\n"
        "    _carb_sklearn_compat()\n"
        "except Exception:\n"
        "    pass\n",
        encoding="utf-8")


def write_sklearn_shims(workspace: Path):
    """The 0.22 base commits sit mid-module-rename; the release wheel only
    provides the renamed compiled modules. Write minimal re-export shims so the
    base-commit source can import them (protected from git clean)."""
    shims = {
        "sklearn/decomposition/_online_lda.py":
            "from ._online_lda_fast import mean_change, _dirichlet_expectation_1d, "
            "_dirichlet_expectation_2d\n",
    }
    exclude = workspace / ".git" / "info" / "exclude"
    lines = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    for rel, content in shims.items():
        target = workspace / rel
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        if rel not in lines:
            lines += f"\n{rel}\n"
    exclude.write_text(lines, encoding="utf-8")


def prepare_pytest_version(workspace: Path, install_root: str, pkg_version: str):
    """pytest's checkout needs the setuptools-scm generated _version.py."""
    if not pkg_version or not pkg_version[0].isdigit():
        return
    ver = pkg_version if "." in pkg_version else f"{pkg_version}.0"
    target = workspace / install_root / "_pytest" / "_version.py"
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"version = {ver!r}\n", encoding="utf-8")
    exclude = workspace / ".git" / "info" / "exclude"
    lines = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if "_version.py" not in lines:
        exclude.write_text(lines + "\n_pytest/_version.py\n", encoding="utf-8")


def run_tests(venv: Path, workspace: Path, repo: str, args: list[str],
              label: str) -> tuple[int, str]:
    py = venv_python(venv)
    install_root = get_install_root(workspace, repo)
    env = {
        "PYTHONPATH": str(workspace / install_root),
        "MPLBACKEND": "Agg",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
        "HOME": str(ROOT / "carb_benchmark" / "validation" / "home"),
    }
    if repo == "django":
        cmd = [str(py), "tests/runtests.py", "--verbosity", "2",
               "--settings=test_sqlite", "--parallel", "1"] + args
    else:
        cmd = [str(py), "-m", "pytest", "-x", "-rA", "--tb=short",
               "-p", "no:cacheprovider", "--continue-on-collection-errors"] + args
    t0 = time.time()
    rc, out = run(cmd, cwd=workspace, env=env, timeout=TEST_TIMEOUT)
    dt = time.time() - t0
    # trim output for storage
    trimmed = out[-6000:] if len(out) > 6000 else out
    return rc, f"# {label} rc={rc} ({dt:.0f}s)\n{trimmed}"


# Known genuine platform/ABI limitations (verified manually against phase logs):
# the F2P failure is identical in buggy AND gold states, so the environment
# itself cannot run the fix — these are NOT harness or dataset bugs.
KNOWN_ABI_REJECTS = {
    "astropy__astropy-14309": (
        "ModuleNotFoundError: astropy.io.fits._tiled_compression._compression in buggy AND gold "
        "states — the era astropy Windows wheel does not ship the _compression compiled "
        "extension (Linux/macOS-only build artifact); the package cannot import on this platform"
    ),
    "scikit-learn__scikit-learn-14053": (
        "TypeError: _splitter.Splitter.__cinit__() takes 5 positional args (6 given) in buggy "
        "AND gold states — base commit sits mid-refactor between 0.22.0 and 0.22.2; the only "
        "available cp38 Windows wheel (0.22.2.post1) is ABI-incompatible with the base-commit "
        "tree.py, not bridgeable by overlay"
    ),
}


def record(instance_id: str, verdict: str, detail: str, phases: dict):
    VALIDATION.mkdir(exist_ok=True)
    rec = {
        "instance_id": instance_id,
        "verdict": verdict,
        "detail": detail,
        "phases": phases,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (VALIDATION / f"{instance_id}.json").write_text(
        json.dumps(rec, indent=2), encoding="utf-8")
    print(f"  ==> {instance_id}: {verdict} — {detail}")


def main():
    args = sys.argv[1:]
    only = None
    if "--only" in args:
        only = args[args.index("--only") + 1]
    registry_path = REGISTRY
    if "--registry" in args:
        registry_path = Path(args[args.index("--registry") + 1])

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    verified = {}
    with VERIFIED.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                verified[r["instance_id"]] = r

    tasks = [t for t in registry if only is None or t["instance_id"] == only]
    summary = []
    for t in tasks:
        iid = t["instance_id"]
        print(f"\n===== {iid} =====")
        v = verified[iid]
        repo = t["repo"].split("/")[1]
        pkg_version = v["version"]
        workspace = WORKSPACES / iid
        private = PRIVATE / iid
        test_patch = private / "test_patch.patch"
        gold_patch = private / "gold_patch.patch"
        f2p = json.loads(v["FAIL_TO_PASS"])
        p2p = json.loads(v["PASS_TO_PASS"])

        if PY_MAP.get(repo, {}).get(pkg_version) is None:
            record(iid, "REJECTED",
                   f"{repo} {pkg_version}: no runnable env (no era-appropriate Python "
                   "with Windows wheels available)", {})
            summary.append((iid, "REJECTED"))
            continue

        venv = ensure_venv(repo, pkg_version)
        if venv is None:
            record(iid, "REJECTED", "venv setup failed", {})
            summary.append((iid, "REJECTED"))
            continue

        overlay_compiled(venv, repo, pkg_version, workspace)
        if repo == "pytest":
            prepare_pytest_version(workspace, get_install_root(workspace, repo), pkg_version)
        if repo == "scikit-learn":
            write_sklearn_compat(venv)
            write_sklearn_shims(workspace)

        # NOTE: F2P labels are resolved AFTER the hidden test patch is applied —
        # patch-added tests (e.g. sympy test_issue_17624 added by test_patch) are
        # found by the workspace search only once the patch is in place; resolving
        # before patching yields bare names and pytest "file or directory not
        # found" errors (observed on sympy-17630 during v3 validation).

        phases = {}
        # --- phase 1: buggy state, expect F2P to fail -----------------------
        git_reset(workspace)
        if not apply_patch(workspace, test_patch):
            record(iid, "REJECTED", "test_patch does not apply", {})
            summary.append((iid, "REJECTED"))
            continue
        test_args = resolve_test_args(f2p, test_patch, workspace, repo)
        unresolvable = [a for a in test_args if a.startswith("__UNRESOLVABLE__")]
        if unresolvable:
            record(iid, "REJECTED",
                   f"F2P entries not mappable to test labels: {unresolvable}", {})
            summary.append((iid, "REJECTED"))
            continue
        p2p_args = [a for a in resolve_test_args(p2p, test_patch, workspace, repo)
                    if not a.startswith("__UNRESOLVABLE__")]
        rc_buggy, out_buggy = run_tests(venv, workspace, repo, test_args, "BUGGY")
        phases["buggy_f2p"] = {"rc": rc_buggy, "output": out_buggy}
        bug_fails = rc_buggy != 0

        # --- phase 2: gold state, expect F2P pass + P2P pass -----------------
        git_reset(workspace)
        if not apply_patch(workspace, test_patch) or not apply_patch(workspace, gold_patch):
            record(iid, "REJECTED", "patches do not apply on gold state", phases)
            summary.append((iid, "REJECTED"))
            continue
        rc_gold, out_gold = run_tests(venv, workspace, repo, test_args, "GOLD-F2P")
        phases["gold_f2p"] = {"rc": rc_gold, "output": out_gold}
        fix_passes = rc_gold == 0
        rc_p2p, out_p2p = run_tests(venv, workspace, repo, p2p_args, "GOLD-P2P")
        phases["gold_p2p"] = {"rc": rc_p2p, "output": out_p2p}

        if bug_fails and fix_passes:
            extra = "" if rc_p2p == 0 else f" | P2P rc={rc_p2p} (note)"
            record(iid, "VALIDATED", f"bug fails F2P (rc={rc_buggy}), gold passes F2P (rc=0){extra}", phases)
            summary.append((iid, "VALIDATED"))
        elif not bug_fails and fix_passes:
            record(iid, "REJECTED", f"buggy state already passes F2P (rc={rc_buggy}) — bug not reproduced", phases)
            summary.append((iid, "REJECTED"))
        else:
            # Genuine platform/ABI limitations: the failure occurs identically in
            # buggy AND gold states, so the eval env itself cannot exercise the fix.
            reason = KNOWN_ABI_REJECTS.get(iid)
            if reason is None:
                reason = (f"bug_fails={bug_fails} fix_passes={fix_passes} — failure occurs in "
                          "both buggy and gold states (env/ABI limitation, see phase logs)")
            record(iid, "REJECTED", reason, phases)
            summary.append((iid, "REJECTED"))

        git_reset(workspace)

    print("\n===== SUMMARY =====")
    for iid, verdict in summary:
        print(f"  {verdict:10s} {iid}")


if __name__ == "__main__":
    main()
