#!/usr/bin/env python3
"""記事「React／Frontendにおけるアクセシビリティテストの整理」の図版を決定論的に生成する。

体裁：幅1000px、最小フォント14px、注記16px、Python標準ライブラリのみ。
配色は役割で固定する（claudedocs/publication-plan.md §4.1）。
  NEUTRAL   区別を付けない基本要素、画面・コンポーネントの箱
  PRIMARY   自動テスト（Lint・axe-core・Testing Library・Playwright）とその検出範囲
  HUMAN     人と支援技術（スクリーンリーダー・目視・利用者評価）
  POSITIVE  自動化できる・検証済みの資産として再利用できる
  ATTENTION ツールでは保証できない・手動が要る・限界（1図に1系統）
  INK       結論・題名の強調（色ではなく太字）
1図で使う色相は最大3（NEUTRALは数えない）、地の塗りは最大4種。文字と地色のコントラスト比は4.5以上。
数値を使う図は作らず、定性的な塗り分けと配置だけで示す。要素は2〜5個、矢印は1方向に限る。
"""
from __future__ import annotations
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

# --- 中立 ---
BG = '#fcfdfd'; INK = '#18324b'; T1 = '#223e53'; T2 = '#36556d'; MUTED = '#55646d'
LINE = '#607a91'; STROKE = '#8ea6b2'; NEUTRAL = '#eef3f1'; WATER = '#d6e6f2'
# --- 役割色（地 / 線 / 文字） ---
PRIMARY = '#e1edf8'; PRI_TEXT = '#2b5f9e'
HUMAN = '#e9e4f5'; HUM_LINE = '#8a6cc1'; HUM_TEXT = '#6a4ea6'
POSITIVE = '#e0f0e9'; POS_LINE = '#5aa06f'; POS_TEXT = '#2f6b45'
ATTENTION = '#f7e9d4'; ATT_LINE = '#c0604a'; ATT_TEXT = '#9c3f2a'

PALETTE = {BG, INK, T1, T2, MUTED, LINE, STROKE, NEUTRAL, WATER,
           PRIMARY, PRI_TEXT, HUMAN, HUM_LINE, HUM_TEXT, POSITIVE, POS_LINE, POS_TEXT, ATTENTION, ATT_LINE, ATT_TEXT}
FONT = 'font-family="sans-serif"'
MIN_FONT = 14
NOTE_FONT = 16
CAPTION_MAX = 30  # キャプション（aria-label＝記事の alt）の最大文字数


def esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def est_w(s: str, size: float) -> float:
    """文字幅の保守的な概算。ASCIIは0.6em、それ以外（全角・矢印・記号）は1.0em。"""
    return sum(size * (0.6 if ord(c) < 0x80 else 1.0) for c in s)


def text(x, y, s, size=17, weight=400, fill=T2, anchor='middle', extra=''):
    size = max(size, MIN_FONT)
    w = f' font-weight="{weight}"' if weight != 400 else ''
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" {FONT} font-size="{size:g}"{w} fill="{fill}"{extra}>{esc(s)}</text>'


def lines(x, y, rows, size=14, weight=400, fill=T2, anchor='middle', lh=None):
    """複数行テキスト。rows の各要素は文字列か (文字列, weight, fill) のタプル。"""
    lh = lh or size + 6
    out = []
    for i, r in enumerate(rows):
        if isinstance(r, tuple):
            s, wt, fl = r
        else:
            s, wt, fl = r, weight, fill
        if s:
            out.append(text(x, y + i * lh, s, size, wt, fl, anchor))
    return ''.join(out)


def title(s):
    """図の題名（結論文）。"""
    return text(50, 50, s, 24, 700, INK, 'start')


