#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <audio-path> [language=zh|en|auto]"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUDIO_PATH="$1"
LANGUAGE="${2:-zh}"

cd "$ROOT_DIR"

.venv/bin/python scripts/asr_demo.py \
  --input "$AUDIO_PATH" \
  --model base \
  --language "$LANGUAGE" \
  --compute-type int8
