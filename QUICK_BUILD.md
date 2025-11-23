# Quick Build Guide - Desktop Executable

## 🚀 Super Simple: 3 Commands

```bash
cd /Users/zhyshkevichr/text_analyzer
source venv/bin/activate
./build_executable.sh
```

**That's it!** In 5-10 minutes you'll have: `dist/TextAnalyzer`

---

## 📦 Share With User

### Option 1: Send Executable Only

```bash
zip TextAnalyzer.zip dist/TextAnalyzer
```

Send `TextAnalyzer.zip` to user (200-300MB)

**User:**
1. Unzip
2. Double-click `TextAnalyzer`
3. Browser opens with app

### Option 2: Send Complete Package

```bash
# Create package
mkdir TextAnalyzer_Package
cp dist/TextAnalyzer TextAnalyzer_Package/
echo "Дважды кликните на TextAnalyzer для запуска" > TextAnalyzer_Package/README.txt

# Zip it
zip -r TextAnalyzer_Package.zip TextAnalyzer_Package/
```

Send `TextAnalyzer_Package.zip`

---

## ⚠️ What User Needs to Know

1. **First Run**: Downloads ~37MB of language data (happens once)
2. **Browser Opens**: App runs in default web browser
3. **Keep Window Open**: Don't close the terminal window (or hide console in build)
4. **macOS Security**: Right-click → Open (first time only)

---

## 📝 User Instructions (Copy & Paste)

```
ИНСТРУКЦИЯ:

1. Распакуйте архив
2. Дважды кликните на TextAnalyzer
3. Подождите несколько секунд
4. Браузер откроется автоматически
5. Используйте приложение!

При первом запуске загрузится ~37MB данных (происходит один раз).

Для остановки: закройте окно терминала или нажмите Ctrl+C.
```

---

## 🎯 Comparison

| Method | Size to Send | User Setup | Updates |
|--------|--------------|------------|---------|
| **Executable** | 200-300MB | None | Send new file |
| Source Code | 50KB | 10 minutes | Send files |

---

## 🔍 Technical Details

See `BUILD_EXECUTABLE.md` for:
- Troubleshooting
- Customization (icons, hide console)
- Platform-specific notes
- Creating installers (.dmg, .exe)

---

## ✅ You're Ready!

Run the build script and you'll have a shareable executable in minutes!


