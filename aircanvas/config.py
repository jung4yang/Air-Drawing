# ─────────────────────────────────────────
# config.py  –  전역 설정
# ─────────────────────────────────────────

# 색상 (BGR)
COLORS = {
    "BLUE":   (255, 100,  20),
    "RED":    (  0,  50, 220),
    "GREEN":  ( 50, 200,  50),
    "YELLOW": (  0, 220, 220),
    "WHITE":  (255, 255, 255),
}
COLOR_ORDER = list(COLORS.keys())

# 기본 드로잉 설정
DEFAULT_COLOR      = "BLUE"
DEFAULT_LINE_SIZE  = 5
DEFAULT_ERASER_R   = 60

# MediaPipe
MAX_HANDS              = 1
DETECTION_CONFIDENCE   = 0.7
TRACKING_CONFIDENCE    = 0.7

# UI
UI_BAR_HEIGHT = 50