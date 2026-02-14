#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Local ASR demo for Telegram voice")
    p.add_argument("--input", required=True, help="Audio file path (ogg/opus/mp3/wav/m4a)")
    p.add_argument("--model", default="base", help="Whisper model size")
    p.add_argument("--language", default="zh", help="Language code: zh/en/auto")
    p.add_argument("--compute-type", default="int8", help="Compute type for faster-whisper")
    p.add_argument("--output", default="", help="Optional output txt path")
    p.add_argument("--segments-json", default="", help="Optional segments json path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input not found: {input_path}")

    language = None if args.language == "auto" else args.language

    model = WhisperModel(args.model, device="cpu", compute_type=args.compute_type)
    segments, info = model.transcribe(str(input_path), language=language, vad_filter=True)

    rows = []
    text_parts = []
    for s in segments:
        part = s.text.strip()
        if not part:
            continue
        text_parts.append(part)
        rows.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": part})

    final_text = "\n".join(text_parts).strip()

    print("=== ASR RESULT ===")
    print(f"input: {input_path}")
    print(f"detected_language: {info.language} (p={info.language_probability:.3f})")
    print("--- transcript ---")
    print(final_text or "<empty>")

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(final_text, encoding="utf-8")
        print(f"saved text: {out}")

    if args.segments_json:
        outj = Path(args.segments_json).expanduser().resolve()
        outj.parent.mkdir(parents=True, exist_ok=True)
        outj.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved segments: {outj}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
