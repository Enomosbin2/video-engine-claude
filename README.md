# video-engine

Turns a plain-text script into a narrated, animated MP4 (1280×720, 30 fps). It produces real maps, moving units, arrows, quotes, timelines, counters and stamps, not slides.

## Make a video

```
./setup.sh                                  # once: Python packages, voice, map data
python3 make_video.py examples/demo.txt     # -> examples/demo.mp4
```

Write your own script using `GUIDE.md`. Run with `--check` first to get narration timings and contact sheets of test frames before the full render.

## What `setup.sh` downloads (not stored in this repo)

| File | Source |
|---|---|
| `kokoro-v1.0.onnx`, `voices-v1.0.bin` (narrator, ~350 MB) | github.com/thewh1teagle/kokoro-onnx, release model-files-v1.0 |
| `land`, `borders`, `cities`, `countries` (.geojson) | Natural Earth, github.com/nvkelso/natural-earth-vector |

It also installs the Python packages `kokoro-onnx`, `soundfile`, `pycairo`, `pillow` and `numpy`. It needs `ffmpeg`. Everything goes in `data/` (or `$VENGINE_DATA`), and maps are cached in `data/cache/`.

## Layout

```
make_video.py        one command: narrate, plan, render scenes in parallel, join, add audio
setup.sh             one-time downloads
GUIDE.md             script format and tag reference (read this)
vengine/core.py      drawing primitives
vengine/geo.py       world maps on demand, place-name lookup, camera
vengine/speech.py    offline narration and number pronunciation
vengine/script.py    script parser
vengine/scenes.py    boards and overlays, frame drawing
vengine/customs.py   special animations (magnets, gears, hub, water, curve, ladder, scales)
examples/demo.txt    50-second sample
examples/handcoded/  the original Sun Tzu / Clausewitz scene code, for reference
```

Rendering takes about 1 to 1.5 times the video length on 2 CPU cores.
