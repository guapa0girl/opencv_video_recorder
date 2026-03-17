import cv2

# 카메라 연결
cap = cv2.VideoCapture(0)

# 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

recording = False  # 녹화 상태

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 추가 기능 (좌우 반전)
    frame = cv2.flip(frame, 1)

    # 녹화 중일 때
    if recording:
        # 빨간 점 표시
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
        out.write(frame)

    # 화면 출력
    cv2.imshow('Smart Video Recorder', frame)

    key = cv2.waitKey(1)

    # Space → 녹화 ON/OFF
    if key == 32:
        recording = not recording

    # ESC → 종료
    elif key == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()