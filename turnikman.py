import requests
import cv2
import time

video_capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
while True:
    time.sleep(0.125)
    ret, frame = video_capture.read()
    data, bbox, straight_qrcode = detector.detectAndDecode(frame)
    if data:
        cnt = requests.get(f'http://10.20.2.67/open/{data}').content.decode()
        if cnt == '{"should_open": 1}':
            print('открыть врата')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('detector', frame)

video_capture.release()
cv2.destroyAllWindows()