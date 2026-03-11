import streamlit as st

st.set_page_config(
    page_title="One City. One ZIP Code. | National ZIP Code Advocacy Coalition",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get help": "mailto:afung@eastvaleca.gov"}
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --blue:#1A3A6B; --blue-m:#2251A3; --blue-lt:#EEF3FB;
  --red:#C0181B;  --red-m:#E02020;  --red-lt:#FEF2F2; --red-dark:#7F1518;
  --white:#FFFFFF; --g50:#F8F9FB; --g100:#F1F3F7; --g200:#E2E6EE;
  --g300:#C8CFD8; --g400:#9AA3B0; --g500:#6B7585; --g900:#0F1623;
  --text:#1A2233; --muted:#505A6E; --border:#D6DCE8;
  --green:#15803D; --green-lt:#F0FDF4;
  --amber:#B45309; --amber-lt:#FFFBEB;
}

/* ── STREAMLIT RESET ──────────────────────────────────────────────────────── */
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{
  background:var(--white)!important; font-family:'Inter',sans-serif!important;
  color:var(--text)!important;
}
[data-testid="stHeader"],[data-testid="stSidebar"]{display:none!important;}
[data-testid="stMainBlockContainer"],.block-container,.main .block-container{
  padding:0!important; max-width:100%!important;
}
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"]{gap:0!important;}
[data-testid="stMarkdownContainer"]{width:100%!important;}
[data-testid="stMarkdownContainer"] p{margin:0;}
[data-testid="stMarkdownContainer"] div{max-width:100%;}
.element-container{margin:0!important;padding:0!important;width:100%!important;}
.stMarkdown{width:100%!important;}
footer{visibility:hidden;}
.stButton>button{all:unset;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-thumb{background:var(--blue);border-radius:99px;}

/* ── NAV ──────────────────────────────────────────────────────────────────── */
.nav{
  position:sticky;top:0;z-index:9999;background:var(--lightblue);
  height:60px;display:flex;align-items:center;
  padding:0 3.5rem;justify-content:space-between;
  border-bottom:1px solid rgba(255,255,255,0.07);
}
.nav-brand{display:flex;align-items:center;gap:0.7rem;text-decoration:none;}
.nav-seal{width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,0.12);
  border:2px solid rgba(255,255,255,0.25);display:flex;align-items:center;
  justify-content:center;font-size:1rem;flex-shrink:0;}
.nav-name{font-weight:800;font-size:0.9rem;color:var(--blue);line-height:1.2;}
.nav-sub{font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:var(--blue);
  letter-spacing:0.08em;text-transform:uppercase;display:block;}
.nav-links{display:flex;align-items:center;gap:0.1rem;}
.nav-a{font-size:0.82rem;font-weight:500;color:rgba(255,255,255,0.72);text-decoration:none;
  padding:0.4rem 0.75rem;border-radius:4px;transition:all 0.15s;white-space:nowrap;}
.nav-a:hover{background:rgba(255,255,255,0.1);color:var(--white);}
.nav-urgent{display:inline-flex;align-items:center;gap:0.45rem;background:var(--red);
  color:var(--white)!important;font-size:0.82rem;font-weight:700;padding:0.45rem 1.1rem;
  border-radius:5px;text-decoration:none;margin-left:0.85rem;transition:background 0.15s;}
.nav-urgent:hover{background:var(--red-m);}
.nav-dot{width:7px;height:7px;border-radius:50%;background:#FCA5A5;
  animation:pulse 1.5s ease-in-out infinite;flex-shrink:0;}

/* ── ALERT BAR ────────────────────────────────────────────────────────────── */
.alert-bar{background:var(--red-dark);padding:0.55rem 3.5rem; position: relative; /* Relative position is required for z-index to work */
  z-index: 9998;      /* One layer below the Nav, but above the Hero */
  background: var(--red-dark);
  padding: 0.55rem 3.5rem;
  display:flex;align-items:center;gap:1.1rem;font-size:0.82rem;}
