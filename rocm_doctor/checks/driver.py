import re
from pathlib import Path
from rocm_doctor.core.result import CheckResult, Status
from rocm_doctor.core.runner import run_command

def check_driver() -> CheckResult:
    data = {}
    status = Status.OK
    issues = []

    # 1. Module loaded
    success, out, _ = run_command("lsmod | grep amdgpu")
    data["amdgpu module"] = "Loaded" if success and out else "Not loaded"
    if data["amdgpu module"] == "Not loaded":
        status = Status.ERROR
        issues.append("amdgpu module not loaded")

    # 2. Module version
    success, out, _ = run_command("modinfo amdgpu | grep version:")
    if success and out:
        match = re.search(r"version:\s+(.+)", out)
        data["Driver version"] = match.group(1) if match else "Unknown"
    else:
        data["Driver version"] = "Unknown"

    # 3. KFD and Render nodes
    data["/dev/kfd"] = "Present" if Path("/dev/kfd").exists() else "Missing"
    if data["/dev/kfd"] == "Missing":
        status = Status.ERROR
        issues.append("/dev/kfd is missing (ROCm will not work)")

    render_nodes = list(Path("/dev/dri").glob("renderD*")) if Path("/dev/dri").exists() else []
    data["render nodes"] = [n.name for n in render_nodes] if render_nodes else ["None"]

    # 4. Firmware
    data["Firmware"] = "Installed" if Path("/lib/firmware/amdgpu").exists() else "Missing"
    if data["Firmware"] == "Missing":
        status = Status.ERROR
        issues.append("amdgpu firmware is missing")

    # 5. dmesg errors
    success, out, _ = run_command("dmesg | grep -i amdgpu | tail -20")
    dmesg_errors = []
    if success and out:
        for line in out.splitlines():
            line_lower = line.lower()
            if any(err in line_lower for err in ["failed to", "error", "firmware not found", "hang"]):
                dmesg_errors.append(line)
    
    if dmesg_errors:
        data["dmesg errors"] = dmesg_errors
        status = Status.WARNING if status != Status.ERROR else Status.ERROR

    return CheckResult(
        name="Driver",
        status=status,
        data=data,
        message="; ".join(issues) if issues else None
    )