def rect(x, y, w, h, fill, stroke=STROKE, sw=1, rx=12, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'


def box(x, y, w, h, fill, head, sub=None, hs=20, ss=15, stroke=STROKE, sw=1, head_fill=T1):
    out = [rect(x, y, w, h, fill, stroke, sw)]
    cx = x + w / 2
    if sub:
        out.append(text(cx, y + h / 2 - 4, head, hs, 700, head_fill))
        out.append(text(cx, y + h / 2 + 20, sub, ss))
    else:
        out.append(text(cx, y + h / 2 + 7, head, hs, 700, head_fill))
    return ''.join(out)


def card(x, y, w, h, fill, head, rows, hs=18, rs=14, stroke=STROKE, sw=1, head_fill=T1, row_fill=T2, top=30, lh=22):
    """見出し＋複数行の箱。head は太字、rows は lines() の形式。"""
    return rect(x, y, w, h, fill, stroke, sw) + text(x + w / 2, y + top, head, hs, 700, head_fill) + lines(x + w / 2, y + top + 28, rows, rs, 400, row_fill, lh=lh)


def pill(x, y, w, h, s, fill=NEUTRAL, size=14, weight=400, color=T1, stroke=STROKE, sw=1):
    return rect(x, y, w, h, fill, stroke, sw, rx=h / 2) + text(x + w / 2, y + h / 2 + size * 0.36, s, size, weight, color)


def arrow(x1, y1, x2, y2, dashed=False, color=LINE, width=3):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    ex, ey = x2 - ux * 10, y2 - uy * 10
    nx, ny = -uy, ux
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return (f'<path d="M{x1:.1f} {y1:.1f} L{ex:.1f} {ey:.1f}" stroke="{color}" stroke-width="{width}" fill="none"{dash}/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {x2 - ux * 12 + nx * 7:.1f},{y2 - uy * 12 + ny * 7:.1f} {x2 - ux * 12 - nx * 7:.1f},{y2 - uy * 12 - ny * 7:.1f}" fill="{color}"/>')


def path_arrow(d, end, color=LINE, dashed=False, width=3):
    """任意の経路（d）の末尾に矢頭を付ける。end は (x, y, ux, uy)：矢頭の先端と向きの単位ベクトル。"""
    x, y, ux, uy = end; nx, ny = -uy, ux
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return (f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none"{dash}/>'
            f'<polygon points="{x:.1f},{y:.1f} {x - ux * 12 + nx * 7:.1f},{y - uy * 12 + ny * 7:.1f} {x - ux * 12 - nx * 7:.1f},{y - uy * 12 - ny * 7:.1f}" fill="{color}"/>')


def bracket(x1, x2, y, label, color=LINE, size=15, weight=700, up=True, tick=12):
    """横方向のブラケット。up=True なら線の上にラベル。"""
    sgn = -1 if up else 1
    d = f'M{x1} {y + sgn * tick} V{y} H{x2} V{y + sgn * tick}'
    ly = y - tick - 10 if up else y + tick + size + 6
    return (f'<path d="{d}" stroke="{color}" stroke-width="2" fill="none"/>'
            + text((x1 + x2) / 2, ly, label, size, weight, color))


def note(y, s, size=NOTE_FONT):
    """図下部の注記。幅880pxを超える場合は句点（なければ中央付近の読点）で2行に折り返す。"""
    if est_w(s, size) <= 880:
        return text(500, y, s, size, 400, MUTED)
    cut = s.find('。')
    if not (0 < cut < len(s) - 1):
        cut = s.rfind('、', 0, len(s) // 2 + 6)
    parts = [s[:cut + 1], s[cut + 1:]]
    return lines(500, y, parts, size, 400, MUTED, lh=22)


def svg(w, h, caption, body, desc=''):
    """caption は図の主題を表す名詞句（全角30字以内、要素の列挙はしない）。記事の alt とキャプションになる。
    desc は図の内容の詳しい説明で、SVG を直接開いたときの支援技術向けに <desc> として残す。"""
    if len(caption) > CAPTION_MAX:
        raise ValueError(f'caption too long ({len(caption)} > {CAPTION_MAX}): {caption}')
    d = f'<desc id="desc">{esc(desc)}</desc>\n' if desc else ''
    aria = ' aria-describedby="desc"' if desc else ''
    content = '\n'.join(b for b in body if b)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(caption)}"{aria}>\n'
            f'{d}<rect width="100%" height="100%" fill="{BG}"/>\n' + content + '\n</svg>\n')


# =====================================================================