.alert-pill{background:var(--white);color:var(--red-dark);font-family:'IBM Plex Mono',monospace;
  font-size:0.6rem;font-weight:700;letter-spacing:0.1em;padding:0.22rem 0.7rem;
  border-radius:3px;white-space:nowrap;flex-shrink:0;}
.alert-msg{color:rgba(255,255,255,0.9);}
.alert-link{color:#FCA5A5;font-weight:700;text-decoration:none;}
.alert-link:hover{color:var(--white);text-decoration:underline;}

/* ── HERO — full-width dark, headline + stat bar ──────────────────────────── */
.hero{
  background:var(--g900);padding:7rem 0 0;
  position:relative;overflow:hidden;
}
.hero::before{content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse 55% 70% at 70% 40%,rgba(34,81,163,0.35) 0%,transparent 65%),
    radial-gradient(ellipse 30% 50% at 5% 80%,rgba(192,24,27,0.14) 0%,transparent 60%);
  pointer-events:none;}
.hero::after{content:'';position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,0.07) 1px,transparent 1px);
  background-size:32px 32px;pointer-events:none;}
.hero-inner{
  max-width:1160px;margin:0 auto;padding:0 3.5rem;
  position:relative;z-index:1;
}
.hero-kicker{
  display:inline-flex;align-items:center;gap:0.5rem;
  background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.14);
  border-radius:99px;padding:0.32rem 0.9rem 0.32rem 0.5rem;margin-bottom:2rem;
}
.hero-dot{width:7px;height:7px;border-radius:50%;background:#4ADE80;
  box-shadow:0 0 8px #4ADE80;flex-shrink:0;animation:pulse 2s ease-in-out infinite;}
.hero-kicker-t{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
  letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.65);}
.hero-h1{
  font-size:clamp(3rem,5.5vw,5.2rem);font-weight:900;color:var(--white);
  line-height:1.04;letter-spacing:-0.035em;margin-bottom:1.5rem;
  max-width:820px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            
}
.hero-h1-red{color:#FCA5A5;}
.hero-sub{
  font-size:clamp(1rem,1.6vw,1.15rem);color:rgba(255,255,255,0.62);
  max-width:580px;line-height:1.85;margin-bottom:2.5rem;font-weight:400;
}
.hero-ctas{display:flex;gap:0.85rem;flex-wrap:wrap;margin-bottom:0;}
.btn-hero-red{
  display:inline-flex;align-items:center;gap:0.5rem;
  background:var(--red);color:var(--white);font-weight:700;font-size:0.95rem;
  padding:0.9rem 2rem;border-radius:6px;text-decoration:none;
  border:2px solid var(--red);transition:all 0.2s;
  animation:redpulse 2.5s ease-in-out infinite;
}
.btn-hero-red:hover{background:var(--red-m);border-color:var(--red-m);
  transform:translateY(-2px);box-shadow:0 10px 24px rgba(192,24,27,0.4);animation:none;}
.btn-hero-ghost{display:inline-block;background:transparent;color:rgba(255,255,255,0.78);
  font-weight:600;font-size:0.95rem;padding:0.9rem 2rem;border-radius:6px;
  text-decoration:none;border:2px solid rgba(255,255,255,0.22);transition:all 0.2s;}
.btn-hero-ghost:hover{border-color:rgba(255,255,255,0.55);color:var(--white);}

/* Stat bar — full-width band at bottom of hero */
.hero-statbar{
  margin-top:4.5rem;
  background:rgba(255,255,255,0.04);
  border-top:1px solid rgba(255,255,255,0.08);
  display:grid;
  grid-template-columns:repeat(5,1fr);
}
.hst{
  padding:2rem 2.5rem;
  border-right:1px solid rgba(255,255,255,0.07);
  display:flex;flex-direction:column;
}
.hst:last-child{border-right:none;}
.hst-n{
  font-size:2.6rem;font-weight:900;color:var(--white);
  line-height:1;letter-spacing:-0.03em;margin-bottom:0.4rem;
}
.hst-l{
  font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
  letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.38);
}

