# rocm-doctor

A zero-dependency diagnostic tool for AMD ROCm installations. Checks hardware, driver, runtime, and frameworks. Survives broken systems.

```bash
pip install rocm-doctor
python -m rocm_doctor
```

## Why?

AMD systems are hard to debug. Not because the information isn't there, but because it's scattered across a dozen tools that each tell part of the truth — and some of them (like `rocm-smi`) occasionally just report "N/A" when they get confused.

- `rocm-smi` reports "N/A" for GPU names on some hardware
- Version mismatches between ROCm, HIP, and PyTorch are silent failures
- PyTorch built for CUDA instead of HIP looks like a driver error
- Permission errors look like runtime errors
- `hipcc` being installed doesn't mean ROCm is installed

`rocm-doctor` fixes this. One command, one report, every layer checked. It aggregates all the scattered diagnostic sources, cross-references them, and tells you what's actually wrong in plain English.

## How it works

For each check, `rocm-doctor` queries multiple sources and prefers the most reliable. The kernel knows the truth; `rocm-smi` is a rumor.

**Hardware detection priority:**
1. `/sys/class/drm/` (kernel truth)
2. `lspci` (PCI truth)
3. `rocminfo` (ROCm's view)
4. `rocm-smi` (last resort)

It identifies GPUs by their gfx code (e.g., `gfx942` for MI300X) rather than marketing names, because the gfx code is the one thing that's always reliable. The included `gfx_map` database translates these codes to human names, architectures, and supported ROCm versions.

## What it checks

| Layer | What it verifies |
|---|---|
| **Hardware** | GPU model, gfx code, VRAM, PCI ID. Detects multiple GPUs. |
| **Driver** | Is amdgpu loaded? Firmware present? `/dev/kfd` exists? Any errors in dmesg? |
| **ROCm Runtime** | Is `/opt/rocm` installed? `hipcc` in PATH? `rocminfo` functional? Version compatibility with your gfx code. |
| **Vulkan** | Does `vulkaninfo` see the AMD GPU? Is the ICD installed? |
| **OpenCL** | Does `clinfo` detect the AMD platform? |
| **ML Frameworks** | Is PyTorch/TF/JAX installed? Built with HIP support or CUDA? |
| **Permissions** | Is the user in the video and render groups? Can they access `/dev/kfd`? |
| **Environment** | Are `CUDA_VISIBLE_DEVICES` or `HSA_OVERRIDE_GFX_VERSION` set? (Common pitfalls) |
| **Compute Test** | Runs a minimal GPU kernel to verify compute actually works, not just that libraries are installed. |
  
## Example Output

```markdown
# rocm-doctor Diagnostic Report

## Summary
- Status: ⚠ CRITICAL ISSUES FOUND
- GPU: AMD Instinct MI300X (gfx942)
- ROCm: Unknown

## ROCm Runtime: PARTIAL INSTALL ⚠
- ROCm Version: Unknown
- HIP Version: 7.2.53211
- hipcc: found at /usr/bin/hipcc (installed via package manager)
- /opt/rocm: does NOT exist (full ROCm stack not installed)

**Recommendation**: Install full ROCm stack from AMD's repo for ML workloads. hipcc alone is not sufficient for PyTorch/ROCm.
```

## The signature: Never crash, always report

A diagnostic tool that crashes on broken systems is useless. `rocm-doctor` is built to run on a system where ROCm is completely broken, the driver is missing, and `rocm-smi` segfaults — because that's exactly when you need it most.

- **Zero dependencies.** Pure Python stdlib. If it depended on a broken library, it couldn't diagnose the breakage.
- **Never raises.** Every check is wrapped. Every failure is captured. The report always generates.
- **Multiple sources.** If `rocm-smi` fails, it uses `rocminfo`. If `rocminfo` fails, it uses `/sys/class`. The tool always finds an answer.

## Supported Hardware

The `gfx_map` database includes:

| gfx Code | GPU Family |
|---|---|
| **gfx906** | Radeon VII, MI50/MI60 |
| **gfx908** | Instinct MI100 |
| **gfx90a** | Instinct MI200 (MI210/MI250/MI250X) |
| **gfx942** | Instinct MI300X / MI300A |
| **gfx1030** | RDNA2 (Radeon RX 6800/6900 XT) |
| **gfx1100** | RDNA3 (Radeon RX 7900 XTX) |
| **gfx1101** | RDNA3 (Radeon RX 7900 XT) |
| **gfx1102** | RDNA3 (Radeon RX 7600/7700 XT) |
| **gfx1151** | RDNA3.5 (Strix Halo iGPU) |
  
## License

MIT
