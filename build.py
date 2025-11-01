import os, time
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from multiprocessing import Pool, cpu_count

FRAMES_DIR = "frames"
OUTPUT = "reconstructed.mp4"
FPS = 30.0
SIZE = (320, 180)

def load_frame(p):
    img = cv2.imread(p)
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, SIZE, interpolation=cv2.INTER_AREA)
    return small, (w, h)

def pair_sim(a):
    i, j, ai, aj = a
    try: v = ssim(ai, aj)
    except: v = float(np.corrcoef(ai.flatten(), aj.flatten())[0,1])
    return i, j, v

def sim_matrix(data):
    n = len(data)
    args = []
    for i in range(n):
        for j in range(i+1, n):
            args.append((i, j, data[i], data[j]))
    sim = np.zeros((n, n), np.float32)
    with Pool(max(1, cpu_count()-1)) as p:
        for i, j, v in p.imap_unordered(pair_sim, args, chunksize=256):
            sim[i, j] = v
            sim[j, i] = v
    np.fill_diagonal(sim, 1.0)
    return sim

def order_frames(sim):
    n = sim.shape[0]
    start = int(np.argmin(sim.sum(axis=1)))
    order = [start]
    left = set(range(n)) - {start}
    while left:
        last = order[-1]
        nxt = max(left, key=lambda x: sim[last, x])
        order.append(nxt)
        left.remove(nxt)
    return order

def write_video(paths, order):
    first = cv2.imread(paths[order[0]])
    h, w = first.shape[:2]
    out = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))
    for i in order:
        out.write(cv2.imread(paths[i]))
    out.release()

def main():
    start_time = time.time()
    files = [f for f in os.listdir(FRAMES_DIR) if f.startswith("f")]
    if not files:
        print("no frames")
        return
    
    def idx(f):
        s = "".join(ch if ch.isdigit() else " " for ch in f)
        x = [int(a) for a in s.split() if a]
        return x[0] if x else 0

    files = sorted(files, key=idx)
    paths = [os.path.join(FRAMES_DIR, f) for f in files]
    small = [load_frame(p)[0] for p in paths]

    sim = sim_matrix(small)
    order = order_frames(sim)

    write_video(paths, order)
    with open("frame_order.txt","w") as f:
        f.write("\n".join(map(str, order)))

    print("done in", round(time.time() - start_time, 1), "s")

if __name__ == "__main__":
    main()
