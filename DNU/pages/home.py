import streamlit as st
import streamlit.components.v1 as components
import os

# ── Data ──────────────────────────────────────────────────────────────────────
CITIES = [
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
]

BILLS = [
    {
        "id": "H.R. 672",
        "author": "Rep. Mario Diaz-Balart (R-FL)",
        "cities": "8 cities",
        "chamber": "House",
        "status": "PASSED HOUSE",
        "status_class": "pill-passed",
        "date": "July 2025",
        "url": "https://www.congress.gov/bill/119th-congress/house-bill/672",
        "companion": "S. 1455",
        "note": "Companion to S. 1455. Awaiting Senate action."
    },
    {
        "id": "H.R. 3095",
        "author": "Rep. Lauren Boebert (R-CO)",
        "cities": "66 cities",
        "chamber": "House",
        "status": "PASSED HOUSE",
        "status_class": "pill-passed",
        "date": "July 2025",
        "url": "https://www.congress.gov/bill/119th-congress/house-bill/3095",
        "companion": "S. 2961",
        "note": "Companion to S. 2961. Awaiting Senate action."
    },
    {
        "id": "S. 1455",
        "author": "Sen. Rick Scott (R-FL)",
        "cities": "14 cities",
        "chamber": "Senate",
        "status": "STALLED — COMMITTEE",
        "status_class": "pill-stalled",
        "date": "—",
        "url": "https://www.congress.gov/bill/119th-congress/senate-bill/1455",
        "companion": "H.R. 672",
        "note": "Senate Homeland Security & Governmental Affairs Committee. Chairman: Sen. Rand Paul (R-KY)."
    },
    {
        "id": "S. 2961",
        "author": "Sen. Mike Banks (R-IN)",
        "cities": "69 cities",
        "chamber": "Senate",
        "status": "STALLED — COMMITTEE",
        "status_class": "pill-stalled",
        "date": "—",
        "url": "https://www.congress.gov/bill/119th-congress/senate-bill/2961",
        "companion": "H.R. 3095",
        "note": "Senate Homeland Security & Governmental Affairs Committee. Chairman: Sen. Rand Paul (R-KY)."
    },
]

PROBLEMS = [
    {
        "icon": "🚨",
        "title": "911 Emergency Delays",
        "body": "ZIP code confusion routes emergency calls to wrong dispatch centers, adding critical minutes. When a city's boundary crosses ZIP lines, first responders can be sent to the wrong jurisdiction.",
    },
    {
        "icon": "💸",
        "title": "Sales Tax Leakage",
        "body": "Local tax dollars generated inside a city's boundary are misallocated to neighboring jurisdictions. Greenwood Village, CO has one ZIP but four tax rates — a compliance nightmare for every business inside.",
    },
    {
        "icon": "📈",
        "title": "Insurance Premium Penalty",
        "body": "Insurers use ZIP codes to define rating territories. Low-risk cities sharing a ZIP with higher-risk neighbors absorb inflated premiums — with no recourse until the ZIP boundary changes.",
    },
    {
        "icon": "📦",
        "title": "Logistics Friction",
        "body": "Carriers use ZIP-based geofencing for delivery routing. New cities like Eastvale, CA are still classified under decades-old carrier routes — triggering rural surcharges and 'Address Not Found' errors.",
    },
    {
        "icon": "🗳️",
        "title": "Election Confusion",
        "body": "Voters in cities split across ZIP codes receive incorrect sample ballots, voter guides, and polling place instructions tied to neighboring jurisdictions — not their actual municipality.",
    },
    {
        "icon": "📊",
        "title": "Data Integrity Failure",
        "body": "Census data, crime analytics, health records, and economic reports are all aggregated by ZIP code. Cities without unique ZIPs are invisible or misrepresented in every dataset that drives public policy.",
    },
]

