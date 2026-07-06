import sys
from rocm_doctor.checks.hardware import check_hardware
from rocm_doctor.checks.driver import check_driver
from rocm_doctor.checks.rocm_runtime import check_rocm_runtime
from rocm_doctor.report import generate_markdown_report

def main() -> int:
    results = [
        check_hardware(),
        check_driver(),
        check_rocm_runtime()
    ]
    
    report = generate_markdown_report(results)
    print(report)
    
    return 0
