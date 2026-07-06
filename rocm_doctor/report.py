import datetime
import getpass
import socket
from typing import List
from rocm_doctor.core.result import CheckResult, Status

def generate_markdown_report(results: List[CheckResult]) -> str:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        user = getpass.getuser()
    except Exception:
        user = "unknown"
    hostname = socket.gethostname()
    
    # Check overall status
    overall_status = "OK ✓"
    for r in results:
        if r.status == Status.ERROR:
            overall_status = "⚠ CRITICAL ISSUES FOUND"
            break
        elif r.status == Status.WARNING:
            overall_status = "⚠ WARNINGS FOUND"
            
    # Get summary details
    gpu_name = "Unknown"
    gfx_code = "Unknown"
    rocm_ver = "Unknown"
    
    for r in results:
        if r.name == "Hardware" and r.data.get("gpus"):
            gpu_name = r.data["gpus"][0].get("GPU", "Unknown")
            gfx_code = r.data["gpus"][0].get("gfx Code", "Unknown")
        elif r.name == "ROCm Runtime":
            rocm_ver = r.data.get("ROCm Version", "Unknown")

    lines = [
        "# rocm-doctor Diagnostic Report",
        "",
        f"Generated: {now}",
        f"User: {user}",
        f"Hostname: {hostname}",
        "",
        "## Summary",
        f"- Status: {overall_status}",
        f"- GPU: {gpu_name} ({gfx_code})",
        f"- ROCm: {rocm_ver}",
        ""
    ]

    for r in results:
        lines.append(f"## {r.name}")
        
        # Hardware specific rendering
        if r.name == "Hardware" and r.data.get("gpus"):
            for idx, gpu in enumerate(r.data["gpus"]):
                if len(r.data["gpus"]) > 1:
                    lines.append(f"### GPU {idx}")
                lines.append("| Property | Value |")
                lines.append("|---|---|")
                lines.append(f"| GPU | {gpu.get('GPU', 'Unknown')} |")
                lines.append(f"| gfx Code | {gpu.get('gfx Code', 'Unknown')} |")
                lines.append(f"| Architecture | {gpu.get('Architecture', 'Unknown')} |")
                lines.append(f"| VRAM | {gpu.get('VRAM', 'Unknown')} |")
                lines.append(f"| PCI ID | {gpu.get('PCI ID', 'Unknown')} |")
                lines.append(f"| Driver | {gpu.get('Driver', 'Unknown')} |")
                lines.append("")
        else:
            # Generic rendering
            for key, val in r.data.items():
                if isinstance(val, list):
                    lines.append(f"- {key}:")
                    for item in val:
                        lines.append(f"  - {item}")
                else:
                    lines.append(f"- {key}: {val}")
        
        if r.message:
            lines.append(f"\n**Message**: {r.message}")
        if r.error:
            lines.append(f"\n**Error**: {r.error}")
            
        lines.append("")

    return "\n".join(lines)
