#!/usr/bin/env bash
# One-time setup per session/machine: Python packages, narrator voice, map data. Safe to re-run.
set -e
cd "$(dirname "$0")"
D=${VENGINE_DATA:-data}; mkdir -p "$D/cache"
python3 -c "import kokoro_onnx, cairo, soundfile, PIL, numpy" 2>/dev/null || \
  pip install -q kokoro-onnx soundfile pycairo pillow numpy 2>/dev/null || pip install -q --break-system-packages kokoro-onnx soundfile pycairo pillow numpy
command -v ffmpeg >/dev/null || { echo "ffmpeg is missing: install it (apt install ffmpeg / brew install ffmpeg / winget install ffmpeg)"; exit 1; }
NE=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
KO=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
get() { [ -s "$D/$1" ] || { echo "downloading $1"; curl -sSfL -o "$D/$1.part" "$2" && mv "$D/$1.part" "$D/$1"; }; }
get land.geojson      $NE/ne_10m_land.geojson
get borders.geojson   $NE/ne_50m_admin_0_boundary_lines_land.geojson
get cities.geojson    $NE/ne_10m_populated_places_simple.geojson
get countries.geojson $NE/ne_50m_admin_0_countries.geojson
get kokoro-v1.0.onnx  $KO/kokoro-v1.0.onnx
get voices-v1.0.bin   $KO/voices-v1.0.bin
fc-list 2>/dev/null | grep -qi "Liberation Serif" || echo "note: Liberation Serif font not found; text will use a fallback serif"
echo "video-engine ready."
