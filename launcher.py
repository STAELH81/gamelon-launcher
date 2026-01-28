import os
import json
import hashlib
import requests
import subprocess
import sys
from pathlib import Path

# ⚙️ CONFIGURATION
MANIFEST_URL = "https://github.com/STAELH81/gamelon-launcher/releases/download/v1.0/manifest.json"
MINECRAFT_DIR = os.path.join(os.getenv('APPDATA'), '.minecraft')
MODS_DIR = os.path.join(MINECRAFT_DIR, 'mods')

def calculate_hash(filepath):
    """Calcule le hash SHA256 d'un fichier"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def download_file(url, destination, filename):
    """Télécharge un fichier avec barre de progression"""
    print(f"\n📥 Téléchargement: {filename}")
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        downloaded = 0
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    bar_length = 40
                    filled = int(bar_length * downloaded / total_size)
                    bar = '█' * filled + '░' * (bar_length - filled)
                    print(f'\r   [{bar}] {percent:.1f}% ({downloaded/(1024*1024):.1f}MB)', end='')
        
        print(f"\n   ✅ Téléchargé !")
        
    except Exception as e:
        print(f"\n   ❌ Erreur: {e}")
        sys.exit(1)

def get_manifest():
    """Récupère le manifest depuis GitHub"""
    print("🔍 Vérification des mises à jour...\n")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(MANIFEST_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Impossible de récupérer le manifest:")
        print(f"   {e}")
        print(f"\n💡 Vérifie que:")
        print(f"   - Tu as une connexion internet")
        print(f"   - La release GitHub existe bien")
        input("\nAppuie sur Entrée pour quitter...")
        sys.exit(1)

def sync_mods(manifest):
    """Synchronise les mods avec le serveur"""
    os.makedirs(MODS_DIR, exist_ok=True)
    
    print(f"📂 Dossier mods: {MODS_DIR}\n")
    
    # Mods requis
    required_mods = {mod['name']: mod for mod in manifest['mods']}
    
    # Supprimer les mods obsolètes
    if os.path.exists(MODS_DIR):
        for file in os.listdir(MODS_DIR):
            if file.endswith('.jar') and file not in required_mods:
                print(f"🗑️  Suppression: {file} (non présent dans le pack)")
                try:
                    os.remove(os.path.join(MODS_DIR, file))
                except Exception as e:
                    print(f"   ⚠️  Impossible de supprimer: {e}")
    
    # Vérifier et télécharger les mods
    total_mods = len(required_mods)
    updated = 0
    downloaded = 0
    
    for i, (mod_name, mod_info) in enumerate(required_mods.items(), 1):
        local_path = os.path.join(MODS_DIR, mod_name)
        local_hash = calculate_hash(local_path)
        
        print(f"\n[{i}/{total_mods}] {mod_name}")
        
        if local_hash != mod_info['hash']:
            if local_hash is None:
                print(f"   ➕ Mod manquant")
                downloaded += 1
            else:
                print(f"   🔄 Mise à jour nécessaire")
                updated += 1
            
            download_file(mod_info['url'], local_path, mod_name)
        else:
            print(f"   ✔️  À jour")
    
    print("\n" + "="*60)
    print(f"✅ Synchronisation terminée !")
    print(f"   📥 Téléchargés: {downloaded}")
    print(f"   🔄 Mis à jour: {updated}")
    print(f"   ✔️ Déjà à jour: {total_mods - downloaded - updated}")
    print("="*60 + "\n")

def launch_minecraft(manifest):
    """Lance Minecraft"""
    print(f"🚀 Lancement de Minecraft {manifest['minecraft_version']} (Fabric {manifest['fabric_version']})...\n")
    
    # Chemins possibles du launcher
    launcher_paths = [
        os.path.join(os.getenv('APPDATA'), '..', 'Local', 'Programs', 'Minecraft Launcher', 'MinecraftLauncher.exe'),
        os.path.join(os.getenv('ProgramFiles(x86)'), 'Minecraft Launcher', 'MinecraftLauncher.exe'),
        os.path.join(os.getenv('ProgramFiles'), 'Minecraft Launcher', 'MinecraftLauncher.exe'),
    ]
    
    launcher_found = False
    for launcher_path in launcher_paths:
        if os.path.exists(launcher_path):
            try:
                subprocess.Popen([launcher_path])
                launcher_found = True
                print("✅ Minecraft Launcher démarré !")
                print("\n💡 N'oublie pas de sélectionner le profil Fabric 1.21.10 dans le launcher !")
                break
            except Exception as e:
                print(f"⚠️  Erreur au lancement: {e}")
    
    if not launcher_found:
        print("⚠️  Launcher Minecraft non trouvé automatiquement")
        print(f"\n📂 Les mods sont installés dans:")
        print(f"   {MODS_DIR}")
        print(f"\n💡 Lance Minecraft manuellement avec le profil Fabric 1.21.10")
    
    input("\nAppuie sur Entrée pour quitter...")

def main():
    print("\n" + "="*60)
    print("      🎮 LAUNCHER MODPACK - Serveur Akliz 🎮")
    print("="*60 + "\n")
    
    # Récupérer le manifest
    manifest = get_manifest()
    
    print(f"📦 Modpack:")
    print(f"   🎯 Minecraft: {manifest['minecraft_version']}")
    print(f"   🧵 Fabric: {manifest['fabric_version']}")
    print(f"   📝 Mods: {len(manifest['mods'])}")
    
    # Synchroniser les mods
    sync_mods(manifest)
    
    # Lancer Minecraft
    launch_minecraft(manifest)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Annulé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuie sur Entrée pour quitter...")
        sys.exit(1)