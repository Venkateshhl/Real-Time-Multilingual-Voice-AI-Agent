# Deployment Guide: Get Your Public Link

This guide walks you through deploying your Multilingual Voice AI Chatbot so anyone can access it via a public URL.

---

## Option A: Railway (Recommended – Easy & Free Tier)

### Step 1: Push Your Code to GitHub

1. Open PowerShell in your project folder:
   ```powershell
   cd "c:\Users\venka\OneDrive\Desktop\multilaungauge chatbot"
   ```

2. Stage and commit your deployment changes:
   ```powershell
   git add run.py frontend/index.html railway.toml
   git commit -m "Configure deployment with full frontend"
   ```

3. Push to GitHub:
   ```powershell
   git push origin main
   ```
   *(If prompted, sign in to GitHub or use a Personal Access Token)*

---

### Step 2: Create Railway Account

1. Go to **https://railway.app**
2. Click **Login**
3. Choose **Login with GitHub**
4. Authorize Railway to access your GitHub account

---

### Step 3: Deploy from GitHub

1. On Railway dashboard, click **New Project**
2. Select **Deploy from GitHub repo**
3. If asked to install Railway on GitHub, click **Configure GitHub App** and select your account
4. Choose the repo: **Venkateshhl/Real-Time-Multilingual-Voice-AI-Agent** (or your repo name)
5. Railway will auto-detect your Dockerfile and start building

---

### Step 4: Add Environment Variable

1. Click on your deployed service
2. Go to the **Variables** tab
3. Click **+ New Variable**
4. Add:
   - **Variable:** `OPENAI_API_KEY`
   - **Value:** your OpenAI API key (e.g. `sk-...`)
5. Save – Railway will automatically redeploy

---

### Step 5: Generate Public Domain

1. Stay in your service
2. Go to the **Settings** tab
3. Scroll to **Networking** → **Public Networking**
4. Click **Generate Domain**
5. Railway will assign a URL like: `https://real-time-multilingual-voice-ai-agent-production.up.railway.app`

**That URL is your public link.** Share it and anyone can use your chatbot.

---

## Option B: Render

### Step 1: Push Code to GitHub (same as above)

---

### Step 2: Create Render Account

1. Go to **https://render.com**
2. Click **Get Started**
3. Sign up with **GitHub**

---

### Step 3: Create Web Service

1. Click **Dashboard** → **New +** → **Web Service**
2. Connect your GitHub repo (authorize if needed)
3. Select your repository
4. Use these settings:
   - **Name:** `multilang-voice-chatbot` (or any name)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
5. Click **Advanced** and add environment variable:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** your API key
6. Click **Create Web Service**

---

### Step 4: Get Your Public Link

Render will build and deploy. When done, you'll see a URL like:

`https://multilang-voice-chatbot.onrender.com`

That is your public link.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Ensure `requirements.txt` exists and all dependencies are listed |
| App crashes on start | Check **Logs** in Railway/Render; verify `OPENAI_API_KEY` is set |
| WebSocket not connecting | Ensure you're using HTTPS; WebSocket auto-upgrades to WSS |
| 502 Bad Gateway | Service may be starting; wait 1–2 minutes and refresh |

---

## After Deployment

- **Health check:** Visit `https://your-url/api/health` to verify the API is running
- **Chat UI:** Visit `https://your-url/` for the voice chatbot interface
- **Free tier limits:** Railway and Render may sleep inactive services; first load can take 30–60 seconds
