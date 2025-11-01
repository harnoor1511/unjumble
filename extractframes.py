import cv2

v = cv2.VideoCapture("jumbled_video.mp4")
n = 0

while True:
    r, f = v.read()
    if not r:
        break
    cv2.imwrite("frame" + str(n) + ".jpg", f)
    n = n + 1

v.release()
print("done")
