# ─────────────────────────────────────────
# hand_tracker.py  –  손 추적 & 제스처 인식
# ─────────────────────────────────────────

import mediapipe as mp
from config import MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils


class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )

    def process(self, rgb_frame):
        return self.hands.process(rgb_frame)

    def draw_landmarks(self, frame, hand_landmarks):
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    def get_finger_point(self, landmarks, frame_w, frame_h):
        lm = landmarks.landmark
        ix = int(lm[8].x * frame_w)
        iy = int(lm[8].y * frame_h)
        return (ix, iy)

    def get_gesture(self, landmarks, handedness="Right"):
        lm = landmarks.landmark
        finger_up = self._count_fingers(lm, handedness)
        total = sum(finger_up)

        if total == 0:
            return "IDLE"
        if total == 5:
            return "ERASER"
        # 굿 (엄지만) → BLUE
        if finger_up[0] == 1 and finger_up[1] == 0 and finger_up[2] == 0 and finger_up[3] == 0 and finger_up[4] == 0:
            return "BLUE"
        # 검지만 → DRAWING
        if finger_up[1] == 1 and finger_up[2] == 0 and finger_up[3] == 0 and finger_up[4] == 0:
            return "DRAWING"
        # 브이 → RED
        if finger_up[1] == 1 and finger_up[2] == 1 and finger_up[3] == 0 and finger_up[4] == 0:
            return "RED"
        # 샤카 → YELLOW
        if finger_up[0] == 1 and finger_up[1] == 0 and finger_up[2] == 0 and finger_up[3] == 0 and finger_up[4] == 1:
            return "YELLOW"
        # 오케이 → GREEN
        if self._is_ok(lm):
            return "GREEN"
        return "IDLE"

    def _is_ok(self, lm):
        thumb_tip = lm[4]
        index_tip = lm[8]
        dist = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
        return dist < 0.07

    def _count_fingers(self, lm, handedness):
        finger_up = []
        if handedness == "Right":
            finger_up.append(1 if lm[4].x < lm[3].x else 0)
        else:
            finger_up.append(1 if lm[4].x > lm[3].x else 0)
        for tip in [8, 12, 16, 20]:
            finger_up.append(1 if lm[tip].y < lm[tip - 2].y else 0)
        return finger_up