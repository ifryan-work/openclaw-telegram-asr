#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[install] apt deps"
sudo apt-get update
sudo apt-get install -y python3-pip python3.12-venv

echo "[install] create venv"
python3 -m venv .venv

echo "[install] install faster-whisper"
.venv/bin/pip install --upgrade pip
.venv/bin/pip install faster-whisper

echo "[install] done"
