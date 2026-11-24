#!/usr/bin/env python3
"""assets/*.svg を同名の PNG（幅 2000px、2倍解像度）に書き出す。個別の図を資料に貼るための併存ファイル。

rsvg-convert（librsvg）を使う。macOS では `brew install librsvg`。scripts/draw_figures.py の後に実行する。
--check を付けると書き出さず、すべての SVG に対応する PNG があり、SVG より古くないことだけを確認する。"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
WIDTH = 2000


def export(svg: Path) -> Path:
    png = svg.with_suffix('.png')
    subprocess.run(['rsvg-convert', '--width', str(WIDTH), '--keep-aspect-ratio', '--output', str(png), str(svg)], check=True)
    return png


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='書き出さずに PNG の存在と新しさだけを確認する')
    args = parser.parse_args()
    svgs = sorted(ASSETS.glob('*.svg'))
    if not svgs:
        print('assets/ に SVG がない。先に scripts/draw_figures.py を実行する。', file=sys.stderr)
        return 1
    if args.check:
        errors = [f'{s.name}: PNG が無いか古い' for s in svgs
                  if not s.with_suffix('.png').exists() or s.with_suffix('.png').stat().st_mtime < s.stat().st_mtime]
        for e in errors:
            print(e, file=sys.stderr)
        print(f'checked {len(svgs)} figures, {len(errors)} problem(s)')
        return 1 if errors else 0
    if not shutil.which('rsvg-convert'):
        print('rsvg-convert が無い。macOS では `brew install librsvg`。', file=sys.stderr)
        return 1
    for svg in svgs:
        png = export(svg)
        print('wrote', png.relative_to(ROOT), png.stat().st_size, 'bytes')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
