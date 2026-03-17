import cv2

# 카메라 열기
cap = cv2.VideoCapture(0)

# 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

recording = False  # 녹화 상태

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 좌우 반전 (추가 기능)
    frame = cv2.flip(frame, 1)

    # 녹화 중이면 저장 + 빨간 점
    if recording:
        out.write(frame)
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)

    cv2.imshow("Video Recorder", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break
    elif key == 32:  # Space
        recording = not recording
        print("Recording:", recording)

cap.release()
out.release()
cv2.destroyAllWindows()