import cv2
import numpy as np
import mediapipe as mp

# MediaPipe 설정 (사람 분리)
mp_selfie = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie.SelfieSegmentation(model_selection=1)

# 카메라 열기
cap = cv2.VideoCapture(0)

# 해상도 설정 (선택)
cap.set(3, 640)
cap.set(4, 480)

# VideoWriter 설정 (mp4 저장)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

recording = False  # 녹화 상태

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 좌우 반전 (거울 느낌)
    frame = cv2.flip(frame, 1)

    # MediaPipe 처리 (사람 분리)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = selfie_segmentation.process(rgb_frame)

    mask = result.segmentation_mask
    condition = mask > 0.5  # 사람 영역

    # 배경 블러
    blurred = cv2.GaussianBlur(frame, (55, 55), 0)

    # 사람은 유지, 배경만 블러
    output = np.where(condition[..., None], frame, blurred)

    # 녹화 표시 (빨간 점 + REC)
    if recording:
        cv2.circle(output, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(output, "REC", (50, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)

        out.write(output)  # 영상 저장

    # 화면 출력
    cv2.imshow("Video Recorder", output)

    key = cv2.waitKey(1) & 0xFF

    # ESC 키 → 종료
    if key == 27:
        break

    # Space 키 → 녹화 ON/OFF
    elif key == 32:
        recording = not recording

# 자원 해제
cap.release()
out.release()
cv2.destroyAllWindows()