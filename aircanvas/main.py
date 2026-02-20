# ─────────────────────────────────────────
# main.py  –  메인 루프
# ─────────────────────────────────────────

import cv2
from hand_tracker import HandTracker
from canvas import Canvas
from ui import draw_ui, draw_cursor

COLOR_GESTURES = {"BLUE", "RED", "GREEN", "YELLOW"}

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        return

    h, w    = frame.shape[:2]
    tracker = HandTracker()
    canvas  = Canvas(w, h)
    state   = "IDLE"

    print("Air Drawing 시작! (ESC 또는 q 로 종료)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = tracker.process(rgb)

        finger_point = None

        if result.multi_hand_landmarks:
            for hand_lm, hand_info in zip(result.multi_hand_landmarks,
                                          result.multi_handedness):
                handedness   = hand_info.classification[0].label
                state        = tracker.get_gesture(hand_lm, handedness)
                finger_point = tracker.get_finger_point(hand_lm, w, h)
                tracker.draw_landmarks(frame, hand_lm)

        # 색상 제스처 처리
        if state in COLOR_GESTURES:
            canvas.set_color(state)
            state = "DRAWING"

        # 캔버스 업데이트
        if finger_point:
            if state == "DRAWING":
                canvas.draw(finger_point)
            elif state == "ERASER":
                canvas.erase(finger_point)
            else:
                canvas.reset_prev()
        else:
            state = "IDLE"
            canvas.reset_prev()

        # 합성 & UI
        output = canvas.blend(frame)
        draw_ui(output, state, canvas)
        draw_cursor(output, finger_point, state, canvas)

        cv2.imshow("AIR - DRAWING", output)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("종료")

if __name__ == "__main__":
    main()