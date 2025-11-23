# Building Desktop Executable

This guide explains how to create a single executable file for Text Analyzer.

## ⚠️ Important Notes

1. **File Size**: The executable will be ~200-300MB (includes Python, Streamlit, and all libraries)
2. **Still Uses Browser**: The app opens in your default web browser (it's still Streamlit)
3. **Platform-Specific**: Build on macOS for macOS, Windows for Windows, Linux for Linux
4. **First Run Slow**: Lemmatizer downloads data (~37MB) on first use

## 🛠️ Build Instructions

### Prerequisites

Make sure you have the app working first:
```bash
cd /Users/zhyshkevichr/text_analyzer
source venv/bin/activate
streamlit run src/app.py  # Test that it works
```

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

```bash
pyinstaller TextAnalyzer.spec
```

This will take 5-10 minutes.

### Step 3: Find Your Executable

The executable will be in:
```
dist/TextAnalyzer      (macOS/Linux)
dist/TextAnalyzer.exe  (Windows)
```

### Step 4: Test It

```bash
./dist/TextAnalyzer
```

Should:
1. Print "🚀 Запуск Text Analyzer..."
2. Open browser automatically
3. Show the app

## 📦 Distribution

### Option A: Just Send the Executable (Simple)

**Pros**: One file to send
**Cons**: Large file (200-300MB), first run downloads lemmatizer data

1. Compress the executable:
   ```bash
   zip TextAnalyzer.zip dist/TextAnalyzer
   ```

2. Send to user

3. User instructions:
   - Unzip
   - Double-click `TextAnalyzer`
   - Wait for browser to open

### Option B: Bundle Everything (Better)

Create a complete package:

```bash
# Create distribution folder
mkdir TextAnalyzer_App
cp dist/TextAnalyzer TextAnalyzer_App/
cp INSTALL_FOR_USER.md TextAnalyzer_App/README.md

# Zip it
zip -r TextAnalyzer_App.zip TextAnalyzer_App/
```

## 🔧 Troubleshooting

### Build Fails

**Error: "Module not found"**
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
pip install pyinstaller
```

**Error: "Permission denied"**
```bash
chmod +x desktop_launcher.py
```

### Executable Doesn't Start

**macOS: "Cannot be opened because the developer cannot be verified"**
```bash
# Right-click → Open (first time only)
# Or remove quarantine:
xattr -d com.apple.quarantine dist/TextAnalyzer
```

**Windows: Antivirus blocks it**
- Add exception in Windows Defender
- This is common with PyInstaller executables

### Browser Doesn't Open

The app should open automatically. If not:
1. Check console output for the port number
2. Manually open: `http://localhost:8501`

## 🎨 Customization

### Add an Icon

1. Create/download an icon file:
   - macOS: `.icns` file
   - Windows: `.ico` file

2. Update `TextAnalyzer.spec`:
   ```python
   icon='path/to/your/icon.icns'
   ```

3. Rebuild

### Hide Console Window

In `TextAnalyzer.spec`, change:
```python
console=True,  # Change to False
```

**Note**: Debugging is harder with console hidden.

## 📊 Expected Sizes

| Component | Size |
|-----------|------|
| Executable | ~250MB |
| Lemmatizer data (downloaded on first run) | ~37MB |
| **Total first run** | ~287MB |

## 🚀 Alternative: Create Installer

### macOS (.dmg)

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "Text Analyzer" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "TextAnalyzer.dmg" \
  "dist/"
```

### Windows (.exe installer)

Use Inno Setup or NSIS to create an installer.

## ✅ Final Checklist

Before distributing:
- [ ] Tested executable on clean machine
- [ ] Documented any first-run setup
- [ ] Included README/instructions
- [ ] File size is acceptable
- [ ] Antivirus doesn't flag it (false positive common)

## 💡 Tips

1. **Test on target OS**: Always test on the same OS as your user
2. **Compress**: Use 7zip or similar for better compression
3. **Cloud storage**: For large files, use Google Drive, Dropbox, etc.
4. **Version naming**: `TextAnalyzer-v1.0-macOS.zip`

## 🤔 Still Too Complex?

If this seems complicated, the original approach is simpler:
- Send the project folder (50KB)
- User installs Python + dependencies (10 minutes)
- More flexible for updates

Desktop executable is convenient but adds complexity.


