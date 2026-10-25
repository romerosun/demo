"""Interactive illustrative case study for labor standards and warehouse simulation."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Labor Standards + Simulation",
    page_icon="▦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def euro(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"€{value / 1_000_000:,.2f}m"
    return f"€{value / 1_000:,.0f}k"


def box(fig: go.Figure, x0, x1, y0, y1, z0, z1, color, label, opacity=1.0):
    """Add a simple cuboid to a Plotly scene."""
    x = [x0, x1, x1, x0, x0, x1, x1, x0]
    y = [y0, y0, y1, y1, y0, y0, y1, y1]
    z = [z0, z0, z0, z0, z1, z1, z1, z1]
    fig.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=[0, 0, 0, 1, 1, 2, 4, 4, 5, 6, 3, 2],
            j=[1, 2, 4, 2, 5, 3, 5, 6, 6, 7, 7, 7],
            k=[2, 3, 5, 6, 6, 7, 6, 7, 2, 3, 0, 0],
            color=color,
            opacity=opacity,
            flatshading=True,
            hovertemplate=f"{label}<extra></extra>",
            showscale=False,
        )
    )


def warehouse(improved: bool) -> go.Figure:
    """Create a simplified 3D current or improved warehouse."""
    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=[[0, 100], [0, 100]],
            y=[[0, 0], [70, 70]],
            z=[[0, 0], [0, 0]],
            colorscale=[[0, "#152032"], [1, "#152032"]],
            showscale=False,
            hoverinfo="skip",
        )
    )

    for x in range(8, 96, 14):
        box(fig, x, x + 8, -3, 0, 0, 3, "#4C7DFF", "Shipping dock")
        box(fig, x, x + 8, 70, 73, 0, 3, "#915EFF", "Receiving dock")

    for x in range(10, 74, 13):
        for y in (11, 31, 51):
            box(fig, x, x + 8, y, y + 12, 0, 11, "#55728D", "Pallet rack", 0.92)

    if improved:
        fast_zone = (76, 96, 7, 22)
        path = [(86, 14, 1), (78, 14, 1), (62, 8, 1), (42, 5, 1), (20, 3, 1)]
        rack_color, path_color, heat_color = "#32B88A", "#33D69F", "#51E3A7"
        title = "Improved layout: fast movers near shipping and separated travel paths"
        forklift_points = [(79, 12), (61, 10), (45, 8), (30, 6)]
        worker_points = [(84, 18), (67, 13), (52, 8), (34, 6), (16, 4)]
        heat_points = [(28, 13), (44, 21), (66, 33)]
    else:
        fast_zone = (78, 98, 48, 64)
        path = [(88, 56, 1), (82, 48, 1), (62, 33, 1), (38, 18, 1), (20, 3, 1)]
        rack_color, path_color, heat_color = "#EB956E", "#FF755C", "#FF5D6C"
        title = "Current layout: fast movers create long, congested travel paths"
        forklift_points = [(83, 54), (73, 41), (59, 28), (45, 20)]
        worker_points = [(88, 58), (79, 48), (65, 34), (48, 20), (21, 5)]
        heat_points = [(66, 33), (72, 37), (80, 44), (53, 26)]

    fx0, fx1, fy0, fy1 = fast_zone
    for x in np.arange(fx0, fx1, 6):
        for y in np.arange(fy0, fy1, 7):
            box(fig, x, x + 4.5, y, y + 5.2, 0, 6, rack_color, "Fast-mover pick rack")

    px, py, pz = zip(*path)
    fig.add_trace(
        go.Scatter3d(
            x=px,
            y=py,
            z=pz,
            mode="lines+markers",
            line={"color": path_color, "width": 12},
            marker={"size": 4, "color": path_color},
            hovertemplate="Primary forklift travel path<extra></extra>",
        )
    )
    for hx, hy in heat_points:
        fig.add_trace(
            go.Scatter3d(
                x=[hx],
                y=[hy],
                z=[0.5],
                mode="markers",
                marker={"size": 24, "color": heat_color, "opacity": 0.42},
                hovertemplate="Travel / congestion intensity<extra></extra>",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter3d(
            x=[p[0] for p in forklift_points],
            y=[p[1] for p in forklift_points],
            z=[1.3] * len(forklift_points),
            mode="markers",
            marker={"size": 8, "color": "#F7C948", "symbol": "square"},
            hovertemplate="Forklift<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[p[0] for p in worker_points],
            y=[p[1] for p in worker_points],
            z=[1.1] * len(worker_points),
            mode="markers",
            marker={"size": 6, "color": "#E6EDF7", "symbol": "circle"},
            hovertemplate="Operator<extra></extra>",
        )
    )

    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left", "font": {"size": 16}},
        height=510,
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        paper_bgcolor="#0E1625",
        plot_bgcolor="#0E1625",
        font={"color": "#E6EDF7"},
        showlegend=False,
        scene={
            "bgcolor": "#0E1625",
            "xaxis": {"visible": False, "range": [0, 100]},
            "yaxis": {"visible": False, "range": [-4, 74]},
            "zaxis": {"visible": False, "range": [0, 14]},
            "aspectmode": "manual",
            "aspectratio": {"x": 1.55, "y": 1.15, "z": 0.28},
            "camera": {"eye": {"x": 1.55, "y": -1.6, "z": 1.25}},
        },
    )
    return fig


def pph_chart(generic_pph: int) -> tuple[go.Figure, float]:
    """Create a reproducible 28-day example of generic PPH error."""
    rng = np.random.default_rng(7)
    dates = pd.date_range("2026-09-01", periods=28, freq="D")
    pallets = 650 + 85 * np.sin(np.linspace(0, 3.5 * np.pi, 28)) + rng.normal(0, 38, 28)
    planned = pallets / generic_pph
    travel = 0.10 * np.sin(np.linspace(0, 4 * np.pi, 28) + 0.5)
    mix = rng.normal(0.02, 0.09, 28)
    congestion = np.where(np.arange(28) % 7 < 2, 0.10, -0.02)
    actual = planned * (1 + travel + mix + congestion)
    error = float(np.mean(np.abs(actual - planned) / actual) * 100)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=planned,
            mode="lines",
            name="Generic PPH plan",
            line={"color": "#A8B3C7", "width": 3, "dash": "dash"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=actual,
            mode="lines",
            name="Actual task-hours needed",
            line={"color": "#FF755C", "width": 3},
            fill="tonexty",
            fillcolor="rgba(255,117,92,0.10)",
        )
    )
    fig.update_layout(
        height=330,
        margin={"l": 0, "r": 0, "t": 42, "b": 0},
        title={"text": "The same pallet volume can require very different labor hours", "x": 0.01},
        paper_bgcolor="#0E1625",
        plot_bgcolor="#0E1625",
        font={"color": "#E6EDF7"},
        legend={"orientation": "h", "y": 1.14, "x": 0},
        xaxis={"showgrid": False, "zeroline": False},
        yaxis={"title": "Labor hours for pallet-movement team", "gridcolor": "#26354B", "zeroline": False},
    )
    return fig, error


st.markdown(
    """
    <style>
      .stApp { background: #0B1220; color: #E6EDF7; }
      [data-testid="stSidebar"] { background: #101A2A; }
      .eyebrow { color: #62D8AD; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
      .hero { font-size: clamp(2.2rem, 5vw, 4.3rem); font-weight: 750; line-height: 1.03; letter-spacing: -0.055em; margin: 0.25rem 0 1rem 0; }
      .subhero { font-size: 1.15rem; line-height: 1.55; color: #B8C4D8; max-width: 780px; }
      .card { background: linear-gradient(145deg, #16243A, #101A2A); border: 1px solid #283B57; border-radius: 16px; padding: 1.05rem 1.1rem; min-height: 138px; }
      .card h3 { font-size: 1rem; margin: 0 0 0.4rem 0; color: #F4F7FB; }
      .card p { color: #B8C4D8; font-size: 0.9rem; line-height: 1.45; margin: 0; }
      .step { color: #62D8AD; font-size: 0.76rem; font-weight: 700; letter-spacing: 0.08em; }
      .note { background: #142338; border-left: 3px solid #62D8AD; border-radius: 6px; padding: 0.85rem 1rem; color: #CAD5E5; }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title("Illustrative case inputs")
st.sidebar.caption("Change assumptions to see the financial opportunity update.")
hourly_rate = st.sidebar.number_input("Loaded labor cost per hour (€)", 15.0, 80.0, 29.0, 1.0)
generic_pph = st.sidebar.slider("Generic pallets per hour", 10, 25, 16)
annual_labor_spend = st.sidebar.number_input(
    "Annual direct labor spend (€)", 500_000, 10_000_000, 2_175_000, 25_000
)
excess_hours = st.sidebar.number_input("Annual excess scheduled hours", 0, 30_000, 3_620, 100)
shortage_hours = st.sidebar.number_input("Annual understaffed hours", 0, 30_000, 2_530, 100)
service_impact = st.sidebar.number_input("Annual late-order / expedite impact (€)", 0, 2_000_000, 195_000, 5_000)

st.sidebar.divider()
st.sidebar.subheader("Expected improvement")
schedule_recovery = st.sidebar.slider("Excess labor prevented", 0, 100, 75, 5) / 100
overtime_recovery = st.sidebar.slider("Overtime prevented", 0, 100, 65, 5) / 100
service_recovery = st.sidebar.slider("Late-order impact prevented", 0, 100, 70, 5) / 100
layout_gain = st.sidebar.slider("Layout-driven labor capacity released", 0, 15, 5, 1) / 100

overstaff_cost = excess_hours * hourly_rate
overtime_cost = shortage_hours * hourly_rate * 1.5
avoidable_cost = overstaff_cost + overtime_cost + service_impact
scheduling_saving = overstaff_cost * schedule_recovery + overtime_cost * overtime_recovery
service_saving = service_impact * service_recovery
layout_capacity = annual_labor_spend * layout_gain
total_opportunity = scheduling_saving + service_saving + layout_capacity
volume_chart, generic_error = pph_chart(generic_pph)

st.markdown('<p class="eyebrow">Illustrative warehouse case study</p>', unsafe_allow_html=True)
st.markdown('<div class="hero">Stop staffing a complex warehouse with one average PPH.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subhero">Build task-level labor standards, forecast the work that demand actually creates, and test layout and staffing decisions before changing the operation.</div>',
    unsafe_allow_html=True,
)

metrics = st.columns(4)
metrics[0].metric("Avoidable annual cost", euro(avoidable_cost))
metrics[1].metric("Illustrative annual opportunity", euro(total_opportunity))
metrics[2].metric("Generic PPH planning error", f"{generic_error:.1f}%")
metrics[3].metric("Layout travel opportunity", f"{layout_gain * 100:.0f}%")
st.caption("Illustrative example only. Results are calculated from editable assumptions, not client results.")

st.divider()
st.markdown("## 1. The problem: volume is not work")
left, right = st.columns([1.35, 1])
with left:
    st.plotly_chart(warehouse(False), width="stretch", config={"displayModeBar": False})
with right:
    st.markdown("### A generic PPH misses the drivers of labor")
    st.markdown(
        "A pallet moved from a nearby ground-level slot is not equivalent to a heavy pallet, a long-travel replenishment, or a movement interrupted by dock traffic. Yet the legacy plan treats all of them as the same unit of work."
    )
    before = pd.DataFrame(
        {
            "Impact of generic PPH planning": [
                "Excess scheduled labor",
                "Overtime from understaffing",
                "Late orders / expedited freight",
                "Total annual avoidable cost",
            ],
            "Illustrative value": [
                euro(overstaff_cost),
                euro(overtime_cost),
                euro(service_impact),
                euro(avoidable_cost),
            ],
        }
    )
    st.dataframe(before, hide_index=True, width="stretch")
    st.markdown(
        '<div class="note"><b>Core issue:</b> the plan forecasts pallets, but not task mix, travel, handling, or congestion.</div>',
        unsafe_allow_html=True,
    )

st.plotly_chart(volume_chart, width="stretch", config={"displayModeBar": False})
st.caption("Illustrative 28-day pallet-movement example. The generic rate reacts to volume but cannot see task complexity.")

st.divider()
st.markdown("## 2. The solution: turn demand into task-hours")
cards = st.columns(3)
cards[0].markdown(
    '<div class="card"><div class="step">01 · ENGINEER</div><h3>Build defensible labor standards</h3><p>MOST breaks work into travel, locate, lift, pick, confirm, place, and appropriate allowances. Standards vary by zone, equipment, location, weight, and process.</p></div>',
    unsafe_allow_html=True,
)
cards[1].markdown(
    '<div class="card"><div class="step">02 · FORECAST</div><h3>Forecast the operational workload</h3><p>Forecast order lines, pallet moves, SKU mix, inbound workload, and zone-level demand, then convert those drivers into required labor hours.</p></div>',
    unsafe_allow_html=True,
)
cards[2].markdown(
    '<div class="card"><div class="step">03 · SIMULATE</div><h3>Test before implementing</h3><p>Use discrete-event simulation to test staffing, shift rules, slotting, layout, replenishment, and peak-volume scenarios before spending money on the floor.</p></div>',
    unsafe_allow_html=True,
)
st.latex(r"\text{Forecasted workload} \times \text{engineered task standard} = \text{required labor hours}")

st.divider()
st.markdown("## 3. The redesigned operation")
left, right = st.columns([1.35, 1])
with left:
    st.plotly_chart(warehouse(True), width="stretch", config={"displayModeBar": False})
with right:
    st.markdown("### Better decisions, tested before implementation")
    st.markdown(
        "The redesign moves fast movers toward shipping, separates major travel paths, and uses forecasted task-hours to assign people by zone and shift. In a real project, each scenario is validated in the facility's simulation model."
    )
    after = pd.DataFrame(
        {
            "Source of opportunity": [
                "Excess labor and overtime prevented",
                "Late-order / expedite impact prevented",
                "Layout-driven labor capacity released",
                "Total annual opportunity",
            ],
            "Illustrative value": [
                euro(scheduling_saving),
                euro(service_saving),
                euro(layout_capacity),
                euro(total_opportunity),
            ],
        }
    )
    st.dataframe(after, hide_index=True, width="stretch")
    st.markdown(
        '<div class="note"><b>Decision principle:</b> do not start with “hire more people.” Test whether the bottleneck is labor, layout, task mix, slotting, or scheduling.</div>',
        unsafe_allow_html=True,
    )

st.markdown("### Scenario comparison")
scenarios = pd.DataFrame(
    {
        "Scenario": [
            "Current layout + generic PPH",
            "Add labor only",
            "Standards + forecast + layout redesign",
        ],
        "Annual labor / service burden": [
            euro(annual_labor_spend + avoidable_cost),
            euro(annual_labor_spend + avoidable_cost - overtime_cost * overtime_recovery),
            euro(annual_labor_spend + avoidable_cost - total_opportunity),
        ],
        "On-time shipment": ["92.4%", "96.8%", "98.1%"],
        "Travel index": ["100", "100", f"{100 - layout_gain * 360:.0f}"],
        "Planning basis": ["Average PPH", "Average PPH + buffer", "Task-hours by zone"],
    }
)
st.dataframe(scenarios, hide_index=True, width="stretch")

st.divider()
st.markdown("### From illustrative case to real facility")
st.markdown(
    "A client engagement replaces these assumptions with WMS, labor, order, layout, and process data. The output is a validated labor standard library, workload forecast, staffing plan, and simulation-tested improvement roadmap."
)
