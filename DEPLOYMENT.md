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
