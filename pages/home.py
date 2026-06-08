import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import urllib.parse

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

CITIES = sorted([
    ("Burr Ridge","IL"),("Caledonia","WI"),("Camargo","KY"),("Canyon Lake","CA"),
    ("Carmel","IN"),("Castle Pines","CO"),("Centennial","CO"),("Cherry Hills Village","CO"),
    ("Coconut Creek","FL"),("Cooper City","FL"),("Deerfield Beach","FL"),("Eastvale","CA"),
    ("Estero","FL"),("Fairlawn","VA"),("Fairview","TX"),("Fate","TX"),("Flanders","NY"),
    ("Franklin","WI"),("Frederick","CO"),("Glendale","NY"),("Glendale","WI"),
    ("Goose Creek","SC"),("Grass Valley","NV"),("Green","OH"),("Greenfield","WI"),
    ("Greenwood Village","CO"),("Harnett County","NC"),("Harrison","WI"),("Heath","TX"),
    ("Hidden Hills","CA"),("Highlands Ranch","CO"),("Hochatown","OK"),("Hollywood","FL"),
    ("Industry","CA"),("Josephine","TX"),("Keystone","CO"),("Kinnelon","NJ"),
    ("Lawrence","IN"),("Lighthouse Point","FL"),("Mauldin","SC"),("Miami Lakes","FL"),
    ("Mills","WY"),("Montz","LA"),("Mount Pleasant","WI"),("Mountain Village","CO"),
    ("Mt. Crested Butte","CO"),("Murphy","TX"),("Noblesville","IN"),("North Enid","OK"),
    ("North Tustin","CA"),("Northampton","NY"),("Northlake","TX"),("Oakland Park","FL"),
    ("Ocoee","FL"),("Parker","TX"),("Parkland","FL"),("Pendleton","NY"),("Riverside","NY"),
    ("Rochester","WI"),("Sargent","TX"),("Scotland","CT"),("Severance","CO"),
    ("Silver Cliff","CO"),("Somers","WI"),("Sterling Ranch","CO"),("Superior","CO"),
    ("Swanzey","NH"),("Tehachapi","CA"),("Telluride","CO"),("Urbandale","IA"),
    ("Weddington","NC"),("Westfield","IN"),("Wheatfield","NY"),("Wilton Manors","FL"),
    ("Zionsville","IN"),
], key=lambda x: x[0])

STATE_SENATORS = {
    "KY":[("Rand Paul","R","Chair")],
    "WI":[("Ron Johnson","R","")],
    "OK":[("James Lankford","R","")],
    "FL":[("Rick Scott","R",""),("Ashley Moody","R","")],
    "MO":[("Josh Hawley","R","")],
    "OH":[("Bernie Moreno","R","")],
    "IA":[("Joni Ernst","R","")],
    "MI":[("Gary Peters","D","Ranking Member"),("Elissa Slotkin","D","")],
    "NH":[("Margaret Hassan","D","")],
    "CT":[("Richard Blumenthal","D","")],
    "PA":[("John Fetterman","D","")],
    "NJ":[("Andy Kim","D","")],
    "AZ":[("Ruben Gallego","D","")],
}

COMMITTEE = [
    ("Rand Paul","R","KY","Chair"),("Ron Johnson","R","WI",""),
    ("James Lankford","R","OK",""),("Rick Scott","R","FL",""),
    ("Josh Hawley","R","MO",""),("Bernie Moreno","R","OH",""),
    ("Joni Ernst","R","IA",""),("Ashley Moody","R","FL",""),
    ("Gary Peters","D","MI","Ranking Member"),("Margaret Hassan","D","NH",""),
    ("Richard Blumenthal","D","CT",""),("John Fetterman","D","PA",""),
    ("Andy Kim","D","NJ",""),("Ruben Gallego","D","AZ",""),
    ("Elissa Slotkin","D","MI",""),
]

# ── S.4505 is the primary consolidated bill; prior bills shown as history ──
PRIMARY_BILL = {
    "id": "S. 4505",
    "author": "Sen. Joni Ernst (R-IA)",
    "cities": "75 cities",
    "status": "SENATE — ACTIVE",
    "badge": "b-g",
    "prog": 50,
    "cls": "bcard-p",
    "url": "https://www.congress.gov/search?q=%22S.+4505%22&searchField=allfields",
    "note": "Consolidated bill introduced by Sen. Ernst. Incorporates H.R. 672, H.R. 3095, S. 1455, and S. 2961. Wisconsin communities excluded due to Sen. Ron Johnson (R-WI) objections — amendments being sought.",
}

PRIOR_BILLS = [
    {"id":"H.R. 672","author":"Rep. Mario Diaz-Balart (R-FL)","cities":"8 cities",
     "badge":"b-a","prog":75,"cls":"bcard-p","companion":"S. 1455",
     "status":"HOUSE PASSED · CONSOLIDATED INTO S. 4505",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/672",
     "note":"Passed House July 2025. Consolidated into S. 4505 by Sen. Ernst."},
    {"id":"H.R. 3095","author":"Rep. Lauren Boebert (R-CO)","cities":"66 cities",
     "badge":"b-a","prog":75,"cls":"bcard-p","companion":"S. 2961",
     "status":"HOUSE PASSED · CONSOLIDATED INTO S. 4505",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/3095",
     "note":"Passed House July 2025. Consolidated into S. 4505 by Sen. Ernst."},
    {"id":"S. 1455","author":"Sen. Rick Scott (R-FL)","cities":"14 cities",
     "badge":"b-a","prog":35,"cls":"bcard-s","companion":"H.R. 672",
     "status":"CONSOLIDATED INTO S. 4505",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/1455",
     "note":"Senate companion to H.R. 672. Consolidated into S. 4505 by Sen. Ernst."},
    {"id":"S. 2961","author":"Sen. Mike Banks (R-IN)","cities":"69 cities",
     "badge":"b-a","prog":35,"cls":"bcard-s","companion":"H.R. 3095",
     "status":"CONSOLIDATED INTO S. 4505",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/2961",
     "note":"Senate companion to H.R. 3095. Consolidated into S. 4505 by Sen. Ernst."},
]

