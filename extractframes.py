import cv2
import os

video_path = "jumbled_video.mp4"
output_folder = "frames"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("video missing")
    raise SystemExit

n = 0
while True:
    r, f = cap.read()
    if not r:
        break
    cv2.imwrite(f"{output_folder}/f{n}.jpg", f)
    n += 1

cap.release()
print("done")
