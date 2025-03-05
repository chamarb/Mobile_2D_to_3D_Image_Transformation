import torch
import cv2
import numpy as np
from segment_anything import SamPredictor, sam_model_registry
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
from huggingface_hub import login
import argparse
import os
import json
import open3d as o3d

# ✅ Log in to Hugging Face programmatically
login(token='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')  # Replace with your actual Hugging Face token

# ✅ Set device to CPU for compatibility
device = "cpu"

# ✅ Load SAM (Fastest: ViT-B for CPU)
sam_checkpoint = "/Users/chamarb/Downloads/sam_vit_b_01ec64.pth"
sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint).to(device)
predictor = SamPredictor(sam)

# ✅ Load PaLI-Gemma for object description
model_name = "google/paligemma-3b-pt-448"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForImageTextToText.from_pretrained(model_name)

# ✅ Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Process images with segmentation and description.')
parser.add_argument('image_paths', type=str, nargs='+', help='Paths to the image files to process')
args = parser.parse_args()

# Function to process a single image
def process_image(image_path):
    # ✅ Load & Process Image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Preserve original dimensions
    original_shape = image.shape[:2]

    # Resize for faster CPU processing
    image_resized = cv2.resize(image, (512, 512))
    predictor.set_image(image_resized)

    # ✅ Provide a segmentation point (adjust for your image)
    point_coords = np.array([[256, 256]])  # Center of the image
    point_labels = np.array([1])  # Foreground

    # ✅ Get segmentation mask
    masks, scores, logits = predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels
    )

    # ✅ Post-process the mask (Resize to original dimensions)
    segmented_mask = cv2.resize(masks[0].astype(np.uint8), (original_shape[1], original_shape[0]))

    # ✅ Create a new image with the background removed
    background_removed = np.zeros_like(image)  # Create an empty image with the same shape
    background_removed[segmented_mask == 1] = image[segmented_mask == 1]  # Keep the foreground

    # ✅ Save Final Segmented Image
    output_image_path = os.path.splitext(image_path)[0] + "_background_removed.jpg"
    cv2.imwrite(output_image_path, background_removed)

    # ✅ Convert to PIL for PaLI-Gemma
    image_pil = Image.fromarray(image)

    # ✅ Generate Object Description with PaLI-Gemma
    text_input = "<image> "  # Add an image token if you want to include text
    inputs = processor(images=image_pil, text=text_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    description = processor.batch_decode(outputs, skip_special_tokens=True)[0]

    # ✅ Create a JSON object for the description
    description_data = {
        "image_path": image_path,
        "description": description
    }
    
    # ✅ Save Description in JSON format
    description_path = os.path.splitext(image_path)[0] + "_object_description.json"
    with open(description_path, "w") as f:
        json.dump(description_data, f, indent=4)

    print(f"\n🔍 **Detected Objects in {image_path}:**", description)
    print(f"✅ Segmentation and background removal completed! Check {output_image_path} & {description_path}")

    # ✅ 2D to 3D Conversion (Using Gaussian Splatting)
    generate_3d_from_image(image, segmented_mask, description_data)

# Function to generate 3D point cloud from image using Gaussian Splatting
def generate_3d_from_image(image, mask, description_data):
    height, width, _ = image.shape
    points = []
    colors = []

    # Iterate over the pixels and create points for the foreground
    for y in range(height):
        for x in range(width):
            if mask[y, x] == 1:  # Only consider foreground pixels
                points.append([x, y, 0])  # Assuming z=0 for 2D image
                colors.append(image[y, x] / 255.0)  # Normalize color values

    points = np.array(points)
    colors = np.array(colors)

    # Create Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Save the point cloud to a file
    pcd_file_path = os.path.splitext(description_data["image_path"])[0] + "_point_cloud.ply"
    o3d.io.write_point_cloud(pcd_file_path, pcd)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd])

    print("✅ 3D Point Cloud generated and displayed.")
    print(f"✅ Point cloud saved to {pcd_file_path}")

# Process each image provided in the command line
for image_path in args.image_paths:
    process_image(image_path)
