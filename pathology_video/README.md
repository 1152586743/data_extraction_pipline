# Caption Extraction Pipeline 

This repo contains a **2-stage pipeline** to (1) collect YouTube videos by keyword and (2) extract **English captions** into clean per-video CSVs.

---

## 0) Directory layout (convention)

```
/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/
├─ playlist/
│  └─ dermatology_all_20251017.csv        # list of videos (video_id, title, url, …)
└─ caption/
   ├─ terminal_pipline.txt                # shell pipeline you run in Terminal
   ├─ vtt_to_segments.py                  # caption .vtt → segments.csv converter
   ├─ caption_origin/                     # raw .vtt per video_id
   │  └─ <video_id>/
   │     └─ <video_id>.*en*.vtt          # e.g., NdrYA3Tc82w.es.en.vtt
   └─ caption_orgainized/                 # cleaned segments per video_id
      └─ <video_id>/
         └─ segments.csv                  # start/end/text per caption cue
```

> Only these two output folders are produced by the pipeline:
> - **caption_origin/** → raw `.vtt`
> - **caption_orgainized/** → cleaned `segments.csv`

---

## 1) Build the video list (Notebook)

- Open the notebook:  
  `/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/youtube_video_playlist_extraction.ipynb`
- Set your **keyword** (e.g., `dermatology`) and run the cells.
- The notebook writes a playlist CSV to:  
  `/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/playlist/dermatology_all_20251017.csv`

**What’s inside:** at least `video_id`, `title`, `url` (plus any other fields you collected).

---

## 2) Extract captions & convert to CSV (Terminal)

- The exact shell pipeline is saved in:  
  `/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/caption/terminal_pipline.txt`

- What it does for the **first N** videos from the playlist CSV:
  1. Download **English** captions (`.vtt`) via `yt-dlp` using the **web_embedded** client + **Chrome cookies** (this combo works around PO-token issues in your environment).
  2. Select the **best English-like track** matching `*en*` (covers `en`, `en-en`, `es.en`, etc.).
  3. Convert to normalized **segments.csv** (`video_id, idx, start, end, text`) using `webvtt-py` + `pandas`.

### Minimal config inside `terminal_pipline.txt`
```bash
# Input playlist
CSV_IN="/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/playlist/dermatology_all_20251017.csv"

# Caption workspace
BASE_CAP="/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/caption"
DIR_ORIG="$BASE_CAP/caption_origin"
DIR_ORGZ="$BASE_CAP/caption_orgainized"

TOP_N=3                     # how many videos to process (change as needed)
CHROME_PROFILE="Default"    # your Chrome profile name
```

### Outputs produced
- Raw **.vtt** →  
  `.../caption/caption_origin/<video_id>/<video_id>.*en*.vtt`
- Clean **segments.csv** →  
  `.../caption/caption_orgainized/<video_id>/segments.csv`

---

## 3) Expected per-video outputs

**Raw captions (VTT):**
```
/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/caption/caption_origin/<video_id>/<video_id>.*en*.vtt
```
Examples: `NdrYA3Tc82w.en.vtt`, `NdrYA3Tc82w.en-en.vtt`, `NdrYA3Tc82w.es.en.vtt`

**Clean segments (CSV):**
```
/Users/yhu10/Desktop/VLM/data_extraction_pipline/pathology_video/caption/caption_orgainized/<video_id>/segments.csv
```
Columns:
- `video_id` — YouTube ID  
- `idx` — 0-based cue index  
- `start` — start timestamp (HH:MM:SS.mmm)  
- `end` — end timestamp (HH:MM:SS.mmm)  
- `text` — normalized caption text

---

## 4) Dependencies

- **yt-dlp** (caption downloader)
- **Python 3.10+** recommended (3.9 shows deprecation warnings)
- **Python packages:** `webvtt-py`, `pandas`
- **(Optional)** `ffmpeg` (not required for captions; only needed if you later extract frames)

> The terminal pipeline auto-installs `webvtt-py` and `pandas` if missing.  
> If you hit rate-limits (HTTP 429), light sleep/retry flags are included; adjust as needed.

---

## 5) Notes / Tips

- Using **web_embedded + Chrome cookies** avoids “PO token required” failures that can block automatic captions under the regular `web` client.
- Filenames like `*.es.en.vtt` are still treated as **English** thanks to the `*en*` match.
- To process more videos, raise `TOP_N` or adapt the selection logic.