#!/bin/bash
# filepath: run_benchmarks.sh

cmake --fresh -B build_omp -DKokkos_ENABLE_OPENMP=ON && cmake --fresh -B build_cuda -DKokkos_ENABLE_CUDA=ON && cmake --build build_omp -j20 && cmake --build build_cuda -j20

NMAX=${1:-26}         # N max (exposant, donc N=1..NMAX)
SERIES=${2:-5}        # Nombre de séries à faire (par défaut 5)
LAYOUT=${3:-left}     # left ou right (par défaut left)
OMP_EXE=./build_omp/04_Exercise
CUDA_EXE=./build_cuda/04_Exercise

mkdir -p logs/omp logs/cuda

for s in $(seq 1 $SERIES); do
    echo "=== Série $s/$SERIES : OMP ($LAYOUT) ==="
    for N in $(seq 1 $NMAX); do
        echo "[OMP] Série $s/$SERIES - N=$N"
        $OMP_EXE -N $N >> logs/omp/omp_test_layout_${LAYOUT}_N${N}_S${s}.log
    done
    echo "=== Série $s/$SERIES : CUDA ($LAYOUT) ==="
    for N in $(seq 1 $NMAX); do
        echo "[CUDA] Série $s/$SERIES - N=$N"
        $CUDA_EXE -N $N >> logs/cuda/cuda_test_layout_${LAYOUT}_N${N}_S${s}.log
    done
done

echo "Tous les tests sont terminés."