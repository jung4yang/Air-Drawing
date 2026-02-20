# ─────────────────────────────────────────
# ui.py  –  상단 UI 바 렌더링
# ─────────────────────────────────────────

import cv2
from config import COLORS, COLOR_ORDER, UI_BAR_HEIGHT

FONT       = cv2.FONT_HERSHEY_SIMPLEX
BTN_W      = 120
BTN_MARGIN = 10
BTN_PAD    = 5


def draw_ui(frame, state: str, canvas):
    """
    상단 UI 바를 frame 위에 직접 그린다.
    canvas 에서 color_name, line_size, eraser_r 를 읽는다.
    """
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, UI_BAR_HEIGHT), (30, 30, 30), -1)

    x = BTN_MARGIN

    # ── IDLE 버튼 ────────────────────────────
    col = (0, 200, 0) if state == "IDLE" else (80, 80, 80)
    _draw_button(frame, x, "IDLE", (255, 255, 255), col)
    x += BTN_W + BTN_MARGIN

    # ── 색상 버튼 ────────────────────────────
    for name in COLOR_ORDER:
        bgr    = COLORS[name]
        active = (state == "DRAWING" and canvas.color_name == name)
        border = (0, 255, 255) if active else (60, 60, 60)
        _draw_button(frame, x, name, (255, 255, 255), bgr, border)
        x += BTN_W + BTN_MARGIN

    # ── LINE SIZE ────────────────────────────
    cv2.putText(frame, f"LINE: {canvas.line_size}",
                (x, 33), FONT, 0.6, (200, 200, 200), 2)
    x += 110

    # ── ERASER ───────────────────────────────
    ecol = (0, 200, 255) if state == "ERASER" else (120, 120, 120)
    cv2.putText(frame, f"ERASER: {canvas.eraser_r}",
                (x, 33), FONT, 0.6, ecol, 2)
    x += 150

    # ── ESC ──────────────────────────────────
    cv2.putText(frame, "ESC: Exit", (x, 33), FONT, 0.6, (100, 100, 200), 2)

    # ── 현재 상태 (우측) ─────────────────────
    state_colors = {"IDLE": (0, 200, 0), "DRAWING": (0, 200, 255), "ERASER": (0, 100, 255)}
    scol = state_colors.get(state, (255, 255, 255))
    cv2.putText(frame, f"[ {state} ]",
                (w - 180, 33), FONT, 0.8, scol, 2)


def draw_cursor(frame, point, state, canvas):
    """손가락 끝에 커서 표시"""
    if point is None:
        return
    if state == "ERASER":
        cv2.circle(frame, point, canvas.eraser_r, (0, 100, 255), 2)
    elif state == "DRAWING":
        cv2.circle(frame, point, canvas.line_size // 2 + 2,
                   COLORS[canvas.color_name], -1)


# ── private ──────────────────────────────────
def _draw_button(frame, x, label, text_color, bg_color, border_color=(50, 50, 50)):
    y1, y2 = BTN_PAD, UI_BAR_HEIGHT - BTN_PAD
    cv2.rectangle(frame, (x, y1), (x + BTN_W, y2), bg_color, -1)
    cv2.rectangle(frame, (x, y1), (x + BTN_W, y2), border_color, 2)
    tx = x + 10
    cv2.putText(frame, label, (tx, 33), FONT, 0.55, text_color, 2)