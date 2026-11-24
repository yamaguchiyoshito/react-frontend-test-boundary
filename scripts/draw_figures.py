#!/usr/bin/env python3
"""記事「React／Frontendにおける単体テストと結合テストの境界」の図版を決定論的に生成する。

体裁：幅1000px、最小フォント14px、注記16px、Python標準ライブラリのみ。
配色は役割で固定する（claudedocs/publication-plan.md §4.1）。
  NEUTRAL   画面・コンポーネント・Hook など構成要素の箱、区別を付けない要素
  PRIMARY   FE単体テスト＝個別の責務（1つの箱の中を検証する範囲）
  LINK      FE内部結合テスト＝責務間の連携（箱と箱をつなぐ線を検証する範囲。Mock API を含む）
  POSITIVE  Backend の完成を待たずに検証できる範囲（PG・UT 工程に入るもの）
  ATTENTION 実 Backend がないと検証できない事項、IT 工程へ持ち越される事項（1図に1系統）
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
LINK = '#e9e4f5'; LINK_LINE = '#8a6cc1'; LINK_TEXT = '#6a4ea6'
POSITIVE = '#e0f0e9'; POS_LINE = '#5aa06f'; POS_TEXT = '#2f6b45'
ATTENTION = '#f7e9d4'; ATT_LINE = '#c0604a'; ATT_TEXT = '#9c3f2a'

PALETTE = {BG, INK, T1, T2, MUTED, LINE, STROKE, NEUTRAL, WATER,
           PRIMARY, PRI_TEXT, LINK, LINK_LINE, LINK_TEXT, POSITIVE, POS_LINE, POS_TEXT, ATTENTION, ATT_LINE, ATT_TEXT}
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


def box(x, y, w, h, fill, head, sub=None, hs=20, ss=15, stroke=STROKE, sw=1, head_fill=T1, dashed=False):
    out = [rect(x, y, w, h, fill, stroke, sw, dashed=dashed)]
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


def link(x1, y1, x2, y2, color=LINK_LINE, width=3, dashed=False):
    """箱と箱のつながり（矢頭のない線）。"""
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{width}" fill="none"{dash}/>'


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
# 共通部品：テストレベルの鎖（01・03・05・06 で使う）
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
LEVEL_STYLE = dict(fills={0: PRIMARY, 1: LINK}, colors={0: PRI_TEXT, 1: LINK_TEXT}, strokes={0: LINE, 1: LINK_LINE})


def levels(y, styled=True, x0=60, total_w=880):
    """4段階のテストレベルを横一列のピルで描く。styled=True なら FE単体を PRIMARY、FE内部結合を LINK で塗る。
    戻り値は chain() と同じ (svg, [(x, w), ...])。"""
    style = LEVEL_STYLE if styled else {}
    return chain(x0, y, LEVELS, total_w=total_w, **style)


def up_axis(x, y_top, y_bottom, top_label, bottom_label, top_color=ATT_TEXT, bottom_color=PRI_TEXT):
    """右端の縦矢印（下から上）と、その上下のラベル。"""
    return (arrow(x, y_bottom, x, y_top)
            + text(x, y_top - 12, top_label, 14, 700, top_color)
            + text(x, y_bottom + 20, bottom_label, 14, 700, bottom_color))


# =====================================================================
# §1 4段階のテストレベルとAPI接続
# =====================================================================
def fig_01_four_levels():
    body = [title('単体と結合の間にFE内部結合を置き、Backendの完成を待たずに進める')]
    ch, cols = levels(96)
    body.append(ch)
    pw = cols[0][1]
    y, h = 160, 70
    body.append(box(cols[0][0], y, pw, h, PRIMARY, '個別の責務', 'API接続：なし／Mock', 17, 14, LINE, 1, PRI_TEXT))
    body.append(box(cols[1][0], y, pw, h, LINK, '責務間の連携', 'API接続：原則Mock', 17, 14, LINK_LINE, 1, LINK_TEXT))
    body.append(box(cols[2][0], y, pw, h, ATTENTION, '実APIとの連携', 'API接続：実API', 17, 14, ATT_LINE, 1, ATT_TEXT))
    body.append(box(cols[3][0], y, pw, h, ATTENTION, '業務シナリオ', 'API接続：実API＋外部接続', 17, 14, ATT_LINE, 1, ATT_TEXT))
    body.append(bracket(cols[0][0], cols[1][0] + pw, 252, 'Backendの完成を待たずに実施できる', POS_TEXT, 15, 700, up=False))
    body.append(bracket(cols[2][0], cols[3][0] + pw, 252, '実Backendが要る', ATT_TEXT, 15, 700, up=False))
    body.append(note(330, '区分を決めるのは、テスト対象の大きさや使う道具ではなく、依存先との接続範囲'))
    return svg(1000, 358, '4段階のテストレベルとAPI接続', body,
               desc='FE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階を左から右へ1本の矢印でつなぎ、それぞれの下に「個別の責務（API接続：なし／Mock）」「責務間の連携（API接続：原則Mock）」「実APIとの連携（API接続：実API）」「業務シナリオ（API接続：実API＋外部接続）」を置き、左2列を「Backendの完成を待たずに実施できる」、右2列を「実Backendが要る」のブラケットで括った図')


# =====================================================================
# §2 顧客検索画面の構成と検証の範囲
# =====================================================================
def fig_02_search_page_structure():
    body = [title('箱の中は単体、箱と箱の間はFE内部結合、Backendとの線はFE・BE結合')]
    # 画面の枠
    body.append(rect(60, 90, 580, 250, NEUTRAL, STROKE, 1))
    body.append(text(80, 114, 'CustomerSearchPage（顧客検索画面）', 15, 700, T1, 'start'))
    # つながり（箱の下に描く）
    body.append(link(211, 210, 350, 250))          # SearchForm → Hook
    body.append(link(489, 210, 350, 250))          # CustomerTable → Hook
    body.append(link(435, 285, 450, 285))          # Hook → API Client
    body.append(link(250, 285, 265, 285))          # Schema → Hook
    body.append(link(535, 320, 535, 366, ATT_LINE))  # API Client → Backend
    # 上段：表示とフォーム
    body.append(box(80, 126, 262, 84, PRIMARY, 'SearchForm', '検索フォーム：顧客名・区分', 17, 14, LINE, 1, PRI_TEXT))
    body.append(box(358, 126, 262, 84, PRIMARY, 'CustomerTable', '検索結果：一覧・件数', 17, 14, LINE, 1, PRI_TEXT))
    # 下段：処理
    body.append(box(80, 250, 170, 70, PRIMARY, 'Schema・変換関数', 'バリデーション・変換', 15, 14, LINE, 1, PRI_TEXT))
    body.append(box(265, 250, 170, 70, PRIMARY, 'カスタムHook', 'useCustomerSearch', 15, 14, LINE, 1, PRI_TEXT))
    body.append(box(450, 250, 170, 70, PRIMARY, 'API Client', 'リクエスト・応答処理', 15, 14, LINE, 1, PRI_TEXT))
    # Backend
    body.append(box(80, 366, 540, 50, ATTENTION, 'Backend API／Database', None, 16, 14, ATT_LINE, 1, ATT_TEXT, dashed=True))
    # 右：範囲の凡例
    body.append(card(680, 96, 260, 72, PRIMARY, '単体テスト', ['箱の中：個別の責務'], hs=16, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=22))
    body.append(card(680, 186, 260, 72, LINK, 'FE内部結合テスト', ['箱と箱の間：責務間の連携'], hs=16, rs=14, stroke=LINK_LINE, head_fill=LINK_TEXT, top=28, lh=22))
    body.append(card(680, 276, 260, 72, ATTENTION, 'FE・BE結合テスト', ['Backendとの線：実API'], hs=16, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=22))
    body.append(note(456, 'どの箱を見るかではなく、箱の中か、箱の間か、Backendとの線かで区分が決まる'))
    return svg(1000, 484, '顧客検索画面の構成と検証の範囲', body,
               desc='CustomerSearchPage（顧客検索画面）の枠の中に、上段「SearchForm（検索フォーム：顧客名・区分）」「CustomerTable（検索結果：一覧・件数）」、下段「Schema・変換関数（バリデーション・変換）」「カスタムHook（useCustomerSearch）」「API Client（リクエスト・応答処理）」の箱を置き、箱同士を紫の線で、API Clientと枠外の「Backend API／Database」を橙の線で結び、右に「単体テスト：箱の中（個別の責務）」「FE内部結合テスト：箱と箱の間（責務間の連携）」「FE・BE結合テスト：Backendとの線（実API）」の凡例を置いた図')


# =====================================================================
# §3 テストレベルと実行環境の2軸
# =====================================================================
def fig_03_env_vs_level():
    body = [title('実行環境はテストレベルを決めない。どちらも別々に選ぶ')]
    ch, cols = levels(96, x0=220, total_w=720)
    body.append(ch)
    body.append(lines(135, 112, ['横：テストレベル', '縦：実行環境'], 14, 400, MUTED, lh=18))
    envs = [('Node.js', 'Vitest'), ('仮想DOM', 'jsdom等'), ('実ブラウザ', 'Browser Mode等'), ('実システム環境', 'Playwright等')]
    ys = [150, 218, 286, 354]
    pw = cols[0][1]
    for y, (head, sub) in zip(ys, envs):
        body.append(box(60, y, 150, 60, NEUTRAL, head, sub, 15, 14))
        for x, _ in cols:
            body.append(rect(x, y, pw, 60, BG, STROKE, 1, rx=6))
    # 例：環境が同じでもレベルは違う／レベルが同じでも環境は違う
    body.append(rect(cols[0][0], ys[2], pw, 60, PRIMARY, LINE, 1, rx=6))
    body.append(lines(cols[0][0] + pw / 2, ys[2] + 26, ['Playwrightで', 'コンポーネントだけ'], 14, 700, PRI_TEXT, lh=18))
    body.append(rect(cols[1][0], ys[1], pw, 60, LINK, LINK_LINE, 1, rx=6))
    body.append(lines(cols[1][0] + pw / 2, ys[1] + 26, ['Vitest＋jsdomで', '画面全体の連携'], 14, 700, LINK_TEXT, lh=18))
    # ほかの典型的な置き場所
    body.append(text(cols[0][0] + pw / 2, ys[0] + 35, 'ロジック・Store', 14, 400, T2))
    body.append(text(cols[0][0] + pw / 2, ys[1] + 35, 'コンポーネント', 14, 400, T2))
    body.append(text(cols[1][0] + pw / 2, ys[2] + 35, '画面遷移', 14, 400, T2))
    body.append(text(cols[2][0] + pw / 2, ys[3] + 35, '実APIとの結合', 14, 400, T2))
    body.append(text(cols[3][0] + pw / 2, ys[3] + 35, '業務シナリオ', 14, 400, T2))
    body.append(note(450, '実ブラウザを使っても対象がコンポーネントだけなら単体。Vitestでも連携を見れば内部結合'))
    return svg(1000, 478, 'テストレベルと実行環境の2軸', body,
               desc='横にFE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階、縦にNode.js（Vitest）、仮想DOM（jsdom等）、実ブラウザ（Browser Mode等）、実システム環境（Playwright等）の4つの実行環境を置いた格子の図。FE単体×実ブラウザに「Playwrightでコンポーネントだけ」、FE内部結合×仮想DOMに「Vitest＋jsdomで画面全体の連携」を強調して置き、ほかにFE単体×Node.jsに「ロジック・Store」、FE単体×仮想DOMに「コンポーネント」、FE内部結合×実ブラウザに「画面遷移」、FE・BE結合×実システム環境に「実APIとの結合」、ST×実システム環境に「業務シナリオ」を置いている')


# =====================================================================
# §4 8種別が検証する範囲
# =====================================================================
def fig_04_unit_test_types():
    body = [title('8種別は、純粋な処理から通信までを個別に検証し、品質は横断で見る')]
    xs = [60, 285, 510, 735]
    w, y, h = 205, 96, 118
    cards = [
        ('純粋な処理', ['① ロジックテスト', '② バリデーションテスト', ('対象：関数・Schema', 400, T2)]),
        ('状態', ['③ Hooksテスト', '④ 状態管理テスト', ('対象：Hook・Store', 400, T2)]),
        ('コンポーネント', ['⑤ 表示テスト', '⑥ 操作テスト', ('対象：Props・イベント', 400, T2)]),
        ('通信', ['⑦ APIクライアントテスト', ('対象：リクエスト・応答', 400, T2)]),
    ]
    for x, (head, rows) in zip(xs, cards):
        body.append(card(x, y, w, h, PRIMARY, head, rows, hs=16, rs=14, stroke=LINE, head_fill=PRI_TEXT, row_fill=T1, top=28, lh=22))
    body.append(box(60, 236, 880, 50, NEUTRAL, '⑧ コンポーネント品質テスト', '視覚的品質・アクセシビリティ・レスポンシブ・キーボード操作・オーバーフロー（種別を横断して見る）', 16, 14))
    body.append(arrow(60, 312, 940, 312))
    body.append(text(xs[0] + w / 2, 338, 'UIから離れた処理：最も速く安定', 14, 400, T1))
    body.append(text(xs[2] + w / 2, 338, 'UIに近い', 14, 400, T1))
    body.append(text(xs[3] + w / 2, 338, '外部との境界', 14, 400, T1))
    body.append(note(380, 'いずれも単体テストの範囲。⑧はレベルとは別の分類軸だが、コンポーネント単位で行えるものは単体工程に含める'))
    return svg(1000, 408, '8種別が検証する範囲', body,
               desc='左から「純粋な処理：① ロジックテスト、② バリデーションテスト（対象：関数・Schema）」「状態：③ Hooksテスト、④ 状態管理テスト（対象：Hook・Store）」「コンポーネント：⑤ 表示テスト、⑥ 操作テスト（対象：Props・イベント）」「通信：⑦ APIクライアントテスト（対象：リクエスト・応答）」の4枚のカードを並べ、その下に全幅の帯「⑧ コンポーネント品質テスト（視覚的品質・アクセシビリティ・レスポンシブ・キーボード操作・オーバーフロー。種別を横断して見る）」を置き、左から右への矢印に「UIから離れた処理：最も速く安定」「UIに近い」「外部との境界」と添えた図')


# =====================================================================
# §4.5 コンポーネントの4つの表示状態
# =====================================================================
def fig_04b_component_states():
    body = [title('表示状態ごとにStoryを定義し、デザイン確認とテストで共有する')]
    xs = [60, 290, 520, 750]
    w, y, h = 190, 96, 124
    names = ['正常', 'Loading', 'Empty', 'Error']
    for x, name in zip(xs, names):
        body.append(rect(x, y, w, h, NEUTRAL, STROKE, 1))
        body.append(text(x + w / 2, y + 24, name, 15, 700, T1))
        if name == '正常':
            for i, row in enumerate(['C001 山田 太郎', 'C002 山田 花子', 'C003 山田商事']):
                ry = y + 40 + i * 24
                body.append(rect(x + 15, ry, 160, 22, WATER, STROKE, 1, rx=4))
                body.append(text(x + 23, ry + 17, row, 14, 400, T1, 'start'))
        elif name == 'Loading':
            body.append(text(x + w / 2, y + 80, '読み込み中…', 14, 400, MUTED))
        elif name == 'Empty':
            body.append(lines(x + w / 2, y + 72, ['該当するデータが', 'ありません'], 14, 400, MUTED, lh=20))
        else:
            body.append(text(x + w / 2, y + 80, 'データ取得に失敗しました', 14, 400, ATT_TEXT))
        body.append(arrow(x + w / 2, y + h, x + w / 2, 254))
    body.append(box(60, 254, 880, 56, PRIMARY, 'Storyとして定義し、表示テストの入力にする', 'デザイン確認とテスト資産を共通化する', 16, 14, LINE, 1, PRI_TEXT))
    body.append(note(350, 'Loading・Empty・Errorは、状態として定義しなければ検証されない'))
    return svg(1000, 378, 'コンポーネントの4つの表示状態', body,
               desc='検索結果テーブルの4つの表示状態「正常（C001 山田 太郎、C002 山田 花子、C003 山田商事の3行）」「Loading（読み込み中…）」「Empty（該当するデータがありません）」「Error（データ取得に失敗しました）」を小さな枠で並べ、それぞれから下の「Storyとして定義し、表示テストの入力にする（デザイン確認とテスト資産を共通化する）」へ矢印を引いた図')


# =====================================================================
# §5 種別ごとの主たる検証工程
# =====================================================================
def fig_05_main_level_per_type():
    body = [title('各種別は、最も低コストで確実に検証できる工程を主たる工程にする')]
    ch, cols = levels(96)
    body.append(ch)
    pw = cols[0][1]
    y, h = 160, 170
    body.append(card(cols[0][0], y, pw, h, PRIMARY, '個別の責務', ['ロジック', 'バリデーション', 'Hooks・状態管理', 'UI表示・UI操作', 'VRT・a11y・レスポンシブ'], hs=17, rs=14, stroke=LINE, head_fill=PRI_TEXT, top=28, lh=20))
    body.append(card(cols[1][0], y, pw, h, LINK, '責務間の連携', ['状態管理の連携', '画面遷移', 'API通信（Mock）', 'UI表示・操作の連携'], hs=17, rs=14, stroke=LINK_LINE, head_fill=LINK_TEXT, top=28, lh=20))
    body.append(card(cols[2][0], y, pw, h, ATTENTION, '実APIとの連携', ['API通信（実API）', '認証認可', 'データ永続化'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(card(cols[3][0], y, pw, h, ATTENTION, '業務シナリオ', ['業務シナリオ', 'システム全体の要求充足'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(bracket(cols[0][0], cols[1][0] + pw, 352, '主たる工程の大半はPG・UT', POS_TEXT, 15, 700, up=False))
    body.append(note(430, '同じ観点をすべての工程で繰り返さず、主たる工程を1つ決め、ほかの工程は補完にとどめる'))
    return svg(1000, 458, '種別ごとの主たる検証工程', body,
               desc='FE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階の下に、それぞれ「個別の責務（ロジック、バリデーション、Hooks・状態管理、UI表示・UI操作、VRT・a11y・レスポンシブ）」「責務間の連携（状態管理の連携、画面遷移、API通信（Mock）、UI表示・操作の連携）」「実APIとの連携（API通信（実API）、認証認可、データ永続化）」「業務シナリオ（業務シナリオ、システム全体の要求充足）」のカードを置き、左2列をブラケットで括って「主たる工程の大半はPG・UT」とした図')


# =====================================================================
# §6 テストレベルと開発工程の対応
# =====================================================================
def fig_06_process_mapping():
    body = [title('FE内部結合は技法上は結合テスト、管理上はPG・UT工程に含める')]
    ch, cols = levels(120)
    pw = cols[0][1]
    body.append(bracket(cols[0][0], cols[1][0] + pw, 112, 'PG・UT工程', POS_TEXT, 15, 700, up=True))
    body.append(bracket(cols[2][0], cols[2][0] + pw, 112, 'IT工程', T1, 15, 700, up=True))
    body.append(bracket(cols[3][0], cols[3][0] + pw, 112, 'ST工程', T1, 15, 700, up=True))
    body.append(ch)
    y, h = 184, 96
    body.append(card(cols[0][0], y, cols[1][0] + pw - cols[0][0], h, POSITIVE, '完了条件',
                     ['Backendに依存せず、Frontendの機能要求を満たしている', 'FE内部結合テストは技法上は結合テストでも、この工程に含める'],
                     hs=15, rs=14, stroke=POS_LINE, head_fill=POS_TEXT, top=30, lh=22))
    body.append(card(cols[2][0], y, pw, h, NEUTRAL, '完了条件', ['実Backendとの連携を', '含めて機能要求を満たす'], hs=15, rs=14, top=30, lh=22))
    body.append(card(cols[3][0], y, pw, h, NEUTRAL, '完了条件', ['システム全体として', '業務・非機能要求を満たす'], hs=15, rs=14, top=30, lh=22))
    body.append(bracket(cols[0][0], cols[1][0] + pw, 300, 'Backendチームと並行して進められる', POS_TEXT, 15, 700, up=False))
    body.append(note(388, 'Frontendの工程完了を、Backendの完成に依存させずに判定できる'))
    return svg(1000, 416, 'テストレベルと開発工程の対応', body,
               desc='FE単体、FE内部結合、FE・BE結合、ST（システムテスト）の4段階の上に「PG・UT工程」（左2段）「IT工程」「ST工程」のブラケットを置き、下にそれぞれの完了条件「Backendに依存せず、Frontendの機能要求を満たしている（FE内部結合テストは、テスト技法上は結合テストでも、この工程に含める）」「実Backendとの連携を含めて機能要求を満たす」「システム全体として業務・非機能要求を満たす」のカードを置き、左2段を「Backendチームと並行して進められる」のブラケットで括った図')


# =====================================================================
# §7 概念上のテスト配分
# =====================================================================
def fig_07_test_architecture():
    body = [title('下の層ほど速く安定し、数が多い。上に行くほど実環境に近づく')]
    layers = [
        (200, ATTENTION, ATT_LINE, ATT_TEXT, 'E2E・ST', '業務シナリオ'),
        (340, ATTENTION, ATT_LINE, ATT_TEXT, 'FE・BE結合（実API）', 'Playwright'),
        (480, LINK, LINK_LINE, LINK_TEXT, 'FE内部結合（画面全体・画面遷移）', 'Testing Library＋MSW／Playwright＋MSW'),
        (620, PRIMARY, LINE, PRI_TEXT, 'コンポーネントの表示・操作', 'Testing Library・Storybook'),
        (760, PRIMARY, LINE, PRI_TEXT, 'ロジック・Schema・Hooks・Store', 'Vitest：最も多く、最も速い'),
    ]
    y0, h, gap = 96, 52, 6
    for i, (w, fill, stroke, tcol, head, sub) in enumerate(layers):
        y = y0 + i * (h + gap)
        body.append(box(500 - w / 2, y, w, h, fill, head, sub, 15, 14, stroke, 1, tcol))
    body.append(up_axis(950, 110, 376, '実環境', '速い・多い'))
    body.append(note(420, '概念上の配分であり、テストケース数の固定比率ではない'))
    return svg(1000, 448, '概念上のテスト配分', body,
               desc='上から「E2E・ST（業務シナリオ）」「FE・BE結合（実API）：Playwright」「FE内部結合（画面全体・画面遷移）：Testing Library＋MSW／Playwright＋MSW」「コンポーネントの表示・操作：Testing Library・Storybook」「ロジック・Schema・Hooks・Store：Vitest（最も多く、最も速い）」の5層を、下ほど幅が広い段々のピラミッドとして積み、右端の下から上への矢印に「速い・多い」から「実環境」へと記した図')


# =====================================================================
# 図の一覧（ファイル名 → 生成関数）。章番号で始める。
# =====================================================================
FIGURES = {
    '01-four-levels': fig_01_four_levels,
    '02-search-page-structure': fig_02_search_page_structure,
    '03-env-vs-level': fig_03_env_vs_level,
    '04-unit-test-types': fig_04_unit_test_types,
    '04b-component-states': fig_04b_component_states,
    '05-main-level-per-type': fig_05_main_level_per_type,
    '06-process-mapping': fig_06_process_mapping,
    '07-test-architecture': fig_07_test_architecture,
}


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, fn in FIGURES.items():
        (ASSETS / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('wrote', name)


if __name__ == '__main__':
    main()
