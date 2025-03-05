# Résumé du script : Segmentation, Description et Reconstruction 3D d’Images

Ce script réalise trois tâches principales sur une image donnée :

1. **Segmentation et suppression d’arrière-plan**
2. **Génération d’une description textuelle de l’image**
3. **Conversion d’image 2D en un nuage de points 3D**

## 1. Segmentation et Suppression d’Arrière-Plan

- **Modèle utilisé :** Segment Anything Model (SAM)
- L’image est chargée et redimensionnée pour accélérer le traitement.
- Un point de référence (au centre de l’image) est utilisé pour segmenter l’objet principal.
- Le masque généré est appliqué pour supprimer l’arrière-plan et ne garder que l’objet d’intérêt.
- L’image segmentée est enregistrée en sortie.

## 2. Génération d’une Description Textuelle

- **Modèle utilisé :** PaLI-Gemma 3B (modèle de vision et langage)
- L’image segmentée est convertie en format PIL et traitée par le modèle.
- Une description textuelle de l’objet est générée et stockée dans un fichier JSON.

## 3. Conversion 2D → 3D (Nuage de Points)

- **Méthode utilisée :** Gaussian Splatting avec Open3D
- À partir de l’image segmentée, les pixels appartenant à l’objet sont extraits.
- Chaque pixel est transformé en un point 3D avec une couleur correspondante.
- Un nuage de points 3D est généré et enregistré au format `.ply`.
- Le nuage est ensuite visualisé avec Open3D.

## Objectifs et Impact sur le Projet

Ce script s’aligne avec les objectifs du projet en permettant une analyse multimodale des images :

- **Optimisation de l’interaction avec SmolVLM et PaLI-Gemma** pour extraire des descriptions pertinentes.
- **Amélioration de la segmentation automatique** en vue de futures optimisations sur mobile.
- **Création d’une base pour la reconstruction 3D** en vue de mesurer le volume d’objets.
- **Réduction du besoin en puissance de calcul** en utilisant des modèles adaptés au CPU.

En intégrant ce processus dans une application mobile Flutter, l’utilisateur pourra :
- Prendre une photo,
- Obtenir une description précise,
- Voir l’objet en 3D,
- Éventuellement estimer son volume.

## 📌 Commande pour exécuter le script

Après avoir cloné le projet et accédé au répertoire, exécutez la commande suivante :
```bash
python gaussian_scrypt.py --image chemin/vers/image.jpg
```
Remplacez `chemin/vers/image.jpg` par le chemin de l’image que vous souhaitez traiter.