PROBLEMS = [
    {"icon":"🚨","cls":"pcard-red","title":"Public Safety",
     "body":"ZIP confusion routes 911 calls to wrong dispatch centers. In Somers, WI, firefighters from the wrong department were dispatched because two residences in different municipalities shared the same address and ZIP code. A street had to be renamed as a result. Seconds determine outcomes.",
     "stat":"14 ZIP","stat_lbl":"codes span Somers, WI — one city"},
    {"icon":"💰","cls":"pcard-amber","title":"Lost Tax Revenue",
     "body":"Sales tax generated inside your city is credited to neighboring jurisdictions. Frederick, CO estimates a conservative $1.5M in lost annual sales tax due to shared ZIP codes. Green, OH identified $614,000 in unpaid taxes in 2023 alone — from ZIP-driven resident confusion.",
     "stat":"$1.5M","stat_lbl":"est. annual lost sales tax · Frederick, CO"},
    {"icon":"📋","cls":"pcard-blue","title":"Insurance Inequity",
     "body":"Insurers rate policies by ZIP, not city boundary. Eastvale, CA shares ZIP 92880 with Corona — a high-risk wildfire zone. Despite Eastvale not being classified high-risk by CalFire, residents pay inflated premiums based on their neighbor's risk profile. Some cannot get coverage at all.",
     "stat":"20%+","stat_lbl":"territory mis-assignment error rate"},
    {"icon":"📦","cls":"pcard-green","title":"Logistics & Commerce",
     "body":"Carriers geofence by ZIP. Mills, WY has a post office ZIP (82644) that only covers a single P.O. box location — all home delivery uses Casper's 82604. Residents ordering online face returns, failed deliveries, and packages routed to Casper. One resident cannot receive medical supplies at home.",
     "stat":"2 ZIP","stat_lbl":"codes for one city · Mills, WY"},
    {"icon":"🏙️","cls":"pcard-blue","title":"Business Attraction",
     "body":"Commercial developers use GIS platforms that categorize opportunity data by ZIP code. When a city's ZIP carries a neighboring city's label, it is systematically excluded from site selection. Green, OH's 1,200+ businesses appear under Akron, Uniontown, or North Canton — never Green.",
     "stat":"6 ZIPs","stat_lbl":"carve through Green, OH — none say 'Green'"},
]

CASES = [
    {"stat":"$614K","sub":"in unpaid taxes identified in Green, OH — 2023 alone",
     "lbl":"Case Study A · Tax Revenue · Green, OH",
     "title":"ZIP-Driven Tax Confusion Costs Green $614K a Year",
     "desc":"Green, OH has 27,475 residents and 1,200+ businesses — yet not a single home or business address says 'Green.' All six ZIP codes identify with other cities. In 2023, the city's Income Tax Division identified $614,000 in unpaid taxes from residents and businesses filing with the wrong jurisdiction. Every year, Green expends significant resources reversing improper tax payments. In 2024, First Energy incorrectly assigned over 1,500 utility accounts due to ZIP confusion, resulting in billing errors that took multiple cycles to correct.",
     "src":"Source: City of Green, OH · Mayor's Letter to USPS, February 2025"},
    {"stat":"$1.5M","sub":"conservative estimate of annual lost sales tax · Frederick, CO",
     "lbl":"Case Study B · Fiscal Loss · Frederick, CO",
     "title":"Frederick Loses Millions to Neighboring ZIP Codes",
     "desc":"Over 4,000 Frederick households are assigned to Longmont's ZIP code (80504), and more than 2,000 have the Erie ZIP (80516). This misattribution redirects sales tax revenue out of Frederick — a conservative estimate of $1.5 million annually. Residents confirm the impact firsthand: large purchases like automobiles are auto-assigned to Boulder County tax rates, which are higher than Frederick's. The town cannot verify that its sales taxes haven't been going to neighboring cities for years.",
     "src":"Source: Town of Frederick, CO · Coalition White Paper 2026"},
    {"stat":"40 yrs","sub":"of advocacy with no resolution · Superior, CO",
     "lbl":"Case Study C · Systemic Failure · Superior, CO",
     "title":"Four Decades of Requests. Zero Resolution.",
     "desc":"Superior, CO has been seeking a unique ZIP code since 1988 — formally requesting one in 1992, 1997, 2000, and multiple times since. Every request has been denied. In Esri's ArcGIS — used daily by city staff — some Superior addresses default to Louisville. Staff spend significant time cleaning misattributed data. Annual revenue loss is estimated in the hundreds of thousands. The town had 250 residents in 1988. Today it has 13,000+. The ZIP code has never been updated to reflect this.",
     "src":"Source: Town of Superior, CO · Coalition White Paper 2026"},
]

TESTIMONIALS = [
    {"city":"Green, OH","quote":"Not a single home or business address in Green belongs to Green. All are divided up and assigned to neighboring communities — even though Green is the largest city in southern Summit County.",
     "role":"Mayor Rocco P. Yeargin · City of Green"},
    {"city":"Somers, WI","quote":"A major incident led to the renaming of one of the village's streets after firefighters from the wrong department were dispatched to a call because two residences in two different municipalities shared the same address and ZIP code.",
     "role":"Kevin Poirier · Assistant to the Village Administrator, Somers, WI"},
    {"city":"Eastvale, CA","quote":"Despite Eastvale not being deemed a high-risk zone by CalFire, the city's shared ZIP code impacts residents' insurance rates. While most residents experience increases, some are unable to obtain coverage at all.",
     "role":"City of Eastvale · Coalition White Paper 2026"},
    {"city":"Frederick, CO","quote":"Over 4,000 households are assigned to the Longmont ZIP code, and more than 2,000 have the Erie ZIP. This situation has the potential to cause a conservative estimate of $1.5 million in lost sales tax revenue annually.",
     "role":"Town of Frederick, CO · Coalition White Paper 2026"},
    {"city":"Mills, WY","quote":"She recently tried to order furniture online and had to cancel the order because the delivery company could not verify it was an actual home.",
     "role":"Darcie Gudger · Mills, WY resident (re: elderly mother's medical supply deliveries)"},
    {"city":"Urbandale, IA","quote":"New USPS staff reversed course, telling Urbandale that many areas of our City had been assigned Urbandale ZIP codes 'in error' and outlining a plan to change those ZIP codes — forcing hundreds of residents and businesses to change their mailing address.",
     "role":"City of Urbandale, IA · Coalition White Paper 2026"},
]

