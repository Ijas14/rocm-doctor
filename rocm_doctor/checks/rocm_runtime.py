import re
from pathlib import Path
from rocm_doctor.core.result import CheckResult, Status
from rocm_doctor.core.runner import run_command

def check_rocm_runtime() -> CheckResult:
    data = {}
    status = Status.OK
    issues = []

    # 1. Canonical version file
    rocm_version = "Unknown"
    version_file = Path("/opt/rocm/.info/version")
    if version_file.exists():
        rocm_version = version_file.read_text().strip()
    data["ROCm Version"] = rocm_version

    # 2. hipconfig
    success, out, _ = run_command("hipconfig --version")
    if success and out:
        data["HIP Version"] = out.strip()
    else:
        data["HIP Version"] = "Not found"
        
    # 3. ROCM_PATH
    success, out, _ = run_command("echo ${ROCM_PATH:-/opt/rocm}")
    rocm_path = out.strip() if out.strip() else "/opt/rocm"
    data["ROCm Path"] = rocm_path
    if not Path(rocm_path).exists():
        status = Status.ERROR
        issues.append(f"ROCm path {rocm_path} does not exist")

    # 4. hipcc
    success, out, _ = run_command("which hipcc")
    data["hipcc"] = out.strip() if success and out else "Not found"
    
    # 5. rocminfo
    success, out, _ = run_command("rocminfo")
    data["rocminfo"] = "Functional" if success else "Broken/Not found"
    if not success:
        status = Status.WARNING if status == Status.OK else status
        issues.append("rocminfo failed to run")

    if rocm_version == "Unknown" and data["HIP Version"] == "Not found":
        status = Status.ERROR
        issues.append("ROCm not detected")

    if not Path(rocm_path).exists() and data.get("hipcc") != "Not found":
        return CheckResult(
            name="ROCm Runtime: PARTIAL INSTALL ⚠",
            status=Status.ERROR,
            data={
                "hipcc": f"found at {data['hipcc']} (installed via package manager)",
                rocm_path: "does NOT exist (full ROCm stack not installed)",
                "HIP Version": f"{data['HIP Version']} (from hipconfig)",
                "Recommendation": "Install full ROCm stack from AMD's repo for ML workloads.\n  hipcc alone is not sufficient for PyTorch/ROCm."
            }
        )

    return CheckResult(
        name="ROCm Runtime",
        status=status,
        data=data,
        message="; ".join(issues) if issues else None
    )