# =====================================================================
# 共通部品：テストレベルの鎖（02・06 で使う）と、縦積みの層（01・11 で使う）
# =====================================================================
def chain(x0, y, labels, total_w=880, gap=12, h=38, size=15, fills=None, colors=None, strokes=None):
    """工程のピルを横一列に並べ、背後に左から右への1本の矢印を引く。戻り値は (svg, [(x, w), ...])。
    fills / colors / strokes は {添字: 色} で個々のピルの地・文字・枠を上書きする（既定は NEUTRAL / T1 / STROKE）。"""
    n = len(labels)
    pw = (total_w - gap * (n - 1)) / n
    cy = y + h / 2
    out = [arrow(x0 + pw / 2, cy, x0 + total_w + 22, cy)]
    cols = []
    for i, s in enumerate(labels):
        x = x0 + i * (pw + gap)
        out.append(pill(x, y, pw, h, s, (fills or {}).get(i, NEUTRAL), size, 700, (colors or {}).get(i, T1), (strokes or {}).get(i, STROKE)))
        cols.append((x, pw))
    return ''.join(out), cols


LEVELS = ['FE単体', 'FE内部結合', 'FE・BE結合', 'ST（システムテスト）']


def levels(y, fills=None, colors=None, strokes=None):
    """4段階のテストレベルを横一列のピルで描く。戻り値は chain() と同じ (svg, [(x, w), ...])。"""
    return chain(60, y, LEVELS, total_w=880, fills=fills, colors=colors, strokes=strokes)


def stack(y0, rows, lx=60, lw=390, rx=470, rw=330, h=56, gap=8):
    """上から順に層を積む。rows の各要素は (fill, stroke, head_fill, head, sub, right)。
    左の箱に head（太字）と sub、右の箱（地は背景色）に right を置く。戻り値は (svg, [各層の y, ...])。"""
    out = []
    ys = []
    for i, (fill, stroke, hf, head, sub, right) in enumerate(rows):
        y = y0 + i * (h + gap)
        ys.append(y)
        out.append(box(lx, y, lw, h, fill, head, sub, 18, 14, stroke, 1, hf))
        out.append(box(rx, y, rw, h, BG, right, None, 15, 14, STROKE, 1, T1))
    return ''.join(out), ys


def up_axis(x, y_top, y_bottom, top_label, bottom_label):
    """右端の縦矢印（下から上）と、その上下のラベル。"""
    return (arrow(x, y_bottom, x, y_top)
            + text(x, y_top - 12, top_label, 14, 700, HUM_TEXT)
            + text(x, y_bottom + 20, bottom_label, 14, 700, PRI_TEXT))


# =====================================================================
# §1 4つの観点と主な手段
# =====================================================================
def fig_01_four_viewpoints():
    body = [title('4つの観点は積み上がり、上の観点ほど人の判断が要る')]
    rows = [
        (HUMAN, HUM_LINE, HUM_TEXT, '業務の遂行可能性', '支援技術を使った業務フローの完遂', 'シナリオテスト・利用者評価'),
        (NEUTRAL, STROKE, T1, '操作可能性', 'キーボード・フォーカス・入力操作', 'ブラウザテスト・手動操作'),
        (NEUTRAL, STROKE, T1, '情報の認識可能性', 'コントラスト・拡大表示・読み上げ', '自動テスト・目視確認'),
        (PRIMARY, LINE, PRI_TEXT, '実装の妥当性', 'HTML・ARIA・アクセシブルネーム', '静的解析・自動テスト'),
    ]
    s, ys = stack(92, rows)
    body.append(s)
    body.append(text(255, 84, '観点', 14, 700, MUTED))
    body.append(text(635, 84, '主な手段', 14, 700, MUTED))
    body.append(up_axis(880, 112, 332, '人の判断', '機械で確認'))
    body.append(note(384, '実装が妥当でなければ情報は伝わらず、情報が伝わらなければ操作も業務も成立しない'))
    return svg(1000, 412, '4つの観点と主な手段', body,
               desc='上から「業務の遂行可能性（支援技術を使った業務フローの完遂）：シナリオテスト・利用者評価」「操作可能性（キーボード・フォーカス・入力操作）：ブラウザテスト・手動操作」「情報の認識可能性（コントラスト・拡大表示・読み上げ）：自動テスト・目視確認」「実装の妥当性（HTML・ARIA・アクセシブルネーム）：静的解析・自動テスト」の4層を積み、右端の下から上への矢印に「機械で確認」から「人の判断」へと記した図')


