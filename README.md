# Jumbled Frames Reconstruction Challenge

## Overview
This project reconstructs a shuffled video by restoring its correct frame sequence using image similarity analysis and an optimized greedy approach. The input consists of 300 shuffled frames extracted from a continuous 10-second, 1080p, 30 FPS video. The objective is to reassemble the frames into the correct order without any prior reference to the original sequence.

---

## Problem Description
* **Input:** 300 unordered frames extracted from a single-shot video  
* **Output:** Reconstructed `.mp4` video with correct temporal order   

---

## System Workflow

```
Jumbled Video
      │
      ▼
Frame Extraction  →  Preprocessing (Resize + Grayscale)
      │
      ▼
Similarity Matrix (SSIM + Parallel Processing)
      │
      ▼
Greedy Ordering Strategy
      │
      ▼
Final Video Reconstruction (Full Resolution)
```

---

## Algorithm Explanation

### 1. Preprocessing
Each input frame is:
* Converted to grayscale  
* Downscaled to reduce memory usage  
* Maintains motion and structure for similarity comparison  

### 2. Similarity Computation (SSIM)
* Structural Similarity Index Measure used to compare each frame pair  
* If SSIM fails due to uniform regions, normalized cross-correlation is used as fallback  

**Performance optimizations:**
* Store only upper triangular similarity computations  
* Utilize multiprocessing across available CPU cores  
* Construct a symmetric NxN similarity matrix  

**Similarity score:**
* Range: −1 to +1  
* Higher value indicates frames closer in temporal order  

### 3. Greedy Frame Ordering Strategy
**Assumption:** Temporally adjacent frames have highest mutual similarity.  

**Procedure:**
1. Compute sum of similarities for each frame  
2. Select starting frame as one with lowest global similarity  
3. Iteratively append the most similar remaining frame  
4. Continue until all frames are included  

This reduces the combinatorial complexity compared to full graph search problems such as Hamiltonian Path or TSP.  

### 4. Video Reconstruction
* Utilize original full-resolution frames  
* Rebuild video using OpenCV at 30 FPS  
* Save frame ordering to a log file (`frame_order.txt`)  

---

## Computational Complexity

| Component | Complexity | Notes |
|------------|-------------|-------|
| Similarity Matrix | O(N²) | Parallelized across CPU cores |
| Ordering Strategy | O(N²) | Lightweight greedy calculations |
| Video Writing | O(N) | Disk I/O dependent |

For **N = 300**, the implementation remains efficient and scalable.

---

## Setup and Installation

### Requirements
* Python 3.11+  

Install dependencies:
```sh
pip install opencv-python numpy scikit-image
```

---

## Project Structure
```
build.py                # Reconstruction script
extractframes.py        # Frame extraction script
frames/                 # Directory for extracted frames
frame_order.txt         # Generated order logs
reconstructed.mp4       # Final output video
```

---

## How to Run

### Step 1: Extract Frames
Place `jumbled_video.mp4` in the project directory and run:
```sh
py -3.11 extractframes.py
```

Extracted frames will be saved as:
```
frames/f0.jpg ... frames/f299.jpg
```

### Step 2: Reconstruct Video
Run:
```sh
py -3.11 build.py
```

**Outputs:**
* Frames folder with 300 frames
* reconstructed.mp4  
* frame_order.txt  
* Total execution time displayed in terminal  

---

## Contributors
* **Harnoor Arora**