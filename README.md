# Web3Ideathon-2026-archives-of-wisdom-demo

A Web3 knowledge platform demo where financial wisdom becomes verifiable, ownable, and tradable NFTs.  
Three-tier NFT structure (Course / Certificate / Badge) with Flask + Bootstrap.  
By Harchimedes — participant of 2026 HK Web3 Ideathon.

## Archives of Wisdom (AoW) — Flask Web3 NFT Demo

A simple Flask + Bootstrap 5 demo for **Archives of Wisdom (AoW)**: a Web3 knowledge platform with a **three-tier NFT structure**:

- **Tier 1: Course NFTs** (transferable) — buy, learn, resell  
- **Tier 2: Certificate NFTs** (soulbound) — on-chain resume  
- **Tier 3: Badge NFTs** (achievement rewards) — recognition

This is a **mock** app: no real blockchain calls, just **Flask session storage** to simulate wallet + progress.

## Project structure

```text
/app
  /static
    /css/style.css
    /js/main.js
    /img/ (optional placeholders)
  /templates
    base.html
    index.html
    courses.html
    dashboard.html
    course_detail.html
  app.py
requirements.txt
README.md
```

## How to run (Windows / PowerShell)

From the project root:

1. (First time) allow local scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. Create + activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the app:

```powershell
python .\app\app.py
```

5. Open in your browser:

- `http://127.0.0.1:5000/`

## Demo flows to try

- **Connect Wallet** (top-right) → shows mock address `0x7f...3dE2`
- Go to **Courses** → **Buy NFT** → “Success! NFT added to wallet”
- Open a course → **Complete Course** → “Certificate Minted!” + badge appears
- Go to **Dashboard** → owned Course NFT → **Resell** → “Listed for sale”

## Notes

- Session data resets if you clear cookies or change the Flask `secret_key`.
- This is intentionally minimal and easy to extend (real wallet connect, contract calls, database, etc.).