# =====================================================================
# §2 検証の単位とテストレベル
# =====================================================================
def fig_02_units_and_levels():
    body = [title('確認の単位ごとに主たる工程を決め、すべてをSTに回さない')]
    ch, cols = levels(96)
    body.append(ch)
    pw = cols[0][1]
    body.append(box(cols[0][0], 170, pw, 70, PRIMARY, 'コンポーネント単位', 'Role・名称・操作・配色', 17, 14, LINE, 1, PRI_TEXT))
    body.append(box(cols[1][0], 170, pw, 70, PRIMARY, '画面単位', '構造・フォーカス・通知', 17, 14, LINE, 1, PRI_TEXT))
    body.append(lines(cols[2][0] + pw / 2, 202, ['実APIに依存する', '操作だけ'], 14, 400, MUTED, lh=20))
    body.append(box(cols[3][0], 170, pw, 70, HUMAN, '業務シナリオ単位', '支援技術で業務を完遂', 17, 14, HUM_LINE, 1, HUM_TEXT))
    body.append(bracket(cols[0][0], cols[1][0] + pw, 262, 'PG・UT工程（Backendの完成を待たない）', POS_TEXT, 15, 700, up=False))
    body.append(note(344, 'Backendが要るのは、実APIに依存する操作と、業務シナリオの完遂だけ'))
    return svg(1000, 372, '検証の単位とテストレベル', body,
               desc='FE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階を左から右へ1本の矢印でつなぎ、FE単体の列に「コンポーネント単位（Role・名称・操作・配色）」、FE内部結合の列に「画面単位（構造・フォーカス・通知）」、FE・BE結合の列に「実APIに依存する操作だけ」、STの列に「業務シナリオ単位（支援技術で業務を完遂）」を置き、左2列をブラケットで括って「PG・UT工程（Backendの完成を待たない）」とした図')


# =====================================================================
# §4 手段と自動化の度合い
# =====================================================================
def fig_04_means_gradient():
    body = [title('左の手段ほど機械で確認でき、右に進むほど人の判断が要る')]
    xs = [60, 290, 520, 750]
    w, y, h = 210, 96, 150
    body.append(card(xs[0], y, w, h, PRIMARY, '◎ 自動化に適する', ['静的コード解析', 'DOM解析', 'コンポーネントテスト', 'ブラウザ操作テスト'], hs=17, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=22))
    body.append(card(xs[1], y, w, h, NEUTRAL, '○ 部分的に自動化', ['視覚的検証', '拡大表示・配色・リフロー'], hs=17, rs=14, top=28, lh=22))
    body.append(card(xs[2], y, w, h, HUMAN, '△ 原則手動', ['支援技術による検証', 'スクリーンリーダー', '音声操作'], hs=17, rs=14, stroke=HUM_LINE, head_fill=HUM_TEXT, top=28, lh=22))
    body.append(card(xs[3], y, w, h, HUMAN, '― 人による評価', ['ユーザビリティ評価', '理解・操作・業務遂行'], hs=17, rs=14, stroke=HUM_LINE, head_fill=HUM_TEXT, top=28, lh=22))
    body.append(text(500, 282, '確認の対象が、実際の利用に近づく', 14, 700, T2))
    body.append(arrow(60, 296, 960, 296))
    for x, s in zip(xs, ['ソース・DOM・ブラウザ', '見た目', '支援技術', '利用者']):
        body.append(text(x + w / 2, 322, s, 14, 400, T1))
    body.append(note(364, 'ツールだけでは適合を判断できず、人による評価が必要（W3C）'))
    return svg(1000, 392, '手段と自動化の度合い', body,
               desc='4枚のカードを左から「◎ 自動化に適する（静的コード解析、DOM解析、コンポーネントテスト、ブラウザ操作テスト）」「○ 部分的に自動化（視覚的検証：拡大表示・配色・リフロー）」「△ 原則手動（支援技術による検証：スクリーンリーダー、音声操作）」「― 人による評価（ユーザビリティ評価：理解・操作・業務遂行）」と並べ、下の左から右への矢印に「確認の対象が、実際の利用に近づく」と記し、対象を「ソース・DOM・ブラウザ」「見た目」「支援技術」「利用者」と添えた図')


