import os
import json
import hashlib

# ⚙️ CONFIGURATION - Modifie ces valeurs
MODS_FOLDER = "./mods"
GITHUB_USER = "STAELH81"
REPO_NAME = "gamelon-launcher"
VERSION = "v1.0"
BASE_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/releases/download/{VERSION}"

# Info sur ton serveur
MINECRAFT_VERSION = "1.21.10"
FABRIC_VERSION = "0.17.3"

def calculate_hash(filepath):
    """Calcule le hash SHA256 d'un fichier"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest():
    """Génère le manifest.json depuis le dossier mods"""
    print("🔨 Génération du manifest...\n")
    
    if not os.path.exists(MODS_FOLDER):
        print(f"❌ Le dossier {MODS_FOLDER} n'existe pas !")
        print("   Crée un dossier 'mods' et mets tes fichiers .jar dedans")
        return
    
    mods = []
    
    # Parcourir tous les fichiers .jar
    jar_files = [f for f in os.listdir(MODS_FOLDER) if f.endswith('.jar')]
    
    if not jar_files:
        print(f"❌ Aucun fichier .jar trouvé dans {MODS_FOLDER}")
        return
    
    print(f"📦 {len(jar_files)} mods trouvés\n")
    
    for i, filename in enumerate(sorted(jar_files), 1):
        filepath = os.path.join(MODS_FOLDER, filename)
        file_hash = calculate_hash(filepath)
        
        mod_info = {
            "name": filename,
            "hash": file_hash,
            "url": f"{BASE_URL}/{filename}"
        }
        mods.append(mod_info)
        print(f"[{i:2d}/{len(jar_files)}] ✅ {filename}")
        print(f"        Hash: {file_hash[:16]}...")
    
    # Créer le manifest complet
    manifest = {
        "minecraft_version": MINECRAFT_VERSION,
        "loader": "fabric",
        "fabric_version": FABRIC_VERSION,
        "mods": mods
    }
    
    # Sauvegarder le manifest
    manifest_path = "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Manifest généré avec succès !")
    print(f"📁 Fichier: {manifest_path}")
    print(f"📊 Nombre de mods: {len(mods)}")
    print(f"\n💡 Prochaine étape :")
    print(f"   1. Upload tous les .jar + manifest.json sur GitHub Release")
    print(f"   2. Assure-toi que le tag de la release est bien '{VERSION}'")

if __name__ == "__main__":
    generate_manifest()