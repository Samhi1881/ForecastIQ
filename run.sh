#!/usr/bin/env bash

set -euo pipefail

DATA_DIR="${1:-./data}"
MODEL_PATH="${2:-./pickle/model.pkl}"
OUTPUT_PATH="${3:-./output/predictions.csv}"

echo "=========================================="
echo "ForecastIQ Pipeline Starting"
echo "=========================================="
echo "DATA_DIR: $DATA_DIR"
echo "MODEL_PATH: $MODEL_PATH"
echo "OUTPUT_PATH: $OUTPUT_PATH"

mkdir -p output

echo ""
echo "[1/2] Generating Features..."

py src/generate_features.py `
    --data-dir "$DATA_DIR" `
    --output features.parquet

echo ""
echo "[2/2] Generating Predictions..."

py src/predict.py

echo ""
echo "=========================================="
echo "Pipeline Completed Successfully"
echo "=========================================="
echo "Predictions saved to output/predictions.csv"
