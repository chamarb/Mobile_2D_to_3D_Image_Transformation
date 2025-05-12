import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../services/api_service.dart';
import 'result_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  File? _imageFile;
  bool _isUploading = false;

  Future<void> _pickImage(ImageSource source) async {
    final picker = ImagePicker();
    try {
      final pickedFile = await picker.pickImage(source: source);
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
        await _uploadImage(_imageFile!);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("❌ Error picking image: $e")),
      );
    }
  }

  Future<void> _uploadImage(File image) async {
    setState(() => _isUploading = true);

    try {
      final response = await ApiService().uploadImage(image);  // Modify as per your backend API
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(
              description: response["result"]["description"] ?? "No description available",
              imageUrl: "http://192.168.1.60:8000/static/uploads/${response['result']['segmented_image']}",
              modelUrl: "http://192.168.1.60:8000/static/uploads/${response['result']['model_file']}"
            ),
          ),
        ).then((_) {
          setState(() => _imageFile = null);
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("❌ Error uploading image: $e")),
      );
    } finally {
      setState(() => _isUploading = false);
    }
  }

  Widget _buildImagePreview() {
    return _imageFile != null
        ? Hero(
            tag: 'uploaded-image',
            child: ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: Image.file(
                _imageFile!,
                height: 250,
                width: 250,
                fit: BoxFit.cover,
              ),
            ),
          )
        : Column(
            children: const [
              Icon(Icons.image_search, size: 120, color: Colors.white70),
              SizedBox(height: 10),
              Text(
                "No image selected",
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
            ],
          );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.deepPurple[700],
      appBar: AppBar(
        title: const Text("Image Processor AI"),
        backgroundColor: Colors.deepPurple,
        elevation: 0,
        centerTitle: true,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                AnimatedSwitcher(
                  duration: const Duration(milliseconds: 500),
                  child: _buildImagePreview(),
                ),
                const SizedBox(height: 40),
                _isUploading
                    ? Column(
                        children: const [
                          CircularProgressIndicator(color: Colors.white),
                          SizedBox(height: 10),
                          Text("Uploading & Processing...", style: TextStyle(color: Colors.white)),
                        ],
                      )
                    : _buildButtons(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildButtons() {
    return Column(
      children: [
        _buildButton("📂 Pick from Gallery", Icons.photo_album, () => _pickImage(ImageSource.gallery)),
        const SizedBox(height: 20),
        _buildButton("📸 Take a Picture", Icons.camera_alt, () => _pickImage(ImageSource.camera)),
      ],
    );
  }

  Widget _buildButton(String text, IconData icon, VoidCallback onPressed) {
    return ElevatedButton.icon(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white24,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 14),
      ),
      onPressed: onPressed,
      icon: Icon(icon, size: 24),
      label: Text(text, style: const TextStyle(fontSize: 16)),
    );
  }
}
