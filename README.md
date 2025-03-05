# Mobile_2D_to_3D_Image_Transformation

# Application de Description d'Image et Reconstruction 3D

## Schéma de l’Architecture de l’Application

Cette application mobile permet de télécharger une image, de la traiter, puis de générer une description textuelle et une reconstruction 3D de l’image à l’aide de modèles d'intelligence artificielle optimisés pour le mobile. Voici un aperçu détaillé de l'architecture de l'application :

### 1. **Téléchargement de l'Image**
- L'utilisateur télécharge une image depuis son appareil mobile via l'interface de l'application.
- Cette étape se fait en utilisant un formulaire simple d'upload d'image dans l'application Flutter.

### 2. **Prétraitement de l'Image**
- Avant l'inférence, l'image subit un prétraitement pour supprimer l'arrière-plan, si nécessaire.
- Un modèle de segmentation d'image (par exemple, basé sur DeepLabv3 ou une autre solution optimisée pour mobile) est utilisé pour cette étape. Cette étape assure que le modèle de description d'image se concentre uniquement sur les éléments pertinents de l'image.

### 3. **Génération de la Description Textuelle**
- Une fois l'image prétraitée, le modèle **PaLI-Gemma 2** (converti en format TensorFlow Lite) est utilisé pour générer une description textuelle de l'image.
- Le modèle de vision et langage fonctionne en local, sans serveur, ce qui garantit que les données de l'utilisateur restent privées et sécurisées sur l'appareil.
- Cette étape est optimisée pour s'exécuter sur le GPU ou via NNAPI pour une meilleure performance.

### 4. **Reconnaissance 3D avec Gaussian Splatting**
- Le modèle **Gaussian Splatting**, optimisé pour les appareils mobiles, est utilisé pour reconstruire l'image en 3D à partir des données de l'image 2D.
- Cette technique permet de créer un modèle 3D de l'objet ou de la scène dans l'image sans nécessiter de calculs complexes côté serveur.

### 5. **Affichage des Résultats**
L'application affiche les résultats de manière interactive pour l'utilisateur :
- **Texte descriptif** : La description textuelle générée par le modèle SmolVLM2 ou PaLI-Gemma 2 est affichée à l'utilisateur. Cela permet à l'utilisateur de mieux comprendre le contenu de l'image.
- **Modèle 3D interactif** : Un moteur de rendu intégré ou un WebViewer est utilisé pour afficher le modèle 3D reconstruit. L'utilisateur peut interagir avec ce modèle, le zoomer, le faire pivoter et obtenir des informations supplémentaires sur les objets présents dans l'image.
- Le WebViewer peut être intégré pour afficher un modèle 3D interactif sans besoin de ressources serveur supplémentaires.

## Outils Utilisés

- **Flutter & Dart** : Framework mobile utilisé pour développer l'application, permettant une interface fluide et intuitive.
- **TensorFlow Lite** : Utilisé pour exécuter les modèles d'IA localement sur l'appareil, optimisant les performances avec le GPU ou NNAPI.
- **SmolVLM2 / PaLI-Gemma 2** : Modèles de vision et de langage pour générer des descriptions textuelles des images. Convertis en TensorFlow Lite pour une exécution locale.
- **Gaussian Splatting** : Technique de reconstruction 3D utilisée pour créer des modèles 3D interactifs à partir des images.
- **WebViewer / Moteur de Rendu 3D** : Utilisé pour afficher les modèles 3D interactifs dans l'application.

## Fonctionnalités
- **Upload d'images** : Permet à l'utilisateur de télécharger une image.
- **Prétraitement de l'image** : Supprime l'arrière-plan pour se concentrer sur les éléments principaux.
- **Génération de description** : Crée une description textuelle basée sur l'image.
- **Reconstruction 3D** : Génère un modèle 3D à partir de l'image.
- **Interaction 3D** : Permet à l'utilisateur de zoomer et de pivoter le modèle 3D.

## Dépendances
- `flutter_tflite`: pour intégrer les modèles TensorFlow Lite.
- `image_picker`: pour gérer l'upload des images.
- `image_processing_lib`: pour le prétraitement de l'image (suppression de l’arrière-plan).
- `flutter_webview`: pour afficher le modèle 3D interactif via un WebViewer.
- `geometrical_3d_renderer`: pour le rendu des modèles 3D sur mobile.

## Installation

1. Clonez ce projet sur votre machine locale.
2. Installez les dépendances Flutter :
   ```bash
   flutter pub get
