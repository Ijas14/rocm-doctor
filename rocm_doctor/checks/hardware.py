import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any
from rocm_doctor.core.result import CheckResult, Status
from rocm_doctor.core.runner import run_command
from rocm_doctor.data.gfx_map import GFX_DATABASE

def get_vram_sysfs(card_path: Path) -> str:
    vram_path = card_path / "device" / "mem_info_vram_total"
    if vram_path.exists():
        try:
            bytes_val = int(vram_path.read_text().strip())
            gb_val = bytes_val / (1024**3)
            return f"{gb_val:.1f} GB"
        except Exception:
            pass
    return "Unknown"

def check_hardware() -> CheckResult:
    # 1. /sys/class/drm
    gpus = []
    drm_dir = Path("/sys/class/drm")
    if drm_dir.exists():
        for card in drm_dir.glob("card*"):
            if not card.is_dir() or "-" in card.name:
                continue
            uevent = card / "device" / "uevent"
            if not uevent.exists():
                continue
            
            content = uevent.read_text()
            if "DRIVER=amdgpu" in content or "PCI_ID=1002:" in content:
                pci_id = "Unknown"
                pci_match = re.search(r"PCI_ID=([0-9A-Fa-f:]+)", content)
                if pci_match:
                    pci_id = pci_match.group(1).lower()
                
                vram = get_vram_sysfs(card)
                
                gpus.append({
                    "source": "/sys/class/drm",
                    "pci_id": pci_id,
                    "vram": vram,
                    "driver": "amdgpu" if "DRIVER=amdgpu" in content else "Unknown"
                })

    # 3. rocminfo
    gfx_codes = []
    success, out, _ = run_command("rocminfo")
    if success:
        for line in out.splitlines():
            if "Name:" in line and "gfx" in line:
                match = re.search(r"(gfx[0-9a-fA-F]+)", line)
                if match:
                    gfx_codes.append(match.group(1).lower())
                    
    # Remove duplicates preserving order
    gfx_codes = list(dict.fromkeys(gfx_codes))

    if not gpus and not gfx_codes:
        # Fallback to lspci
        success, out, _ = run_command("lspci -nn | grep -i amd | grep -i vga")
        if success and out:
            return CheckResult(
                name="Hardware",
                status=Status.WARNING,
                message="Found AMD PCI devices, but not via DRM/rocminfo.",
                data={"lspci": out.splitlines()}
            )
        return CheckResult(
            name="Hardware",
            status=Status.ERROR,
            message="No AMD GPU detected."
        )

    # Correlate
    results = []
    for i in range(max(len(gpus), len(gfx_codes))):
        gpu = gpus[i] if i < len(gpus) else {"pci_id": "Unknown", "vram": "Unknown", "driver": "Unknown"}
        gfx = gfx_codes[i] if i < len(gfx_codes) else "Unknown"
        
        info = GFX_DATABASE.get(gfx, {})
        
        results.append({
            "GPU": info.get("name", "Unknown AMD GPU"),
            "gfx Code": gfx,
            "Architecture": info.get("architecture", "Unknown"),
            "VRAM": gpu["vram"],
            "PCI ID": gpu["pci_id"],
            "Driver": gpu["driver"]
        })
        
    return CheckResult(
        name="Hardware",
        status=Status.OK if results else Status.ERROR,
        data={"gpus": results}
    )
