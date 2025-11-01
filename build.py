import os, cv2, numpy as np

folder = "frames"
out = "output.mp4"
fps = 30

fs = sorted(os.listdir(folder))
imgs = [cv2.imread(os.path.join(folder, x)) for x in fs if x.endswith(".jpg")]

h,w = imgs[0].shape[:2]
v = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w,h))

o = np.random.permutation(len(imgs))
for i in o:
    v.write(imgs[i])
v.release()
