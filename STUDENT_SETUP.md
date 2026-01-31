# Student Setup (Session 3)

You do **not** need coding experience.
You do **not** need to install Docker.

This session is designed to work on **Windows and Mac** using **GitHub Codespaces**.

---

## 0) What you will do in class
You will:
- Open a ready-to-run repository
- Run the system in **mock mode** (no API key needed)
- Observe how governance and monitoring work
- Run a **CrewAI multi-agent orchestration demo** (mock mode works; live mode optional)

---

## 1) Install Cursor (5 minutes)
1. Go to https://cursor.sh
2. Download and install Cursor (Free is fine)
3. Open Cursor once after installing

---

## 2) Create / log in to GitHub (5 minutes)
1. Go to https://github.com
2. Sign up or log in
3. Confirm you can access GitHub from your laptop

---

## 3) Open the repo in GitHub Codespaces (10 minutes)
1. Open the repo link your instructor shares
2. Click the green **Code** button
3. Click the **Codespaces** tab
4. Click **Create new codespace**
5. Wait for the browser editor to load

If this step is blocked on your laptop, you can still follow in **observe mode**.

---

## 4) Pre-install dependencies (recommended before class)
In the Codespaces terminal, run:

```bash
python -m pip install -r requirements.txt
cp -n .env.example .env || true
python scripts/smoke_test.py
```

If you see **SMOKE TEST PASSED**, you’re ready.

---

## 5) Optional: Live mode API key
Mock mode works without any API key.

If you want live LLM outputs:
1. Put your key in `.env`:
   - `OPENAI_API_KEY=...`
2. Run:
   - `python run.py --mode live --data data/tickets_sample.json`

If live mode fails, switch back to mock mode.
