#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${1:-./data}"
MODEL_PATH="${2:-./pickle/model.pkl}"
OUTPUT_PATH="${3:-./output/predictions.csv}"

mkdir -p "$(dirname "$OUTPUT_PATH")"

echo "Starting ForecastIQ pipeline..."
echo "DATA_DIR: $DATA_DIR"
echo "MODEL_PATH: $MODEL_PATH"
echo "OUTPUT_PATH: $OUTPUT_PATH"

echo "Step 1/3: Generating features..."
python src/generate_features.py \
  --data-dir "$DATA_DIR" \
  --output features.parquet

echo "Step 2/3: Loading model and generating predictions..."
python src/predict.py \
  --features features.parquet \
  --model "$MODEL_PATH" \
  --output "$OUTPUT_PATH"

echo "Step 3/3: Generating probabilistic forecasts..."
python src/monte_carlo.py \
  --predictions "$OUTPUT_PATH"

echo "✅ Pipeline completed successfully!"
echo "📊 Predictions written to: $OUTPUT_PATH"
