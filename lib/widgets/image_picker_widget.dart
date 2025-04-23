import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

class ImagePickerWidget extends StatefulWidget {
  final Function(File) onImagePicked;
  const ImagePickerWidget({super.key, required this.onImagePicked});

  @override
  _ImagePickerWidgetState createState() => _ImagePickerWidgetState();
}

class _ImagePickerWidgetState extends State<ImagePickerWidget> {
  File? _selectedImage;
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;

  Future<void> _pickImage(ImageSource source) async {
    setState(() => _isLoading = true);

    // Request permissions for camera or gallery
    PermissionStatus permissionStatus =
        source == ImageSource.camera ? await Permission.camera.request() : await Permission.photos.request();

    if (!permissionStatus.isGranted) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("⛔ Permission refusée pour accéder à la ${source == ImageSource.camera ? 'caméra' : 'galerie'}")),
      );
      return;
    }

    try {
      final pickedFile = await _picker.pickImage(source: source);
      if (pickedFile != null) {
        setState(() {
          _selectedImage = File(pickedFile.path);
        });
        widget.onImagePicked(_selectedImage!);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("❌ Erreur de sélection d'image: $e")),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _selectedImage == null
            ? const Text('📷 Aucune image sélectionnée', style: TextStyle(fontSize: 16, color: Colors.grey))
            : Image.file(_selectedImage!, height: 250),

        const SizedBox(height: 20),

        _isLoading
            ? const CircularProgressIndicator()
            : Column(
                children: [
                  ElevatedButton.icon(
                    onPressed: () => _pickImage(ImageSource.gallery),
                    icon: const Icon(Icons.image),
                    label: const Text('📂 Choisir depuis la Galerie'),
                  ),
                  ElevatedButton.icon(
                    onPressed: () => _pickImage(ImageSource.camera),
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('📸 Prendre une Photo'),
                  ),
                ],
              ),
      ],
    );
  }
}
