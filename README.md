# One City. One ZIP Code.
## National ZIP Code Advocacy Coalition — Advocacy Website

A full single-page advocacy website built with Streamlit.
Navy/gold theme, responsive layout, embedded coalition map,
legislative tracker, member city directory, and action hub.

---

## 📁 Project Structure

```
zipcoalition_site/
├── app.py                              ← Main entry point (run this)
├── requirements.txt                    ← Python dependencies
├── usa_municipalities_status_map.html  ← Interactive coalition map
├── .streamlit/
│   └── config.toml                     ← Theme + server config
└── pages/
    ├── __init__.py
    └── home.py                         ← Full website content & layout
```

---

## 🚀 Quick Start (VS Code)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run locally

```bash
streamlit run app.py
```

Opens at → http://localhost:8501

---

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. Push this folder to a **GitHub repository** (public or private)
2. Go to → https://share.streamlit.io
3. Click **"New app"**
4. Select your repo, branch, and set **Main file path** to `app.py`
5. Click **Deploy** — live in ~2 minutes

> **Important**: Make sure `usa_municipalities_status_map.html` is committed
> to the repo alongside `app.py`. Streamlit Cloud serves it from the same directory.

---

## ✏️ How to Edit Content

All content is in `pages/home.py` as Python lists/dicts at the top of the file.
No HTML knowledge required for data updates.

| What to update | Where in home.py |
|---|---|
| Member cities | `CITIES` list (line ~4) |
| Bill info / links | `BILLS` list |
| Problem cards | `PROBLEMS` list |
| Business case stats | `CASE_STUDIES` list |
| Resource links | `RESOURCES` list |
| Committee members | `COMMITTEE_MEMBERS` list |
| Action steps | `ACTIONS` list |

---

## 🎨 Design System

- **Fonts**: Playfair Display (headings) + DM Sans (body) + Space Mono (labels)
- **Colors**: Navy `#001E46` · Gold `#C9A84C` · Background `#F8F6F0`
- **Layout**: Full-width sections, max-width 1200px content container

---

## 📬 Contact

Alexander Fung — Economic Development Manager, City of Eastvale, CA
afung@eastvaleca.gov

Coalition website: https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/
# National-ZIP-Code-Advocacy-Coalition