/* ── SECTION LAYOUT ───────────────────────────────────────────────────────── */
.section{padding:5.5rem 0;}
.section-g{background:var(--g50);}
.section-w{background:var(--white);}
.section-blue{background:var(--blue);}
.inner{max-width:1160px;margin:0 auto;padding:0 3.5rem;}
.sec-divider{height:1px;background:var(--border);}

/* ── SECTION HEADER — accent-line style ──────────────────────────────────── */
.sec-label{
  display:block;
  font-family:'IBM Plex Mono',monospace;font-size:0.7rem;font-weight:600;
  letter-spacing:0.22em;text-transform:uppercase;color:var(--blue-m);
  padding-top:1rem;border-top:3px solid var(--blue-m);
  width:fit-content;margin-bottom:1rem;
}
.sec-label-red{color:var(--red);border-top-color:var(--red);}
.sec-label-green{color:var(--green);border-top-color:var(--green);}
.sec-label-amber{color:var(--amber);border-top-color:var(--amber);}
.sec-label-light{color:rgba(255,255,255,0.6);border-top-color:rgba(255,255,255,0.35);}
.sec-h{
  font-size:clamp(2rem,3.8vw,3rem);font-weight:800;color:var(--blue);
  line-height:1.1;letter-spacing:-0.028em;margin-bottom:1.1rem;
}
.sec-h-white{color:var(--white);}
.sec-lead{
  font-size:1.0625rem;color:var(--muted);line-height:1.85;
  max-width:580px;letter-spacing:0.004em;
}
.sec-lead-light{color:rgba(255,255,255,0.65);}

/* ── TRACKER — bill progress bar ──────────────────────────────────────────── */
.tracker-band{
  background:var(--g50);border-top:3px solid var(--blue);
  padding:2.75rem 0;
}
.tracker-inner{max-width:1160px;margin:0 auto;padding:0 3.5rem;}
.tracker-label{
  font-family:'IBM Plex Mono',monospace;font-size:0.65rem;font-weight:600;
  letter-spacing:0.18em;text-transform:uppercase;color:var(--blue-m);
  display:block;margin-bottom:1.5rem;
}
.tracker-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.1rem;}
.tcard{
  background:var(--white);border:1px solid var(--border);border-radius:10px;
  padding:1.4rem 1.5rem;position:relative;overflow:hidden;
}
.tcard-passed{border-left:4px solid var(--green);}
.tcard-stalled{border-left:4px solid var(--amber);}
.tcard-num{position:absolute;top:1rem;right:1.1rem;font-size:1.9rem;font-weight:900;
  color:rgba(26,58,107,0.06);font-family:'Inter',sans-serif;line-height:1;}
.tcard-id{font-family:'IBM Plex Mono',monospace;font-size:1.15rem;font-weight:600;
  color:var(--blue);margin-bottom:0.35rem;}
.tcard-author{font-size:0.82rem;color:var(--muted);margin-bottom:0.6rem;line-height:1.4;}
.tbadge{display:inline-flex;align-items:center;padding:0.22rem 0.65rem;
  border-radius:99px;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;font-weight:600;
  letter-spacing:0.04em;}
