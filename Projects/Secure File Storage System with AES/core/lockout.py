import hashlib
import json
import time
from pathlib import Path

LOCK_DIR = Path("data/lockout")
LOCK_DIR.mkdir(parents=True, exist_ok=True)

LOCK_STEPS = [30, 60, 300, 600, 900, 1800, 3600]


def _fid(path):
    return hashlib.sha256(path.encode()).hexdigest()


def _path(fid):
    return LOCK_DIR / f"{fid}.json"


def check_lock(file_path):
    fid = _fid(file_path)
    if not _path(fid).exists():
        return False, 0
    data = json.loads(_path(fid).read_text())
    if time.time() < data.get("locked_until", 0):
        return True, int(data["locked_until"] - time.time())
    return False, 0


def record_failure(file_path):
    fid = _fid(file_path)
    data = {"fails": 0, "step": 0, "locked_until": 0}
    if _path(fid).exists():
        data = json.loads(_path(fid).read_text())
    data["fails"] += 1
    if data["fails"] >= 3:
        delay = LOCK_STEPS[min(data["step"], len(LOCK_STEPS) - 1)]
        data["locked_until"] = time.time() + delay
        data["step"] += 1
        data["fails"] = 0
    _path(fid).write_text(json.dumps(data))


def reset_lock(file_path):
    fid = _fid(file_path)
    if _path(fid).exists():
        _path(fid).unlink()
