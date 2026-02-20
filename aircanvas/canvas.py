# ─────────────────────────────────────────
# canvas.py  –  드로잉 캔버스 관리
# ─────────────────────────────────────────

import cv2
import numpy as np
from config import COLORS, DEFAULT_COLOR, DEFAULT_LINE_SIZE, DEFAULT_ERASER_R, UI_BAR_HEIGHT


class Canvas:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.surface   = np.zeros((height, width, 3), dtype=np.uint8)
        self.color_name = DEFAULT_COLOR
        self.line_size  = DEFAULT_LINE_SIZE
        self.eraser_r   = DEFAULT_ERASER_R
        self.prev_point = None

    # ── 드로잉 ───────────────────────────────
    def draw(self, point):
        """DRAWING 상태: 이전 점과 현재 점을 선으로 연결"""
        if self._in_draw_zone(point):
            if self.prev_point:
                cv2.line(self.surface, self.prev_point, point,
                         COLORS[self.color_name], self.line_size)
            self.prev_point = point
        else:
            self.prev_point = None

    def erase(self, point):
        """ERASER 상태: 원형으로 지우기"""
        if self._in_draw_zone(point):
            cv2.circle(self.surface, point, self.eraser_r, (0, 0, 0), -1)
        self.prev_point = None

    def reset_prev(self):
        self.prev_point = None

    def clear(self):
        self.surface = np.zeros((self.h, self.w, 3), dtype=np.uint8)

    def save(self, path="drawing_saved.png"):
        cv2.imwrite(path, self.surface)
        print(f"저장 완료: {path}")

    # ── 합성 ─────────────────────────────────
    def blend(self, frame):
        """카메라 프레임 위에 캔버스를 합성해 반환"""
        return cv2.addWeighted(frame, 0.6, self.surface, 0.8, 0)

    # ── 색상 / 두께 ──────────────────────────
    def set_color(self, name):
        if name in COLORS:
            self.color_name = name

    def change_line_size(self, delta):
        self.line_size = max(1, min(30, self.line_size + delta))

    # ── private ──────────────────────────────
    def _in_draw_zone(self, point):
        """UI 바 아래 영역인지 확인"""
        return point[1] > UI_BAR_HEIGHT