import subprocess
from typing import Tuple, Optional

def run_command(cmd: str, timeout: int = 5) -> Tuple[bool, str, str]:
    """
    Runs a shell command safely. Never crashes.
    Returns: (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", f"Exception: {e}"
