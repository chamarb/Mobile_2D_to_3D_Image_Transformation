# PFE Project Dashboard - Image Description & 3D Visualization

Welcome to the **PFE Project Dashboard**, a powerful tool for visualizing and interacting with AI-driven image understanding and 3D reconstruction.

## 🏠 Overview

This section introduces the main objectives and technologies behind the project.

### 📌 Project Overview: AI-Powered Image Understanding & 3D Visualization
This project aims to turn 2D images into semantically rich textual descriptions and interactive 3D visualizations. It employs state-of-the-art AI models and techniques to enhance the understanding of visual content.

#### 🛠️ Tech Stack:
- **Flutter** (Frontend)
- **FastAPI** (Backend)
- **HuggingFace** (PaLI-Gemma3B)
- **SAM** (Segment Anything Model)
- **Gaussian Splatting** (3D Reconstruction)
- **Three.js** (3D Rendering)

#### 🌟 Features:
- **AI-driven Image Understanding:** Using multi-modal models to generate textual descriptions from images.
- **Background Removal & Object Segmentation:** Isolating key objects for better processing.
- **3D Reconstruction & Rendering:** (In development) Transforming images into 3D models for interactive visualization.

#### 🧠 AI Models Used:
1. **PaLI-Gemma3B**: A high-performance model for generating detailed text descriptions from images.
2. **SAM (Segment Anything Model)**: A model designed for segmenting and removing backgrounds from images.
3. **Gaussian Splatting**: A cutting-edge method for 3D reconstruction of segmented images, currently under development.

### 📈 Quick Stats:
- **Number of demo images processed:** 36
- **Backend Inference:** FastAPI + HuggingFace Transformers
- **Frontend:** Flutter (Mobile App) + Dash (Dashboard)

---

## 🧠 Model Showcase

This section highlights the AI model's capability to generate textual descriptions from images.

### 💻 Example: Laptop

- **Original Image:** 
  ![Laptop](assets/demo_laptop.jpg)
- **Background Removed:** 
  ![Laptop Background Removed](assets/demo_laptop_background_removed.jpg)
- **Description (PaLI-Gemma2):** 
  "A modern laptop with a thin profile, featuring a metallic finish and a large screen."

### 🪑 Example: Chair

- **Original Image:** 
  ![Chair](assets/demo_chair.jpg)
- **Background Removed:** 
  ![Chair Background Removed](assets/demo_chair_background_removed.jpg)
- **Description (PaLI-Gemma2):** 
  "An ergonomic office chair with adjustable armrests, a cushioned seat, and a sleek design."

---

## 🧊 3D Preview

In this section, users can select an object (e.g., a chair or laptop) to view the segmented image and its corresponding 3D model.

### Select an object to view its 3D model:
- **Chair**
- **Laptop**

**3D Model:** Rendered using **Gaussian Splatting**.

---

## 📐 Architecture

This section provides a visual overview of the system architecture, illustrating how various components like Flutter, FastAPI, and AI models interact.

### Architecture Diagram:
![System Architecture](assets/architecture.png)

---

## 📊 Comparison

This section compares the **SmolVLM2** and **PaLI-Gemma2** models based on key performance metrics.

### Comparison Metrics:
- **Model Size (GB)**
- **VRAM Needed (GB)**
- **Inference Speed (s/img)**


## 🔚 Conclusion

In the final section, we wrap up the project, highlighting the key achievements and next steps.

### Conclusion:
- ✅ **End-to-End System**: From image input to AI-driven description.
- ⚙️ **Gaussian Splatting 3D**: Volume estimation under active development.
- 🚀 **Next Steps**: Optimize for mobile, real-time inference, and improved UX.

### Future Outlook:
- **Mobile Optimization**: Enhance performance and reduce latency.
- **Volume Estimation**: Implement and fine-tune 3D volume measurement features.

---

## 🚀 Development Team

### 👩‍💻 Author:
- **Chaimae Rouineb**

### 📚 Sources:
- **PaLI-Gemma3B on HuggingFace:** [Link](https://huggingface.co/google/paligemma-3b-pt-448)
- **SAM (Segment Anything Model) on GitHub:** [Link](https://github.com/facebookresearch/segment-anything)
- **Gaussian Splatting Blog by HuggingFace:** [Link](https://huggingface.co/blog/gaussian-splatting)
