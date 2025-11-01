import os, cv2

folder = "frames"
out = "reconstructed.mp4"
fps = 30

fs = sorted(os.listdir(folder))
paths = [os.path.join(folder, f) for f in fs]

first = cv2.imread(paths[0])
h,w = first.shape[:2]
v = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w,h))

for p in paths:
    v.write(cv2.imread(p))
v.release()
