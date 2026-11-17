import streamlit as st
import pandas as pd, numpy as np, joblib, json, os
from pathlib import Path
from datetime import date, datetime
import plotly.express as px
from agents import Pipeline, new_id

ROOT=Path(__file__).parent
st.set_page_config(page_title="JalSakhi AI | SDG 6",page_icon="💧",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
:root{--cream:#f7f6ef;--paper:#ffffff;--ink:#1c3028;--green:#23845b;--deep:#123f32;--mint:#e4f4eb;--aqua:#e7f4f4;--gold:#f4e7c8;--muted:#5c7066;--line:#e1e9e2}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:var(--ink)}
.stApp{background:linear-gradient(180deg,#f8f8f1 0%,#f2f7f2 100%);color:var(--ink)}
.block-container{padding-top:1.6rem;padding-bottom:3rem;max-width:1500px}
h1,h2,h3{font-family:'Manrope',sans-serif!important;letter-spacing:-.035em;color:var(--deep)!important}
h1{font-size:clamp(2.35rem,4.8vw,4.2rem)!important;line-height:1.03!important;font-weight:800!important}
h2{font-size:1.9rem!important;font-weight:800!important}h3{font-size:1.15rem!important;font-weight:800!important}
p,li,label,.stMarkdown{color:#263c32}
[data-testid="stSidebar"]{background:#edf4ed;border-right:1px solid #dce8dd}
[data-testid="stSidebar"] [data-testid="stMarkdown"] h2{color:#174b39!important}
[data-testid="stSidebar"] .stRadio label{font-weight:650;color:#294638}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 20px;box-shadow:0 8px 24px #173c2510;transition:transform .22s,box-shadow .22s}
[data-testid="stMetric"]:hover{transform:translateY(-3px);box-shadow:0 14px 28px #173c2518}
[data-testid="stMetricLabel"]{color:#5c7066!important;font-weight:700}
[data-testid="stMetricValue"]{color:#174b39!important;font-family:'Manrope',sans-serif;font-weight:800}
div[data-testid="stForm"],div[data-testid="stExpander"]{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px}
.stButton>button,.stDownloadButton>button{border-radius:999px;font-weight:750;min-height:2.8rem;border:1px solid #cbded0;transition:all .22s}
.stButton>button[kind="primary"]{background:#1f7652;color:white;border:0}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 9px 22px #173c2520;border-color:#23845b}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] div[data-baseweb="select"]{border-radius:12px}
.hero-shell{position:relative;overflow:hidden;border-radius:30px;background:linear-gradient(105deg,rgba(10,54,41,.93),rgba(18,82,59,.76)),url('https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?auto=format&fit=crop&w=1800&q=85') center/cover;padding:clamp(28px,5vw,58px);color:#fff;min-height:330px;display:flex;align-items:center;box-shadow:0 18px 50px #153f2b22;animation:fadeUp .65s ease both}
.hero-shell h1{color:#fff!important;max-width:760px}.hero-shell p{color:#eef8f0!important;font-size:1.1rem;max-width:650px;line-height:1.7}.hero-kicker{color:#bce8ca;font-size:.75rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;margin-bottom:16px}.hero-pill{display:inline-block;border:1px solid #ffffff55;background:#ffffff18;color:#fff;border-radius:999px;padding:8px 13px;margin:5px 6px 0 0;font-size:.82rem;font-weight:700}
.card{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;height:100%;box-shadow:0 8px 24px #173c2509;transition:transform .22s,box-shadow .22s}.card:hover{transform:translateY(-4px);box-shadow:0 15px 32px #173c2516}.card p{color:#53675c;line-height:1.65}.kicker{font-size:.75rem;text-transform:uppercase;letter-spacing:.16em;font-weight:800;color:#32835d;margin-bottom:7px}.section-note{color:#5b7065;font-size:1rem;line-height:1.65}.image-tile{border-radius:22px;overflow:hidden;border:1px solid #dce8dd;background:white;box-shadow:0 8px 24px #173c2510}.image-tile img{width:100%;height:150px;object-fit:cover;display:block}.image-tile div{padding:14px 16px}.image-tile strong{color:#174b39}.image-tile p{font-size:.9rem;margin:5px 0 0;color:#5b7065}
.notice{border-left:4px solid #e0ad4d;background:#fff8e8;color:#59451f;padding:14px 17px;border-radius:0 14px 14px 0}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#2d9869,#8bcf9b)}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:16px;overflow:hidden}

.section-banner{min-height:220px;border-radius:26px;background-size:cover;background-position:center;display:flex;align-items:center;padding:34px 42px;margin:4px 0 24px;box-shadow:0 14px 36px #153f2b18;animation:fadeUp .55s ease both}
.section-banner-copy{max-width:760px}
.section-banner h1{color:#fff!important;font-size:clamp(2rem,3.8vw,3.1rem)!important;margin:0 0 10px!important}
.section-banner p{color:#f0f8f1!important;font-size:1rem;line-height:1.6;margin:0;max-width:650px}
[data-testid="stSidebar"]{box-shadow:4px 0 22px #173c2508}
[data-testid="stRadio"] label{transition:background .2s ease,border-radius .2s ease}
[data-testid="stRadio"] label:hover{background:#dceee1;border-radius:12px}

@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes floatIn{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:translateY(0)}}
section[data-testid="stVerticalBlock"]>div{animation:floatIn .45s ease both}
@media(max-width:700px){.hero-shell{min-height:300px;padding:26px 22px}.hero-shell h1{font-size:2.4rem!important}.block-container{padding-left:1rem;padding-right:1rem}}

/* GLOBAL LIGHT TEXT FOR EVERY DARK / COLOURED STATUS BOX */
/* Covers Streamlit success, info, warning and error message containers,
   plus custom dark panels used anywhere in the application. */
[data-testid="stAlert"],
[data-testid="stAlert"] *,
[data-testid="stNotification"],
[data-testid="stNotification"] *,
.stAlert,
.stAlert *,
.dark-box,
.dark-box *,
.status-box,
.status-box *,
.notice-dark,
.notice-dark * {
    color: #F4FAF6 !important;
}

/* Keep links readable inside dark panels. */
[data-testid="stAlert"] a,
[data-testid="stNotification"] a,
.dark-box a,
.status-box a {
    color: #C8F1D8 !important;
    text-decoration: underline;
}

/* Ensure headings and emphasized status text are also light. */
[data-testid="stAlert"] h1,
[data-testid="stAlert"] h2,
[data-testid="stAlert"] h3,
[data-testid="stNotification"] h1,
[data-testid="stNotification"] h2,
[data-testid="stNotification"] h3,
.dark-box h1, .dark-box h2, .dark-box h3,
.status-box h1, .status-box h2, .status-box h3 {
    color: #FFFFFF !important;
}


/* JALSAKHI VILLAGE-FRIENDLY PREMIUM THEME */
:root{
 --cream:#f7f2e7;--paper:#fffefa;--ink:#19392e;--green:#24965f;
 --deep:#123d30;--mint:#e5f3e9;--muted:#52675d;--line:#e8e2d5;
}
.stApp{background:linear-gradient(180deg,#fbfaf6 0%,#f5f3eb 100%)!important;color:#19392e!important}
.block-container{max-width:1380px;padding-top:1.25rem;padding-bottom:3rem}
h1,h2,h3,h4{color:#173d30!important}
p,li,label,[data-testid="stMarkdownContainer"]{color:#29463a}
[data-testid="stSidebar"]{background:#f0eadc!important;border-right:1px solid #e2d8c5}
[data-testid="stSidebar"] *{color:#254638}
[data-testid="stSidebar"] [data-testid="stRadio"] label{font-weight:700;padding:7px 9px;border-radius:12px}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#e0eadf}
.hero-shell{
 min-height:340px;border-radius:28px;padding:clamp(30px,5vw,64px);
 background:linear-gradient(100deg,rgba(255,254,250,.97),rgba(247,242,231,.88)),
 url('https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?auto=format&fit=crop&w=1800&q=85') center/cover;
 color:#19392e;box-shadow:0 14px 38px #473c2512;display:flex;align-items:center;
 animation:fadeUp .65s ease both;border:1px solid #eee7d8
}
.hero-shell h1{color:#183d30!important;max-width:760px;font-size:clamp(2.3rem,4.7vw,4.1rem)!important}
.hero-shell p{color:#425d50!important;font-size:1.08rem;line-height:1.7;max-width:650px}
.hero-kicker{color:#27845a!important;font-weight:850;letter-spacing:.16em;font-size:.75rem}
.hero-pill{display:inline-block;background:#e5f3e9;color:#20583d;border:1px solid #cfe5d4;border-radius:999px;padding:9px 14px;margin:5px 6px 0 0;font-weight:750}
.card,.image-tile{background:#fffefa!important;color:#19392e!important;border:1px solid #e8e2d5!important;border-radius:22px;box-shadow:0 8px 26px #3c34200d;transition:transform .22s,box-shadow .22s}
.card{padding:22px;height:100%}
.card:hover,.image-tile:hover{transform:translateY(-3px);box-shadow:0 15px 30px #3c342018}
.card h2,.card h3,.card strong,.image-tile strong{color:#173d30!important}
.card p,.image-tile p{color:#52675d!important;line-height:1.65}
.kicker{color:#238354!important;font-weight:850;letter-spacing:.15em}
.section-banner{border-radius:24px;min-height:220px;padding:34px 42px;box-shadow:0 12px 30px #3c342018}
.section-banner h1,.section-banner p{color:#fff!important}
[data-testid="stMetric"]{background:#fffefa;border:1px solid #e8e2d5;border-radius:18px;padding:16px;box-shadow:0 7px 20px #3c34200b}
[data-testid="stMetricLabel"]{color:#586e62!important}
[data-testid="stMetricValue"]{color:#1d6947!important}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"] button{
 border-radius:999px;min-height:3rem;font-weight:800;border:1px solid #c8dcca;
 transition:all .2s ease
}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"] button[kind="primary"]{
 background:#23845b!important;color:#fff!important;border:0!important
}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 20px #153f2b20}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:#fffefa!important;color:#19392e!important;border-radius:12px}
[data-testid="stSelectbox"] div[data-baseweb="select"]{background:#fffefa!important;border-radius:12px}
div[data-testid="stForm"],div[data-testid="stExpander"]{background:#fffefa;border:1px solid #e8e2d5;border-radius:18px;padding:16px}
.image-tile img{height:175px;object-fit:cover;width:100%}
.notice{background:#fff4d9!important;color:#604a1e!important;border-left:5px solid #d9a441;padding:16px 18px;border-radius:0 14px 14px 0}
.notice *{color:#604a1e!important}
/* Dark alerts and dark panels always get light, readable text. */
[data-testid="stAlert"],[data-testid="stAlert"] *,
[data-testid="stNotification"],[data-testid="stNotification"] *,
.dark-box,.dark-box *,.status-box,.status-box *,.notice-dark,.notice-dark *{
 color:#f5fbf6!important
}
[data-testid="stAlert"]{background:#174b38!important;border:1px solid #28664e!important;border-radius:14px}
[data-testid="stAlert"] a,.dark-box a,.status-box a{color:#d6f5df!important;text-decoration:underline}
.dark-box,.status-box,.notice-dark{background:#123d30!important;border-radius:16px;padding:16px}
[data-testid="stDataFrame"]{border:1px solid #e8e2d5;border-radius:15px;overflow:hidden}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes softFloat{0%{transform:translateY(8px);opacity:0}100%{transform:translateY(0);opacity:1}}
section[data-testid="stVerticalBlock"]>div{animation:softFloat .35s ease both}
@media(max-width:700px){.hero-shell{min-height:280px;padding:24px}.section-banner{padding:24px;min-height:190px}.block-container{padding-left:1rem;padding-right:1rem}}

</style>
""",unsafe_allow_html=True)

SOURCES=pd.DataFrame([
 {"source_id":"BW-01","name":"Borewell 1","type":"Borewell","location":"North hamlet","active":True},
 {"source_id":"BW-02","name":"Borewell 2","type":"Borewell","location":"Main road","active":True},
 {"source_id":"OT-01","name":"Overhead Tank","type":"Tank","location":"Village center","active":True},
 {"source_id":"HP-01","name":"Hand Pump 1","type":"Hand pump","location":"School lane","active":True},
 {"source_id":"HP-02","name":"Hand Pump 2","type":"Hand pump","location":"South hamlet","active":True},
 {"source_id":"HP-03","name":"Hand Pump 3","type":"Hand pump","location":"Temple lane","active":True},
])
if "tests" not in st.session_state:
 rng=np.random.default_rng(17); rows=[]
 for _,s in SOURCES.iterrows():
  rows.append({"test_id":new_id("T"),"source_id":s.source_id,"source_name":s["name"],"test_date":date.today().isoformat(),
  "ph":round(float(rng.normal(7.2,.3)),2),"tds":int(rng.normal(330,60)),"turbidity":round(float(rng.uniform(.4,3.2)),2),
  "nitrate":round(float(rng.uniform(3,28)),1),"iron":round(float(rng.uniform(.05,.25)),2),"chlorine":round(float(rng.uniform(.15,.7)),2),
  "verified":False,"tester":"Demo record"})
 st.session_state.tests=pd.DataFrame(rows)
if "complaints" not in st.session_state: st.session_state.complaints=[]
if "messages" not in st.session_state: st.session_state.messages=[]
if "actions" not in st.session_state: st.session_state.actions=[]
if "pipeline" not in st.session_state: st.session_state.pipeline=Pipeline()

def latest(source_id):
 d=st.session_state.tests[st.session_state.tests.source_id==source_id]
 return d.sort_values("test_date").iloc[-1].to_dict() if len(d) else None
def risk_predict(row):
 path=ROOT/"water_risk_model.joblib"
 if not path.exists(): return None,None
 bundle=joblib.load(path); model=bundle["model"]
 vals=pd.DataFrame([{k:row.get(k,np.nan) for k in bundle["features"]}])
 prob=float(model.predict_proba(vals)[0][1])
 return ("Review recommended" if prob>=.5 else "No model flag"),prob
def status(row):
 if not row:return "No record available"
 if not row.get("verified",False):return "Awaiting VWSC verification"
 # prototype screening only, deliberately no safety certification
 label,prob=risk_predict(row)
 return "VWSC review recommended" if label=="Review recommended" else "No screening flag — verification still required"


def section_banner(title, subtitle, image_url, label="JALSAKHI • COMMUNITY WATER"):
    """Consistent photographic header used across all application sections."""
    st.markdown(f"""
    <div class="section-banner" style="background-image:linear-gradient(90deg,rgba(13,55,42,.88),rgba(13,55,42,.25)),url('{image_url}')">
      <div class="section-banner-copy">
        <div class="hero-kicker">{label}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)


def activate_resident_workspace():
    st.session_state.staff_page_active = False


def activate_staff_workspace():
    st.session_state.staff_page_active = True


with st.sidebar:
    st.markdown("## 💧 JalSakhi")
    st.caption("पाणी • COMMUNITY WATER")
    st.markdown("### For every household")

    resident_choice = st.radio(
        "Choose what you need",
        [
            "🏡 Home",
            "💧 Check water",
            "📝 Report a problem",
            "✅ Household checklist",
            "🤝 Simple help"
        ],
        label_visibility="collapsed",
        key="resident_choice",
        on_change=activate_resident_workspace
    )

    resident_pages = {
        "🏡 Home": "Home",
        "💧 Check water": "Is My Water Safe?",
        "📝 Report a problem": "Quick Report",
        "✅ Household checklist": "Household Water Checklist",
        "🤝 Simple help": "Village Help Center"
    }

    staff_pages = {
        "Village dashboard": "VWSC Dashboard",
        "Water tests": "Water Sources & Tests",
        "Maintenance": "Maintenance Planner",
        "Community updates": "Community Updates",
        "Agent activity": "Agent Activity",
        "Reports & export": "Reports & Export"
    }

    with st.expander("VWSC / Staff workspace"):
        staff_choice = st.radio(
            "Staff tools",
            list(staff_pages.keys()),
            label_visibility="collapsed",
            key="staff_choice",
            on_change=activate_staff_workspace
        )

        if st.button("Open staff workspace"):
            st.session_state.staff_page_active = True

    if st.session_state.get("staff_page_active", False):
        page = staff_pages[st.session_state.staff_choice]
    else:
        page = resident_pages[st.session_state.resident_choice]

    st.divider()
    st.caption("Large, simple steps · Marathi + English")
    st.caption("AI suggestions need VWSC verification")
if page=="Home":
 st.markdown("""<div class="hero-shell"><div><div class="hero-kicker">JALSAKHI • COMMUNITY WATER NETWORK • SDG 6</div><h1>Every drop matters.<br>Every voice counts.</h1><p>A simpler way for village households and the VWSC to report water concerns, track testing, coordinate action and share trusted updates.</p><span class="hero-pill">✦ Community-led</span><span class="hero-pill">✓ Human verified</span><span class="hero-pill">◉ Marathi + English</span></div></div>""",unsafe_allow_html=True)
 st.markdown("### Your village at a glance")
 st.markdown("### Start here — just choose one")
 quick_cols = st.columns(3)
 quick_cards = [
  ("💧", "Check my water", "See the latest recorded test and whether it has been verified."),
  ("📝", "Report a problem", "Tell the village committee about dirty water, smell or a leak."),
  ("✅", "Household checklist", "A short daily checklist for safe water storage habits.")
 ]
 for col,(ico,title,desc) in zip(quick_cols,quick_cards):
  with col:
   st.markdown(f'<div class="card"><div style="font-size:2.2rem">{ico}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
 st.info("Use the simple choices in the left menu. Staff tools are kept separately below.")
 a,b,c,d=st.columns(4)
 a.metric("Water sources",len(SOURCES),"being tracked")
 b.metric("Open concerns",sum(x["status"] not in ["Resolved"] for x in st.session_state.complaints),"need follow-up")
 c.metric("Test records",len(st.session_state.tests),"in village register")
 d.metric("Verified tests",int(st.session_state.tests.verified.sum()),"VWSC / tester confirmed")
 st.markdown("### What do you need today?")
 cols=st.columns(3)
 tiles=[("💧","Check a water source","View the latest available test record and verification status."),("📝","Report a concern","Tell the VWSC about muddy water, smell, leakage or supply issues."),("📊","Open VWSC workspace","Review cases, assign follow-ups and record committee actions.")]
 for col,(ico,title,desc) in zip(cols,tiles):
  with col: st.markdown(f'<div class="card"><div style="font-size:2rem;margin-bottom:12px">{ico}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
 st.markdown("### A connected village water workflow")
 flow=st.columns(5)
 steps=[("01","Community","Resident shares a concern"),("02","Understand","Communication Agent classifies it"),("03","Coordinate","Testing & Alert Agents route action"),("04","Verify","VWSC / lab records findings"),("05","Inform","Community receives an update")]
 for col,(n,title,desc) in zip(flow,steps):
  with col: st.markdown(f'<div class="card" style="padding:16px"><div class="kicker">STEP {n}</div><h3>{title}</h3><p style="font-size:.88rem">{desc}</p></div>',unsafe_allow_html=True)
 st.markdown("### Water is a shared responsibility")
 im1,im2,im3=st.columns(3)
 with im1: st.markdown('<div class="image-tile"><img src="https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=900&q=80"><div><strong>Reliable water sources</strong><p>Keep source records clear and up to date.</p></div></div>',unsafe_allow_html=True)
 with im2: st.markdown('<div class="image-tile"><img src="https://images.unsplash.com/photo-1581093458791-9d42e3c4e4f4?auto=format&fit=crop&w=900&q=80"><div><strong>Testing & verification</strong><p>Record field results and responsible review.</p></div></div>',unsafe_allow_html=True)
 with im3: st.markdown('<div class="image-tile"><img src="https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=900&q=80"><div><strong>Community action</strong><p>Bring residents and the VWSC into one workflow.</p></div></div>',unsafe_allow_html=True)
 st.markdown('<div class="notice"><strong>Important:</strong> JalSakhi is a decision-support prototype. An AI model or an unverified record cannot certify drinking-water safety. Follow the VWSC and responsible public-health authority guidance.</div>',unsafe_allow_html=True)
elif page=="Is My Water Safe?":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Is my water safe?', 'View the latest recorded water test and verification status for your village source.', 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">COMMUNITY QUICK CHECK</div><h1>Is my water safe?</h1><p>Choose your water source to see the latest recorded test and verification status.</p>',unsafe_allow_html=True)
 source=st.selectbox("Select water source",SOURCES.name.tolist())
 sid=SOURCES.loc[SOURCES.name==source,"source_id"].iloc[0]; row=latest(sid)
 if row:
  st.markdown(f'<div class="card"><div class="kicker">LATEST AVAILABLE RECORD</div><h2>{source}</h2><p>Test date: {row["test_date"]} · {row["tester"]}</p><h3>{status(row)}</h3></div>',unsafe_allow_html=True)
  x,y,z=st.columns(3);x.metric("pH",row["ph"]);y.metric("TDS",f'{row["tds"]} mg/L');z.metric("Turbidity",f'{row["turbidity"]} NTU')
  st.caption("This is a prototype record. Confirm with the VWSC/testing authority before drinking-water decisions.")
 else: st.warning("No test record is available. Please contact the VWSC for verification.")
 st.markdown("### Ask in Marathi or English")
 msg=st.text_input("Your question",placeholder="उदा. Borewell 1 water safe आहे का?")
 if st.button("Get community response",type="primary"):
  st.session_state.messages.append({"time":datetime.now().isoformat(timespec="minutes"),"message":msg,"response":f"{source}: {status(row)}"})
  st.success(f"{source}: {status(row)}")

elif page=="Quick Report":
 st.markdown('<div class="kicker">JALSAKHI • QUICK COMMUNITY REPORT</div>',unsafe_allow_html=True)
 section_banner('Tell us what happened.', 'Choose a problem, select the water source and send a short report to the village register.', 'https://images.unsplash.com/photo-1531206715517-5c0ba140b2b8?auto=format&fit=crop&w=1600&q=85')
 st.markdown("### 1. What did you notice?")
 issue = st.radio("Choose one option", [
  "पाणी गढूळ आहे / Water looks muddy",
  "पाण्याला वास येतो / Water smells unusual",
  "पाणी येत नाही / No water supply",
  "गळती आहे / Leak or broken pipe",
  "इतर समस्या / Something else"
 ], label_visibility="collapsed")
 with st.form("easy_report_form"):
  source = st.selectbox("2. Which water source?", SOURCES.name.tolist())
  details = st.text_area("3. Add a few words (optional)", placeholder="Where did this happen?")
  language = st.radio("Preferred language",["Marathi","English"],horizontal=True)
  sent = st.form_submit_button("Send report",type="primary",use_container_width=True)
 if sent:
  source_row=SOURCES[SOURCES.name==source].iloc[0].to_dict()
  message = issue + (f" — {details}" if details.strip() else "")
  case=st.session_state.pipeline.run(message,language,source_row["source_id"],source_row,st.session_state.complaints,latest(source_row["source_id"]))
  st.session_state.complaints.insert(0,case)
  receipt=f"JALSAKHI COMMUNITY REPORT\nReference: {case['case_id']}\nSource: {source}\nConcern: {message}\nDate: {case['created_at']}\nStatus: {case['status']}\nNext step: VWSC review is pending.\n"
  st.success(f"Report saved. Your reference number is {case['case_id']}.")
  st.download_button("Download your report receipt",receipt,file_name=f"{case['case_id']}_receipt.txt")
  st.caption("This saves the report on this running demo only. It does not send an SMS or contact officials automatically.")
elif page=="Household Water Checklist":
 st.markdown('<div class="kicker">JALSAKHI • HOUSEHOLD WATER CARE</div>',unsafe_allow_html=True)
 section_banner('Small habits. Better water care.', 'A simple household checklist for keeping stored water containers clean and covered.', 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=1600&q=85')
 st.markdown("### Tick each step as you complete it")
 st.caption("This checklist supports good storage habits. It cannot confirm that water is safe to drink.")
 checklist = [
  "I use a clean container for drinking water.",
  "The drinking-water container has a lid.",
  "I use a clean ladle or tap instead of dipping hands or cups.",
  "I keep the container away from chemicals and animals.",
  "I clean the container regularly.",
  "I report unusual colour, smell, taste or supply changes to the VWSC."
 ]
 completed = 0
 for item in checklist:
  if st.checkbox(item,key="household_"+str(checklist.index(item))):
   completed += 1
 st.progress(completed/len(checklist))
 st.markdown(f"**{completed} of {len(checklist)} steps completed**")
 if completed == len(checklist):
  st.success("Great work. Keep following local public-health guidance.")
 st.markdown('<div class="notice"><strong>Remember:</strong> Clear-looking water is not proof that it is safe. For drinking-water safety, follow verified test results and local health-authority instructions.</div>',unsafe_allow_html=True)

elif page=="Report a Concern":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Your voice matters.', 'Report water quality concerns, supply interruptions and maintenance issues in a few simple steps.', 'https://images.unsplash.com/photo-1531206715517-5c0ba140b2b8?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">COMMUNITY VOICE</div><h1>Tell us what happened.</h1><p>Short, simple reports help the VWSC arrange checks and follow-up.</p>',unsafe_allow_html=True)
 with st.form("complaint"):
  source=st.selectbox("Water source",SOURCES.name.tolist())
  language=st.radio("Language",["Marathi","English"],horizontal=True)
  msg=st.text_area("What did you notice?",placeholder="पाणी गढूळ आहे / Water looks muddy")
  contact=st.text_input("Optional phone/contact (demo only)")
  submit=st.form_submit_button("Send concern",type="primary")
 if submit:
  s=SOURCES[SOURCES.name==source].iloc[0].to_dict()
  case=st.session_state.pipeline.run(msg,language,s["source_id"],s,st.session_state.complaints,latest(s["source_id"]))
  case["contact"]=contact; st.session_state.complaints.insert(0,case)
  st.success(f"Concern recorded. Reference: {case['case_id']}")
  st.info("VWSC review is pending. This demo does not send a real SMS or WhatsApp message.")
elif page=="VWSC Dashboard":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Village water overview', 'A clear workspace for reviewing concerns, assigning follow-ups and recording committee action.', 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">COMMITTEE WORKSPACE</div><h1>Village water overview</h1>',unsafe_allow_html=True)
 cases=st.session_state.complaints
 a,b,c,d=st.columns(4);a.metric("Open",sum(x["status"]=="Open" for x in cases));b.metric("High priority",sum(x["priority"]=="High" for x in cases));c.metric("Testing",sum(x["status"]=="Testing" for x in cases));d.metric("Resolved",sum(x["status"]=="Resolved" for x in cases))
 if cases:
  df=pd.DataFrame([{k:x.get(k) for k in ["case_id","created_at","source_name","message","priority","status","assigned_to"]} for x in cases])
  st.dataframe(df,use_container_width=True,hide_index=True)
  selected=st.selectbox("Select case", [x["case_id"] for x in cases])
  case=next(x for x in cases if x["case_id"]==selected)
  col1,col2=st.columns(2)
  with col1:
   newstatus=st.selectbox("Update workflow status",["Open","Testing","Escalated","Resolved"],index=["Open","Testing","Escalated","Resolved"].index(case["status"]) if case["status"] in ["Open","Testing","Escalated","Resolved"] else 0)
   assigned=st.text_input("Assigned VWSC member",case.get("assigned_to","VWSC"))
  with col2:
   verified=st.checkbox("VWSC verification completed",value=case.get("verified",False))
   action=st.text_area("Action taken / notes",case.get("action_taken",""))
  if st.button("Save case update",type="primary"):
   case.update(status=newstatus,assigned_to=assigned,verified=verified,action_taken=action,updated_at=datetime.now().isoformat(timespec="minutes"))
   if newstatus=="Resolved":
    st.session_state.messages.append({"time":datetime.now().isoformat(timespec="minutes"),"message":case["case_id"],"response":f"Verified update: {action}"})
   st.success("Case updated.")
 else: st.info("No community concerns yet. Use Report a Concern to create one.")
elif page=="Water Sources & Tests":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Water sources & testing', 'Keep field measurements, source details and verification records together.', 'https://images.unsplash.com/photo-1581093458791-9d42e3c4e4f4?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">SOURCE RECORDS</div><h1>Water sources & tests</h1>',unsafe_allow_html=True)
 st.dataframe(SOURCES.rename(columns={"source_id":"ID","name":"Source","type":"Type","location":"Area","active":"Active"}),hide_index=True,use_container_width=True)
 st.markdown("### Add a field test")
 with st.form("test"):
  source=st.selectbox("Source",SOURCES.name.tolist()); testdate=st.date_input("Test date",date.today())
  x1,x2,x3=st.columns(3)
  ph=x1.number_input("pH",4.0,11.0,7.2,.1);tds=x2.number_input("TDS (mg/L)",0,5000,300);turb=x3.number_input("Turbidity (NTU)",0.0,100.0,1.0,.1)
  x4,x5,x6=st.columns(3)
  nitrate=x4.number_input("Nitrate (mg/L)",0.0,200.0,10.0);iron=x5.number_input("Iron (mg/L)",0.0,20.0,.1);chlor=x6.number_input("Chlorine (mg/L)",0.0,5.0,.4)
  tester=st.text_input("Tester / VWSC member"); verified=st.checkbox("Verified by responsible tester")
  save=st.form_submit_button("Save test record",type="primary")
 if save:
  sid=SOURCES.loc[SOURCES.name==source,"source_id"].iloc[0]
  row={"test_id":new_id("T"),"source_id":sid,"source_name":source,"test_date":str(testdate),"ph":ph,"tds":tds,"turbidity":turb,"nitrate":nitrate,"iron":iron,"chlorine":chlor,"verified":verified,"tester":tester or "VWSC"}
  st.session_state.tests=pd.concat([st.session_state.tests,pd.DataFrame([row])],ignore_index=True);st.success("Test record saved.")
 st.markdown("### Test history")
 st.dataframe(st.session_state.tests.sort_values("test_date",ascending=False),hide_index=True,use_container_width=True)
elif page=="Village Help Center":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Water help, made simple.', 'Practical guidance for households and an easy way to raise a village water request.', 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">HELP FOR EVERY HOUSEHOLD</div><h1>Water help, made simple.</h1>',unsafe_allow_html=True)
 topic=st.selectbox("Choose a help topic",["Water storage","What to do if water looks muddy","Report a leak","Monsoon water precautions","Contact VWSC"])
 helptext={
 "Water storage":"Use a clean, covered container. Avoid dipping hands or cups into stored water. Follow local health-authority advice.",
 "What to do if water looks muddy":"Do not assume appearance confirms safety. Report the source and concern to the VWSC and follow official local instructions.",
 "Report a leak":"Select Report a Concern and describe the location. The maintenance planner can record a responsible member and due date.",
 "Monsoon water precautions":"Keep storage containers covered and clean. Report sudden changes in smell, color, or taste. Follow verified local advisories.",
 "Contact VWSC":"Use Report a Concern to create a tracked record. This prototype uses demo communication and does not contact officials automatically."
 }
 st.markdown(f'<div class="card"><h2>{topic}</h2><p style="font-size:1.2rem">{helptext[topic]}</p></div>',unsafe_allow_html=True)
 st.markdown("### Quick concern")
 quick=st.text_input("Describe your concern")
 if st.button("Create help request"):
  st.session_state.complaints.append({"case_id":new_id("HELP"),"created_at":datetime.now().isoformat(timespec="minutes"),"source_id":"Unknown","source_name":"Village Help Center","message":quick,"intent":"general","priority":"Normal","status":"Open","assigned_to":"VWSC"})
  st.success("Help request added to VWSC Dashboard.")
elif page=="Maintenance Planner":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Care for every water source.', 'Plan inspections, assign responsibility and keep maintenance follow-ups visible.', 'https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">PREVENTIVE FOLLOW-UP</div><h1>Keep sources maintained.</h1><p>Record leaks, tank cleaning, and maintenance reminders. This is a local planner, not an automated government schedule.</p>',unsafe_allow_html=True)
 with st.form("maintenance"):
  title=st.text_input("Maintenance task",placeholder="Inspect overhead tank")
  source=st.selectbox("Source",SOURCES.name.tolist())
  due=st.date_input("Due date",date.today())
  owner=st.text_input("Responsible person / group","VWSC")
  notes=st.text_area("Notes")
  add=st.form_submit_button("Add maintenance task",type="primary")
 if add:
  st.session_state.actions.append({"task_id":new_id("M"),"task":title,"source":source,"due":str(due),"owner":owner,"notes":notes,"status":"Planned"})
  st.success("Maintenance task added.")
 if st.session_state.actions:
  st.dataframe(pd.DataFrame(st.session_state.actions),hide_index=True,use_container_width=True)
  tid=st.selectbox("Mark task complete", [x["task_id"] for x in st.session_state.actions])
  if st.button("Mark completed"):
   next(x for x in st.session_state.actions if x["task_id"]==tid)["status"]="Completed";st.success("Updated.")
 else: st.info("No maintenance tasks yet.")
elif page=="Community Updates":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Updates for everyone.', 'Share clear, committee-confirmed information with the whole community.', 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">TRANSPARENT STATUS</div><h1>Updates for everyone.</h1><p>Only committee-confirmed messages should be treated as verified public updates.</p>',unsafe_allow_html=True)
 for m in reversed(st.session_state.messages):
  st.markdown(f'<div class="card"><small>{m["time"]}</small><h3>{m["message"]}</h3><p>{m["response"]}</p></div>',unsafe_allow_html=True)
 if not st.session_state.messages: st.info("No updates yet.")
 st.markdown("### Draft community notice")
 source=st.selectbox("Source",SOURCES.name.tolist(),key="notice_source");sid=SOURCES.loc[SOURCES.name==source,"source_id"].iloc[0];row=latest(sid)
 notice=f"VILLAGE WATER UPDATE\\nSource: {source}\\nLatest record: {row['test_date'] if row else 'Unavailable'}\\nStatus: {status(row)}\\nPlease follow verified VWSC/authority instructions."
 st.text_area("Notice-board-ready text",notice,height=160)
 st.download_button("Download notice (.txt)",notice,file_name="village_water_notice.txt")
elif page=="Agent Activity":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Five agents. One shared workflow.', 'See how each specialist agent contributes to a single traceable water-response process.', 'https://images.unsplash.com/photo-1581093588401-fbb62a02f120?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">MULTI-AGENT PIPELINE</div><h1>Five agents. One shared workflow.</h1>',unsafe_allow_html=True)
 agents=[("01","Community Communication Agent","Understands report intent, language, source, and creates a case."),("02","Local Testing Agent","Attaches source/test context and recommends field verification."),("03","Alert Agent","Creates priority alert and acknowledgment tracking."),("04","Escalation & Lab Coordination Agent","Routes high-priority concerns for VWSC/lab review."),("05","Village Water Record Agent","Adds source history context and supports traceability.")]
 for n,name,desc in agents:
  st.markdown(f'<div class="card"><div class="kicker">AGENT {n}</div><h3>{name}</h3><p>{desc}</p><span style="color:#159447;font-weight:700">● Ready</span></div>',unsafe_allow_html=True)
 st.markdown("### Live pipeline demo")
 st.caption("The five agents share one case record. Their output is a recommendation for committee review, not an automatic public alert.")
 msg=st.text_input("Sample village message", "पाणी गढूळ आहे")
 source=st.selectbox("Source for demo",SOURCES.name.tolist(),key="pipeline_source")
 if st.button("Run multi-agent pipeline",type="primary"):
  s=SOURCES[SOURCES.name==source].iloc[0].to_dict()
  result=st.session_state.pipeline.run(msg,"Marathi",s["source_id"],s,st.session_state.complaints,latest(s["source_id"]))
  st.json(result)
elif page=="Reports & Export":
 st.markdown('<div class="kicker">JALSAKHI • COMMUNITY WATER</div>', unsafe_allow_html=True)
 section_banner('Village reports & records', 'Review key activity and export records for transparent follow-up.', 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600&q=85')
 st.markdown('<div class="kicker">ACCOUNTABILITY</div><h1>Village reports</h1>',unsafe_allow_html=True)
 tests=st.session_state.tests;cases=st.session_state.complaints
 st.metric("Concerns logged",len(cases));st.metric("Verified test records",int(tests.verified.sum()))
 st.markdown("### Source-wise testing")
 if len(tests): st.plotly_chart(px.bar(tests,x="source_name",y="tds",color="source_name",title="Recorded TDS by source"),use_container_width=True)
 st.markdown("### Download records")
 st.download_button("Download test records CSV",tests.to_csv(index=False),file_name="water_tests.csv")
 st.download_button("Download concerns CSV",pd.DataFrame(cases).to_csv(index=False),file_name="community_concerns.csv")
 st.download_button("Download maintenance CSV",pd.DataFrame(st.session_state.actions).to_csv(index=False),file_name="maintenance_tasks.csv")
 st.download_button("Download full prototype JSON",json.dumps({"tests":tests.to_dict(orient="records"),"complaints":cases,"messages":st.session_state.messages,"maintenance":st.session_state.actions},indent=2,default=str),file_name="jalSakhi_records.json")
