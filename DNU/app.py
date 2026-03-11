import streamlit as st

st.set_page_config(
    page_title="One City. One ZIP Code. | National ZIP Code Advocacy Coalition",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get help": "mailto:afung@eastvaleca.gov",
        "About": "National ZIP Code Advocacy Coalition — Fighting for Geographic Integrity since 2023."
    }
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #F8F6F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stMarkdownContainer"] p { margin: 0; }
footer { visibility: hidden; }
.stButton > button { all: unset; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F8F6F0; }
::-webkit-scrollbar-thumb { background: #003366; border-radius: 3px; }

/* ── NAV ── */
.nav-wrapper {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(0,30,70,0.97);
    backdrop-filter: blur(12px);
    border-bottom: 2px solid #C9A84C;
    padding: 0 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
}
.nav-logo {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #C9A84C;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    line-height: 1.3;
}
.nav-links {
    display: flex;
    gap: 0.15rem;
    align-items: center;
}
.nav-link {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    color: rgba(255,255,255,0.8);
    text-decoration: none;
    padding: 0.45rem 0.9rem;
    border-radius: 4px;
    letter-spacing: 0.04em;
    transition: all 0.2s;
    cursor: pointer;
    border: 1px solid transparent;
}
.nav-link:hover { color: #C9A84C; border-color: rgba(201,168,76,0.3); background: rgba(201,168,76,0.08); }
.nav-link.active { color: #C9A84C; border-color: #C9A84C; background: rgba(201,168,76,0.1); }
.nav-cta {
    background: #C9A84C;
    color: #001E46 !important;
    font-weight: 700 !important;
    padding: 0.45rem 1.1rem !important;
}
.nav-cta:hover { background: #E8C46A !important; border-color: #E8C46A !important; color: #001E46 !important; }

/* ── HERO ── */
.hero-section {
    min-height: 92vh;
    background: linear-gradient(135deg, #001E46 0%, #003366 45%, #0A4A8A 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 6rem 2rem 4rem;
    position: relative;
    overflow: hidden;
}
.hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(201,168,76,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(201,168,76,0.06) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 1.5rem;
    opacity: 0.9;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3.5rem, 8vw, 7rem);
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.0;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}
.hero-title-accent {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3.5rem, 8vw, 7rem);
    font-weight: 900;
    color: #C9A84C;
    line-height: 1.0;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: rgba(255,255,255,0.75);
    max-width: 640px;
    margin: 0 auto 3rem;
    line-height: 1.7;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    gap: 0;
    justify-content: center;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}
.stat-pill {
    text-align: center;
    padding: 1.5rem 2.5rem;
    border: 1px solid rgba(201,168,76,0.3);
    border-right: none;
    background: rgba(0,0,0,0.2);
    backdrop-filter: blur(8px);
}
.stat-pill:first-child { border-radius: 8px 0 0 8px; }
.stat-pill:last-child { border-radius: 0 8px 8px 0; border-right: 1px solid rgba(201,168,76,0.3); }
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #C9A84C;
    line-height: 1;
    display: block;
}
.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    margin-top: 0.4rem;
    display: block;
}
.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}
.btn-primary {
    display: inline-block;
    background: #C9A84C;
    color: #001E46;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 0.85rem 2rem;
    border-radius: 6px;
    text-decoration: none;
    letter-spacing: 0.05em;
    transition: all 0.2s;
    border: 2px solid #C9A84C;
}
.btn-primary:hover { background: #E8C46A; border-color: #E8C46A; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(201,168,76,0.3); }
.btn-outline {
    display: inline-block;
    background: transparent;
    color: #FFFFFF;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.85rem 2rem;
    border-radius: 6px;
    text-decoration: none;
    letter-spacing: 0.05em;
    transition: all 0.2s;
    border: 2px solid rgba(255,255,255,0.4);
}
.btn-outline:hover { border-color: #C9A84C; color: #C9A84C; transform: translateY(-2px); }

/* ── SECTION CONTAINERS ── */
.section { padding: 5rem 2rem; max-width: 1200px; margin: 0 auto; }
.section-full { padding: 5rem 0; }
.section-dark { background: #001E46; }
.section-mid { background: #F0EDE4; }

.section-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 0.75rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 900;
    color: #001E46;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.section-title-light {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.section-sub {
    font-size: 1.05rem;
    color: #4A5568;
    max-width: 580px;
    line-height: 1.7;
}
.section-sub-light {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.65);
    max-width: 580px;
    line-height: 1.7;
}

/* ── PROBLEM CARDS ── */
.prob-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-top: 3rem; }
.prob-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #C9A84C;
    border-radius: 8px;
    padding: 2rem 1.75rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.prob-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,0,0,0.1); }