# =====================================================================
# §5 axe-core と Playwright の責務
# =====================================================================
def fig_05_axe_vs_playwright():
    body = [title('axe-coreは一瞬の状態を検査し、Playwrightは操作と遷移を検証する')]
    body.append(rect(60, 90, 410, 230, NEUTRAL, STROKE, 1))
    body.append(text(265, 124, 'axe-core', 20, 700, PRI_TEXT))
    body.append(text(265, 148, 'ルール違反の検出', 15, 700, T1))
    body.append(box(90, 170, 350, 56, PRIMARY, 'ある瞬間に描画されたDOM', 'ラベル・ARIA・コントラストの違反を列挙', 15, 14, LINE, 1, PRI_TEXT))
    body.append(text(265, 268, '違反は見るが、操作の成立は見ない', 14, 700, ATT_TEXT))
    body.append(rect(530, 90, 410, 230, NEUTRAL, STROKE, 1))
    body.append(text(735, 124, 'Playwright', 20, 700, PRI_TEXT))
    body.append(text(735, 148, '操作と状態遷移の成立', 15, 700, T1))
    px = [548, 683, 818]
    for x, s in zip(px, ['開く前', '開いた直後', 'Tabの後']):
        body.append(pill(x, 176, 104, 40, s, PRIMARY, 14, 700, PRI_TEXT, LINE))
    body.append(arrow(652, 196, 683, 196))
    body.append(arrow(787, 196, 818, 196))
    body.append(text(667, 170, '操作', 14, 400, T2))
    body.append(text(802, 170, '操作', 14, 400, T2))
    body.append(text(735, 240, '各状態でフォーカスや表示を検証', 14, 400, T1))
    body.append(text(735, 268, '遷移は見るが、違反の網羅はしない', 14, 700, ATT_TEXT))
    body.append(bracket(60, 940, 336, '両方が要る。片方で他方を代替できない', T1, 15, 700, up=False))
    body.append(note(404, 'axe-coreの検査を操作テストの途中に組み込むと、状態ごとの違反も検出できる'))
    return svg(1000, 432, 'axe-coreとPlaywrightの責務', body,
               desc='左の枠「axe-core：ルール違反の検出」には「ある瞬間に描画されたDOM（ラベル・ARIA・コントラストの違反を列挙）」と「違反は見るが、操作の成立は見ない」、右の枠「Playwright：操作と状態遷移の成立」には「開く前」「開いた直後」「Tabの後」の3状態を操作の矢印でつなぎ「各状態でフォーカスや表示を検証」「遷移は見るが、違反の網羅はしない」を置き、2枠をブラケットで束ねて「両方が要る。片方で他方を代替できない」とした図')


# =====================================================================
# §6 工程ごとの主な確認対象
# =====================================================================
def fig_06_levels_and_targets():
    body = [title('アクセシビリティの確認対象の大半は、PG・UT工程に主戦場がある')]
    ch, cols = levels(96)
    body.append(ch)
    pw = cols[0][1]
    y, h = 160, 150
    body.append(card(cols[0][0], y, pw, h, PRIMARY, 'コンポーネント', ['HTML・ARIA属性', '名称・役割', '操作', 'コントラスト'], hs=17, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=20))
    body.append(card(cols[1][0], y, pw, h, PRIMARY, '画面', ['画面全体の構造', 'フォーカス順序', '画面遷移後のフォーカス', '拡大・リフロー', 'APIエラー時の通知'], hs=17, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=20))
    body.append(card(cols[2][0], y, pw, h, NEUTRAL, '実APIとの結合', ['認証画面の操作'], hs=17, rs=14, top=28, lh=20))
    body.append(card(cols[3][0], y, pw, h, HUMAN, '業務シナリオ', ['スクリーンリーダー操作', '業務シナリオの完遂'], hs=17, rs=14, stroke=HUM_LINE, head_fill=HUM_TEXT, top=28, lh=20))
    body.append(bracket(cols[0][0], cols[1][0] + pw, 332, '主戦場：PG・UT工程', POS_TEXT, 15, 700, up=False))
    body.append(note(410, 'Backendの完成を待たずに検証できる不具合が大半を占める'))
    return svg(1000, 438, '工程ごとの主な確認対象', body,
               desc='FE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階の下に、それぞれ「コンポーネント（HTML・ARIA属性、名称・役割、操作、コントラスト）」「画面（画面全体の構造、フォーカス順序、画面遷移後のフォーカス、拡大・リフロー、APIエラー時の通知）」「実APIとの結合（認証画面の操作）」「業務シナリオ（スクリーンリーダー操作、業務シナリオの完遂）」のカードを置き、左2列をブラケットで括って「主戦場：PG・UT工程」とした図')