CASE_STUDIES = [
    {
        "tag": "Case Study A · Sales Tax",
        "title": "The Greenwood Village Model",
        "stat": "$20K+",
        "stat_lbl": "annual audit exposure per $2M in sales",
        "body": "ZIP code 80111 in Greenwood Village, CO contains four distinct sales tax rates within a single postal code. Standard ZIP-based tax software applies the wrong rate — and businesses don't discover the error until an audit. Coalition cities like Centennial, CO face the identical problem: sharing a ZIP with Aurora, Englewood, and Littleton means automated compliance tools misfile taxes by default.",
        "source": "Source: Avalara / Colorado DOR documented multi-jurisdiction cases",
    },
    {
        "tag": "Case Study B · Insurance",
        "title": "The Territory Penalty Trap",
        "stat": "20%+",
        "stat_lbl": "policy mis-assignment rate using ZIP-based territories",
        "body": "Actuarial research published in Insurance Journal found that companies using postal ZIP codes to define insurance rating territories mis-assign more than 20% of policies — and the error consistently skews toward overcharging in shared-ZIP situations. Low-crime coalition cities are paying high-crime insurance rates because their ZIP code is anchored to a neighboring metro's loss experience.",
        "source": "Source: Insurance Journal actuarial study; Consumer Federation of America research",
    },
    {
        "tag": "Case Study C · Logistics",
        "title": "The Eastvale Address Problem",
        "stat": "$26K",
        "stat_lbl": "annual surcharge cost at 100 shipments/week",
        "body": "Eastvale, CA incorporated in 2010 but still carries Mira Loma, CA as its official mailing city — a designation from when the area was unincorporated. UPS, FedEx, and Amazon systems route based on ZIP, triggering 'Address Not Found' errors, rural delivery surcharges, and 1–3 day delays on every affected shipment. For warehouse operations, this is a direct competitive disadvantage.",
        "source": "Source: City of Eastvale documented logistics cases; USPS carrier route designations",
    },
]

ACTIONS = [
    {
        "num": "01",
        "title": "Pass a Council Resolution",
        "body": "Formally resolve your city's support for ZIP code reform and send copies to your Senators and Congressmember. Template available in the Resources section."
    },
    {
        "num": "02",
        "title": "Write to Your Senator",
        "body": "Send an individual letter to each Senator on the Senate Homeland Security & Governmental Affairs Committee — especially Chairman Sen. Rand Paul (R-KY)."
    },
    {
        "num": "03",
        "title": "File a USPS Boundary Review",
        "body": "Submit a formal letter to USPS requesting a ZIP code boundary review. USPS must respond within 60 days. This runs parallel to legislative action."
    },
    {
        "num": "04",
        "title": "Submit a Story to the Bank",
        "body": "One verified incident of 911 confusion, sales tax error, insurance penalty, or logistics delay. Stories are the coalition's most powerful Congressional lobbying asset."
    },
    {
        "num": "05",
        "title": "Join the Coalition",
        "body": "No cost, no formal membership structure. Monthly meetings, shared resources, coordinated lobbying. Contact Alexander Fung at afung@eastvaleca.gov."
    },
    {
        "num": "06",
        "title": "Post the Social Wave",
        "body": "Each first Tuesday of the month, all 79+ coalition cities post simultaneously. Use the pre-designed graphic and caption from our media kit to create trending visibility."
    },
]

