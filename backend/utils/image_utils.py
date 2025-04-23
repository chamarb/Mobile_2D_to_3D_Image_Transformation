import os
import cv2
import numpy as np
import open3d as o3d

def remove_background(image_path, predictor):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found!")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictor.set_image(image_rgb)

    # Use center point for segmentation
    point_coords = np.array([[image.shape[1] // 2, image.shape[0] // 2]])
    point_labels = np.array([1])

    masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)
    segmented_mask = masks[0].astype(np.uint8) * 255

    # Apply mask
    result = cv2.bitwise_and(image_rgb, image_rgb, mask=segmented_mask)
    output_path = image_path.replace(".jpg", "_segmented.jpg").replace(".png", "_segmented.png")
    cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))

    return output_path

import trimesh

def generate_3d_from_image(image_path, downsample_factor=4):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found!")

    # Resize for speed
    height, width = image.shape[:2]
    new_width = width // downsample_factor
    new_height = height // downsample_factor
    image_resized = cv2.resize(image, (new_width, new_height))
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

    # Generate coordinates grid
    x_coords, y_coords = np.meshgrid(np.arange(new_width), np.arange(new_height))
    z_coords = gray.astype(np.float32) / 255.0
    y_coords = new_height - y_coords

    points = np.stack([x_coords, y_coords, z_coords], axis=-1).reshape(-1, 3)
    colors = image_resized.reshape(-1, 3).astype(np.float32) / 255.0

    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Voxel downsample
    voxel_size = 0.08
    pcd_down = pcd.voxel_down_sample(voxel_size)

    # Save PLY
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    ply_filename = f"{base_name}_3d.ply"
    ply_path = os.path.join("static/uploads", ply_filename)
    o3d.io.write_point_cloud(ply_path, pcd_down)

    # Convert to GLB using Trimesh
    trimesh_points = np.asarray(pcd_down.points)
    trimesh_colors = (np.asarray(pcd_down.colors) * 255).astype(np.uint8)

    cloud = trimesh.points.PointCloud(vertices=trimesh_points, colors=trimesh_colors)
    glb_filename = f"{base_name}_3d.glb"
    glb_path = os.path.join("static/uploads", glb_filename)
    cloud.export(glb_path)

    return glb_path  # return .glb path by default
