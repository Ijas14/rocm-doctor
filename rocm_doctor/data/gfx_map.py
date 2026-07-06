GFX_DATABASE = {
    # Legacy & Polaris (GCN 4.0)
    "gfx803": {
        "name": "Polaris (RX 400/500 Series)",
        "architecture": "GCN 4.0",
        "products": ["Radeon RX 480", "Radeon RX 580", "Radeon RX 590", "Radeon Pro Duo"],
        "rocm_support": "<5.0",
        "notes": "Legacy architecture. Deprecated in modern ROCm. Often requires community patches to run ML workloads.",
    },

    # Vega (GCN 5.0)
    "gfx900": {
        "name": "Vega 10",
        "architecture": "GCN 5.0",
        "products": ["Radeon RX Vega 56", "Radeon RX Vega 64", "Instinct MI25"],
        "rocm_support": ">=2.0, <=5.0",
        "notes": "Deprecated. Not officially supported in ROCm 5.1+.",
    },
    "gfx902": {
        "name": "Raven Ridge APU",
        "architecture": "GCN 5.0",
        "products": ["Ryzen 2000G", "Ryzen 3000G APUs"],
        "rocm_support": "Unofficial",
        "notes": "APU graphics. Usually requires HSA_OVERRIDE_GFX_VERSION.",
    },
    "gfx904": {
        "name": "Vega 12",
        "architecture": "GCN 5.0",
        "products": ["Radeon Pro Vega 20"],
        "rocm_support": "<=5.0",
    },
    "gfx906": {
        "name": "Vega 20",
        "architecture": "GCN 5.0",
        "products": ["Radeon VII", "Instinct MI50", "Instinct MI60"],
        "rocm_support": ">=2.0, <=5.7",
        "notes": "Radeon VII works but unsupported. Use HSA_OVERRIDE_GFX_VERSION for newer ROCm.",
    },
    "gfx909": {
        "name": "Raven2 APU",
        "architecture": "GCN 5.0",
        "products": ["Athlon 200GE / 3000G"],
        "rocm_support": "Unofficial",
    },
    "gfx90c": {
        "name": "Renoir APU",
        "architecture": "GCN 5.0",
        "products": ["Ryzen 4000G", "Ryzen 5000G APUs"],
        "rocm_support": "Unofficial",
        "notes": "APU graphics. Often used for budget ML setups via HSA_OVERRIDE_GFX_VERSION.",
    },

    # CDNA (Compute)
    "gfx908": {
        "name": "CDNA1 (MI100)",
        "architecture": "CDNA",
        "products": ["Instinct MI100"],
        "rocm_support": ">=4.0",
    },
    "gfx90a": {
        "name": "CDNA2 (MI200)",
        "architecture": "CDNA2",
        "products": ["Instinct MI210", "Instinct MI250", "Instinct MI250X"],
        "rocm_support": ">=5.0",
        "notes": "Matrix Core support requires ROCm 5.1+.",
    },
    "gfx940": {
        "name": "CDNA3 (MI300 early)",
        "architecture": "CDNA3",
        "products": ["Instinct MI300 (engineering)"],
        "rocm_support": ">=6.0",
    },
    "gfx941": {
        "name": "CDNA3 (MI300X)",
        "architecture": "CDNA3",
        "products": ["Instinct MI300X"],
        "rocm_support": ">=6.0",
    },
    "gfx942": {
        "name": "CDNA3 (MI300X/A production)",
        "architecture": "CDNA3",
        "products": ["Instinct MI300X", "Instinct MI300A"],
        "rocm_support": ">=6.0",
        "notes": "Production MI300 silicon. FP8 support requires ROCm 6.1+.",
    },

    # RDNA 1
    "gfx1010": {
        "name": "RDNA1 (Navi 10)",
        "architecture": "RDNA1",
        "products": ["Radeon RX 5700", "Radeon RX 5700 XT"],
        "rocm_support": "Unofficial",
        "notes": "Consumer GPU. Requires HSA_OVERRIDE_GFX_VERSION=10.3.0 on ROCm > 5.0.",
    },
    "gfx1011": {
        "name": "RDNA1 (Navi 12)",
        "architecture": "RDNA1",
        "products": ["Radeon Pro 5600M"],
        "rocm_support": "Unofficial",
    },
    "gfx1012": {
        "name": "RDNA1 (Navi 14)",
        "architecture": "RDNA1",
        "products": ["Radeon RX 5500", "Radeon RX 5500 XT"],
        "rocm_support": "Unofficial",
    },

    # RDNA 2
    "gfx10": {
        "name": "AMD APU Integrated Graphics",
        "architecture": "RDNA1/RDNA2 (APU variant)",
        "products": ["Ryzen APU iGPU (truncated gfx code)"],
        "rocm_support": "varies",
        "notes": "rocminfo sometimes reports 'gfx10' without the full code for APU iGPUs. Usually not officially ROCm-compatible.",
    },
    "gfx1030": {
        "name": "RDNA2 (Navi 21)",
        "architecture": "RDNA2",
        "products": ["Radeon RX 6800", "Radeon RX 6800 XT", "Radeon RX 6900 XT"],
        "rocm_support": ">=5.0",
        "notes": "Consumer GPU. ROCm works but officially unsupported. Good for dev/testing.",
    },
    "gfx1031": {
        "name": "RDNA2 (Navi 22)",
        "architecture": "RDNA2",
        "products": ["Radeon RX 6700", "Radeon RX 6700 XT"],
        "rocm_support": "Unofficial",
        "notes": "Requires HSA_OVERRIDE_GFX_VERSION=10.3.0.",
    },
    "gfx1032": {
        "name": "RDNA2 (Navi 23)",
        "architecture": "RDNA2",
        "products": ["Radeon RX 6600", "Radeon RX 6600 XT"],
        "rocm_support": "Unofficial",
        "notes": "Requires HSA_OVERRIDE_GFX_VERSION=10.3.0.",
    },
    "gfx1034": {
        "name": "RDNA2 (Navi 24)",
        "architecture": "RDNA2",
        "products": ["Radeon RX 6400", "Radeon RX 6500 XT"],
        "rocm_support": "Unofficial",
        "notes": "Requires HSA_OVERRIDE_GFX_VERSION=10.3.0.",
    },
    "gfx1035": {
        "name": "RDNA2 (Rembrandt APU)",
        "architecture": "RDNA2",
        "products": ["Ryzen 6000 Series APU (Radeon 680M)"],
        "rocm_support": "Unofficial",
        "notes": "APU graphics. Requires HSA_OVERRIDE_GFX_VERSION=10.3.0.",
    },
    "gfx1036": {
        "name": "RDNA2 (Raphael APU)",
        "architecture": "RDNA2",
        "products": ["Ryzen 7000 Desktop iGPU"],
        "rocm_support": "Unofficial",
        "notes": "APU graphics.",
    },

    # RDNA 3 & 3.5
    "gfx1100": {
        "name": "RDNA3 (Navi 31)",
        "architecture": "RDNA3",
        "products": ["Radeon RX 7900 XTX", "Radeon RX 7900 XT"],
        "rocm_support": ">=5.7",
        "notes": "Consumer GPU. Officially supported in newer ROCm for PyTorch on Linux.",
    },
    "gfx1101": {
        "name": "RDNA3 (Navi 32)",
        "architecture": "RDNA3",
        "products": ["Radeon RX 7800 XT", "Radeon RX 7700 XT"],
        "rocm_support": "Unofficial",
        "notes": "Requires HSA_OVERRIDE_GFX_VERSION=11.0.0.",
    },
    "gfx1102": {
        "name": "RDNA3 (Navi 33)",
        "architecture": "RDNA3",
        "products": ["Radeon RX 7600", "Radeon RX 7600 XT"],
        "rocm_support": "Unofficial",
        "notes": "Requires HSA_OVERRIDE_GFX_VERSION=11.0.0.",
    },
    "gfx1103": {
        "name": "RDNA3 (Phoenix APU)",
        "architecture": "RDNA3",
        "products": ["Ryzen 7040/8040 Series APU (Radeon 780M)"],
        "rocm_support": "Unofficial",
        "notes": "APU graphics. Often requires HSA_OVERRIDE_GFX_VERSION=11.0.0 for ML inference.",
    },
    "gfx1150": {
        "name": "RDNA3.5 (Strix Point NPU)",
        "architecture": "RDNA3.5",
        "products": ["Ryzen AI 300 series NPU"],
        "rocm_support": ">=6.1",
        "notes": "NPU, not GPU. Often requires dedicated SDK/Server.",
    },
    "gfx1151": {
        "name": "RDNA3.5 (Strix Halo iGPU)",
        "architecture": "RDNA3.5",
        "products": ["Ryzen AI Max+ 395 (Strix Halo)"],
        "rocm_support": ">=6.2 (experimental)",
        "notes": "Unified memory architecture. High compute iGPU.",
    },
}
