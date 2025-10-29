import os
import re
import json
import glob
import argparse
from typing import List, Dict, Any

def infer_participant_id_from_path(path: str) -> str:
    base = os.path.basename(path)
    if base.endswith("_NR_processed.json"):
        return base[:-len("_NR_processed.json")]
    return os.path.splitext(base)[0]

def extract_from_sentence(sent: Dict[str, Any]) -> Dict[str, Any]:
    words = sent.get("words", [])
    words_sequence = [w.get("content", "") for w in words]

    word_index_sequence: List[int] = []
    fix_seq = sent.get("fixation_sequence", []) or sent.get("fixations", [])
    for f in fix_seq:
        if "word_idx" in f:
            try:
                word_index_sequence.append(int(f["word_idx"]))
            except Exception:
                pass

    return dict(
        sentence_id=sent.get("sentence_id", -1),
        word_index_sequence=word_index_sequence,
        words_sequence=words_sequence,
    )

def find_input_files(input_dir: str) -> List[str]:
    files = sorted(glob.glob(os.path.join(input_dir, "*_NR_processed.json")))
    if not files:
        files = sorted(glob.glob(os.path.join(input_dir, "*.json")))
    return files

def main():
    ap = argparse.ArgumentParser(description="Pack fixation sequences from participant JSONs into one JSON file.")
    ap.add_argument("--input_dir", required=True, help="Directory containing per-participant *_NR_processed.json files")
    ap.add_argument("--output_json", required=True, help="Output JSON path")
    args = ap.parse_args()

    files = find_input_files(args.input_dir)
    if not files:
        print(f"No JSON files found in {args.input_dir}")
        return

    out = {"fixation sequences": []}  # Key name as requested

    total = 0
    for path in files:
        pid = infer_participant_id_from_path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to read {path}: {e}")
            continue

        if not isinstance(data, list):
            print(f"[WARN] Unexpected file structure in {path}; expecting a list per file")
            continue

        for sent in data:
            rec = extract_from_sentence(sent)
            rec["participant_id"] = pid
            out["fixation sequences"].append(rec)
            total += 1

    os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Done. Wrote {total} records to {args.output_json}")

if __name__ == "__main__":
    main()