# =====================================================================
# §7 3層で保証する品質
# =====================================================================
def fig_07_responsibility_layers():
    body = [title('共通コンポーネントで保証した品質は、画面ごとに再検証しない')]
    h = 86
    # システム（上）
    y = 96
    body.append(rect(60, y, 880, h, HUMAN, HUM_LINE, 1))
    body.append(text(80, y + 50, 'システム', 17, 700, HUM_TEXT, 'start'))
    body.append(pill(260, y + 12, 160, 30, '業務フロー', BG, 14, 700, T1))
    body.append(text(600, y + 70, '保証：支援技術を使用して業務を完遂できること', 14, 400, T1))
    # 個別画面（中）
    y = 196
    body.append(rect(60, y, 880, h, NEUTRAL, STROKE, 1))
    body.append(text(80, y + 50, '個別画面', 17, 700, T1, 'start'))
    for i, s in enumerate(['顧客検索', '顧客登録', '契約一覧', '契約詳細']):
        body.append(pill(260 + i * 150, y + 12, 140, 30, s, BG, 14, 700, T1))
    body.append(text(600, y + 70, '保証：文脈に応じたラベル・配置・画面遷移・エラー通知', 14, 400, T1))
    # デザインシステム（下）
    y = 296
    body.append(rect(60, y, 880, h, PRIMARY, LINE, 1))
    body.append(lines(80, y + 42, [('デザインシステム', 700, PRI_TEXT), ('検証済みを再利用', 700, POS_TEXT)], 15, anchor='start', lh=22))
    for i, s in enumerate(['Button', 'Input', 'Dialog', 'Select', 'Checkbox', 'Tabs']):
        body.append(pill(260 + i * 100, y + 12, 90, 30, s, BG, 14, 700, T1))
    body.append(text(600, y + 70, '保証：Role・ARIA・キー操作・フォーカス管理・基本配色', 14, 400, T1))
    body.append(note(422, '画面数が増えても、共通コンポーネントの回帰テストは増えない。組み合わせの問題だけを画面で確認する'))
    return svg(1000, 452, '3層で保証する品質', body,
               desc='上から「システム：業務フロー。保証：支援技術を使用して業務を完遂できること」「個別画面：顧客検索・顧客登録・契約一覧・契約詳細。保証：文脈に応じたラベル・配置・画面遷移・エラー通知」「デザインシステム（検証済みを再利用）：Button・Input・Dialog・Select・Checkbox・Tabs。保証：Role・ARIA・キー操作・フォーカス管理・基本配色」の3層を積んだ図')


# =====================================================================
# §8.2 入力コンポーネントの状態ごとの検査
# =====================================================================
def fig_08_component_states():
    body = [title('状態ごとにStoryを定義し、各状態をaxe-coreで検査する')]
    xs = [60, 290, 520, 750]
    w, y, h = 190, 96, 124
    states = [('Default', 'メールアドレス', 'user@example.com', T1, None),
              ('Required', 'メールアドレス *', '未入力', MUTED, None),
              ('Error', 'メールアドレス', 'abc', T1, '形式が正しくありません'),
              ('Disabled', 'メールアドレス', 'user@example.com', MUTED, None)]
    for x, (name, label, value, vcol, err) in zip(xs, states):
        body.append(rect(x, y, w, h, NEUTRAL, STROKE, 1))
        body.append(text(x + w / 2, y + 24, name, 15, 700, T1))
        body.append(text(x + 15, y + 48, label, 14, 400, T1, 'start'))
        body.append(rect(x + 15, y + 56, 160, 30, WATER if name == 'Disabled' else BG, ATT_LINE if err else STROKE, 1, rx=6))
        body.append(text(x + 23, y + 76, value, 14, 400, vcol, 'start'))
        if err:
            body.append(text(x + 15, y + 108, err, 14, 400, ATT_TEXT, 'start'))
        body.append(arrow(x + w / 2, y + h, x + w / 2, 254))
    body.append(box(60, 254, 880, 56, PRIMARY, 'axe-coreによる各Storyの検査', 'ラベルの関連付け・ARIA属性・コントラスト', 16, 14, LINE, 1, PRI_TEXT))
    body.append(note(350, 'Loading・モーダル表示なども、状態として定義しなければ検査されない'))
    return svg(1000, 378, '入力コンポーネントの状態ごとの検査', body,
               desc='入力コンポーネントの4つの状態「Default（user@example.com）」「Required（必須の印付きで未入力）」「Error（abc、形式が正しくありません）」「Disabled（非活性）」を小さな枠で並べ、それぞれから下の「axe-coreによる各Storyの検査（ラベルの関連付け・ARIA属性・コントラスト）」へ矢印を引いた図')