.tbadge-g{background:var(--green-lt);color:var(--green);border:1px solid #BBF7D0;}
.tbadge-a{background:var(--amber-lt);color:var(--amber);border:1px solid #FDE68A;}
.tcard-note{font-size:0.78rem;color:var(--g500);margin-top:0.65rem;line-height:1.55;}
.tprog{margin-top:0.9rem;height:4px;background:var(--g200);border-radius:99px;overflow:hidden;}
.tprog-fill{height:100%;border-radius:99px;}
.tprog-green{background:var(--green);}
.tprog-amber{background:var(--amber);}

/* ── PROBLEM CARDS — 4 up ─────────────────────────────────────────────────── */
.prob-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;margin-top:3rem;}
.pcard{
  background:var(--white);border:1px solid var(--border);
  border-top:4px solid var(--blue);border-radius:0 0 10px 10px;
  padding:1.75rem;transition:box-shadow 0.2s,transform 0.2s;
}
.pcard:hover{box-shadow:0 16px 32px rgba(0,0,0,0.09);transform:translateY(-3px);}
.pcard-red{border-top-color:var(--red);}
.pcard-amber{border-top-color:var(--amber);}
.pcard-blue{border-top-color:var(--blue-m);}
.pcard-green{border-top-color:var(--green);}
.pcard-icon{font-size:2.1rem;margin-bottom:1.1rem;display:block;}
.pcard-t{font-size:1.05rem;font-weight:800;color:var(--blue);
  margin-bottom:0.65rem;letter-spacing:-0.01em;}
.pcard-b{font-size:0.9rem;color:var(--muted);line-height:1.8;}
.pcard-stat{font-size:2rem;font-weight:900;color:var(--red);
  letter-spacing:-0.02em;display:block;margin-top:1.1rem;line-height:1;}
.pcard-stat-lbl{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
  color:var(--g400);letter-spacing:0.07em;display:block;margin-top:0.3rem;}

/* ── CASE STUDY CARDS ─────────────────────────────────────────────────────── */
.case-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:3rem;}
.ccase{border:1px solid var(--border);border-top:4px solid var(--blue-m);
  border-radius:0 0 12px 12px;overflow:hidden;background:var(--white);
  transition:box-shadow 0.2s,transform 0.2s;}
.ccase:hover{box-shadow:0 16px 32px rgba(0,0,0,0.09);transform:translateY(-4px);}
.ccase-top{background:var(--blue);padding:1.75rem 1.85rem 1.5rem;position:relative;overflow:hidden;}
.ccase-top::after{content:'';position:absolute;width:120px;height:120px;border-radius:50%;
  background:rgba(255,255,255,0.05);right:-25px;top:-25px;}
.ccase-stat{font-size:3.2rem;font-weight:900;color:var(--white);line-height:1;letter-spacing:-0.035em;}
.ccase-sub{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
  letter-spacing:0.07em;color:rgba(255,255,255,0.42);margin-top:0.4rem;}
.ccase-body{padding:1.6rem 1.85rem;}
.ccase-lbl{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.16em;
  text-transform:uppercase;color:var(--blue-m);margin-bottom:0.4rem;}
.ccase-t{font-size:1.08rem;font-weight:800;color:var(--blue);margin-bottom:0.75rem;
  letter-spacing:-0.01em;}
.ccase-d{font-size:0.9rem;color:var(--muted);line-height:1.82;}
.ccase-src{font-size:0.74rem;color:var(--g400);margin-top:1rem;font-style:italic;}

/* ── BILL TRACKER CARDS ───────────────────────────────────────────────────── */
.bill-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-top:3rem;}
.bcard{border:1px solid var(--border);border-radius:10px;padding:1.6rem 1.75rem;
  background:var(--white);transition:box-shadow 0.15s;}
.bcard:hover{box-shadow:0 4px 18px rgba(0,0,0,0.07);}
.bcard-p{border-left:4px solid var(--green);}
.bcard-s{border-left:4px solid var(--amber);}
.bill-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.75rem;}
.bill-id{font-family:'IBM Plex Mono',monospace;font-size:1.25rem;font-weight:600;color:var(--blue);}
.badge{display:inline-flex;align-items:center;padding:0.22rem 0.65rem;border-radius:99px;
  font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;letter-spacing:0.05em;}
