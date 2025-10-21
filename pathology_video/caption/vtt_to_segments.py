#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 /<BASE>/<video_id>/captions/*.vtt 解析成 /<BASE>/<video_id>/segments.csv
用法:
  python3 vtt_to_segments.py --base "/Users/yhu10/Desktop/VLM/pathology_video/YT" 8N0IZZpF8ts
  # 也可用 URL:
  # python3 vtt_to_segments.py --base "/Users/.../YT" "https://www.youtube.com/watch?v=8N0IZZpF8ts"

依赖: webvtt-py, pandas
  python3 -m pip install --user webvtt-py pandas
"""
import argparse, re, sys
from pathlib import Path
import pandas as pd
import webvtt

def parse_video_id(url_or_id: str) -> str:
    m = re.search(r"(?:v=|/shorts/|youtu\.be/)([A-Za-z0-9_-]{6,})", url_or_id)
    return m.group(1) if m else url_or_id

def list_vtts(capdir: Path, vid: str):
    # 兼容 en.vtt / en-en.vtt / en-orig.vtt / NA.en.vtt 等
    return list(capdir.glob(f"{vid}*.vtt"))

def is_english(name: str) -> bool:
    # 识别 en-orig / en-en / *.en.vtt / *.NA.en.vtt
    if "en-orig" in name or "en-en" in name:
        return True
    return bool(re.search(r'(\.|-)en(\.|-|$)', name))

def pick_best_english_vtt(vtts):
    ens = [p for p in vtts if is_english(p.name)]
    if not ens:
        return None
    # 优先级: en-orig > 普通 en（含 NA.en） > en-en；同级取体积更大
    def rank(p: Path):
        n = p.name
        if "en-orig" in n: base = 3
        elif "en-en" in n: base = 1
        elif re.search(r'(\.|-)en(\.|-|$)', n): base = 2
        else: base = 0
        return (base, p.stat().st_size)
    return sorted(ens, key=rank, reverse=True)[0]

def vtt_to_segments(vtt_path: Path, out_csv: Path, vid: str):
    def norm(s: str) -> str: return re.sub(r"\s+", " ", s).strip()
    rows = []
    for i, c in enumerate(webvtt.read(str(vtt_path))):
        rows.append({"video_id": vid, "idx": i, "start": c.start, "end": c.end, "text": norm(c.text)})
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"[ok] Picked:   {vtt_path.name}")
    print(f"[ok] Written:  {out_csv} ({len(rows)} rows)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="项目根目录，例如 /Users/.../pathology_video/YT")
    ap.add_argument("url_or_id", help="YouTube URL 或视频ID")
    args = ap.parse_args()

    base = Path(args.base)
    vid = parse_video_id(args.url_or_id)
    vdir = base / vid
    capdir = vdir / "captions"
    out_csv = vdir / "segments.csv"

    if not capdir.exists():
        print(f"[error] 字幕目录不存在: {capdir}\n请先用 yt-dlp 下载 .vtt 到该目录。")
        sys.exit(2)

    vtts = list_vtts(capdir, vid)
    if not vtts:
        print(f"[error] 未在 {capdir} 找到 {vid}*.vtt 文件")
        sys.exit(3)

    best = pick_best_english_vtt(vtts)
    if not best:
        print(f"[error] 找到 .vtt 但没有英文轨道: {[p.name for p in vtts]}")
        sys.exit(4)

    vtt_to_segments(best, out_csv, vid)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Interrupted]")

