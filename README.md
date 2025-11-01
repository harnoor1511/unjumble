Jumbled Frames Reconstruction Challenge
Overview

This project reconstructs a shuffled video by restoring its correct frame sequence using image similarity analysis and a greedy ordering approach. The challenge involves a 10-second, 1080p, 30 FPS video whose 300 frames have been randomly reordered. The goal is to produce a sequence as close as possible to the original continuous recording.

Problem Description

Input: 300 unordered frames extracted from a single-shot video clip

Output: A reconstructed .mp4 video with the most likely correct frame order

Constraint: No prior knowledge of true ordering and no scene cuts

Evaluation: Accuracy, efficiency, innovation, and clarity of implementation

Algorithm Explanation
1. Frame Extraction and Preprocessing

All frames are first converted to grayscale and downscaled to a lower resolution.
Purpose:

Speed up similarity calculations

Reduce memory usage

Retain structural and motion continuity cues

The original full-resolution frames remain untouched for final reconstruction.

2. Similarity Computation (SSIM-Based)

This step determines how visually close each frame is to every other frame.
The Structural Similarity Index Measure (SSIM) compares:

Luminance structure

Texture patterns

Local contrast

Properties:

Score ranges from −1 to 1

Higher value = more similar

If SSIM fails for any frame pair, normalized cross-correlation is used as fallback.

Optimization:

Only compute upper triangle of the similarity matrix to avoid duplication

Use multiprocessing to parallelize pairwise comparisons

Store results in a symmetric similarity matrix of shape NxN

3. Frame Ordering (Greedy Adjacency Strategy)

Assumption:
A continuous real-world motion should result in consecutive frames being most similar to each other.

Steps:

Compute total similarity of each frame with all others

Choose the frame with the lowest total similarity as the starting frame

Likely the beginning or end of the sequence

Iteratively select the remaining frame with the highest similarity to the last chosen frame

Continue until all frames are ordered

This greedy technique dramatically reduces complexity compared to optimal Hamiltonian path search while maintaining strong alignment with natural video motion.

4. Video Reconstruction

Once ordering is complete:

Frames are read at original resolution

A new MP4 video is created at 30 FPS

Frame indices are logged in frame_order.txt for verification

Time Complexity Considerations
Phase	Complexity	Notes
Similarity Matrix	O(N²)	Parallelized across CPU cores
Greedy Ordering	O(N²)	Lightweight operations
Video Writing	O(N)	I/O bound

For N = 300, the approach remains efficient and scalable for the evaluation system.

Installation and Setup
Dependencies

Python 3.11+

Required libraries:

pip install opencv-python numpy scikit-image

Project Structure
build.py                // Reconstruction
extractframes.py        // Frame extraction
frames/                 // Folder created during extraction
reconstructed.mp4       // Output (provided separately in Drive)
frame_order.txt         // Ordering output

How to Execute
Step 1: Extract frames from shuffled video

Place jumbled_video.mp4 in the project directory and run:

py -3.11 extractframes.py


Frames stored to:

frames/f0.jpg ... frames/f299.jpg

Step 2: Reconstruct the video

Run:

py -3.11 build.py


Outputs:

reconstructed.mp4

frame_order.txt

Execution time logs in terminal