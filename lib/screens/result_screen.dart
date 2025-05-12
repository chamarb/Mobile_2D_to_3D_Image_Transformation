import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter/services.dart';
import 'package:share_plus/share_plus.dart';

class ResultScreen extends StatefulWidget {
  final String description;
  final String imageUrl;
  final String modelUrl;

  const ResultScreen({
    super.key,
    required this.description,
    required this.imageUrl,
    required this.modelUrl,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  late final WebViewController _controller;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    final modelFileName = Uri.parse(widget.modelUrl).pathSegments.last;
    final String modelViewerUrl =
        "http://192.168.1.60:8000/3d_viewer/model_viewer.html?model=$modelFileName";

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse(modelViewerUrl))
      ..setNavigationDelegate(NavigationDelegate(
        onPageFinished: (_) => setState(() => _isLoading = false),
        onPageStarted: (_) => setState(() => _isLoading = true),
        onWebResourceError: (error) {
          setState(() => _isLoading = false);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("❌ Error loading model: ${error.description}")),
          );
        },
      ));
  }

  void _copyToClipboard() {
    Clipboard.setData(ClipboardData(text: widget.description));
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("📋 Description copied!")));
  }

  void _shareResult() {
    Share.share('AI Image Description:\n${widget.description}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.deepPurple[700],
      appBar: AppBar(
        title: const Text('📌 AI Results'),
        backgroundColor: Colors.deepPurple,
        elevation: 4,
        actions: [
          IconButton(icon: const Icon(Icons.share), onPressed: _shareResult),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            flex: 3,
            child: Stack(
              children: [
                WebViewWidget(
                  controller: _controller,
                  key: UniqueKey(),
                ),
                if (_isLoading)
                  const Center(child: CircularProgressIndicator(color: Colors.white)),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
              ),
              child: Column(
                children: [
                  Hero(
                    tag: 'uploaded-image',
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(15),
                      child: Image.network(
                        widget.imageUrl,
                        height: 150,
                        errorBuilder: (_, __, ___) => const Icon(Icons.broken_image, size: 100),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Expanded(
                        child: Text(widget.description, textAlign: TextAlign.center),
                      ),
                      IconButton(icon: const Icon(Icons.copy), onPressed: _copyToClipboard),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        tooltip: "Back to Home",
        onPressed: () => Navigator.pop(context),
        child: const Icon(Icons.home),
        backgroundColor: Colors.deepPurple,
      ),
    );
  }
}
