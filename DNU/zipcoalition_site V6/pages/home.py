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

BILLS = [
    {"id":"H.R. 672","author":"Rep. Mario Diaz-Balart (R-FL)","cities":"8 cities",
     "badge":"b-g","prog":75,"cls":"bcard-p","companion":"S. 1455",
     "status":"PASSED HOUSE",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/672",
     "note":"Passed full House July 2025. Awaits Senate companion action."},
    {"id":"H.R. 3095","author":"Rep. Lauren Boebert (R-CO)","cities":"66 cities",
     "badge":"b-g","prog":75,"cls":"bcard-p","companion":"S. 2961",
     "status":"PASSED HOUSE",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/3095",
     "note":"Passed full House July 2025. Awaits Senate companion action."},
    {"id":"S. 1455","author":"Sen. Rick Scott (R-FL)","cities":"14 cities",
     "badge":"b-a","prog":35,"cls":"bcard-s","companion":"H.R. 672",
     "status":"SENATE COMMITTEE",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/1455",
     "note":"Stalled in Senate HSGA Committee. Chair: Sen. Rand Paul (R-KY)."},
    {"id":"S. 2961","author":"Sen. Mike Banks (R-IN)","cities":"69 cities",
     "badge":"b-a","prog":35,"cls":"bcard-s","companion":"H.R. 3095",
     "status":"SENATE COMMITTEE",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/2961",
     "note":"Stalled in Senate HSGA Committee. Chair: Sen. Rand Paul (R-KY)."},
]

PROBLEMS = [
    {"icon":"🚨","cls":"pcard-red","title":"Public Safety",
     "body":"ZIP confusion routes 911 calls to wrong dispatch centers. When a city boundary crosses ZIP lines, emergency response is delayed — and seconds determine outcomes.",
     "stat":"3 min+","stat_lbl":"avg 911 delay from mis-routing"},
    {"icon":"💰","cls":"pcard-amber","title":"Fiscal Accuracy",
     "body":"Sales tax revenue generated inside your city is credited to neighboring jurisdictions. ZIP 80111 spans four tax rates — every business is an audit waiting to happen.",
     "stat":"$20K+","stat_lbl":"annual audit exposure per $2M in sales"},
    {"icon":"📋","cls":"pcard-blue","title":"Insurance Equity",
     "body":"Insurers rate policies by ZIP, not city boundary. Low-risk coalition cities sharing a ZIP with higher-risk neighbors absorb inflated premiums with no recourse.",
     "stat":"20%+","stat_lbl":"territory mis-assignment error rate"},
    {"icon":"📦","cls":"pcard-green","title":"Logistics & Commerce",
     "body":"Carriers geofence by ZIP. Incorporated cities like Eastvale, CA still carry decades-old unincorporated labels — triggering rural surcharges and 'Address Not Found' failures.",
     "stat":"$26K","stat_lbl":"annual surcharge per 100 shipments/week"},
]

CASES = [
    {"stat":"$20K+","sub":"annual audit exposure per $2M in sales",
     "lbl":"Case Study A · Sales Tax","title":"The Greenwood Village Audit Trap",
     "desc":"ZIP 80111 spans four distinct sales tax rates. Compliance software applies the wrong rate by default. Coalition cities sharing ZIPs with Aurora, Englewood, and Littleton face identical risk. The IRS does not accept 'our ZIP code made us do it' as a defense.",
     "src":"Source: Avalara / Colorado DOR"},
    {"stat":"20%+","sub":"territory mis-assignment using ZIP-based data",
     "lbl":"Case Study B · Insurance","title":"The Shared-ZIP Premium Trap",
     "desc":"Actuarial research shows insurers using postal ZIPs mis-assign more than 20% of policies — consistently overcharging shared-ZIP municipalities. Low-crime coalition cities pay high-crime rates because their ZIP is anchored to a neighboring metro.",
     "src":"Source: Insurance Journal; Consumer Federation of America"},
    {"stat":"$26K","sub":"annual surcharge at 100 shipments per week",
     "lbl":"Case Study C · Logistics","title":"The Eastvale Address Problem",
     "desc":"Eastvale incorporated in 2010 but still carries 'Mira Loma, CA' as its USPS mailing city. UPS, FedEx, and Amazon trigger rural surcharges, 1–3 day delays, and 'Address Not Found' errors — a direct competitive disadvantage for every business in the city.",
     "src":"Source: City of Eastvale; USPS carrier route data"},
]