# =====================================================================
# §8.5 ダイアログのフォーカス移動
# =====================================================================
def fig_09_dialog_focus_flow():
    body = [title('開いたら最初の項目へフォーカスが移り、閉じたら元のボタンへ戻る')]
    body.append(pill(60, 150, 140, 44, '編集ボタン', NEUTRAL, 15, 700, T1))
    body.append(rect(280, 96, 440, 180, BG, LINE, 1))
    body.append(text(500, 124, 'ダイアログ', 16, 700, T1))
    body.append(pill(310, 150, 160, 44, '顧客名', PRIMARY, 15, 700, PRI_TEXT, LINE))
    body.append(pill(530, 150, 170, 44, 'メールアドレス', NEUTRAL, 15, 700, T1))
    body.append(arrow(200, 172, 310, 172))
    body.append(text(255, 160, '① 開く', 14, 700, T2))
    body.append(arrow(470, 172, 530, 172))
    body.append(text(500, 160, '② Tab', 14, 700, T2))
    body.append(text(390, 222, '開いた直後のフォーカス', 14, 400, PRI_TEXT))
    body.append(text(615, 222, 'Tabで次の項目へ', 14, 400, T2))
    body.append(path_arrow('M500 276 V312 H130 V206', (130, 200, 0, -1), dashed=True))
    body.append(text(315, 336, '③ Escapeで閉じると、フォーカスは開く前のボタンに戻る', 14, 700, T2))
    body.append(note(382, 'フォーカスが消えると、キーボード利用者は現在位置を見失う。axe-coreだけでは検証できない'))
    return svg(1000, 410, 'ダイアログのフォーカス移動', body,
               desc='左の「編集ボタン」から「① 開く」の矢印でダイアログ内の「顧客名」（開いた直後のフォーカス）へ、「② Tab」の矢印で「メールアドレス」へ進み、ダイアログの下から破線の矢印で「③ Escapeで閉じると、フォーカスは開く前のボタンに戻る」と編集ボタンへ戻る図')


