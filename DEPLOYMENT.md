# Deployment Guide

This guide explains how to share and deploy the Text Analyzer application.

## Option 1: Streamlit Cloud (Recommended)

**Best for**: Public sharing, easiest deployment

### Steps:
1. Create a GitHub account (if you don't have one)
2. Create a new repository on GitHub
3. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/text-analyzer.git
   git push -u origin main
   ```
4. Go to [share.streamlit.io](https://share.streamlit.io)
5. Sign in with GitHub
6. Click "New app"
7. Select your repository and branch
8. Set main file path: `src/app.py`
9. Click "Deploy"
10. Share the URL with others!

**Cost**: Free  
**Setup time**: 10-15 minutes  
**User experience**: Just click a link

---

## Option 2: Share Source Code

**Best for**: Users with technical skills

### Via GitHub:
1. Create a GitHub repository
2. Push your code
3. Share the repository URL
4. Users follow installation instructions in README.md

### Via Zip File:
1. Compress the project folder
2. Share via email, cloud storage, etc.
3. Users unzip and follow README.md

**Instructions for recipient**:
```bash
# 1. Extract files
# 2. Open terminal in project folder
# 3. Run:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py
```

**Cost**: Free  
**Setup time**: 5 minutes (for you), 10-15 minutes (for recipient)  
**User experience**: Requires Python knowledge

---

## Option 3: Run on Local Network

**Best for**: Sharing with people on the same network (office, home)

### Steps:
1. Find your local IP address:
   ```bash
   # macOS/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows:
   ipconfig
   ```
2. Run the app with network access:
   ```bash
   streamlit run src/app.py --server.address 0.0.0.0 --server.port 8501
   ```
3. Share the URL with others on your network:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```
   Example: `http://192.168.1.100:8501`

**Cost**: Free  
**Setup time**: 2 minutes  
**User experience**: Simple URL, but only works on same network  
**Note**: Your computer must stay on and running the app

---

## Option 4: Docker Container

**Best for**: Professional deployment, consistent environment

### Create Dockerfile:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0"]
```

### Build and run:
```bash
docker build -t text-analyzer .
docker run -p 8501:8501 text-analyzer
```

**Cost**: Free (or cloud hosting costs)  
**Setup time**: 30 minutes  
**User experience**: Depends on deployment

---

## Option 5: Cloud Deployment (Advanced)

### Heroku:
- [Heroku Streamlit Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku)
- Requires Procfile and setup.sh

### AWS, Google Cloud, Azure:
- Deploy as web service
- More complex but full control

### DigitalOcean, Linode:
- Deploy on VPS
- Install Python and dependencies
- Use systemd or supervisor to keep running

**Cost**: $5-20/month  
**Setup time**: 1-2 hours  
**User experience**: Professional, always online

---

## Comparison Table

| Option | Cost | Setup Time | User Setup | Best For |
|--------|------|------------|------------|----------|
| Streamlit Cloud | Free | 15 min | None | Public sharing |
| Source Code | Free | 5 min | 15 min | Developers |
| Local Network | Free | 2 min | None | Same network |
| Docker | Free* | 30 min | Varies | Professional |
| Cloud VPS | $5-20/mo | 1-2 hrs | None | Production |

*Deployment costs may apply

---

## Recommended Approach

**For most users**: Use **Streamlit Cloud** (Option 1)
- Easiest for both you and recipients
- No infrastructure management
- Automatic updates when you push to GitHub
- Free tier is generous

**For private/enterprise use**: Use **Cloud VPS** (Option 5)
- Full control and privacy
- Custom domain support
- Better for sensitive data

**For quick testing**: Use **Local Network** (Option 3)
- Instant setup
- Good for demos and testing


