import os, cv2, numpy as np
from skimage.metrics import structural_similarity as ssim

folder="frames"
out="reconstructed.mp4"
fps=30

fs=sorted(os.listdir(folder))
paths=[os.path.join(folder,f) for f in fs]

gray=[cv2.cvtColor(cv2.imread(p),cv2.COLOR_BGR2GRAY) for p in paths]
n=len(gray)
sim=np.zeros((n,n),np.float32)

for i in range(n):
    for j in range(n):
        sim[i,j]=ssim(gray[i],gray[j])

start=0
order=[start]
left=set(range(n))-{start}
while left:
    last=order[-1]
    nxt=max(left,key=lambda x: sim[last,x])
    order.append(nxt)
    left.remove(nxt)

first=cv2.imread(paths[0])
h,w=first.shape[:2]
v=cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*"mp4v"),fps,(w,h))

for i in order:
    v.write(cv2.imread(paths[i]))
v.release()
