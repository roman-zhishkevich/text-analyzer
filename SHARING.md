# Quick Sharing Guide

## 🎯 Simplest Method: GitHub + Streamlit Cloud

### Step 1: Prepare Your Code (5 minutes)

```bash
cd /Users/zhyshkevichr/text_analyzer

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Add Text Analyzer application"
```

### Step 2: Upload to GitHub (5 minutes)

1. Go to [github.com](https://github.com) and sign in
2. Click "+" → "New repository"
3. Name it: `text-analyzer`
4. Keep it **Public** (for free Streamlit deployment)
5. Don't initialize with README (we have one)
6. Click "Create repository"

7. Copy the commands GitHub shows and run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/text-analyzer.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud (5 minutes)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository**: `YOUR_USERNAME/text-analyzer`
   - **Branch**: `main`
   - **Main file path**: `src/app.py`
5. Click "Deploy"
6. Wait 2-3 minutes for deployment

### Step 4: Share! 🎉

Your app will be live at:
```
https://YOUR_USERNAME-text-analyzer.streamlit.app
```

Share this URL with anyone - they can use it immediately!

---

## 🏠 Alternative: Local Network Sharing

**If you just want to share with someone nearby:**

1. Start the app:
```bash
cd /Users/zhyshkevichr/text_analyzer
source venv/bin/activate
streamlit run src/app.py --server.address 0.0.0.0
```

2. Find your IP address:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

3. Share this URL with others on your network:
```
http://YOUR_IP:8501
```

**Note**: Your computer must stay on and connected to the same network.

---

## 📦 Alternative: Send Files Directly

**If the recipient knows Python:**

1. Zip the project:
```bash
cd /Users/zhyshkevichr
zip -r text-analyzer.zip text_analyzer -x "*venv/*" "*__pycache__/*" "*.pyc"
```

2. Send the zip file

3. Recipient instructions:
```bash
# Unzip the file
unzip text-analyzer.zip
cd text_analyzer

# Setup and run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run.sh
```

---

## ❓ Which Method Should I Use?

- **Want the easiest for recipient?** → Streamlit Cloud ✅
- **Want privacy/control?** → Cloud VPS or Docker
- **Quick demo to nearby person?** → Local Network
- **Sharing with developers?** → GitHub repository
- **No internet for recipient?** → Send files directly

**Recommended**: Streamlit Cloud (free, easy, professional)