.prob-icon { font-size: 2rem; margin-bottom: 1rem; }
.prob-title { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #001E46; margin-bottom: 0.6rem; }
.prob-body { font-size: 0.9rem; color: #4A5568; line-height: 1.6; }

/* ── BILL TRACKER ── */
.bill-table { width: 100%; border-collapse: collapse; margin-top: 2rem; }
.bill-table th {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    padding: 0.75rem 1.25rem;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.bill-table td { padding: 1rem 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.07); font-size: 0.92rem; color: rgba(255,255,255,0.85); }
.bill-table tr:hover td { background: rgba(201,168,76,0.06); }
.bill-pill {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.pill-passed { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
.pill-stalled { background: rgba(251,191,36,0.15); color: #FBB624; border: 1px solid rgba(251,191,36,0.3); }
.pill-house { background: rgba(99,179,237,0.15); color: #63B3ED; border: 1px solid rgba(99,179,237,0.3); }

/* ── CASE STUDY CARDS ── */
.case-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; margin-top: 3rem; }
.case-card {
    background: #FFFFFF;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}
.case-card:hover { transform: translateY(-6px); box-shadow: 0 20px 48px rgba(0,0,0,0.15); }
.case-header { background: #001E46; padding: 1.5rem; position: relative; overflow: hidden; }
.case-header::after { content: ''; position: absolute; right: -20px; top: -20px; width: 100px; height: 100px; border-radius: 50%; background: rgba(201,168,76,0.1); }
.case-stat { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: #C9A84C; line-height: 1; }
.case-stat-lbl { font-size: 0.78rem; color: rgba(255,255,255,0.55); margin-top: 0.25rem; font-family: 'Space Mono', monospace; letter-spacing: 0.1em; }
.case-body { padding: 1.5rem; }
.case-tag { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.5rem; }
.case-title { font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700; color: #001E46; margin-bottom: 0.75rem; }
.case-desc { font-size: 0.88rem; color: #4A5568; line-height: 1.65; }

/* ── MEMBER CITY GRID ── */
.city-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 2rem; }
.city-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.25);
    color: #001E46;
    font-size: 0.82rem;
    padding: 0.4rem 0.85rem;
    border-radius: 100px;
    font-weight: 500;
    transition: all 0.15s;
}
.city-tag:hover { background: rgba(201,168,76,0.2); border-color: #C9A84C; }
.city-state { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #C9A84C; }

/* ── RESOURCE CARDS ── */
.resource-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2.5rem; }
.resource-card {
    display: flex;
    flex-direction: column;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1.75rem;
    transition: all 0.2s;
    text-decoration: none;
}
.resource-card:hover { border-color: #C9A84C; box-shadow: 0 8px 32px rgba(0,0,0,0.1); transform: translateY(-3px); }
.resource-icon { font-size: 1.75rem; margin-bottom: 1rem; }
.resource-type { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.4rem; }
.resource-title { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: #001E46; margin-bottom: 0.5rem; }
.resource-desc { font-size: 0.85rem; color: #6B7280; line-height: 1.5; flex: 1; }
.resource-link { margin-top: 1rem; font-size: 0.82rem; color: #0A4A8A; font-weight: 600; display: flex; align-items: center; gap: 0.3rem; }

/* ── ACTION STEPS ── */
.action-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 2.5rem; }
.action-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    padding: 1.75rem;
    position: relative;
    transition: background 0.2s, border-color 0.2s;
}
.action-card:hover { background: rgba(201,168,76,0.08); border-color: rgba(201,168,76,0.5); }
.action-num {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: rgba(201,168,76,0.15);
    line-height: 1;
    position: absolute;
    top: 1rem;
    right: 1.25rem;
}
.action-title { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.6rem; }
.action-body { font-size: 0.87rem; color: rgba(255,255,255,0.6); line-height: 1.6; }

/* ── QUOTE BLOCK ── */
.quote-block {
    border-left: 4px solid #C9A84C;
    padding: 1.5rem 2rem;
    background: rgba(201,168,76,0.06);
    border-radius: 0 8px 8px 0;
    margin: 2rem 0;
}
.quote-text { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #001E46; font-style: italic; line-height: 1.65; }
.quote-source { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: #6B7280; margin-top: 0.75rem; letter-spacing: 0.1em; }

/* ── TICKER ── */
.ticker-wrap { background: #C9A84C; overflow: hidden; padding: 0.6rem 0; }
.ticker-text { font-family: 'Space Mono', monospace; font-size: 0.75rem; font-weight: 700; color: #001E46; letter-spacing: 0.12em; white-space: nowrap; display: inline-block; animation: ticker 30s linear infinite; }
@keyframes ticker { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }

/* ── FOOTER ── */
.site-footer {
    background: #000D1F;
    padding: 4rem 2rem 2rem;
    color: rgba(255,255,255,0.5);
    font-size: 0.85rem;
}
.footer-grid { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 3rem; margin-bottom: 3rem; }
.footer-brand { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 900; color: #FFFFFF; margin-bottom: 0.75rem; }
.footer-tagline { color: rgba(255,255,255,0.4); line-height: 1.6; font-size: 0.87rem; }
.footer-heading { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; margin-bottom: 1rem; }
.footer-link { display: block; color: rgba(255,255,255,0.5); text-decoration: none; margin-bottom: 0.5rem; font-size: 0.87rem; transition: color 0.15s; }
.footer-link:hover { color: #C9A84C; }
.footer-divider { max-width: 1200px; margin: 0 auto 1.5rem; border: none; border-top: 1px solid rgba(255,255,255,0.08); }
.footer-bottom { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }

/* ── EMBED MAP ── */
.map-wrapper {
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid rgba(201,168,76,0.3);
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .nav-links { display: none; }
    .stat-pill { padding: 1rem 1.25rem; }
    .footer-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ── Import and run home page ─────────────────────────────────────────────────
from pages import home
home.render()