RESOURCES = [
    {
        "icon": "📋",
        "type": "Legislation",
        "title": "H.R. 672 — Full Bill Text",
        "desc": "View the complete text of H.R. 672 as introduced in the 119th Congress. Authored by Rep. Mario Diaz-Balart (R-FL). Passed the House in July 2025.",
        "url": "https://www.congress.gov/bill/119th-congress/house-bill/672",
        "link_text": "View on Congress.gov →",
    },
    {
        "icon": "📋",
        "type": "Legislation",
        "title": "H.R. 3095 — Full Bill Text",
        "desc": "View the complete text of H.R. 3095 as introduced in the 119th Congress. Authored by Rep. Lauren Boebert (R-CO). Passed the House in July 2025.",
        "url": "https://www.congress.gov/bill/119th-congress/house-bill/3095",
        "link_text": "View on Congress.gov →",
    },
    {
        "icon": "📋",
        "type": "Legislation",
        "title": "S. 1455 — Full Bill Text",
        "desc": "Senate companion to H.R. 672. Authored by Sen. Rick Scott (R-FL). Currently stalled in the Senate Homeland Security & Governmental Affairs Committee.",
        "url": "https://www.congress.gov/bill/119th-congress/senate-bill/1455",
        "link_text": "View on Congress.gov →",
    },
    {
        "icon": "📋",
        "type": "Legislation",
        "title": "S. 2961 — Full Bill Text",
        "desc": "Senate companion to H.R. 3095. Authored by Sen. Mike Banks (R-IN). Currently stalled in the Senate Homeland Security & Governmental Affairs Committee.",
        "url": "https://www.congress.gov/bill/119th-congress/senate-bill/2961",
        "link_text": "View on Congress.gov →",
    },
    {
        "icon": "🏛️",
        "type": "Coalition Website",
        "title": "Official Coalition Webpage",
        "desc": "The coalition's primary information hub, hosted on the City of Eastvale's website. Includes background, partnership opportunities, and contact information.",
        "url": "https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/",
        "link_text": "Visit Eastvale Coalition Page →",
    },
    {
        "icon": "📰",
        "type": "White Paper",
        "title": "Coalition White Paper",
        "desc": "The coalition's published white paper documenting how shared ZIP codes cause measurable harm to municipalities. Available on the City of Eastvale's website.",
        "url": "https://www.eastvaleca.gov",
        "link_text": "Download from eastvaleca.gov →",
    },
    {
        "icon": "⚖️",
        "type": "Legislative Precedent",
        "title": "Postal Accountability Act (2006)",
        "desc": "Section 1009 of this Act successfully mandated unique ZIP codes for Auburn (OH), Bradbury (CA), Discovery Bay (CA), and Hanahan (SC). The coalition's model for success.",
        "url": "https://www.congress.gov/bill/109th-congress/house-bill/6407",
        "link_text": "View on Congress.gov →",
    },
    {
        "icon": "🏛️",
        "type": "Committee",
        "title": "Senate HSGA Committee",
        "desc": "The Senate Homeland Security & Governmental Affairs Committee — where S. 1455 and S. 2961 are currently stalled. Chairman: Sen. Rand Paul (R-KY).",
        "url": "https://www.hsgac.senate.gov/",
        "link_text": "Visit Committee Website →",
    },
    {
        "icon": "💼",
        "type": "Research",
        "title": "ZIP Codes & Sales Tax Compliance",
        "desc": "Avalara's documented research on why ZIP codes fail as sales tax tools — with Colorado case studies directly relevant to coalition cities including Greenwood Village.",
        "url": "https://www.avalara.com/us/en/learn/whitepapers/zip-codes-the-wrong-tool-for-the-job.html",
        "link_text": "Read Avalara Research →",
    },
    {
        "icon": "📊",
        "type": "CBO Estimate",
        "title": "CBO Cost Estimate — H.R. 6303 (2016)",
        "desc": "Congressional Budget Office analysis finding ZIP code boundary adjustments cost approximately $193,000 each in 2025 dollars — a rounding error in USPS's $89 billion annual budget.",
        "url": "https://www.cbo.gov/",
        "link_text": "Search CBO.gov →",
    },
]

COMMITTEE_MEMBERS = [
    ("Rand Paul (Chair)", "R-KY"),
    ("Ron Johnson", "R-WI"),
    ("James Lankford", "R-OK"),
    ("Rick Scott", "R-FL"),
    ("Josh Hawley", "R-MO"),
    ("Bernie Moreno", "R-OH"),
    ("Joni Ernst", "R-IA"),
    ("Ashley Moody", "R-FL"),
    ("Gary Peters (Ranking)", "D-MI"),
    ("Margaret Hassan", "D-NH"),
    ("Richard Blumenthal", "D-CT"),
    ("John Fetterman", "D-PA"),
    ("Andy Kim", "D-NJ"),
    ("Ruben Gallego", "D-AZ"),
    ("Elissa Slotkin", "D-MI"),
]


