#!/usr/bin/env bash
set -euo pipefail

if ! command -v pandoc >/dev/null; then
  echo "[Lỗi] Chưa cài đặt pandoc" >&2
  exit 1
fi

if ! command -v xelatex >/dev/null; then
  echo "[Lỗi] Chưa cài đặt XeLaTeX (xelatex)" >&2
  exit 1
fi

if [[ $# -lt 2 ]]; then
  echo "Sử dụng: $0 <input.md> <output.pdf> [tham_so_pandoc...]" >&2
  exit 64
fi

INPUT="$1"
OUTPUT="$2"
shift 2

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/templates"

pandoc "$INPUT" \
  --from markdown+tex_math_dollars+yaml_metadata_block \
  --to pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --metadata-file "$TEMPLATE_DIR/metadata.yml" \
  --template "$TEMPLATE_DIR/reference.tex" \
  "$@" \
  -o "$OUTPUT"

echo "Đã tạo PDF: $OUTPUT"