RESOURCES = [
    {"icon":"📋","type":"Legislation","title":"H.R. 672 — Full Bill Text",
     "desc":"Rep. Mario Diaz-Balart (R-FL). Passed House July 2025.",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/672","arrow":"View on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"H.R. 3095 — Full Bill Text",
     "desc":"Rep. Lauren Boebert (R-CO). Passed House July 2025.",
     "url":"https://www.congress.gov/bill/119th-congress/house-bill/3095","arrow":"View on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"S. 1455 — Full Bill Text",
     "desc":"Sen. Rick Scott (R-FL). In Senate HSGA Committee.",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/1455","arrow":"View on Congress.gov →"},
    {"icon":"📋","type":"Legislation","title":"S. 2961 — Full Bill Text",
     "desc":"Sen. Mike Banks (R-IN). In Senate HSGA Committee.",
     "url":"https://www.congress.gov/bill/119th-congress/senate-bill/2961","arrow":"View on Congress.gov →"},
    {"icon":"🏛️","type":"Coalition","title":"Official Coalition Webpage",
     "desc":"Primary hub on eastvaleca.gov with background, partners, and contact info.",
     "url":"https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/","arrow":"Visit eastvaleca.gov →"},
    {"icon":"⚖️","type":"Committee","title":"Senate HSGA Committee",
     "desc":"Where S. 1455 and S. 2961 are stalled. Chair: Sen. Rand Paul (R-KY).",
     "url":"https://www.hsgac.senate.gov/","arrow":"Visit Committee →"},
    {"icon":"📖","type":"Precedent","title":"Postal Accountability Act (2006)",
     "desc":"Section 1009 mandated unique ZIPs for Auburn OH, Hanahan SC, and others.",
     "url":"https://www.congress.gov/bill/109th-congress/house-bill/6407","arrow":"View on Congress.gov →"},
    {"icon":"📊","type":"Research","title":"ZIP Codes & Sales Tax (Avalara)",
     "desc":"Why ZIP codes fail as sales tax tools — Colorado case studies.",
     "url":"https://www.avalara.com/us/en/learn/whitepapers/zip-codes-the-wrong-tool-for-the-job.html","arrow":"Read Research →"},
    {"icon":"📰","type":"White Paper","title":"Coalition White Paper",
     "desc":"Published documentation of how shared ZIPs cause measurable municipal harm.",
     "url":"https://www.eastvaleca.gov","arrow":"Download from eastvaleca.gov →"},
]

STEPS = [
    {"n":"01","phase":"Phase 1 — Foundation","urgent":False,
     "title":"Pass a City Council Resolution",
     "body":"Formally resolve your council's support for S. 1455 and S. 2961. Send certified copies to your Senators and Congressmember. A resolution on official letterhead carries significantly more weight than a standard email — it creates an official paper trail that Senate staff catalog.",
     "cta":"Download Resolution Template →",
     "url":"https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/"},
    {"n":"02","phase":"⚡ URGENT — Phase 2","urgent":True,
     "title":"Write to Your Senate HSGA Committee Senator",
     "body":"This is the single most impactful action available right now. Every coalition city must send individual letters to each Senator on the Senate Homeland Security & Governmental Affairs Committee — especially Chairman Sen. Rand Paul (R-KY). Use the pre-filled template below and personalize with one specific impact from your city.",
     "cta":None,"url":None},
    {"n":"03","phase":"Phase 2 — Federal Push","urgent":False,
     "title":"File a USPS Boundary Review Request",
     "body":"Submit a formal letter to USPS requesting a ZIP code boundary review. USPS must acknowledge within 30 days and respond within 60. This runs parallel to — not instead of — the legislative push, and creates a formal administrative record.",
     "cta":"USPS Contact Directory →","url":"https://postalinspectors.uspis.gov/"},
    {"n":"04","phase":"Phase 2 — Federal Push","urgent":False,
     "title":"Submit a Verified Impact Story",
     "body":"One documented incident — a 911 confusion, a sales tax audit, an insurance penalty, or a logistics delay with a dollar figure attached — is the coalition's most powerful lobbying asset. Three sentences and one number is enough. Senators respond to constituent stories with specifics.",
     "cta":"Submit Your Impact Story →",
     "url":"mailto:afung@eastvaleca.gov?subject=Impact Story Submission"},
    {"n":"05","phase":"Phase 3 — Coalition Growth","urgent":False,
     "title":"Join the Formal Coalition",
     "body":"No cost. Monthly coordination meetings. Shared lobbying costs through Van Scoyoc Associates. One email to Alexander Fung gets your city into a working group of 79+ municipalities with active federal legislation already passed by the full House.",
     "cta":"Email Alexander Fung →","url":"mailto:afung@eastvaleca.gov"},
    {"n":"06","phase":"Phase 3 — Coalition Growth","urgent":False,
     "title":"Post the Monthly Social Media Wave",
     "body":"Every first Tuesday of the month, all coalition cities post simultaneously. The pre-designed graphic and caption are in the media kit. Coordinated volume creates national visibility that individual posts cannot. It takes three minutes and builds the political pressure the Senate needs to act.",
     "cta":"Download Social Media Kit →",
     "url":"https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/"},
]

def email_template(senator_name="Sen. Rand Paul"):
    subject = "Urgent: Please Advance S. 1455 and S. 2961 — ZIP Code Geographic Integrity Act"
    body = f"""Dear {senator_name},

I am writing on behalf of [Your City Name], a member of the National ZIP Code Advocacy Coalition — 79+ municipalities across 20+ states representing over 1 million residents.

I urge you to advance S. 1455 and S. 2961 through the Senate Homeland Security & Governmental Affairs Committee. Both companion House bills passed in July 2025. The Senate must act before January 2027.

Three documented harms our community experiences due to outdated ZIP boundaries:

1. PUBLIC SAFETY: 911 calls are routed to wrong dispatch centers. Response times increase. Lives are at risk.

2. FISCAL ACCURACY: Local sales tax revenue is credited to neighboring jurisdictions. Our businesses face audit exposure with no ability to self-correct.

3. ECONOMIC HARM: Insurance, logistics, and federal datasets all use ZIP codes — our city is systematically mis-rated and overcharged.

Congress has done this before. Section 1009 of the Postal Accountability and Enhancement Act (2006) mandated unique ZIP codes for Hanahan, SC and three other cities — and it worked. The estimated cost per adjustment is $193,327 — 0.0002% of USPS's $89B annual budget.

Please bring S. 1455 and S. 2961 to a committee vote.

Respectfully,
[Your Name]
[Your Title]
[City Name, State]"""
    return subject, body


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render():

    # ── NAV + ALERT (one call) ────────────────────────────────────────────────
    st.markdown("""
    <nav class="nav">
      <a class="nav-brand" href="#">
        <div class="nav-seal">🏛️</div>
        <div>
          <div class="nav-name">National ZIP Coalition Advocacy</div>
          <span class="nav-sub">119th Congress</span>
        </div>
      </a>
      <div class="nav-links">
        <a href="#problem"   class="nav-a">The Problem</a>
        <a href="#tracker"   class="nav-a">Bill Status</a>
        <a href="#members"   class="nav-a">Members</a>
        <a href="#action"    class="nav-a">Roadmap</a>
        <a href="#precedent" class="nav-a">Precedent</a>
        <a href="#resources" class="nav-a">Resources</a>
        <a href="#action" class="nav-urgent">
          <span class="nav-dot"></span>Contact Your Senator
        </a>
      </div>
    </nav>
    <div class="alert-bar">
      <span class="alert-pill">⚠ SENATE ACTION NEEDED</span>
      <span class="alert-msg">H.R. 672 and H.R. 3095 passed the House in July 2025.
      S. 1455 and S. 2961 are <strong>stalled in committee.</strong>
      The 119th Congress closes January 2027. —
      <a href="#action" class="alert-link">Take Action Now →</a></span>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO — full-width, stat bar ───────────────────────────────────────────
    st.markdown("""
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-kicker">
          <div class="hero-dot"></div>
        </div>
        <h1 class="hero-h1">
          <span style="color: rgba(255,255,255,0.95);">Congress Passed the Fix.</span><br>
          <span class="hero-h1-red">The Senate Must Act.</span>
        </h1>
        <p class="hero-sub">
          USPS ZIP code boundaries haven't been updated since 1963. Today they delay 911 calls,
          misallocate tax revenue, and systematically overcharge over one million Americans
          in 79 municipalities across 20+ states. Both House bills passed. The Senate is the last obstacle.
        </p>
        <div class="hero-ctas">
          <a href="#action" class="btn-hero-red">Contact Your Senator Now</a>
          <a href="#problem" class="btn-hero-ghost">See the Evidence →</a>
        </div>
      </div>
      <div class="hero-statbar">
        <div class="hst">
          <span class="hst-n">79+</span>
          <span class="hst-l">Member Cities</span>
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
          <span class="hst-n">4</span>
          <span class="hst-l">Active Federal Bills</span>
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
    tracker_html = "".join(f"""
      <div class="tcard {'tcard-passed' if b['prog']>=70 else 'tcard-stalled'}">
        <div class="tcard-num">{i+1}</div>
        <div class="tcard-id">{b['id']}</div>
        <div class="tcard-author">{b['author']}</div>
        <span class="tbadge {'tbadge-g' if b['prog']>=70 else 'tbadge-a'}">{b['status']}</span>
        <div class="tcard-note">{b['note']}</div>
        <div class="tprog">
          <div class="tprog-fill {'tprog-green' if b['prog']>=70 else 'tprog-amber'}"
               style="width:{b['prog']}%"></div>
        </div>
      </div>""" for i, b in enumerate(BILLS))
    st.markdown(f"""
    <div class="tracker-band">
    <div class="tracker-inner">
      <span class="tracker-label">📊 Live Legislative Progress — 119th Congress (Jan 2025 – Jan 2027)</span>
      <div class="tracker-grid">{tracker_html}</div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── THE PROBLEM — 4 cards ─────────────────────────────────────────────────
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
      <h2 class="sec-h">Four Ways Outdated ZIP Codes<br>Are Costing Your City — Right Now</h2>
      <p class="sec-lead">This is not a branding issue. These are documented, measurable harms
      affecting public safety, government revenue, and business competitiveness every single day.</p>
      <div class="prob-grid">{prob_html}</div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── CASE STUDIES ──────────────────────────────────────────────────────────
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
      <span class="sec-label">Business Impact</span>
      <h2 class="sec-h">The Numbers Don't Lie</h2>
      <p class="sec-lead">Three documented case studies. Real costs. Real cities. No ambiguity.</p>
      <div class="case-grid">{case_html}</div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── LEGISLATION + COMMITTEE ───────────────────────────────────────────────
    bill_html = "".join(f"""
      <div class="bcard {b['cls']}">
        <div class="bill-top">
          <div class="bill-id">{b['id']}</div>
          <span class="badge {b['badge']}">{b['status']}</span>
        </div>
        <div class="bill-author">{b['author']}</div>
        <div class="bill-cities">{b['cities']} · Companion: {b['companion']}</div>
        <div class="bill-note">{b['note']}</div>
        <a href="{b['url']}" target="_blank" class="bill-link">View on Congress.gov →</a>
      </div>""" for b in BILLS)

    cm_html = "".join(
        f'<div class="cm{" cm-chair" if r else ""}">'
        f'<span class="{"pr" if p=="R" else "pd"}">{p}-{s}</span>'
        f'{n}{(" ("+r+")" if r else "")}</div>'
        for n,p,s,r in COMMITTEE)

    st.markdown(f"""
    <div class="section section-w" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label">119th Congress · Jan 2025 – Jan 2027</span>
      <h2 class="sec-h">Legislative Tracker</h2>
      <p class="sec-lead">Both House bills passed. The path to law runs entirely through the
      Senate Homeland Security &amp; Governmental Affairs Committee.</p>
      <div class="bill-grid">{bill_html}</div>
      <div class="callout callout-a">
        <div class="callout-t">⚠ The Bottleneck: Senate HSGA Committee</div>
        <div class="callout-b">Both Senate bills pass or fail together. Chairman Sen. Rand Paul (R-KY)
        must bring them to a vote. Once the Senate acts, a House/Senate conference merges all four bills
        for White House signature. The 119th Congress window closes January 2027.</div>
      </div>
      <div style="margin-top:3rem;">
        <span class="sec-label sec-label-amber">Senate HSGA Committee — 15 Members</span>
        <p class="sec-lead" style="margin-bottom:0.5rem;">
          Contact every Senator from your state on this list.</p>
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
    <div class="section section-g" style="border-top:1px solid var(--border);padding-bottom:3rem;">
    <div class="inner">
      <span class="sec-label">Coalition Membership</span>
      <h2 class="sec-h">Is Your City a Member?<br>Who Represents You?</h2>
      <p class="sec-lead">Select your state to see coalition member cities and your HSGA Committee
      senator — then contact them directly with a pre-filled email template.</p>
    </div></div>
    """, unsafe_allow_html=True)

    # State lookup — Streamlit native (needs consistent inner padding)
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
            ✓ Pre-filled contact email
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

            # City chips
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

            # Senator rows
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
                         ✉ Email Senator
                      </a>
                    </div>"""
                senator_block = f"""
                <div style="border-top:1px solid var(--border);padding-top:1.1rem;margin-top:0.25rem;">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:600;
                    letter-spacing:0.18em;text-transform:uppercase;color:var(--red);
                    padding-top:0.85rem;border-top:3px solid var(--red);
                    width:fit-content;margin-bottom:0.85rem;">⚡ Your HSGA Senator(s)</div>
                  {sen_rows}
                </div>"""
            else:
                senator_block = f"""<p style="font-size:0.9rem;color:var(--muted);line-height:1.8;
                  border-top:1px solid var(--border);padding-top:1rem;margin-top:0.5rem;">
                  No HSGA Committee senators from {state_sel}. Contact the full committee at
                  <a href="https://www.hsgac.senate.gov/" target="_blank"
                     style="color:var(--blue-m);">hsgac.senate.gov</a>.</p>"""

            st.markdown(f"""
            <div style="background:var(--white);border:1px solid var(--border);
                 border-radius:10px;padding:1.5rem 1.75rem;">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:600;
                letter-spacing:0.18em;text-transform:uppercase;color:var(--blue-m);
                padding-top:0.85rem;border-top:3px solid var(--blue-m);
                width:fit-content;margin-bottom:0.9rem;">Coalition Cities in {state_sel}</div>
              {city_block}
              {senator_block}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:var(--white);border:2px dashed var(--border);
                 border-radius:10px;padding:3rem 2rem;text-align:center;
                 color:var(--g400);font-size:0.95rem;line-height:1.8;">
              ← Select your state to see coalition cities<br>and your HSGA Committee senator
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive map — wrapped in .inner for consistent alignment
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

    # Member directory dataframe
    st.markdown('<div style="padding:2.5rem 3.5rem 5rem;max-width:1160px;margin:0 auto;">', unsafe_allow_html=True)
    st.markdown("""
    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;font-weight:600;
      letter-spacing:0.22em;text-transform:uppercase;color:var(--blue-m);
      padding-top:1rem;border-top:3px solid var(--blue-m);
      width:fit-content;display:block;margin-bottom:0.85rem;">Member Directory — Searchable</span>
    <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;margin-bottom:1.25rem;max-width:500px;">
      Search by city name or filter by state. Coalition Density shows how many members each state has.</p>
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

    # ── ADVOCACY ROADMAP — TIMELINE ───────────────────────────────────────────
    ''' 
    st.markdown('<div id="action"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section section-g" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label sec-label-red">Advocacy Roadmap</span>
      <h2 class="sec-h">Six Steps. One Goal.<br>Move the Senate.</h2>
      <p class="sec-lead">
        <strong style="color:var(--red);">Step 2 is the most time-sensitive action available.</strong>
        Senate committee votes can happen with little public notice. The 119th Congress
        window closes in January 2027. Complete all six steps and your city has done
        everything possible to move this legislation.
      </p>
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
                  ✉ Open Pre-Filled Email to HSGA Committee
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
    '''

    # ── PRECEDENT + BEFORE/AFTER ──────────────────────────────────────────────
    st.markdown('<div id="precedent"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section section-w" style="border-top:1px solid var(--border);">
    <div class="inner">
      <span class="sec-label sec-label-green">Legislative Precedent &amp; Proof</span>
      <h2 class="sec-h">It Has Been Done Before.<br>It Worked.</h2>
      <p class="sec-lead">Congress mandated ZIP code changes for four specific cities in 2006.
      Every one of those cities saw the harms resolved. This is the coalition's proven template.</p>

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
          <div class="prec-n">$89B</div>
          <div class="prec-s">USPS annual operating budget —<br>the fiscal objection is negligible</div>
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
          <div class="story-body">Discovery Bay carriers incorrectly applied surcharges due to ZIP assignment. Resolution required a congressional mandate — the same path the coalition is now pursuing for 79+ cities simultaneously.</div>
        </div>
        <div class="story-card">
          <div class="story-city">The 2026 Coalition · All 79+ Cities</div>
          <div class="story-title">The Same Fix, at Scale</div>
          <div class="story-body">The coalition is pursuing the exact legislative mechanism that worked in 2006 — for 79+ cities at once, across 20+ states, with four active bills already cleared by the full House. The precedent is established. The Senate must act.</div>
        </div>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # ── RESOURCES + LANGUAGE GUIDE ────────────────────────────────────────────
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
      or a Chamber president. The story writes itself.</p>
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
        <h2 class="cta-h">The Senate Window<br>Closes January 2027</h2>
        <p class="cta-p">Both House bills passed. 79+ cities are organized. The lobbying
        infrastructure is in place. What's missing is Senate action. One email from your
        city to Sen. Rand Paul can change that.</p>
        <div class="cta-btns">
          <a href="#action" class="btn-cred">Contact Your Senator Now</a>
          <a href="mailto:afung@eastvaleca.gov" class="btn-coutline">Join the Coalition — Free →</a>
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
            <div class="fb-desc">A free working group of 79+ municipalities fighting for
            Geographic Integrity — public safety, fiscal accuracy, and data integrity.
            Founded April 2023. Co-Chairs: Michael Penny (Castle Pines, CO)
            and Alexander Fung (Eastvale, CA).</div>
          </div>
          <div>
            <div class="fc-h">Legislation</div>
            <a href="https://www.congress.gov/bill/119th-congress/house-bill/672" target="_blank" class="fa">H.R. 672</a>
            <a href="https://www.congress.gov/bill/119th-congress/house-bill/3095" target="_blank" class="fa">H.R. 3095</a>
            <a href="https://www.congress.gov/bill/119th-congress/senate-bill/1455" target="_blank" class="fa">S. 1455</a>
            <a href="https://www.congress.gov/bill/119th-congress/senate-bill/2961" target="_blank" class="fa">S. 2961</a>
            <a href="https://www.hsgac.senate.gov/" target="_blank" class="fa">HSGA Committee</a>
          </div>
          <div>
            <div class="fc-h">Coalition</div>
            <a href="https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/" target="_blank" class="fa">Coalition Website</a>
            <a href="https://www.eastvaleca.gov" target="_blank" class="fa">City of Eastvale, CA</a>
            <a href="https://www.castlepinesco.gov" target="_blank" class="fa">City of Castle Pines, CO</a>
            <a href="mailto:afung@eastvaleca.gov" class="fa">afung@eastvaleca.gov</a>
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
          <div class="foot-tag">119TH CONGRESS · JAN 2025–JAN 2027 · ONE CITY. ONE ZIP CODE.</div>
        </div>
      </div>
    </footer>
    """, unsafe_allow_html=True)

