# 🎮 Gamelon Launcher - Modpack Fabric 1.21.10

Launcher automatique pour le serveur Gamelon hébergé sur Akliz.

## 📦 Contenu du Modpack

- **Minecraft** : 1.21.10
- **Fabric** : 0.17.3
- **Nombre de mods** : 64

## 🚀 Installation pour les joueurs

1. **Télécharge le launcher** : [GamelonLauncher.exe](https://github.com/STAELH81/gamelon-launcher/releases/latest)
2. **Lance l'exe** : Double-clique sur `GamelonLauncher.exe`
3. **Attends** : Le launcher va télécharger automatiquement tous les mods (environ 200 MB)
4. **Configure Minecraft** :
   - Ouvre le Minecraft Launcher
   - Crée un nouveau profil avec **Fabric 1.21.10**
   - Lance le jeu !

## ✅ Le launcher fait tout automatiquement :

- ✅ Télécharge les mods manquants
- ✅ Met à jour les mods modifiés
- ✅ Supprime les anciens mods
- ✅ Vérifie l'intégrité avec des hash SHA256

## 🔄 Mises à jour

Quand le modpack est mis à jour, il suffit de relancer le launcher !
Il détectera automatiquement les changements et téléchargera seulement les nouveaux mods.

## 🛠️ Pour les développeurs

### Prérequis
- Python 3.9+
- `pip install -r requirements.txt`

### Générer le manifest
```bash
python generate_manifest.py
```

### Compiler le launcher
```bash
python -m PyInstaller --onefile --icon=server-icon.ico --name="GamelonLauncher" launcher.py
```

## 📝 Liste des mods

Voir la [release v1.2](https://github.com/STAELH81/gamelon-launcher/releases/tag/v1.2) pour la liste complète des 64 mods inclus.

## 🌐 Serveur

- **IP du serveur** : gamelonv4.g.akliz.net
- **Hébergement** : Akliz
- **Version** : Fabric 1.21.10

## 📞 Support

Pour toute question ou problème, contacte 'zambiasisacha@gmail.com'.

---

*Créé par STAELH81 à l'aide de Claude IA*