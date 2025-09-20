# Zero-Day OMR Evaluator

## Problem Statement
The goal of this project is to automatically evaluate OMR (Optical Mark Recognition) sheets for multiple-choice questions. Manually checking answer sheets is time-consuming and error-prone. This app allows educators or examiners to upload scanned OMR sheets and get instant results including detailed correctness per question.

---

## Approach
1. **Image Processing:**  
   - The uploaded OMR sheet image is converted to grayscale and thresholded using OpenCV.
   - Contours corresponding to the answer bubbles are detected and sorted.
   
2. **Answer Evaluation:**  
   - Each question has multiple bubbles (A, B, C, D).  
   - The filled bubble is detected by counting non-zero pixels within the contour mask.  
   - The detected answer is compared against a predefined **answer key**.

3. **Result Display:**  
   - Total score is computed.  
   - Detailed per-question results are shown in a table with ✅ for correct and ❌ for incorrect answers.  

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/varsha05sheshadri/omr-evaluator.git
cd omr-evaluator
