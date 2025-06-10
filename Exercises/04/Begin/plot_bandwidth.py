import re
import numpy as np
import matplotlib.pyplot as plt
import glob
from collections import defaultdict

def parse_logs(pattern):
    """Parse tous les fichiers correspondant au pattern et retourne un dict N -> [BW, ...]"""
    data = defaultdict(list)
    for fname in glob.glob(pattern):
        with open(fname) as f:
            n = None
            for line in f:
                m = re.search(r'User N is (\d+)', line)
                if m:
                    n = int(m.group(1))
                m = re.search(r'bandwidth\(\s*([\d\.]+) GB/s', line)
                if m and n is not None:
                    bw = float(m.group(1))
                    data[n].append(bw)
    return data

def average_data(data):
    """Retourne deux listes triées : N, BWmoy"""
    N = sorted(data.keys())
    BW = [np.mean(data[n]) for n in N]
    return np.array(N), np.array(BW)

# Patterns à parser
patterns = {
    "CUDA LayoutLeft":  "logs/cuda/cuda_test_layout_left_N*_S*.log",
    "CUDA LayoutRight": "logs/cuda/cuda_test_layout_right_N*_S*.log",
    "OMP LayoutLeft":   "logs/omp/omp_test_layout_left_N*_S*.log",
    "OMP LayoutRight":  "logs/omp/omp_test_layout_right_N*_S*.log",
}

styles = {
    "CUDA LayoutLeft":  {'color': 'tab:blue',   'linestyle': '-',  'label': 'CUDA LayoutLeft'},
    "CUDA LayoutRight": {'color': 'tab:blue',   'linestyle': '--', 'label': 'CUDA LayoutRight'},
    "OMP LayoutLeft":   {'color': 'tab:orange', 'linestyle': '-',  'label': 'OMP LayoutLeft'},
    "OMP LayoutRight":  {'color': 'tab:orange', 'linestyle': '--', 'label': 'OMP LayoutRight'},
}

plt.figure(figsize=(10,6))

for key, pattern in patterns.items():
    data = parse_logs(pattern)
    if data:
        N, BW = average_data(data)
        plt.plot(N, BW, marker='o', **styles[key])

plt.xscale('log')
plt.xlabel('N (Number of Rows)')
plt.ylabel('Bandwidth (GB/s)')
plt.title('Bandwidth vs N (moyenne sur séries)')
plt.legend()
plt.grid(True, which='both', ls=':')
plt.tight_layout()
plt.savefig('bandwidth_vs_n.png', dpi=300)