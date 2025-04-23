import torch
import cv2
import numpy as np
from segment_anything import SamPredictor, sam_model_registry
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import os
import json
import open3d as o3d
from utils.image_utils import remove_background, generate_3d_from_image

# Chargement du modèle PaLI-Gemma
model_name = "google/paligemma-3b-pt-448"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForImageTextToText.from_pretrained(model_name)

# Configuration SAM
sam_checkpoint = "/Users/chamarb/Downloads/image_processing_app/backend/sam_vit_b_01ec64.pth"
sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint).to("cpu")
predictor = SamPredictor(sam)

def process_image(image_path):
    try:
        # Étape 1 : Suppression de l’arrière-plan
        segmented_image = remove_background(image_path, predictor)

        # Étape 2 : Génération de la description avec PaLI-Gemma
        image_pil = Image.open(segmented_image)
        text_input = "<image>"
        inputs = processor(images=image_pil, text=text_input, return_tensors="pt")
        outputs = model.generate(**inputs)
        description = processor.batch_decode(outputs, skip_special_tokens=True)[0]

        # Étape 3 : Reconstruction 3D avec Gaussian Splatting
        glb_file_path = generate_3d_from_image(segmented_image)

        # Ensure the .glb file is saved in the static/uploads directory
        if glb_file_path:
            glb_filename = os.path.basename(glb_file_path)
        else:
            raise Exception("3D model generation failed")

        # Return the response with the segmented image and model file
        return {
            "description": description,
            "segmented_image": os.path.basename(segmented_image),
            "model_file": glb_filename  # Return the model file name
        }

    except Exception as e:
        raise Exception(f"Erreur dans le traitement de l'image: {str(e)}")