.b-g{background:var(--green-lt);color:var(--green);border:1px solid #BBF7D0;}
.b-a{background:var(--amber-lt);color:var(--amber);border:1px solid #FDE68A;}
.bill-author{font-size:0.9rem;color:var(--muted);margin-bottom:0.4rem;}
.bill-cities{font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
  color:var(--g400);margin-bottom:0.75rem;}
.bill-note{font-size:0.87rem;color:var(--muted);line-height:1.68;}
.bill-link{display:inline-block;margin-top:1rem;font-size:0.83rem;font-weight:600;
  color:var(--blue-m);text-decoration:none;}
.bill-link:hover{text-decoration:underline;}
.callout{border-radius:10px;padding:1.5rem 1.85rem;margin-top:2rem;border:1px solid;}
.callout-a{background:var(--amber-lt);border-color:#FDE68A;}
.callout-t{font-weight:800;color:var(--blue);margin-bottom:0.4rem;font-size:0.95rem;}
.callout-b{font-size:0.9rem;color:var(--muted);line-height:1.75;}
.committee-grid{display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1.5rem;}
.cm{display:flex;align-items:center;gap:0.4rem;padding:0.4rem 0.85rem;border-radius:6px;
  border:1px solid var(--border);background:var(--white);font-size:0.84rem;
  color:var(--text);transition:all 0.15s;}
.cm:hover{border-color:var(--blue);background:var(--blue-lt);}
.cm-chair{border-color:var(--amber);background:var(--amber-lt);font-weight:700;}
.pr{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--red);font-weight:600;}
.pd{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--blue-m);font-weight:600;}

/* ── MAP SECTION — uses .inner for consistent padding ─────────────────────── */
.map-frame{border:1px solid var(--border);border-radius:12px;overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.06);margin-top:2.5rem;}

/* ── TIMELINE STEPPER ─────────────────────────────────────────────────────── */
.timeline{
  position:relative;margin-top:3.5rem;
  padding-left:0;
}
/* Vertical spine */
.timeline::before{
  content:'';position:absolute;left:27px;top:0;bottom:0;width:2px;
  background:linear-gradient(to bottom,var(--blue-lt),var(--blue-lt) 90%,transparent);
  z-index:0;
}
.tl-item{
  display:flex;gap:2rem;padding-bottom:2.75rem;position:relative;
}
.tl-item:last-child{padding-bottom:0;}
/* Left column: number circle */
.tl-left{flex-shrink:0;z-index:1;}
.tl-num{
  width:56px;height:56px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:1rem;letter-spacing:-0.02em;
  background:var(--white);border:2px solid var(--border);color:var(--g400);
  box-shadow:0 2px 8px rgba(0,0,0,0.06);transition:all 0.2s;flex-shrink:0;
}
.tl-urgent .tl-num{
  background:var(--red);border-color:var(--red);color:var(--white);
  animation:redring 2s ease-in-out infinite;
}
/* Right column: card */
.tl-card{
  flex:1;background:var(--white);border:1px solid var(--border);
  border-radius:12px;padding:1.75rem 2rem;
  transition:box-shadow 0.2s;
}
.tl-card:hover{box-shadow:0 8px 28px rgba(0,0,0,0.08);}
.tl-urgent .tl-card{
  border-color:rgba(192,24,27,0.25);
  border-left:4px solid var(--red);
}
.tl-phase{
  font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;
  letter-spacing:0.18em;text-transform:uppercase;
  color:var(--blue-m);background:var(--blue-lt);
  padding:0.22rem 0.7rem;border-radius:4px;
  display:inline-block;margin-bottom:0.85rem;
}
.tl-urgent .tl-phase{color:var(--red);background:var(--red-lt);}
.tl-title{font-size:1.15rem;font-weight:800;color:var(--blue);
  margin-bottom:0.65rem;letter-spacing:-0.015em;}