# =====================================================================
# §10 実行タイミングと品質ゲート
# =====================================================================
def fig_10_ci_pipeline():
    body = [title('自動テストはコミットからビルド後まで段階的に走り、リリース前は人が確認する')]
    ch, cols = chain(60, 96, ['コミット時', 'PR／MR時', 'ビルド後', 'リリース前'], total_w=880,
                     fills={3: HUMAN}, colors={3: HUM_TEXT}, strokes={3: HUM_LINE})
    body.append(ch)
    pw = cols[0][1]
    y, h = 160, 120
    body.append(card(cols[0][0], y, pw, h, PRIMARY, 'ESLint（jsx-a11y）', ['静的な実装ルール違反', 'ゲート：Lintエラー0件'], hs=16, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=22))
    body.append(card(cols[1][0], y, pw, h, PRIMARY, 'Vitest・Storybook', ['axe-core', 'コンポーネントの状態・操作', 'ゲート：自動検査違反0件'], hs=16, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=22))
    body.append(card(cols[2][0], y, pw, h, PRIMARY, 'Playwright', ['axe-core・MSW', '画面構造・キー操作・遷移', 'ゲート：違反0件・成功'], hs=16, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=22))
    body.append(card(cols[3][0], y, pw, h, HUMAN, 'NVDA・VoiceOver', ['手動評価', '主要業務を支援技術で検証', 'ゲート：適合評価完了'], hs=16, rs=14, stroke=HUM_LINE, head_fill=HUM_TEXT, top=28, lh=22))
    body.append(bracket(cols[0][0], cols[2][0] + pw, 302, '自動テスト：毎回実行できる', POS_TEXT, 15, 700, up=False))
    body.append(bracket(cols[3][0], cols[3][0] + pw, 302, '人・支援技術', HUM_TEXT, 15, 700, up=False))
    body.append(note(378, '既存システムでは、既知の違反を管理し、新規違反を増やさない回帰防止方式から始める'))
    return svg(1000, 406, '実行タイミングと品質ゲート', body,
               desc='コミット時、PR／MR時、ビルド後、リリース前の4つのタイミングを左から右へ1本の矢印でつなぎ、それぞれ「ESLint（jsx-a11y）：静的な実装ルール違反、ゲートはLintエラー0件」「Vitest・Storybook：axe-core、コンポーネントの状態・操作、ゲートは自動検査違反0件」「Playwright：axe-core・MSW、画面構造・キー操作・遷移、ゲートは違反0件・成功」「NVDA・VoiceOver：手動評価、主要業務を支援技術で検証、ゲートは適合評価完了」のカードを置き、左3列を「自動テスト：毎回実行できる」、右1列を「人・支援技術」のブラケットで括った図')


# =====================================================================
# §12 4層の標準化
# =====================================================================
def fig_11_four_layers():
    body = [title('アクセシビリティテストは、自動化できる3層と人の1層で標準化する')]
    rows = [
        (HUMAN, HUM_LINE, HUM_TEXT, '人・支援技術', '観点：業務の遂行可能性', '情報を理解し、実際に業務を遂行できる'),
        (PRIMARY, LINE, PRI_TEXT, 'Playwright', '観点：操作可能性', '期待する操作・状態遷移が成立する'),
        (PRIMARY, LINE, PRI_TEXT, 'axe-core', '観点：情報の認識可能性', '描画されたUIに機械検出可能な違反がない'),
        (PRIMARY, LINE, PRI_TEXT, '静的解析', '観点：実装の妥当性', '実装ルールに違反していない'),
    ]
    s, ys = stack(92, rows)
    body.append(s)
    body.append(text(255, 84, '層', 14, 700, MUTED))
    body.append(text(635, 84, '保証する品質', 14, 700, MUTED))
    body.append(up_axis(880, 112, 332, '機会は限られる', '何度でも実行'))
    body.append(note(384, '4層は§1の4つの観点に対応する。下の3層は開発中に繰り返し実行し、最上層は人がリリース前に確認する'))
    return svg(1000, 412, '4層の標準化', body,
               desc='上から「人・支援技術（観点：業務の遂行可能性）：情報を理解し、実際に業務を遂行できる」「Playwright（観点：操作可能性）：期待する操作・状態遷移が成立する」「axe-core（観点：情報の認識可能性）：描画されたUIに機械検出可能な違反がない」「静的解析（観点：実装の妥当性）：実装ルールに違反していない」の4層を積み、右端の下から上への矢印に「何度でも実行」から「機会は限られる」へと記した図')


# =====================================================================
# 図の一覧（ファイル名 → 生成関数）。章番号で始める。
# =====================================================================
FIGURES = {
    '01-four-viewpoints': fig_01_four_viewpoints,
    '02-units-and-levels': fig_02_units_and_levels,
    '04-means-gradient': fig_04_means_gradient,
    '05-axe-vs-playwright': fig_05_axe_vs_playwright,
    '06-levels-and-targets': fig_06_levels_and_targets,
    '07-responsibility-layers': fig_07_responsibility_layers,
    '08-component-states': fig_08_component_states,
    '09-dialog-focus-flow': fig_09_dialog_focus_flow,
    '10-ci-pipeline': fig_10_ci_pipeline,
    '11-four-layers': fig_11_four_layers,
}


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, fn in FIGURES.items():
        (ASSETS / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('wrote', name)


if __name__ == '__main__':
    main()
