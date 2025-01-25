import cv2


ip = "192.168.1.10"
port = 8080
stream = "h264_ulaw.sdp"
url = f"rtsp://{ip}:{port}/{stream}"
camera = cv2.VideoCapture(url)

window_name = "Camera"
window = cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
print(f"URL: {url}")

while camera.isOpened():
    _, frame = camera.read()
    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