.tl-urgent .tl-title{color:var(--red);}
.tl-body{font-size:0.93rem;color:var(--muted);line-height:1.85;margin-bottom:1.25rem;}
/* CTA inside card */
.tl-btn{
  display:inline-flex;align-items:center;gap:0.45rem;
  background:var(--blue-lt);color:var(--blue-m);font-weight:700;font-size:0.87rem;
  padding:0.65rem 1.3rem;border-radius:6px;text-decoration:none;
  border:1px solid rgba(34,81,163,0.2);transition:all 0.15s;
}
.tl-btn:hover{background:#d8e6f8;border-color:var(--blue-m);color:var(--blue);}
.tl-urgent-btn{
  display:inline-flex;align-items:center;gap:0.5rem;
  background:var(--red);color:var(--white);font-weight:700;font-size:0.92rem;
  padding:0.75rem 1.6rem;border-radius:6px;text-decoration:none;
  border:2px solid var(--red);animation:redpulse 2.5s ease-in-out infinite;
  transition:all 0.2s;
}
.tl-urgent-btn:hover{background:var(--red-m);transform:translateY(-2px);
  box-shadow:0 8px 20px rgba(192,24,27,0.35);animation:none;}
.tl-pulse-dot{width:8px;height:8px;border-radius:50%;background:#FCA5A5;
  animation:pulse 1s ease-in-out infinite;flex-shrink:0;}
.email-preview{
  margin-top:1.25rem;background:var(--g50);border:1px solid var(--border);
  border-left:3px solid var(--red);border-radius:8px;padding:1.35rem 1.5rem;
  font-size:0.83rem;color:var(--text);line-height:1.8;
  white-space:pre-wrap;font-family:'IBM Plex Mono',monospace;
}
.email-subject{font-family:'Inter',sans-serif;font-weight:700;color:var(--blue);
  font-size:0.88rem;margin-bottom:0.85rem;}

/* ── BEFORE / AFTER ───────────────────────────────────────────────────────── */
.ba-grid{display:grid;grid-template-columns:1fr 48px 1fr;align-items:stretch;margin-top:2.75rem;}
.ba-col{border-radius:10px;padding:1.85rem;border:1px solid;}
.ba-before{background:#FEF2F2;border-color:#FECACA;}
.ba-after{background:var(--green-lt);border-color:#BBF7D0;}
.ba-div-col{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.5rem;}
.ba-arrow{font-size:1.8rem;color:var(--g300);}
.ba-law{font-family:'IBM Plex Mono',monospace;font-size:0.52rem;letter-spacing:0.12em;
  text-transform:uppercase;color:var(--g400);writing-mode:vertical-rl;}
.ba-head{font-weight:800;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.07em;
  margin-bottom:1.1rem;padding-bottom:0.65rem;border-bottom:2px solid;display:block;}
.ba-before .ba-head{color:var(--red);border-color:#FECACA;}
.ba-after .ba-head{color:var(--green);border-color:#BBF7D0;}
.ba-item{font-size:0.9rem;line-height:1.78;margin-bottom:0.6rem;
  padding-left:1.4rem;position:relative;}
.ba-item::before{position:absolute;left:0;font-weight:700;}
.ba-before .ba-item::before{content:'✗';color:var(--red);}
.ba-after .ba-item::before{content:'✓';color:var(--green);}

/* ── SUCCESS STORIES ──────────────────────────────────────────────────────── */
.story-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;margin-top:2.25rem;}
.story-card{background:var(--white);border:1px solid var(--border);border-radius:10px;
  padding:1.75rem;transition:box-shadow 0.2s;}
.story-card:hover{box-shadow:0 8px 28px rgba(0,0,0,0.08);}
.story-city{font-family:'IBM Plex Mono',monospace;font-size:0.63rem;letter-spacing:0.14em;
  text-transform:uppercase;color:var(--green);margin-bottom:0.5rem;}
.story-title{font-size:1.05rem;font-weight:800;color:var(--blue);margin-bottom:0.65rem;}
.story-body{font-size:0.9rem;color:var(--muted);line-height:1.82;}

/* ── RESOURCES ────────────────────────────────────────────────────────────── */
.res-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-top:2.75rem;}
.rcard{display:flex;flex-direction:column;padding:1.5rem;background:var(--white);
  border:1px solid var(--border);border-radius:10px;text-decoration:none;transition:all 0.2s;}
.rcard:hover{border-color:var(--blue-m);box-shadow:0 6px 24px rgba(26,58,107,0.1);
  transform:translateY(-2px);}
.rcard-icon{font-size:1.4rem;margin-bottom:0.85rem;}
.rcard-type{font-family:'IBM Plex Mono',monospace;font-size:0.61rem;letter-spacing:0.14em;
  text-transform:uppercase;color:var(--blue-m);margin-bottom:0.35rem;}
.rcard-t{font-size:0.96rem;font-weight:700;color:var(--blue);margin-bottom:0.5rem;line-height:1.35;}
.rcard-d{font-size:0.85rem;color:var(--muted);line-height:1.65;flex:1;}
.rcard-arrow{margin-top:1rem;font-size:0.82rem;font-weight:600;color:var(--blue-m);}

/* ── LANGUAGE GUIDE ───────────────────────────────────────────────────────── */
.lang-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-top:2rem;}
.lang-col{border-radius:10px;padding:1.6rem 1.85rem;border:1px solid;}
.lang-avoid{background:#FEF2F2;border-color:#FECACA;}
.lang-use{background:var(--green-lt);border-color:#BBF7D0;}
.lang-h{font-family:'IBM Plex Mono',monospace;font-size:0.68rem;font-weight:600;
  letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.95rem;}
.lang-avoid .lang-h{color:var(--red);}
.lang-use .lang-h{color:var(--green);}
.lang-item{font-size:0.9rem;color:var(--text);line-height:1.78;margin-bottom:0.5rem;
  padding-left:1.2rem;position:relative;}
.lang-item::before{position:absolute;left:0;}
.lang-avoid .lang-item::before{content:'✗';color:var(--red);}
.lang-use .lang-item::before{content:'✓';color:var(--green);}

/* ── PRECEDENT ────────────────────────────────────────────────────────────── */
.prec-law{background:var(--blue-lt);border:1px solid var(--border);
  border-left:4px solid var(--blue-m);border-radius:0 10px 10px 0;
  padding:1.85rem;margin-top:2.5rem;}
.prec-law p{font-size:1rem;font-style:italic;color:var(--text);line-height:1.85;margin-bottom:0.75rem;}
.prec-cite{font-family:'IBM Plex Mono',monospace;font-size:0.63rem;letter-spacing:0.12em;color:var(--g400);}
.prec-stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-top:2rem;}
.prec-stat{background:var(--white);border:1px solid var(--border);
  border-radius:10px;padding:1.75rem;text-align:center;}
.prec-n{font-size:3rem;font-weight:900;color:var(--blue);line-height:1;letter-spacing:-0.03em;}
.prec-s{font-size:0.85rem;color:var(--muted);margin-top:0.45rem;line-height:1.6;}

/* ── CTA BAND ─────────────────────────────────────────────────────────────── */
.cta-band {
  background: #EBF2FF; /* A very light, clean blue */
  padding: 6.5rem 3.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  border-top: 1px solid var(--border); /* Adds definition from previous section */
}
.cta-band::before{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 70% at 50% 50%,rgba(59,108,199,0.55) 0%,transparent 70%);
  pointer-events:none;}
.cta-inner{max-width:640px;margin:0 auto;position:relative;}
.cta-h{font-size:clamp(2.1rem,3.5vw,3rem);font-weight:900;color:var(--blue);
  margin-bottom:1.1rem;letter-spacing:-0.028em;line-height:1.08;}
.cta-p{font-size:1.0625rem;color:rgba(255,255,255,0.9);line-height:1.88;margin-bottom:2.25rem;}
.cta-btns{display:flex;gap:0.85rem;justify-content:center;flex-wrap:wrap;}
.btn-cred{display:inline-block;background:var(--red);color:var(--white);font-weight:700;
  font-size:0.95rem;padding:0.9rem 1.9rem;border-radius:6px;text-decoration:none;
  transition:all 0.2s;border:2px solid var(--red);}
.btn-cred:hover{background:var(--red-m);transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(192,24,27,0.4);}
.btn-coutline{display:inline-block;background:transparent;color:var(--white);
  font-weight:600;font-size:0.95rem;padding:0.9rem 1.9rem;border-radius:6px;
  text-decoration:none;border:2px solid rgba(255,255,255,0.28);transition:all 0.2s;}
.btn-coutline:hover{border-color:rgba(255,255,255,0.65);color:var(--white);}

/* ── FOOTER ───────────────────────────────────────────────────────────────── */
.footer{background:var(--g900);padding:4.5rem 3.5rem 2rem;}
.footer-in{max-width:1160px;margin:0 auto;}
.footer-grid{display:grid;grid-template-columns:2.5fr 1fr 1fr 1fr;
  gap:3rem;padding-bottom:3rem;border-bottom:1px solid rgba(255,255,255,0.07);}
.fb-name{font-size:1.15rem;font-weight:900;color:var(--white);
  margin-bottom:0.65rem;letter-spacing:-0.02em;}
.fb-desc{font-size:0.85rem;color:rgba(255,255,255,0.38);line-height:1.75;max-width:280px;}
.fc-h{font-family:'IBM Plex Mono',monospace;font-size:0.61rem;letter-spacing:0.2em;
  text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:0.95rem;}
.fa{display:block;font-size:0.85rem;color:rgba(255,255,255,0.46);text-decoration:none;
  margin-bottom:0.5rem;transition:color 0.15s;}
.fa:hover{color:rgba(255,255,255,0.92);}
.foot-bar{padding-top:1.5rem;display:flex;justify-content:space-between;
  align-items:center;flex-wrap:wrap;gap:0.75rem;}
.foot-copy{font-size:0.8rem;color:rgba(255,255,255,0.26);}
.foot-tag{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
  color:rgba(255,255,255,0.16);letter-spacing:0.1em;}

/* ── ANIMATIONS ───────────────────────────────────────────────────────────── */
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.35;}}
@keyframes redpulse{0%,100%{box-shadow:0 0 0 0 rgba(192,24,27,0);}
  50%{box-shadow:0 0 0 7px rgba(192,24,27,0.16);}}
