"""A fixed, top-to-bottom visual story about warehouse labor standards."""

from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="From PPH to a Digital Twin",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ASSET_DIR = Path(__file__).parent / "assets"
WAREHOUSE_IMAGE = ASSET_DIR / "warehouse_digital_twin.png"


st.markdown(
    """
    <style>
      :root {
        --ink: #07111F;
        --paper: #F6F8FB;
        --card: #FFFFFF;
        --muted: #5D6B7E;
        --line: #DDE4ED;
        --navy: #10233E;
        --blue: #4D7CFE;
        --mint: #34C99A;
        --orange: #FF9A5D;
        --red: #EE6A63;
      }
      .stApp { background: var(--paper); }
      [data-testid="stSidebar"],
      [data-testid="stSidebarCollapsedControl"] { display: none !important; }
      [data-testid="stHeader"] { background: rgba(0,0,0,0); }
      .block-container {
        max-width: 1180px;
        padding: 3.2rem 2rem 5rem 2rem;
      }
      .eyebrow {
        color: #3B67E5;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
      }
      .hero-title {
        color: var(--ink);
        font-size: clamp(2.45rem, 5vw, 4.8rem);
        font-weight: 780;
        line-height: 1.02;
        letter-spacing: -0.06em;
        margin: 0 0 1.2rem 0;
      }
      .hero-copy {
        color: var(--muted);
        font-size: 1.16rem;
        line-height: 1.58;
        max-width: 510px;
        margin: 0;
      }
      .label {
        color: #3B67E5;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
      }
      .section-title {
        color: var(--ink);
        font-size: clamp(1.7rem, 3vw, 2.55rem);
        font-weight: 750;
        line-height: 1.08;
        letter-spacing: -0.045em;
        margin: 0.35rem 0 0.8rem 0;
      }
      .section-copy {
        color: var(--muted);
        font-size: 1.04rem;
        line-height: 1.55;
        max-width: 740px;
      }
      [data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0 22px 48px rgba(23, 40, 70, 0.18);
      }
      .story-rule {
        height: 1px;
        background: var(--line);
        margin: 5.0rem 0;
      }
      .task-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 26px rgba(24, 43, 70, 0.06);
      }
      .task-card-head {
        display: flex;
        gap: 0.65rem;
        align-items: center;
        padding: 1rem 1.15rem 0.25rem 1.15rem;
      }
      .task-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex: none;
      }
      .task-name {
        color: var(--ink);
        font-weight: 780;
        font-size: 1.05rem;
      }
      .task-copy {
        color: var(--muted);
        line-height: 1.48;
        padding: 0.35rem 1.15rem 1.1rem 1.15rem;
        min-height: 70px;
      }
      .pph-strip {
        background: #EEF2F7;
        color: #3D4E64;
        font-size: 0.8rem;
        font-weight: 750;
        padding: 0.7rem 1.15rem;
        border-top: 1px solid var(--line);
      }
      .center-message {
        background: var(--navy);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 1.35rem 1.15rem;
        margin: 1.25rem 0 0 0;
        text-align: center;
      }
      .center-message .small {
        color: #9CC3FF;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
      }
      .center-message .main {
        font-size: 1.28rem;
        line-height: 1.25;
        font-weight: 720;
        margin-top: 0.35rem;
      }
      .flow {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 2rem;
      }
      .flow-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.1rem;
        min-height: 180px;
        position: relative;
      }
      .flow-card:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.83rem;
        top: 43%;
        z-index: 2;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 50%;
        background: var(--blue);
        color: #FFF;
        display: grid;
        place-items: center;
        font-weight: 800;
      }
      .flow-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: grid;
        place-items: center;
        font-size: 1.05rem;
        margin-bottom: 1rem;
      }
      .flow-card h3 {
        color: var(--ink);
        font-size: 1rem;
        margin: 0 0 0.45rem 0;
      }
      .flow-card p {
        color: var(--muted);
        font-size: 0.87rem;
        line-height: 1.45;
        margin: 0;
      }
      .motion-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.42rem;
        margin-top: 0.8rem;
      }
      .motion {
        color: #254670;
        background: #ECF3FF;
        border: 1px solid #D6E5FF;
        border-radius: 100px;
        padding: 0.24rem 0.52rem;
        font-size: 0.72rem;
        font-weight: 700;
      }
      .twin-board {
        background: linear-gradient(135deg, #0E203A 0%, #142C4E 100%);
        border-radius: 22px;
        padding: 1.6rem;
        box-shadow: 0 22px 44px rgba(23, 40, 70, 0.16);
      }
      .twin-label {
        color: #92B9FF;
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }
      .twin-title {
        color: #FFFFFF;
        font-size: clamp(1.45rem, 3vw, 2.2rem);
        letter-spacing: -0.04em;
        line-height: 1.1;
        margin: 0.45rem 0 0.7rem 0;
      }
      .twin-copy {
        color: #C3D4EC;
        font-size: 0.98rem;
        line-height: 1.5;
        max-width: 610px;
      }
      .test-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1.35rem;
      }
      .test-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(169, 197, 239, 0.20);
        border-radius: 14px;
        padding: 1rem;
      }
      .test-card h3 {
        color: #FFFFFF;
        font-size: 0.96rem;
        margin: 0 0 0.35rem 0;
      }
      .test-card p {
        color: #BFD0E8;
        font-size: 0.82rem;
        line-height: 1.42;
        margin: 0;
      }
      .closing {
        color: var(--ink);
        font-size: clamp(1.8rem, 4vw, 3.3rem);
        font-weight: 760;
        line-height: 1.08;
        letter-spacing: -0.05em;
        max-width: 900px;
        margin-top: 1rem;
      }
      @media (max-width: 800px) {
        .block-container { padding: 2rem 1rem 4rem 1rem; }
        .flow { grid-template-columns: 1fr 1fr; }
        .flow-card:not(:last-child)::after { display: none; }
        .test-grid { grid-template-columns: 1fr; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="eyebrow">Labor standards • workload forecasting • digital twin</div>', unsafe_allow_html=True)
hero_copy, hero_visual = st.columns([0.92, 1.08], gap="large")
with hero_copy:
    st.markdown(
        '<h1 class="hero-title">A warehouse can have the right volume and still schedule the wrong labor.</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-copy">When every pallet is treated as the same unit of work, the plan cannot see the travel, equipment, elevation, handling, or congestion that actually determines labor. Without standards, a workload-driven forecast, or a digital twin, teams are left to react on the floor.</p>',
        unsafe_allow_html=True,
    )
with hero_visual:
    if WAREHOUSE_IMAGE.exists():
        st.image(str(WAREHOUSE_IMAGE), width="stretch")
    else:
        st.info("Warehouse digital-twin visual will appear here.")
    st.caption("Illustrative warehouse digital-twin environment")


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">The PPH problem</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Two pallet moves can share one PPH metric but require completely different work.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">PPH is useful as a high-level output. It becomes misleading when it is used as the labor standard itself. The same count conceals the operational conditions behind each movement.</p>',
    unsafe_allow_html=True,
)

short_html = """
<div class="task-card">
  <div class="task-card-head"><span class="task-dot" style="background:#34C99A"></span><span class="task-name">Pallet A: a simple move</span></div>
  <div style="padding:0.45rem 1.0rem 0.3rem 1.0rem">
    <svg viewBox="0 0 520 185" width="100%" role="img" aria-label="Short ground-level pallet route">
      <rect x="8" y="10" width="504" height="162" rx="14" fill="#F3F8F7"/>
      <rect x="310" y="31" width="118" height="98" rx="4" fill="#7891A5"/>
      <g stroke="#F3F8F7" stroke-width="4"><line x1="310" y1="63" x2="428" y2="63"/><line x1="310" y1="96" x2="428" y2="96"/><line x1="349" y1="31" x2="349" y2="129"/><line x1="389" y1="31" x2="389" y2="129"/></g>
      <rect x="347" y="101" width="37" height="20" fill="#F2C84A"/><rect x="351" y="94" width="29" height="10" fill="#D59B45"/>
      <path d="M100,122 C170,122 220,122 329,122" fill="none" stroke="#34C99A" stroke-width="8" stroke-linecap="round"/>
      <polygon points="329,122 313,113 313,131" fill="#34C99A"/>
      <rect x="67" y="102" width="44" height="26" rx="3" fill="#F7C84C"/><rect x="106" y="92" width="13" height="42" fill="#22344B"/><circle cx="78" cy="135" r="8" fill="#22344B"/><circle cx="108" cy="135" r="8" fill="#22344B"/>
      <text x="55" y="157" fill="#4E657A" font-size="16" font-family="Arial">Forklift</text>
      <text x="305" y="157" fill="#4E657A" font-size="16" font-family="Arial">Ground-level slot</text>
    </svg>
  </div>
  <div class="task-copy">Short travel, ground-level access, familiar equipment, and a direct route.</div>
  <div class="pph-strip">Reported as: one pallet movement</div>
</div>
"""

complex_html = """
<div class="task-card">
  <div class="task-card-head"><span class="task-dot" style="background:#EE6A63"></span><span class="task-name">Pallet B: a complex move</span></div>
  <div style="padding:0.45rem 1.0rem 0.3rem 1.0rem">
    <svg viewBox="0 0 520 185" width="100%" role="img" aria-label="Long high-rack pallet route">
      <rect x="8" y="10" width="504" height="162" rx="14" fill="#FFF5F1"/>
      <rect x="344" y="22" width="118" height="124" rx="4" fill="#7891A5"/>
      <g stroke="#F3F8F7" stroke-width="4"><line x1="344" y1="53" x2="462" y2="53"/><line x1="344" y1="84" x2="462" y2="84"/><line x1="344" y1="115" x2="462" y2="115"/><line x1="383" y1="22" x2="383" y2="146"/><line x1="423" y1="22" x2="423" y2="146"/></g>
      <rect x="420" y="26" width="36" height="19" fill="#F2C84A"/><rect x="424" y="19" width="28" height="10" fill="#D59B45"/>
      <path d="M90,130 C155,152 242,150 278,122 S325,59 410,39" fill="none" stroke="#EE6A63" stroke-width="8" stroke-linecap="round" stroke-dasharray="12 9"/>
      <polygon points="410,39 393,36 400,52" fill="#EE6A63"/>
      <rect x="58" y="109" width="40" height="22" rx="3" fill="#F7C84C"/><rect x="93" y="68" width="12" height="68" fill="#22344B"/><rect x="103" y="67" width="18" height="5" fill="#22344B"/><circle cx="69" cy="137" r="8" fill="#22344B"/><circle cx="97" cy="137" r="8" fill="#22344B"/>
      <text x="43" y="158" fill="#4E657A" font-size="16" font-family="Arial">Reach truck</text>
      <text x="330" y="163" fill="#4E657A" font-size="16" font-family="Arial">High-rack placement</text>
    </svg>
  </div>
  <div class="task-copy">Longer travel, higher placement, specialized equipment, and more potential interference.</div>
  <div class="pph-strip">Reported as: one pallet movement</div>
</div>
"""

task_a, task_b = st.columns(2, gap="large")
with task_a:
    st.markdown(short_html, unsafe_allow_html=True)
with task_b:
    st.markdown(complex_html, unsafe_allow_html=True)

st.markdown(
    '<div class="center-message"><div class="small">The hidden mismatch</div><div class="main">One output metric. Two different labor requirements.</div></div>',
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">Make the work visible</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Create a labor standard for the work actually being performed.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">MOST gives each movement a structured, defensible time. Those standards turn operational variation into a usable system for planning, forecasting, and execution.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flow">
      <div class="flow-card">
        <div class="flow-icon" style="background:#EAF1FF">▣</div>
        <h3>Identify task types</h3>
        <p>Separate the simple move from the high-rack, long-travel, or special-equipment move.</p>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#E7FAF4">◫</div>
        <h3>Build MOST standards</h3>
        <p>Break each task into the motions and conditions that determine its expected time.</p>
        <div class="motion-row"><span class="motion">travel</span><span class="motion">access</span><span class="motion">lift</span><span class="motion">place</span></div>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#FFF0E8">▤</div>
        <h3>Create the standard library</h3>
        <p>Store standards by task, zone, equipment, position, and handling condition.</p>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#F3EDFF">⌁</div>
        <h3>Forecast the work mix</h3>
        <p>Predict the expected mix of task types, then translate it into labor by hour, shift, and zone.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">Test the future safely</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Turn the warehouse into a digital twin before changing the real operation.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Once the work is measured and forecasted, a digital twin lets the operation test alternatives without relying on rough estimates or expensive trial-and-error on the floor.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="twin-board">
      <div class="twin-label">Digital twin scenario environment</div>
      <div class="twin-title">Test the operating design before the operation has to live with it.</div>
      <div class="twin-copy">Use the model to compare choices, observe the flow they create, and select an operating plan with clearer tradeoffs.</div>
      <div class="test-grid">
        <div class="test-card"><h3>Labor</h3><p>Test staffing levels, shift coverage, skills, and work allocation.</p></div>
        <div class="test-card"><h3>Work</h3><p>Test task release, routing, congestion, replenishment, and dock priorities.</p></div>
        <div class="test-card"><h3>Layout</h3><p>Test slotting, storage locations, travel paths, equipment, and material flow.</p></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">The outcome</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="closing">From a generic productivity rate to a testable operating plan built around the work itself.</div>',
    unsafe_allow_html=True,
)