def render():
    # ── NAV ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <nav class="nav-wrapper">
        <div class="nav-logo">National ZIP Code<br>Advocacy Coalition</div>
        <div class="nav-links">
            <a href="#the-problem" class="nav-link">The Problem</a>
            <a href="#business-case" class="nav-link">Business Case</a>
            <a href="#legislation" class="nav-link">Legislation</a>
            <a href="#members" class="nav-link">Members</a>
            <a href="#resources" class="nav-link">Resources</a>
            <a href="#take-action" class="nav-link">Take Action</a>
            <a href="mailto:afung@eastvaleca.gov" class="nav-link nav-cta">Join the Coalition</a>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    # ── TICKER ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="ticker-wrap">
        <span class="ticker-text">
            &nbsp;&nbsp;&nbsp;⚖ H.R. 672 PASSED HOUSE — July 2025 &nbsp;◆&nbsp;
            H.R. 3095 PASSED HOUSE — July 2025 &nbsp;◆&nbsp;
            S. 1455 STALLED — Senate HSGA Committee &nbsp;◆&nbsp;
            S. 2961 STALLED — Senate HSGA Committee &nbsp;◆&nbsp;
            79+ COALITION CITIES &nbsp;◆&nbsp; 20+ STATES &nbsp;◆&nbsp;
            CONTACT YOUR SENATOR TODAY &nbsp;◆&nbsp;
            119th CONGRESS WINDOW CLOSES JANUARY 2027 &nbsp;◆&nbsp;
            ONE CITY. ONE ZIP CODE. &nbsp;&nbsp;&nbsp;
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <section class="hero-section">
        <div class="hero-grid"></div>
        <div class="hero-eyebrow">National ZIP Code Advocacy Coalition &nbsp;·&nbsp; Founded 2023</div>
        <div class="hero-title">One City.</div>
        <div class="hero-title-accent">One ZIP Code.</div>
        <p class="hero-sub">
            79+ municipalities across 20+ states are fighting to end the chaos caused by USPS ZIP boundaries
            that ignore city limits — creating 911 delays, tax leakage, and insurance penalties for 1 million+ residents.
        </p>
        <div class="hero-stats">
            <div class="stat-pill"><span class="stat-num">79+</span><span class="stat-lbl">Member Cities</span></div>
            <div class="stat-pill"><span class="stat-num">20+</span><span class="stat-lbl">States</span></div>
            <div class="stat-pill"><span class="stat-num">1M+</span><span class="stat-lbl">Residents</span></div>
            <div class="stat-pill"><span class="stat-num">4</span><span class="stat-lbl">Federal Bills</span></div>
            <div class="stat-pill"><span class="stat-num">$0</span><span class="stat-lbl">Cost to Join</span></div>
        </div>
        <div class="hero-buttons">
            <a href="mailto:afung@eastvaleca.gov" class="btn-primary">Join the Coalition</a>
            <a href="#take-action" class="btn-outline">Take Action Today</a>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # ── CO-CHAIRS INTRO ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#001E46; padding: 3rem 2rem;">
    <div style="max-width:1200px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:3rem; align-items:center;">
        <div>
            <div class="section-tag">About the Coalition</div>
            <div class="section-title-light" style="font-size:2rem;">Geographic Integrity<br>Is Infrastructure</div>
            <p class="section-sub-light" style="margin-top:1rem;">
                ZIP codes haven't changed since 1963 — but America has.
                The National ZIP Code Advocacy Coalition was founded in April 2023 by the cities of Eastvale, CA and Castle Pines, CO
                to pool resources, share strategies, and push Congress to mandate what the USPS has failed to deliver voluntarily.
            </p>
            <p class="section-sub-light" style="margin-top:1rem;">
                The coalition meets quarterly, shares advocacy costs, and coordinates lobbying trips to Washington, D.C.
                Membership is free. The only requirement is a willingness to fight for your city's identity.
            </p>
        </div>
        <div style="display:flex; flex-direction:column; gap:1.5rem;">
            <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(201,168,76,0.25); border-radius:10px; padding:1.5rem; display:flex; gap:1rem; align-items:center;">
                <div style="font-size:2.5rem;">🏛️</div>
                <div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em; color:#C9A84C; margin-bottom:0.25rem;">CO-CHAIR</div>
                    <div style="font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:700; color:#FFFFFF;">Michael Penny</div>
                    <div style="font-size:0.82rem; color:rgba(255,255,255,0.5);">City Manager · City of Castle Pines, CO</div>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(201,168,76,0.25); border-radius:10px; padding:1.5rem; display:flex; gap:1rem; align-items:center;">
                <div style="font-size:2.5rem;">🏛️</div>
                <div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em; color:#C9A84C; margin-bottom:0.25rem;">CO-CHAIR</div>
                    <div style="font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:700; color:#FFFFFF;">Alexander Fung</div>
                    <div style="font-size:0.82rem; color:rgba(255,255,255,0.5);">Economic Development Manager · City of Eastvale, CA</div>
                    <a href="mailto:afung@eastvaleca.gov" style="font-size:0.78rem; color:#C9A84C; text-decoration:none;">afung@eastvaleca.gov</a>
                </div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── THE PROBLEM ──────────────────────────────────────────────────────────
    st.markdown('<div id="the-problem"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F8F6F0; padding: 5rem 2rem;">
    <div class="section" style="padding-top:0; padding-bottom:0;">
        <div class="section-tag">The Problem</div>
        <div class="section-title">1963 Postal Logic.<br>2026 Real-World Harm.</div>
        <p class="section-sub" style="margin-top:1rem;">
            The USPS designed ZIP codes for mail truck routing efficiency — not governance, fiscal accountability, or public safety.
            Sixty years later, growing municipalities are paying the price.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#F8F6F0; padding:0 2rem 5rem;">', unsafe_allow_html=True)
    col_container = st.container()
    with col_container:
        st.markdown('<div style="max-width:1200px; margin:0 auto;">', unsafe_allow_html=True)
        cards_html = '<div class="prob-grid">'
        for p in PROBLEMS:
            cards_html += f"""
            <div class="prob-card">
                <div class="prob-icon">{p['icon']}</div>
                <div class="prob-title">{p['title']}</div>
                <div class="prob-body">{p['body']}</div>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Eastvale visual callout
    st.markdown("""
    <div style="background:#001E46; padding:4rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="quote-block" style="background:rgba(201,168,76,0.08); border-left-color:#C9A84C;">
            <div class="quote-text" style="color:#FFFFFF;">
                "Eastvale is ONE city split across multiple ZIP codes. This creates confusion for residents,
                businesses, and emergency services — and it happens in 79+ cities across America."
            </div>
            <div class="quote-source" style="color:rgba(255,255,255,0.4); margin-top:0.75rem;">
                CITY OF EASTVALE, CA &nbsp;·&nbsp; VISUAL AID FOR CONGRESS &nbsp;·&nbsp; ZIP CODES 91752 & 92880
            </div>
        </div>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.5); margin-top:1.5rem; line-height:1.6;">
            The USPS acknowledged in its own documentation that "postal ZIP codes do not always align with municipal boundaries
            since ZIP code boundaries are based on mail routes and delivery points." Yet the agency has refused to act at scale
            without Congressional mandate.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── BUSINESS CASE ────────────────────────────────────────────────────────
    st.markdown('<div id="business-case"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F8F6F0; padding:5rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">Business Impact</div>
        <div class="section-title">The Bottom Line for Your Business</div>
        <p class="section-sub" style="margin-top:1rem;">
            This isn't about civic pride — it's about audit liability, insurance premiums, and logistics costs
            that hit your bottom line every quarter.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#F8F6F0; padding:0 2rem 5rem;">', unsafe_allow_html=True)
    cases_html = '<div class="section" style="padding-top:0;"><div class="case-grid">'
    for c in CASE_STUDIES:
        cases_html += f"""
        <div class="case-card">
            <div class="case-header">
                <div class="case-stat">{c['stat']}</div>
                <div class="case-stat-lbl">{c['stat_lbl']}</div>
            </div>
            <div class="case-body">
                <div class="case-tag">{c['tag']}</div>
                <div class="case-title">{c['title']}</div>
                <div class="case-desc">{c['body']}</div>
                <div style="margin-top:1rem; font-size:0.75rem; color:#9CA3AF; font-style:italic;">{c['source']}</div>
            </div>
        </div>"""
    cases_html += '</div></div>'
    st.markdown(cases_html, unsafe_allow_html=True)

    # ── LEGISLATION ──────────────────────────────────────────────────────────
    st.markdown('<div id="legislation"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#001E46; padding:5rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">119th Congress</div>
        <div class="section-title-light">Legislative Tracker</div>
        <p class="section-sub-light" style="margin-top:1rem;">
            Both House bills passed in July 2025. The critical path is now the Senate —
            specifically the Homeland Security &amp; Governmental Affairs Committee.
            The 119th Congress window closes January 2027.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Bill table
    table_html = """
    <div style="background:#001E46; padding:0 2rem 2rem;">
    <div class="section" style="padding:0;">
    <table class="bill-table">
    <thead><tr>
        <th>Bill</th><th>Author</th><th>Cities Covered</th><th>Status</th><th>Date</th><th>Companion</th><th>Link</th>
    </tr></thead><tbody>
    """
    for b in BILLS:
        table_html += f"""
        <tr>
            <td style="font-family:'Space Mono',monospace; font-weight:700; color:#C9A84C;">{b['id']}</td>
            <td>{b['author']}</td>
            <td style="font-family:'Space Mono',monospace; font-size:0.78rem;">{b['cities']}</td>
            <td><span class="bill-pill {b['status_class']}">{b['status']}</span></td>
            <td style="font-size:0.82rem; color:rgba(255,255,255,0.5);">{b['date']}</td>
            <td style="font-family:'Space Mono',monospace; font-size:0.78rem; color:#C9A84C;">{b['companion']}</td>
            <td><a href="{b['url']}" target="_blank" style="color:#63B3ED; font-size:0.82rem; text-decoration:none;">View →</a></td>
        </tr>"""
    table_html += "</tbody></table></div></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # Bill notes
    st.markdown("""
    <div style="background:#001629; padding:0 2rem 3rem;">
    <div class="section" style="padding-top:1.5rem; padding-bottom:0;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:2rem;">
            <div style="background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.2); border-radius:8px; padding:1.5rem;">
                <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em; color:#34D399; margin-bottom:0.5rem;">✓ HOUSE STATUS</div>
                <div style="font-size:0.92rem; color:rgba(255,255,255,0.8); line-height:1.6;">Both H.R. 672 and H.R. 3095 passed the full House of Representatives in July 2025. They represent bipartisan acknowledgment of the ZIP code problem.</div>
            </div>
            <div style="background:rgba(251,191,36,0.06); border:1px solid rgba(251,191,36,0.2); border-radius:8px; padding:1.5rem;">
                <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em; color:#FBB624; margin-bottom:0.5rem;">⏳ SENATE BOTTLENECK</div>
                <div style="font-size:0.92rem; color:rgba(255,255,255,0.8); line-height:1.6;">S. 1455 and S. 2961 are stalled in the Senate Homeland Security &amp; Governmental Affairs Committee. Both bills pass or fail together. Your Senator's voice matters now.</div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Committee
    st.markdown("""
    <div style="background:#001629; padding:0 2rem 4rem;">
    <div class="section" style="padding-top:2rem; padding-bottom:0;">
        <div class="section-tag">Senate Committee</div>
        <div class="section-title-light" style="font-size:1.75rem;">Homeland Security &amp; Governmental Affairs</div>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.5); margin:0.75rem 0 1.5rem; max-width:600px;">
            These 15 Senators hold the fate of ZIP code reform. Each coalition city should contact every Senator
            representing their state on this committee.
        </p>
        <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
    """, unsafe_allow_html=True)

    committee_html = '<div style="background:#001629; padding:0 2rem 0;"><div class="section" style="padding:0 0 0;"><div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0;">'
    for name, party_state in COMMITTEE_MEMBERS:
        color = "#63B3ED" if party_state.startswith("D") else "#FCA5A5"
        is_chair = "Chair" in name or "Ranking" in name
        bg = "rgba(201,168,76,0.12)" if is_chair else "rgba(255,255,255,0.04)"
        border = "rgba(201,168,76,0.4)" if is_chair else "rgba(255,255,255,0.1)"
        committee_html += f"""<div style="background:{bg}; border:1px solid {border}; border-radius:6px; padding:0.5rem 0.9rem; display:flex; align-items:center; gap:0.5rem;">
            <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:{color};">{party_state}</span>
            <span style="font-size:0.82rem; color:rgba(255,255,255,0.85);">{name}</span>
        </div>"""
    committee_html += '</div></div></div>'
    st.markdown(committee_html, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#001629; padding:1.5rem 2rem 4rem;">
    <div class="section" style="padding:0;">
        <a href="https://www.hsgac.senate.gov/" target="_blank" class="btn-outline" style="display:inline-block;">
            Visit Committee Website →
        </a>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MAP + MEMBERS ────────────────────────────────────────────────────────
    st.markdown('<div id="members"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F8F6F0; padding:5rem 2rem 3rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">Coalition Membership</div>
        <div class="section-title">79+ Cities. One Voice.</div>
        <p class="section-sub" style="margin-top:1rem;">
            From Castle Pines, CO to Hollywood, FL — growing cities across America are uniting
            under one demand: Geographic Integrity for public safety and fiscal accuracy.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive map embed
    st.markdown("""
    <div style="background:#F8F6F0; padding:0 2rem 3rem;">
    <div class="section" style="padding:0;">
    <div class="map-wrapper">
    """, unsafe_allow_html=True)

    map_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "usa_municipalities_status_map.html")
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=580, scrolling=False)
    except Exception:
        components.iframe(
            "https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/",
            height=580,
            scrolling=True
        )

    st.markdown("</div></div></div>", unsafe_allow_html=True)

    # City tags
    st.markdown('<div style="background:#F8F6F0; padding:0 2rem 5rem;"><div class="section" style="padding:0;">', unsafe_allow_html=True)
    city_html = '<div class="city-grid">'
    for city, state in sorted(CITIES, key=lambda x: x[0]):
        city_html += f'<div class="city-tag">{city} <span class="city-state">{state}</span></div>'
    city_html += '</div>'
    st.markdown(city_html, unsafe_allow_html=True)

    # State count
    states = sorted(set(s for _, s in CITIES))
    st.markdown(f"""
    <div style="margin-top:2rem; padding:1.25rem 1.5rem; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; display:inline-block;">
        <span style="font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:0.15em; color:#C9A84C;">STATES REPRESENTED</span><br>
        <span style="font-size:0.9rem; color:#001E46; margin-top:0.3rem; display:block;">{' · '.join(states)}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── RESOURCES ────────────────────────────────────────────────────────────
    st.markdown('<div id="resources"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0EDE4; padding:5rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">Media Kit &amp; Resources</div>
        <div class="section-title">Everything You Need to Advocate</div>
        <p class="section-sub" style="margin-top:1rem;">
            When a journalist, Senator's staffer, or business leader asks "Why does this matter?"
            — hand them this kit and the story writes itself.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#F0EDE4; padding:0 2rem 5rem;"><div class="section" style="padding:0;">', unsafe_allow_html=True)
    resources_html = '<div class="resource-grid">'
    for r in RESOURCES:
        resources_html += f"""
        <a href="{r['url']}" target="_blank" class="resource-card" style="text-decoration:none;">
            <div class="resource-icon">{r['icon']}</div>
            <div class="resource-type">{r['type']}</div>
            <div class="resource-title">{r['title']}</div>
            <div class="resource-desc">{r['desc']}</div>
            <div class="resource-link">{r['link_text']}</div>
        </a>"""
    resources_html += '</div>'
    st.markdown(resources_html, unsafe_allow_html=True)

    # Language guide callout
    st.markdown("""
    <div style="margin-top:3rem; background:#001E46; border-radius:12px; padding:2.5rem; position:relative; overflow:hidden;">
        <div style="position:absolute; right:-30px; top:-30px; width:150px; height:150px; border-radius:50%; background:rgba(201,168,76,0.08);"></div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.2em; color:#C9A84C; margin-bottom:1rem;">KEY STRATEGIC LANGUAGE</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;">
            <div>
                <div style="font-size:0.75rem; color:rgba(255,100,100,0.8); font-family:'Space Mono',monospace; letter-spacing:0.1em; margin-bottom:0.5rem;">❌ AVOID</div>
                <div style="font-size:0.9rem; color:rgba(255,255,255,0.6); font-style:italic;">"We want our city's name on the mail."</div>
                <div style="font-size:0.9rem; color:rgba(255,255,255,0.6); font-style:italic; margin-top:0.5rem;">"This is about community identity."</div>
            </div>
            <div>
                <div style="font-size:0.75rem; color:#34D399; font-family:'Space Mono',monospace; letter-spacing:0.1em; margin-bottom:0.5rem;">✓ USE</div>
                <div style="font-size:0.9rem; color:#FFFFFF; font-weight:500;">"We require Geographic Integrity for public safety and fiscal accuracy."</div>
                <div style="font-size:0.9rem; color:#FFFFFF; font-weight:500; margin-top:0.5rem;">"ZIP code confusion costs lives, revenue, and economic opportunity."</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── TAKE ACTION ──────────────────────────────────────────────────────────
    st.markdown('<div id="take-action"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#001E46; padding:5rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">Take Action</div>
        <div class="section-title-light">Six Steps to Move the Needle</div>
        <p class="section-sub-light" style="margin-top:1rem;">
            Every action below directly advances the Senate bill. Do all six and you've done everything
            a coalition city can do. Start with #2 — it's the most urgent.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#001E46; padding:0 2rem 5rem;"><div class="section" style="padding:0;">', unsafe_allow_html=True)
    actions_html = '<div class="action-grid">'
    for a in ACTIONS:
        actions_html += f"""
        <div class="action-card">
            <div class="action-num">{a['num']}</div>
            <div class="action-title">{a['title']}</div>
            <div class="action-body">{a['body']}</div>
        </div>"""
    actions_html += '</div>'
    st.markdown(actions_html, unsafe_allow_html=True)

    # CTA block
    st.markdown("""
    <div style="margin-top:3rem; background:linear-gradient(135deg, #C9A84C, #E8C46A); border-radius:12px; padding:3rem; text-align:center;">
        <div style="font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:#001E46; margin-bottom:0.75rem;">Ready to Join?</div>
        <p style="font-size:1rem; color:#001E46; opacity:0.75; max-width:480px; margin:0 auto 2rem; line-height:1.6;">
            Membership is free. Monthly meetings. Shared resources. Coordinated advocacy.
            One email gets you started.
        </p>
        <div style="display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
            <a href="mailto:afung@eastvaleca.gov" class="btn-primary" style="background:#001E46; border-color:#001E46; color:#C9A84C;">
                Email Alexander Fung →
            </a>
            <a href="https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/" target="_blank" class="btn-outline" style="border-color:#001E46; color:#001E46;">
                Visit Coalition Website →
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── PRECEDENT SECTION ───────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#F8F6F0; padding:4rem 2rem;">
    <div class="section" style="padding:0;">
        <div class="section-tag">Legislative Precedent</div>
        <div class="section-title">It Has Been Done Before</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:2rem; margin-top:2rem;">
            <div class="quote-block">
                <div class="quote-text">
                    "The Postal Accountability and Enhancement Act of 2006 (Section 1009) mandated unique ZIP codes
                    for Auburn, OH; Bradbury, CA; Discovery Bay, CA; and Hanahan, SC.
                    Congress has done this — and it worked."
                </div>
                <div class="quote-source">PUBLIC LAW 109-435 · 109TH CONGRESS · DECEMBER 2006</div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:1.75rem;">
                <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em; color:#C9A84C; margin-bottom:1rem;">CBO COST ESTIMATE</div>
                <div style="font-family:'Playfair Display',serif; font-size:2.5rem; font-weight:900; color:#001E46; line-height:1;">$193K</div>
                <div style="font-size:0.8rem; color:#6B7280; margin-bottom:1rem;">per ZIP code boundary adjustment (2025 dollars)</div>
                <div style="font-size:0.9rem; color:#4A5568; line-height:1.6;">
                    The CBO estimated ZIP code boundary adjustments cost approximately $193,000 each —
                    a rounding error against USPS's $89 billion annual operating budget.
                    Some coalition cities have offered to cost-share.
                </div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ───────────────────────────────────────────────────────────────
    st.markdown("""
    <footer class="site-footer">
        <div class="footer-grid">
            <div>
                <div class="footer-brand">One City.<br>One ZIP Code.</div>
                <div class="footer-tagline">
                    The National ZIP Code Advocacy Coalition is an informal working group of municipalities
                    across America fighting for Geographic Integrity — public safety, fiscal accuracy, and
                    data integrity for communities of every size.
                </div>
                <div style="margin-top:1.5rem; font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.12em; color:rgba(255,255,255,0.25);">
                    HOSTED BY CITY OF EASTVALE, CA<br>
                    CO-CHAIRED WITH CITY OF CASTLE PINES, CO
                </div>
            </div>
            <div>
                <div class="footer-heading">Legislation</div>
                <a href="https://www.congress.gov/bill/119th-congress/house-bill/672" target="_blank" class="footer-link">H.R. 672</a>
                <a href="https://www.congress.gov/bill/119th-congress/house-bill/3095" target="_blank" class="footer-link">H.R. 3095</a>
                <a href="https://www.congress.gov/bill/119th-congress/senate-bill/1455" target="_blank" class="footer-link">S. 1455</a>
                <a href="https://www.congress.gov/bill/119th-congress/senate-bill/2961" target="_blank" class="footer-link">S. 2961</a>
                <a href="https://www.hsgac.senate.gov/" target="_blank" class="footer-link">Senate HSGA Committee</a>
            </div>
            <div>
                <div class="footer-heading">Coalition</div>
                <a href="https://www.eastvaleca.gov/community/national-zip-code-advocacy-coalition/-fsiteid-1#!/" target="_blank" class="footer-link">Coalition Website</a>
                <a href="https://www.eastvaleca.gov" target="_blank" class="footer-link">City of Eastvale, CA</a>
                <a href="https://www.castlepinesco.gov" target="_blank" class="footer-link">City of Castle Pines, CO</a>
                <a href="mailto:afung@eastvaleca.gov" class="footer-link">Contact Alex Fung</a>
            </div>
            <div>
                <div class="footer-heading">Resources</div>
                <a href="#the-problem" class="footer-link">The Problem</a>
                <a href="#business-case" class="footer-link">Business Case</a>
                <a href="#resources" class="footer-link">Media Kit</a>
                <a href="#take-action" class="footer-link">Take Action</a>
                <a href="#members" class="footer-link">Member Cities</a>
            </div>
        </div>
        <hr class="footer-divider">
        <div class="footer-bottom">
            <div>© 2026 National ZIP Code Advocacy Coalition. All rights reserved.</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.1em; color:rgba(255,255,255,0.25);">
                119TH CONGRESS WINDOW · JAN 2025 – JAN 2027
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)
