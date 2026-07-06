# rocm-doctor

`rocm-doctor` is the diagnostic tool AMD developers wish existed.

`rocm-smi` reports "N/A" for GPU names. ROCm version mismatches are hard to debug. PyTorch built for CUDA instead of HIP is a silent failure. Permissions errors look like driver errors.

`rocm-doctor` fixes this. One command, one report, every layer checked. It trusts the kernel before userspace. It cross-references hardware, driver, runtime, and frameworks. It never crashes — even on a system where everything is broken, because that's when you need it most.

## Installation

```bash
pip install rocm-doctor
```

## Usage

```bash
python -m rocm_doctor
```
# rocm-doctor