@keyframes redring{
  0%,100%{box-shadow:0 0 0 5px rgba(192,24,27,0.12),0 0 0 10px rgba(192,24,27,0.05);}
  50%{box-shadow:0 0 0 8px rgba(192,24,27,0.22),0 0 0 16px rgba(192,24,27,0.07);}
}

/* ── RESPONSIVE ───────────────────────────────────────────────────────────── */
@media(max-width:1024px){
  .prob-grid{grid-template-columns:repeat(2,1fr);}
  .tracker-grid{grid-template-columns:repeat(2,1fr);}
}
@media(max-width:900px){
  .nav-links{display:none;}
  .hero-statbar{grid-template-columns:repeat(3,1fr);}
  .case-grid,.bill-grid,.story-grid,.lang-grid,.ba-grid{grid-template-columns:1fr;}
  .ba-div-col{flex-direction:row;padding:0.5rem 0;}
  .ba-law{writing-mode:horizontal-tb;}
  .res-grid{grid-template-columns:1fr 1fr;}
  .footer-grid{grid-template-columns:1fr 1fr;gap:2rem;}
  .prec-stat-row{grid-template-columns:1fr 1fr;}
}
@media(max-width:600px){
  .nav,.alert-bar{padding-left:1.25rem;padding-right:1.25rem;}
  .hero,.tracker-inner,.inner,.cta-band,.footer{padding-left:1.25rem;padding-right:1.25rem;}
  .prob-grid,.res-grid,.prec-stat-row,.tracker-grid,.footer-grid{grid-template-columns:1fr;}
  .hero-statbar{grid-template-columns:1fr 1fr;}
  .timeline::before{left:21px;}
  .tl-num{width:44px;height:44px;font-size:0.88rem;}
}
</style>
""", unsafe_allow_html=True)

from pages import home
home.render()
