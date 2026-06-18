#!/bin/bash
set -euo pipefail

# Robust argument handling
DATA_DIR="${1:-.\/data}"
MODEL_PATH="${2:-.\/pickle\/model.pkl}"
OUTPUT_PATH="${3:-.\/output\/predictions.csv}"

# Create output directory
mkdir -p "$(dirname "$OUTPUT_PATH")" 2>/dev/null || true

echo "=========================================="
echo "ForecastIQ Pipeline Starting"
echo "=========================================="
echo "DATA_DIR: $DATA_DIR"
echo "MODEL_PATH: $MODEL_PATH"  
echo "OUTPUT_PATH: $OUTPUT_PATH"
echo ""

# Step 1: Feature Generation
echo "[Step 1/3] Generating features from raw data..."
if [ ! -f "src/generate_features.py" ]; then
    echo "ERROR: src/generate_features.py not found!"
    exit 1
fi

python3 src/generate_features.py \
    --data-dir "$DATA_DIR" \
    --output features.parquet || { echo "Feature generation failed!"; exit 1; }

# Step 2: Predictions
echo "[Step 2/3] Loading model and generating predictions..."
if [ ! -f "$MODEL_PATH" ]; then
    echo "ERROR: Model not found at $MODEL_PATH"
    exit 1
fi

python3 src/predict.py \
    --features features.parquet \
    --model "$MODEL_PATH" \
    --output "$OUTPUT_PATH" || { echo "Prediction failed!"; exit 1; }

# Step 3: Monte Carlo
echo "[Step 3/3] Running Monte Carlo simulations..."
python3 src/monte_carlo.py \
    --predictions "$OUTPUT_PATH" || { echo "Monte Carlo simulation failed!"; exit 1; }

echo ""
echo "=========================================="
echo "✅ Pipeline completed successfully!"
echo "=========================================="
echo "📊 Output: $OUTPUT_PATH"
ls -lh "$OUTPUT_PATH"
