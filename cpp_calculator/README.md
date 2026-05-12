# ProCalcX — Calculatrice Desktop Professionnelle (Qt6 / C++20)

ProCalcX est une application de calcul moderne, modulaire et évolutive.
Ce projet est structuré pour offrir de bonnes performances, un code maintenable, et une base solide pour intégrer tous les modes avancés (scientifique, programmeur, convertisseur, notes math, historique, graphe, solveur).

---

## ✨ Aperçu des fonctionnalités

- Interface desktop moderne (thème sombre, navigation latérale, architecture responsive)
- Moteur d'expressions C++ (extensible)
- Services persistants JSON :
  - paramètres utilisateur,
  - historique des calculs horodaté,
  - notes/formules.
- Base prête pour : plugins, graphe de fonctions, solveur d'équations, thèmes personnalisés.

---

## 🧱 Prérequis

### Linux (Ubuntu/Debian)
Installez les dépendances système :

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  cmake \
  ninja-build \
  qt6-base-dev \
  qt6-tools-dev \
  qt6-charts-dev \
  nlohmann-json3-dev
```

### Windows 10/11
1. Installer **Visual Studio 2022** (workload **Desktop development with C++**).
2. Installer **CMake** (ou utiliser celui intégré à Visual Studio).
3. Installer **Qt 6.x MSVC 64-bit** via Qt Online Installer.
4. Installer `nlohmann_json` :
   - via **vcpkg** (recommandé), ou
   - via **conan**.

---

## 🚀 Installation & Build — Linux (Tutoriel pas à pas)

> Les commandes ci-dessous sont à exécuter depuis le dossier du projet `cpp_calculator`.

### 1) Se placer dans le dossier projet
```bash
cd cpp_calculator
```

### 2) Générer les fichiers de build (CMake)
```bash
cmake -S . -B build -G Ninja
```

### 3) Compiler
```bash
cmake --build build -j
```

### 4) Lancer l'application
```bash
./build/ProCalcX
```

### 5) (Optionnel) Build Release optimisé
```bash
cmake -S . -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build-release -j
./build-release/ProCalcX
```

---

## 🪟 Installation & Build — Windows (Tutoriel pas à pas)

### Option A — Visual Studio + CMake (recommandé)

1. Ouvrir **x64 Native Tools Command Prompt for VS 2022**.
2. Aller dans le dossier du projet :
```powershell
cd cpp_calculator
```
3. Configurer CMake (adapter le chemin Qt) :
```powershell
cmake -S . -B build -G "Ninja" -DCMAKE_PREFIX_PATH="C:/Qt/6.8.0/msvc2022_64"
```
4. Compiler :
```powershell
cmake --build build --config Release
```
5. Lancer :
```powershell
.\build\ProCalcX.exe
```

### Option B — Intégration vcpkg pour `nlohmann_json`

Si nécessaire, installer la dépendance :
```powershell
vcpkg install nlohmann-json:x64-windows
```
Puis configurer CMake avec le toolchain :
```powershell
cmake -S . -B build -G "Ninja" \
  -DCMAKE_PREFIX_PATH="C:/Qt/6.8.0/msvc2022_64" \
  -DCMAKE_TOOLCHAIN_FILE="C:/vcpkg/scripts/buildsystems/vcpkg.cmake"
```

---

## 🧪 Vérification rapide après installation

- L'application s'ouvre avec une **sidebar** contenant les modes (Basic, Scientific, Programmer, Converter, Notes, History, Graph, Solver).
- Le mode **Basic** permet de saisir une expression simple et d'afficher le résultat.
- Un calcul validé est ajouté à l'historique local (`data/history.json`).

---

## 🗂️ Structure du projet

```text
cpp_calculator/
├─ CMakeLists.txt
├─ README.md
├─ assets/                 # icônes, sons, animations
├─ themes/                 # thèmes QSS
├─ data/                   # stockage local JSON
└─ src/
   ├─ app/                 # bootstrap & orchestration
   ├─ core/                # moteur de calcul/parser
   ├─ services/            # settings/history/notes
   ├─ modules/             # logique des modes (extensible)
   └─ ui/                  # main window, pages, widgets
```

---

## ⚙️ Dépannage

### Erreur : `Could not find Qt6Config.cmake`
- Vérifier que Qt6 dev est installé.
- Passer explicitement `-DCMAKE_PREFIX_PATH` vers le dossier Qt (ex: `.../msvc2022_64` sous Windows).

### Erreur : package `nlohmann_json` introuvable
- Linux : installer `nlohmann-json3-dev`.
- Windows : utiliser `vcpkg install nlohmann-json:x64-windows` et toolchain CMake.

### L'application ne démarre pas après build Windows
- Vérifier que les DLL Qt sont accessibles (windeployqt peut être utilisé si nécessaire).

---

## 🛣️ Roadmap (prochaines étapes)

- Parser scientifique complet (fonctions trigonométriques, parenthèses, priorité opérateurs)
- Mode programmeur avancé (bitwise, shift, conversion de base en temps réel)
- Convertisseur d'unités riche + architecture API devises
- Éditeur notes math (markdown-like + recherche + favoris)
- Grapheur mini (Qt Charts) et solveur d'équations
- Système plugins + thèmes personnalisés + restauration de session

---

## 📄 Licence

Voir le fichier `LICENSE` à la racine du dépôt principal.
