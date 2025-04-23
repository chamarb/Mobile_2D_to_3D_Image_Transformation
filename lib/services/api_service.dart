import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  Future<Map<String, dynamic>> uploadImage(File image) async {
    // Change the URI to your local IP address
    var uri = Uri.parse("http://192.168.0.18:8000/upload/");
    var request = http.MultipartRequest("POST", uri)
      ..files.add(await http.MultipartFile.fromPath("file", image.path));

    var response = await request.send();
    var responseData = await response.stream.bytesToString();

    if (response.statusCode == 200) {
      return json.decode(responseData);
    } else {
      throw Exception("❌ Upload failed: ${response.reasonPhrase}");
    }
  }
}