RESOURCES = [
    {"icon":"📄","type":"White Paper","title":"NZCAC White Paper — 2026 Edition",
     "desc":"Full documentation of how shared ZIPs cause measurable harm across 55+ member municipalities. Municipal testimonials, impact data, legislative history, and the call to action.",
     "url":"https://www.eastvaleca.gov/home/showpublisheddocument/18184/639098699108370000",
     "arrow":"Download White Paper →"},
    {"icon":"📋","type":"Legislation","title":"S. 4505 — Consolidated Bill (Ernst)",
     "desc":"Sen. Joni Ernst (R-IA) consolidated H.R. 672, H.R. 3095, S. 1455, and S. 2961 into S. 4505 covering 75 cities.",
     "url":"https://www.congress.gov/search?q=%22S.+4505%22&searchField=allfields",
     "arrow":"Search on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"H.R. 672 — Full Bill Text",
     "desc":"Rep. Mario Diaz-Balart (R-FL). Passed House July 2025. Consolidated into S. 4505.",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/672","arrow":"View on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"H.R. 3095 — Full Bill Text",
     "desc":"Rep. Lauren Boebert (R-CO). Passed House July 2025. Consolidated into S. 4505.",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/3095","arrow":"View on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"S. 2961 — Full Bill Text",
     "desc":"Sen. Mike Banks (R-IN). In Senate HSGA Committee. Consolidated into S. 4505.",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/2961","arrow":"View on Congress.gov →"},
    {"icon":"🏛️","type":"Coalition","title":"Official Coalition Webpage",
     "desc":"Primary hub on eastvaleca.gov with background, partners, and contact info.",
     "url":"https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/","arrow":"Visit eastvaleca.gov →"},
    {"icon":"⚖️","type":"Committee","title":"Senate HSGA Committee",
     "desc":"Where S. 4505 will be reviewed. Chair: Sen. Rand Paul (R-KY).",
     "url":"https://www.hsgac.senate.gov/","arrow":"Visit Committee →"},
    {"icon":"📖","type":"Precedent","title":"Postal Accountability Act (2006)",
     "desc":"Section 1009 mandated unique ZIPs for Auburn OH, Hanahan SC, Bradbury CA, and Discovery Bay CA.",
     "url":"https://www.congress.gov/bill/109th-congress/house-bill/6407","arrow":"View on Congress.gov →"},
    {"icon":"📊","type":"Research","title":"ZIP Codes & Sales Tax (Avalara)",
     "desc":"Why ZIP codes fail as sales tax tools — Colorado case studies.",
     "url":"https://www.avalara.com/us/en/learn/whitepapers/zip-codes-the-wrong-tool-for-the-job.html","arrow":"Read Research →"},
]

STEPS = [
    {"n":"A","phase":"Recommended Action — USPS","urgent":False,
     "title":"Submit a USPS ZIP Code Boundary Review Request",
     "body":"Send a formal letter to your USPS Local District Manager requesting a ZIP code boundary review. Congress expects cities to receive formal USPS responses — including denials — before pursuing legislative action. USPS must acknowledge within 30 days and provide a final determination within 60. This creates the administrative record the Senate needs.",
     "cta":None,"url":None},
    {"n":"B","phase":"⚡ URGENT — Federal Action","urgent":True,
     "title":"Write to Your Senate HSGA Committee Senator",
     "body":"S. 4505 is the active consolidated bill — introduced by Sen. Joni Ernst (R-IA). It now must clear the Senate Homeland Security & Governmental Affairs Committee. Every coalition city must send individual letters to each Senator on the committee — especially Chairman Sen. Rand Paul (R-KY). Use the pre-filled template and personalize with one specific impact from your city.",
     "cta":None,"url":None},
    {"n":"C","phase":"Recommended Action — Local","urgent":False,
     "title":"Adopt a City Council Resolution",
     "body":"Collaborate with your City Council or Governing Board to adopt a formal resolution supporting an independent ZIP code for your jurisdiction. Official resolutions carry significantly more weight than standard correspondence with federal offices — they create an official paper trail that Senate staff catalog.",
     "cta":None,"url":None},
    {"n":"D","phase":"Recommended Action — Community","urgent":False,
     "title":"Collect Resident and Business Testimonies",
     "body":"Gather documented testimonies from residents and businesses impacted by ZIP misalignment — delayed emergency responses, lost tax revenue, insurance overcharges, or logistics failures. The coalition's 2026 White Paper includes real examples: a Mills, WY resident who cannot receive medical supplies at home; a Somers, WI street renamed after a wrong-department fire dispatch. Three sentences and one dollar figure is enough.",
     "cta":"Download White Paper for Examples →",
     "url":"https://www.eastvaleca.gov/home/showpublisheddocument/18184/639098699108370000"},
    {"n":"E","phase":"Recommended Action — Federal","urgent":False,
     "title":"Share All Documents with Your Senators and Congressmember(s)",
     "body":"Forward your resolution, USPS correspondence, resident testimonies, and the coalition's 2026 White Paper directly to your respective Senators and Congressmember(s). Consistent outreach from every coalition city builds the political record needed for Senate action on S. 4505.",
     "cta":"Join the Coalition — Free →","url":"mailto:afung@eastvaleca.gov"},
]

def email_template(senator_name="Sen. Rand Paul"):
    subject = "Urgent: Please Advance S. 4505 — ZIP Code Geographic Integrity Act"
    body = f"""Dear {senator_name},

I am writing on behalf of [Your City Name], a member of the National ZIP Code Advocacy Coalition — 75+ municipalities across 20+ states representing over 1 million residents.

I urge you to advance S. 4505 through the Senate Homeland Security & Governmental Affairs Committee. This consolidated bill was introduced by Sen. Joni Ernst (R-IA) and incorporates the previously separate H.R. 672, H.R. 3095, S. 1455, and S. 2961. The companion House bills passed in July 2025.

Three documented harms our community experiences due to outdated ZIP boundaries:

1. PUBLIC SAFETY: 911 calls are routed to wrong dispatch centers. In Somers, WI, firefighters from the wrong department responded to an emergency because two residences in different municipalities shared the same address and ZIP code.

2. FISCAL ACCURACY: Local sales tax revenue is credited to neighboring jurisdictions. Frederick, CO estimates $1.5M in lost annual sales tax. Green, OH identified $614,000 in unpaid taxes in 2023 alone — entirely caused by ZIP code confusion.

3. ECONOMIC HARM: Insurance, logistics, and federal datasets all use ZIP codes — our city is systematically mis-rated and overcharged. Some Eastvale, CA residents cannot obtain homeowners insurance at all because their ZIP is coded to a wildfire-risk neighbor.

Congress has done this before. Section 1009 of the Postal Accountability and Enhancement Act (2006) mandated unique ZIP codes for Hanahan, SC and three other cities — and it worked. The estimated cost per adjustment is $193,327 — 0.0002% of USPS's $89B annual budget.

Please bring S. 4505 to a committee vote.

Respectfully,
[Your Name]
[Your Title]
[City Name, State]"""
    return subject, body


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render():

    # ── NAV + ALERT ───────────────────────────────────────────────────────────
    st.markdown("""
    <nav class="nav">
      <a class="nav-brand" href="#">
        <div class="nav-seal">🏛️</div>
        <div>
          <div class="nav-name">National ZIP Code Advocacy Coalition</div>
          <span class="nav-sub">119th Congress</span>
        </div>
      </a>
      <div class="nav-links">
        <a href="#problem"   class="nav-a">The Problem</a>
        <a href="#tracker"   class="nav-a">Bill Status</a>
        <a href="#members"   class="nav-a">Members</a>
        <a href="#action"    class="nav-a">Take Action</a>
        <a href="#precedent" class="nav-a">Precedent</a>
        <a href="#resources" class="nav-a">Resources</a>
        <a href="#action" class="nav-urgent">
          <span class="nav-dot"></span>Take Action Now
        </a>
      </div>
    </nav>
    <div class="alert-bar">
      <span class="alert-pill">⚡ UPDATE: S. 4505 INTRODUCED</span>
      <span class="alert-msg">Sen. Joni Ernst (R-IA) consolidated H.R. 672, H.R. 3095, S. 1455 &amp; S. 2961 into
      <strong>S. 4505</strong> — covering 75 cities. Now before the Senate HSGA Committee. —
      <a href="#action" class="alert-link">Take Action Now →</a></span>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <section class="hero" style="
        background: linear-gradient(rgba(10, 32, 72, 0.85), rgba(10, 32, 72, 0.85)), url('https://lh3.googleusercontent.com/d/1JxS24P-SbB_g6kfUpgoT3VEhkd8xwiZE');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    ">
      <div class="hero-inner">
        <div class="hero-kicker" style="display:none;"></div>
        <h1 class="hero-h1">
          <span style="color: rgba(255,255,255,0.95);">One City.</span><br>
          <span class="hero-h1-red">One ZIP Code.</span>
        </h1>
        <p class="hero-sub">
          Outdated USPS ZIP code boundaries delay 911 calls, misallocate tax revenue, inflate insurance
          rates, and systematically harm over one million Americans across 75+ municipalities in 20+ states.
          S. 4505 is now before the Senate. The 119th Congress ends December 2026.
        </p>
        <div class="hero-ctas">
          <a href="#action" class="btn-hero-red">Take Action on S. 4505</a>
          <a href="#problem" class="btn-hero-ghost">See the Evidence →</a>
        </div>
      </div>
      <div class="hero-statbar">
        <div class="hst">
          <span class="hst-n">75+</span>
          <span class="hst-l">Cities in S. 4505</span>
        </div>
        <div class="hst">
          <span class="hst-n">20+</span>
          <span class="hst-l">States</span>
        </div>
        <div class="hst">
          <span class="hst-n">1M+</span>
          <span class="hst-l">Residents Affected</span>
        </div>
        <div class="hst">
          <span class="hst-n">S.4505</span>
          <span class="hst-l">Active Consolidated Bill</span>
        </div>
        <div class="hst">
          <span class="hst-n">$0</span>
          <span class="hst-l">Cost to Join</span>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    # ── BILL TRACKER ──────────────────────────────────────────────────────────
    st.markdown('<div id="tracker"></div>', unsafe_allow_html=True)

    # Primary bill card (S. 4505)
    b = PRIMARY_BILL
    primary_card = f"""
      <div class="tcard tcard-passed" style="border-left:4px solid var(--green);border-top:3px solid var(--green);position:relative;">
        <div style="position:absolute;top:0.75rem;right:0.85rem;background:var(--green);color:white;
          font-family:'IBM Plex Mono',monospace;font-size:0.58rem;font-weight:700;letter-spacing:0.1em;
          padding:0.2rem 0.6rem;border-radius:3px;text-transform:uppercase;">★ Primary Bill</div>
        <div class="tcard-id" style="font-size:1.4rem;">{b['id']}</div>
        <div class="tcard-author">{b['author']}</div>
        <div style="font-size:0.8rem;color:var(--muted);margin-bottom:0.5rem;">{b['cities']}</div>
        <span class="tbadge tbadge-g">{b['status']}</span>
        <div class="tcard-note" style="margin-top:0.75rem;">{b['note']}</div>
        <div class="tprog" style="margin-top:1rem;">
          <div class="tprog-fill tprog-green" style="width:{b['prog']}%"></div>
        </div>
        <a href="{b['url']}" target="_blank" style="display:inline-block;margin-top:0.85rem;
          font-size:0.83rem;font-weight:600;color:var(--blue-m);text-decoration:none;">
          Search on Congress.gov →</a>
      </div>"""

    prior_cards = "".join(f"""
      <div class="tcard tcard-stalled" style="opacity:0.82;">
        <div style="position:absolute;top:0.75rem;right:0.85rem;background:var(--g200);color:var(--g500);
          font-family:'IBM Plex Mono',monospace;font-size:0.56rem;font-weight:700;letter-spacing:0.09em;
          padding:0.18rem 0.55rem;border-radius:3px;text-transform:uppercase;">Consolidated</div>
        <div class="tcard-id">{pb['id']}</div>
        <div class="tcard-author">{pb['author']}</div>
        <div style="font-size:0.78rem;color:var(--muted);margin-bottom:0.4rem;">{pb['cities']}</div>
        <span class="tbadge tbadge-a" style="font-size:0.56rem;">{pb['status']}</span>
        <div class="tcard-note" style="margin-top:0.6rem;">{pb['note']}</div>
        <div class="tprog" style="margin-top:0.75rem;">
          <div class="tprog-fill tprog-amber" style="width:{pb['prog']}%"></div>
        </div>
      </div>""" for pb in PRIOR_BILLS)

    st.markdown(f"""
    <div class="tracker-band">
    <div class="tracker-inner">
      <span class="tracker-label">📊 Legislative Status — 119th Congress (Jan 2025 – Dec 2026)</span>
      <div style="margin-bottom:1.25rem;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;
          letter-spacing:0.14em;text-transform:uppercase;color:var(--green);margin-bottom:0.6rem;">
          ★ Active Consolidated Bill</div>
        <div style="display:grid;grid-template-columns:1fr;">{primary_card}</div>
      </div>
      <div style="margin-top:1.5rem;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;
          letter-spacing:0.14em;text-transform:uppercase;color:var(--g400);margin-bottom:0.6rem;">
          Prior Bills — Now Consolidated into S. 4505</div>
        <div class="tracker-grid">{prior_cards}</div>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── THE PROBLEM ───────────────────────────────────────────────────────────
    st.markdown('<div id="problem"></div>', unsafe_allow_html=True)
    prob_html = "".join(f"""
      <div class="pcard {p['cls']}">
        <span class="pcard-icon">{p['icon']}</span>
        <div class="pcard-t">{p['title']}</div>
        <div class="pcard-b">{p['body']}</div>
        <span class="pcard-stat">{p['stat']}</span>
        <span class="pcard-stat-lbl">{p['stat_lbl']}</span>
      </div>""" for p in PROBLEMS)
    st.markdown(f"""
    <div class="section section-w" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label sec-label-red">The Problem</span>
      <h2 class="sec-h">Five Ways Outdated ZIP Codes Are Costing Your City — Right Now</h2>
      <p class="sec-lead">This is not a branding issue. These are documented, measurable harms
      affecting public safety, government revenue, and business competitiveness every single day —
      as detailed in the coalition's 2026 White Paper.</p>
      <div class="prob-grid">{prob_html}</div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── CASE STUDIES ─────────────────────────────────────────────────────────
    case_html = "".join(f"""
      <div class="ccase">
        <div class="ccase-top">
          <div class="ccase-stat">{c['stat']}</div>
          <div class="ccase-sub">{c['sub']}</div>
        </div>
        <div class="ccase-body">
          <div class="ccase-lbl">{c['lbl']}</div>
          <div class="ccase-t">{c['title']}</div>
          <div class="ccase-d">{c['desc']}</div>
          <div class="ccase-src">{c['src']}</div>
        </div>
      </div>""" for c in CASES)
    st.markdown(f"""
    <div class="section section-g" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label">Documented Impact · From the 2026 White Paper</span>
      <h2 class="sec-h">Real Cities. Real Numbers. No Ambiguity.</h2>
      <p class="sec-lead">Three case studies drawn directly from the coalition's 2026 White Paper — with verified data, city contacts, and documented sources.</p>
      <div class="case-grid">{case_html}</div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── MUNICIPAL TESTIMONIALS ────────────────────────────────────────────────
    testi_html = "".join(f"""
      <div class="story-card">
        <div class="story-city">{t['city']}</div>
        <div class="story-body" style="font-style:italic;color:var(--text);margin-bottom:0.75rem;">
          "{t['quote']}"</div>
        <div style="font-size:0.78rem;color:var(--g400);font-family:'IBM Plex Mono',monospace;">
          — {t['role']}</div>
      </div>""" for t in TESTIMONIALS)
    st.markdown(f"""
    <div class="section section-w" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label">Municipal Testimonials · 2026 White Paper</span>
      <h2 class="sec-h">In Their Own Words</h2>
      <p class="sec-lead">Direct quotes from city officials, fire chiefs, and residents — drawn
      from the coalition's 2026 White Paper. These are the voices S. 4505 is meant to protect.</p>
      <div class="story-grid">{testi_html}</div>
      <div style="margin-top:2rem;text-align:center;">
        <a href="https://www.eastvaleca.gov/home/showpublisheddocument/18184/639098699108370000"
           target="_blank"
           style="display:inline-flex;align-items:center;gap:0.5rem;background:var(--blue);
           color:white;font-weight:700;font-size:0.92rem;padding:0.85rem 1.9rem;
           border-radius:6px;text-decoration:none;">
          📄 Read the Full 2026 White Paper →
        </a>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── LEGISLATION + COMMITTEE ───────────────────────────────────────────────
    # Primary bill detail
    b = PRIMARY_BILL
    primary_bill_card = f"""
      <div class="bcard bcard-p" style="border-left:4px solid var(--green);grid-column:1/-1;">
        <div class="bill-top">
          <div class="bill-id" style="font-size:1.5rem;">{b['id']} <span style="font-size:0.9rem;font-weight:400;color:var(--muted);">— Active Consolidated Bill</span></div>
          <span class="badge b-g">{b['status']}</span>
        </div>
        <div class="bill-author" style="font-size:1rem;font-weight:600;">{b['author']}</div>
        <div class="bill-cities" style="margin-bottom:0.75rem;">{b['cities']} · Consolidates H.R. 672, H.R. 3095, S. 1455, S. 2961</div>
        <div class="bill-note" style="background:var(--amber-lt);border:1px solid #FDE68A;border-radius:6px;padding:0.85rem 1rem;font-size:0.88rem;color:var(--text);line-height:1.7;">
          ⚠ <strong>Wisconsin communities excluded</strong> due to Sen. Ron Johnson (R-WI) objections.
          The Wisconsin communities (Caledonia, Somers, Mount Pleasant, Franklin, Greenfield, Glendale, Rochester, Harrison)
          are now requesting amendments to be re-included.
        </div>
        <a href="{b['url']}" target="_blank" class="bill-link">Search S. 4505 on Congress.gov →</a>
      </div>"""

    prior_bill_html = "".join(f"""
      <div class="bcard {pb['cls']}" style="opacity:0.78;">
        <div class="bill-top">
          <div class="bill-id">{pb['id']}</div>
          <span class="badge b-a" style="font-size:0.58rem;">{pb['status']}</span>
        </div>
        <div class="bill-author">{pb['author']}</div>
        <div class="bill-cities">{pb['cities']} · Companion: {pb['companion']}</div>
        <div class="bill-note">{pb['note']}</div>
        <a href="{pb['url']}" target="_blank" class="bill-link">View on Congress.gov →</a>
      </div>""" for pb in PRIOR_BILLS)

    cm_html = "".join(
        f'<div class="cm{" cm-chair" if r else ""}">'
        f'<span class="{"pr" if p=="R" else "pd"}">{p}-{s}</span>'
        f'{n}{(" ("+r+")" if r else "")}</div>'
        for n,p,s,r in COMMITTEE)

    st.markdown(f"""
    <div class="section section-g" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label">119th Congress · Jan 2025 – Dec 2026</span>
      <h2 class="sec-h">Legislative Tracker</h2>
      <p class="sec-lead">Sen. Ernst consolidated all four prior bills into <strong>S. 4505</strong>.
      The path to law now runs entirely through the Senate Homeland Security &amp; Governmental Affairs Committee.</p>

      <div style="margin-bottom:1.5rem;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:600;
          letter-spacing:0.18em;text-transform:uppercase;color:var(--green);
          border-top:3px solid var(--green);padding-top:0.85rem;width:fit-content;margin-bottom:0.85rem;">
          ★ Active Consolidated Bill</div>
        <div style="display:grid;grid-template-columns:1fr;">{primary_bill_card}</div>
      </div>

      <div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:600;
          letter-spacing:0.18em;text-transform:uppercase;color:var(--g400);
          border-top:3px solid var(--g200);padding-top:0.85rem;width:fit-content;margin-bottom:0.85rem;">
          Prior Bills — Consolidated into S. 4505</div>
        <div class="bill-grid">{prior_bill_html}</div>
      </div>

      <div class="callout callout-a" style="margin-top:2rem;">
        <div class="callout-t">⚠ The Bottleneck: Senate HSGA Committee</div>
        <div class="callout-b">S. 4505 passes or fails in committee. Chairman Sen. Rand Paul (R-KY)
        must bring it to a vote. Wisconsin communities affected by Sen. Johnson's objection are
        actively seeking amendments to be re-included. The 119th Congress ends December 2026 — no action means starting over.</div>
      </div>

      <div style="margin-top:3rem;">
        <span class="sec-label sec-label-amber">Senate HSGA Committee — 15 Members</span>
        <p class="sec-lead" style="margin-bottom:0.5rem;">
          Contact every Senator from your state on this list. They are the decisive votes on S. 4505.</p>
        <div class="committee-grid">{cm_html}</div>
        <a href="https://www.hsgac.senate.gov/" target="_blank"
           style="display:inline-block;margin-top:1.25rem;font-size:0.85rem;font-weight:600;
           color:var(--blue-m);text-decoration:none;">Visit Senate HSGA Committee Website →</a>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── MEMBER LOOKUP ─────────────────────────────────────────────────────────
    st.markdown('<div id="members"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section section-w" style="border-top:1px solid var(--border);padding-bottom:3rem;">
    <div class="inner">
      <span class="sec-label">Coalition Membership</span>
      <h2 class="sec-h">Is Your City a Member?<br>Who Represents You?</h2>
      <p class="sec-lead">Select your state to see coalition member cities and your HSGA Committee
      senator — then contact them directly with a pre-filled email template for S. 4505.</p>
    </div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 3.5rem 0;max-width:1160px;margin:0 auto;">', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown("""
        <div style="background:var(--white);border:1px solid var(--border);border-radius:10px;
             padding:1.5rem;margin-bottom:0.75rem;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:600;
            letter-spacing:0.18em;text-transform:uppercase;color:var(--blue-m);
            padding-top:0.85rem;border-top:3px solid var(--blue-m);
            width:fit-content;margin-bottom:0.75rem;">State Lookup</div>
          <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;margin:0;">
            Select your state to see:<br>
            ✓ Coalition member cities<br>
            ✓ Your HSGA Committee senator<br>
            ✓ Pre-filled S. 4505 contact email
          </p>
        </div>
        """, unsafe_allow_html=True)
        state_sel = st.selectbox("State",
                                  ["— Choose a state —"] + sorted(set(s for _, s in CITIES)),
                                  label_visibility="collapsed")

    with col_r:
        if state_sel and state_sel != "— Choose a state —":
            state_cities = [c for c, s in CITIES if s == state_sel]
            state_senators = STATE_SENATORS.get(state_sel, [])

            if state_cities:
                chips = "".join(
                    f'<span style="display:inline-flex;align-items:center;padding:0.3rem 0.85rem;'
                    f'border-radius:99px;background:var(--blue-lt);border:1px solid var(--border);'
                    f'font-size:0.84rem;color:var(--blue);font-weight:600;margin:0.2rem;">✓ {c}</span>'
                    for c in state_cities)
                city_block = f'<div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-bottom:1.25rem;">{chips}</div>'
            else:
                city_block = (f'<div style="background:var(--amber-lt);border:1px solid #FDE68A;'
                              f'border-radius:8px;padding:1rem 1.25rem;margin-bottom:1.25rem;'
                              f'font-size:0.9rem;color:var(--amber);">'
                              f'<strong>No coalition cities in {state_sel} yet.</strong> '
                              f'Email <a href="mailto:afung@eastvaleca.gov" style="color:var(--blue-m);">'
                              f'afung@eastvaleca.gov</a> to join.</div>')

            if state_senators:
                sen_rows = ""
                for sname, sparty, srole in state_senators:
                    subj, body = email_template(f"Sen. {sname}")
                    mailto = f"mailto:?subject={urllib.parse.quote(subj)}&body={urllib.parse.quote(body)}"
                    role_txt = f" — {srole}" if srole else ""
                    pc = "var(--red)" if sparty == "R" else "var(--blue-m)"
                    sen_rows += f"""
                    <div style="display:flex;align-items:center;justify-content:space-between;
                         padding:1rem 1.25rem;background:var(--red-lt);border:1px solid #FECACA;
                         border-radius:8px;margin-bottom:0.6rem;gap:1rem;flex-wrap:wrap;">
                      <div>
                        <span style="font-weight:800;color:var(--blue);font-size:0.95rem;">
                          Sen. {sname}</span>
                        <span style="font-size:0.78rem;color:{pc};font-family:'IBM Plex Mono',monospace;
                          margin-left:0.6rem;font-weight:600;">{sparty}{role_txt}</span>
                      </div>
                      <a href="{mailto}"
                         style="display:inline-flex;align-items:center;gap:0.45rem;
                         background:var(--red);color:white;font-weight:700;font-size:0.87rem;
                         padding:0.6rem 1.2rem;border-radius:6px;text-decoration:none;">
                         ✉ Email re: S. 4505
                      </a>
                    </div>"""
                senator_block = (
                    '<div style="border-top:1px solid var(--border);padding-top:1.1rem;margin-top:0.25rem;">'
                    '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.63rem;font-weight:600;'
                    'letter-spacing:0.18em;text-transform:uppercase;color:var(--red);'
                    'padding-top:0.85rem;border-top:3px solid var(--red);'
                    'width:fit-content;margin-bottom:0.85rem;">⚡ Your HSGA Senator(s)</div>'
                    + sen_rows + '</div>'
                )
            else:
                senator_block = (
                    '<p style="font-size:0.9rem;color:var(--muted);line-height:1.8;'
                    'border-top:1px solid var(--border);padding-top:1rem;margin-top:0.5rem;">'
                    f'No HSGA Committee senators from {state_sel}. Contact the full committee at '
                    '<a href="https://www.hsgac.senate.gov/" target="_blank"'
                    ' style="color:var(--blue-m);">hsgac.senate.gov</a>.</p>'
                )

            st.markdown(
                '<div style="background:var(--white);border:1px solid var(--border);'
                'border-radius:10px;padding:1.5rem 1.75rem;">'
                '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.63rem;font-weight:600;'
                'letter-spacing:0.18em;text-transform:uppercase;color:var(--blue-m);'
                'padding-top:0.85rem;border-top:3px solid var(--blue-m);'
                f'width:fit-content;margin-bottom:0.9rem;">Coalition Cities in {state_sel}</div>'
                + city_block + senator_block + '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
            <div style="background:var(--white);border:2px dashed var(--border);
                 border-radius:10px;padding:3rem 2rem;text-align:center;
                 color:var(--g400);font-size:0.95rem;line-height:1.8;">
              ← Select your state to see coalition cities<br>and your HSGA Committee senator
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive map
    st.markdown("""
    <div style="padding:3rem 3.5rem 0;max-width:1160px;margin:0 auto;">
      <span style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;font-weight:600;
        letter-spacing:0.22em;text-transform:uppercase;color:var(--blue-m);
        padding-top:1rem;border-top:3px solid var(--blue-m);
        width:fit-content;display:block;margin-bottom:1rem;">Interactive Coalition Map</span>
    </div>
    """, unsafe_allow_html=True)
    map_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "usa_municipalities_status_map.html")
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        st.markdown('<div style="padding:0 3.5rem;max-width:1160px;margin:0 auto;"><div class="map-frame">', unsafe_allow_html=True)
        components.html(map_html, height=520, scrolling=False)
        st.markdown("</div></div>", unsafe_allow_html=True)
    except Exception:
        pass

    # Member directory
    st.markdown('<div style="padding:2.5rem 0 5rem;max-width:100%;margin:0 auto;">', unsafe_allow_html=True)
    st.markdown("""
    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;font-weight:600;
      letter-spacing:0.22em;text-transform:uppercase;color:var(--blue-m);
      padding-top:1rem;border-top:3px solid var(--blue-m);
      width:fit-content;display:block;margin-bottom:0.85rem;">Member Directory — Searchable</span>
    <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;margin-bottom:1.25rem;max-width:500px;">
      Search by city name or filter by state.</p>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(CITIES, columns=["City", "State"])
    state_counts = df["State"].value_counts().to_dict()
    df["Coalition Density"] = df["State"].map(state_counts)

    c1, c2, _ = st.columns([2, 1.5, 3])
    with c1:
        sq = st.text_input("Search city", placeholder="Search city name…", label_visibility="collapsed")
    with c2:
        ss = st.selectbox("Filter state", ["All States"] + sorted(df["State"].unique().tolist()), label_visibility="collapsed")

    mask = pd.Series([True] * len(df))
    if sq: mask &= df["City"].str.contains(sq, case=False, na=False)
    if ss != "All States": mask &= df["State"] == ss
    filtered = df[mask].reset_index(drop=True)
    filtered.index = filtered.index + 1

    st.dataframe(filtered, use_container_width=True,
        height=min(400, 55 + len(filtered) * 35),
        column_config={
            "City":  st.column_config.TextColumn("City", width="large"),
            "State": st.column_config.TextColumn("State", width="small"),
            "Coalition Density": st.column_config.ProgressColumn(
                "Coalition Density", help="Members per state",
                min_value=0, max_value=int(df["Coalition Density"].max()),
                format="%d cities", width="medium"),
        }, hide_index=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TAKE ACTION ───────────────────────────────────────────────────────────
    st.markdown('<div id="action"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section section-g" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label sec-label-red">Take Action</span>
      <h2 class="sec-h">Five Steps Your City Should Take Now</h2>
      <p class="sec-lead">Congress expects cities to build a documented record before requesting
      legislative action. Complete these steps to strengthen S. 4505's path through the Senate.
      <strong style="color:var(--red);">Step B is the most urgent action available right now.</strong></p>
    </div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 3.5rem 5.5rem;max-width:1160px;margin:0 auto;">'
                '<div class="timeline">', unsafe_allow_html=True)

    for step in STEPS:
        u = step["urgent"]
        item_cls = " tl-urgent" if u else ""
        phase_html = f'<span class="tl-phase">{step["phase"]}</span>'
        title_html = f'<div class="tl-title">{step["title"]}</div>'
        body_html  = f'<div class="tl-body">{step["body"]}</div>'

        if u:
            subj, body_txt = email_template("Sen. Rand Paul and the Senate HSGA Committee")
            mailto = f"mailto:?subject={urllib.parse.quote(subj)}&body={urllib.parse.quote(body_txt)}"
            st.markdown(f"""
            <div class="tl-item{item_cls}">
              <div class="tl-left"><div class="tl-num">{step['n']}</div></div>
              <div class="tl-card">
                {phase_html}{title_html}{body_html}
                <a href="{mailto}" class="tl-urgent-btn">
                  <span class="tl-pulse-dot"></span>
                  ✉ Open Pre-Filled Email re: S. 4505
                </a>
            """, unsafe_allow_html=True)
            with st.expander("Preview email template before sending"):
                st.markdown(f"""
                <div class="email-preview">
                <div class="email-subject">Subject: {subj}</div>{body_txt}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            cta = (f'<a href="{step["url"]}" target="_blank" class="tl-btn">{step["cta"]}</a>'
                   if step.get("cta") else "")
            st.markdown(f"""
            <div class="tl-item">
              <div class="tl-left"><div class="tl-num">{step['n']}</div></div>
              <div class="tl-card">
                {phase_html}{title_html}{body_html}{cta}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── PRECEDENT + BEFORE/AFTER ──────────────────────────────────────────────
    st.markdown('<div id="precedent"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section section-w" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label sec-label-green">Legislative Precedent &amp; Proof</span>
      <h2 class="sec-h">It Has Been Done Before.<br>It Worked.</h2>
      <p class="sec-lead">Congress mandated ZIP code changes for four specific cities in 2006.
      Every one of those cities saw the harms resolved. S. 4505 uses the exact same mechanism — at 75-city scale.</p>

      <div class="prec-law">
        <p>"Section 1009 of the Postal Accountability and Enhancement Act (2006) directed the United States
        Postal Service to assign unique ZIP codes to the cities of Auburn, Ohio; Bradbury, California;
        Discovery Bay, California; and Hanahan, South Carolina."</p>
        <div class="prec-cite">PUBLIC LAW 109-435 · 109TH CONGRESS · SIGNED DECEMBER 20, 2006</div>
      </div>

      <div class="prec-stat-row">
        <div class="prec-stat">
          <div class="prec-n">4</div>
          <div class="prec-s">cities received unique ZIPs<br>via the 2006 precedent law</div>
        </div>
        <div class="prec-stat">
          <div class="prec-n">$193K</div>
          <div class="prec-s">estimated cost per ZIP adjustment<br>(0.0002% of USPS annual budget)</div>
        </div>
        <div class="prec-stat">
          <div class="prec-n">75+</div>
          <div class="prec-s">cities seeking the same fix today<br>via S. 4505 (Ernst)</div>
        </div>
      </div>

      <h3 style="font-size:1.35rem;font-weight:800;color:var(--blue);
        margin:3.5rem 0 0.6rem;letter-spacing:-0.015em;">
        Before vs. After: Hanahan, South Carolina</h3>
      <p style="font-size:0.93rem;color:var(--muted);line-height:1.82;
        margin-bottom:2rem;max-width:580px;">
        Hanahan incorporated in 1973 but shared a ZIP with North Charleston for decades.
        Section 1009 mandated a unique ZIP. Here is what changed immediately.</p>

      <div class="ba-grid">
        <div class="ba-col ba-before">
          <span class="ba-head">Before — Shared ZIP with North Charleston</span>
          <div class="ba-item">911 calls routed to North Charleston dispatch instead of Hanahan's own department</div>
          <div class="ba-item">City tax revenue credited to North Charleston ZIP in all state databases</div>
          <div class="ba-item">Census and federal datasets showed "North Charleston" — not Hanahan</div>
          <div class="ba-item">Businesses paid insurance rates based on North Charleston crime statistics</div>
          <div class="ba-item">Federal grant allocations calculated on incorrect population attribution</div>
        </div>
        <div class="ba-div-col">
          <div class="ba-arrow">→</div>
          <div class="ba-law">2006 Law</div>
        </div>
        <div class="ba-col ba-after">
          <span class="ba-head">After — Unique ZIP Assigned by Congress</span>
          <div class="ba-item">911 dispatch correctly routes all emergency calls to Hanahan Fire/Police</div>
          <div class="ba-item">Tax revenue properly attributed to Hanahan in all state and federal systems</div>
          <div class="ba-item">City appears independently in Census, ACS, and all federal databases</div>
          <div class="ba-item">Insurance rates recalculated on Hanahan's own lower risk profile</div>
          <div class="ba-item">Federal grant allocations corrected to reflect actual Hanahan population</div>
        </div>
      </div>

      <h3 style="font-size:1.2rem;font-weight:800;color:var(--blue);
        margin:3.5rem 0 0.25rem;letter-spacing:-0.015em;">Other 2006 Success Stories</h3>
      <div class="story-grid">
        <div class="story-card">
          <div class="story-city">Auburn, Ohio · 2006</div>
          <div class="story-title">Resolved Emergency Dispatch Conflicts</div>
          <div class="story-body">Auburn shared a ZIP with neighboring communities. After the 2006 unique ZIP mandate, all emergency services were correctly attributed and the city's identity was established in federal datasets for the first time.</div>
        </div>
        <div class="story-card">
          <div class="story-city">Bradbury, California · 2006</div>
          <div class="story-title">Corrected Tax and Data Attribution</div>
          <div class="story-body">This small LA County city had fiscal and census data folded into adjacent jurisdictions. A unique ZIP resolved misattribution in county, state, and federal reporting immediately upon implementation.</div>
        </div>
        <div class="story-card">
          <div class="story-city">Discovery Bay, California · 2006</div>
          <div class="story-title">Eliminated Logistics and Delivery Errors</div>
          <div class="story-body">Discovery Bay carriers incorrectly applied surcharges due to ZIP assignment. Resolution required a congressional mandate — the same path the coalition is now pursuing for 75+ cities simultaneously via S. 4505.</div>
        </div>
        <div class="story-card">
          <div class="story-city">The S. 4505 Coalition · 75+ Cities</div>
          <div class="story-title">The Same Fix, at Scale</div>
          <div class="story-body">S. 4505 uses the exact legislative mechanism that worked in 2006 — for 75+ cities at once, across 20+ states. The four prior bills have already cleared the full House. The precedent is established. The Senate must act.</div>
        </div>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── RESOURCES ─────────────────────────────────────────────────────────────
    st.markdown('<div id="resources"></div>', unsafe_allow_html=True)
    res_html = "".join(f"""
      <a href="{r['url']}" target="_blank" class="rcard">
        <div class="rcard-icon">{r['icon']}</div>
        <div class="rcard-type">{r['type']}</div>
        <div class="rcard-t">{r['title']}</div>
        <div class="rcard-d">{r['desc']}</div>
        <div class="rcard-arrow">{r['arrow']}</div>
      </a>""" for r in RESOURCES)
    st.markdown(f"""
    <div class="section section-g" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label">Media Kit &amp; Resources</span>
      <h2 class="sec-h">Everything You Need<br>to Make the Case</h2>
      <p class="sec-lead">Hand these to a journalist, a Senator's chief of staff,
      or a Chamber president. The 2026 White Paper is the coalition's primary evidence document.</p>
      <div class="res-grid">{res_html}</div>

      <div style="margin-top:4rem;">
        <span class="sec-label">Strategic Communications Guide</span>
        <h3 style="font-size:1.5rem;font-weight:800;color:var(--blue);
          margin-bottom:0.65rem;letter-spacing:-0.015em;">
          What to Say — and What Not to Say</h3>
        <p style="font-size:0.93rem;color:var(--muted);line-height:1.85;
          max-width:560px;margin-bottom:1.75rem;">
          Framing determines whether you're dismissed as a vanity request or treated as
          an infrastructure emergency. Every spokesperson and press contact should know this.</p>
        <div class="lang-grid">
          <div class="lang-col lang-avoid">
            <div class="lang-h">✗ Avoid — Sounds like a vanity request</div>
            <div class="lang-item">"We want our city's name on the mail."</div>
            <div class="lang-item">"This is about community identity and pride."</div>
            <div class="lang-item">"People deserve to have their city recognized."</div>
            <div class="lang-item">"It's confusing when our city name isn't in the address."</div>
          </div>
          <div class="lang-col lang-use">
            <div class="lang-h">✓ Use — Frames it as infrastructure</div>
            <div class="lang-item">"We require Geographic Integrity for public safety and fiscal accuracy."</div>
            <div class="lang-item">"ZIP code confusion costs lives, revenue, and economic opportunity."</div>
            <div class="lang-item">"This is a 911 infrastructure failure with documented consequences."</div>
            <div class="lang-item">"Smart Cities cannot run on 1960s postal routing logic."</div>
          </div>
        </div>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── CTA BAND ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-band">
      <div class="cta-inner">
        <h2 class="cta-h">The 119th Congress ends December 2026.<br>S. 4505 needs a Senate vote now.</h2>
        <p class="cta-p">Sen. Ernst has done her part. 75+ cities are organized. The lobbying
        infrastructure is in place. What's missing is Senate committee action.
        One email from your city to Sen. Rand Paul can change that.</p>
        <div class="cta-btns">
          <a href="#action" class="btn-cred">Take Action on S. 4505</a>
          <a href="mailto:afung@eastvaleca.gov" class="btn-coutline">Join the Coalition — Free →</a>
        </div>
        <div style="margin-top:2.5rem;padding-top:2rem;border-top:1px solid rgba(26,58,107,0.15);
          display:flex;gap:2.5rem;justify-content:center;flex-wrap:wrap;">
          <div style="text-align:center;">
            <div style="font-size:0.7rem;font-family:'IBM Plex Mono',monospace;letter-spacing:0.18em;
              text-transform:uppercase;color:var(--blue-m);margin-bottom:0.4rem;">Co-Chair · Castle Pines, CO</div>
            <div style="font-weight:800;color:var(--blue);font-size:0.95rem;margin-bottom:0.3rem;">Michael Penny</div>
            <a href="mailto:Michael.penny@castlepinesco.gov"
              style="font-size:0.85rem;color:var(--blue-m);text-decoration:none;">
              Michael.penny@castlepinesco.gov</a>
          </div>
          <div style="width:1px;background:rgba(26,58,107,0.12);"></div>
          <div style="text-align:center;">
            <div style="font-size:0.7rem;font-family:'IBM Plex Mono',monospace;letter-spacing:0.18em;
              text-transform:uppercase;color:var(--blue-m);margin-bottom:0.4rem;">Co-Chair · Eastvale, CA</div>
            <div style="font-weight:800;color:var(--blue);font-size:0.95rem;margin-bottom:0.3rem;">Alexander Fung</div>
            <a href="mailto:afung@eastvaleca.gov"
              style="font-size:0.85rem;color:var(--blue-m);text-decoration:none;">
              afung@eastvaleca.gov</a>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown("""
    <footer class="footer">
      <div class="footer-in">
        <div class="footer-grid">
          <div>
            <div class="fb-name">National ZIP Code Advocacy Coalition</div>
            <div class="fb-desc">A free working group of 75+ municipalities fighting for
            Geographic Integrity — public safety, fiscal accuracy, and data integrity.
            Founded April 2023. Co-Chairs: Michael Penny (Castle Pines, CO)
            and Alexander Fung (Eastvale, CA).</div>
          </div>
          <div>
            <div class="fc-h">Legislation</div>
            <a href="https://www.congress.gov/search?q=%22S.+4505%22&searchField=allfields" target="_blank" class="fa">S. 4505 (Ernst) ★</a>
            <a href="https://www.congress.gov/bill/119th-congress/house-bill/672" target="_blank" class="fa">H.R. 672</a>
            <a href="https://www.congress.gov/bill/119th-congress/house-bill/3095" target="_blank" class="fa">H.R. 3095</a>
            <a href="https://www.congress.gov/bill/119th-congress/senate-bill/1455" target="_blank" class="fa">S. 1455</a>
            <a href="https://www.congress.gov/bill/119th-congress/senate-bill/2961" target="_blank" class="fa">S. 2961</a>
            <a href="https://www.hsgac.senate.gov/" target="_blank" class="fa">HSGA Committee</a>
          </div>
          <div>
            <div class="fc-h">Coalition</div>
            <a href="https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/" target="_blank" class="fa">Coalition Website</a>
            <a href="https://www.eastvaleca.gov/home/showpublisheddocument/18184/639098699108370000" target="_blank" class="fa">2026 White Paper</a>
            <a href="https://www.eastvaleca.gov" target="_blank" class="fa">City of Eastvale, CA</a>
            <a href="https://www.castlepinesco.gov" target="_blank" class="fa">City of Castle Pines, CO</a>
            <div class="fc-h" style="margin-top:1.25rem;">Contact</div>
            <span class="fa" style="color:rgba(255,255,255,0.46);cursor:default;">Alexander Fung</span>
            <a href="mailto:afung@eastvaleca.gov" class="fa">afung@eastvaleca.gov</a>
            <span class="fa" style="color:rgba(255,255,255,0.46);cursor:default;">Michael Penny</span>
            <a href="mailto:Michael.penny@castlepinesco.gov" class="fa">Michael.penny@castlepinesco.gov</a>
          </div>
          <div>
            <div class="fc-h">Navigate</div>
            <a href="#problem"   class="fa">The Problem</a>
            <a href="#tracker"   class="fa">Bill Status</a>
            <a href="#members"   class="fa">Member Cities</a>
            <a href="#action"    class="fa">Take Action</a>
            <a href="#precedent" class="fa">Precedent</a>
            <a href="#resources" class="fa">Resources</a>
          </div>
        </div>
        <div class="foot-bar">
          <div class="foot-copy">© 2026 National ZIP Code Advocacy Coalition. All rights reserved.</div>
          <div class="foot-tag">119TH CONGRESS · JAN 2025 – DEC 2026 · S. 4505 · ONE CITY. ONE ZIP CODE.</div>
        </div>
      </div>
    </footer>
    """, unsafe_allow_html=True)
