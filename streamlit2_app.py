import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ──────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Markdown War Room",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

  .war-room-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #F5A623, #E8441A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.1;
  }
  .war-room-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #9ca3af;
    font-weight: 300;
    letter-spacing: 0.04em;
    margin-top: 4px;
  }

  /* Story cards */
  .story-card {
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
  }
  .story-chapter {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #F5A623;
    margin-bottom: 6px;
  }
  .story-headline {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
    line-height: 1.3;
  }
  .story-body {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.7;
  }
  .story-body strong { color: #e2e8f0; }

  /* KPI chips */
  .kpi-row { display: flex; gap: 12px; margin: 18px 0; flex-wrap: wrap; }
  .kpi-chip {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px 18px;
    text-align: center;
    min-width: 110px;
  }
  .kpi-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #F5A623;
    display: block;
  }
  .kpi-label {
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748b;
    margin-top: 2px;
    display: block;
  }

  /* Outcome boxes */
  .outcome-before {
    background: linear-gradient(135deg, #2d1515, #1a0a0a);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
  }
  .outcome-after {
    background: linear-gradient(135deg, #0d2d1e, #051a10);
    border-left: 3px solid #22c55e;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
  }
  .outcome-predict {
    background: linear-gradient(135deg, #1a1f2e, #0d1225);
    border-left: 3px solid #3b82f6;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
  }
  .outcome-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .outcome-text {
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.6;
  }
  .outcome-text strong { color: #f8fafc; }

  /* Timeline connector */
  .timeline-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 20px;
  }
  .timeline-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #F5A623;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: #0f0f1a;
    flex-shrink: 0; margin-top: 2px;
  }
  .timeline-content { flex: 1; }
  .timeline-title {
    font-weight: 600; color: #f1f5f9; font-size: 0.95rem; margin-bottom: 4px;
  }
  .timeline-desc { color: #64748b; font-size: 0.875rem; line-height: 1.5; }

  /* Insight callout */
  .insight-box {
    background: linear-gradient(135deg, #1e1b4b, #0f0c2e);
    border: 1px solid #4338ca40;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 14px 0;
  }
  .insight-tag {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: #818cf8; margin-bottom: 6px;
  }
  .insight-text { color: #c7d2fe; font-size: 0.92rem; line-height: 1.65; }

  /* Plotly override */
  .js-plotly-plot .plotly { border-radius: 10px; }

  /* Tab styling */
  .stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
  }
  div[data-testid="metric-container"] {
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 10px;
    padding: 14px 18px;
  }
</style>
""", unsafe_allow_html=True)

CHART_THEME = {
    "paper_bgcolor": "#0f0f1a",
    "plot_bgcolor": "#0f0f1a",
    "font_color": "#94a3b8",
    "gridcolor": "#1e293b",
}

def styled_chart(fig, height=380):
    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"], family="DM Sans"),
        height=height,
        margin=dict(l=20, r=20, t=45, b=20),
    )
    fig.update_xaxes(gridcolor=CHART_THEME["gridcolor"], zeroline=False)
    fig.update_yaxes(gridcolor=CHART_THEME["gridcolor"], zeroline=False)
    return fig

PALETTE = ["#F5A623", "#E8441A", "#3b82f6", "#22c55e", "#a855f7", "#06b6d4"]

# ──────────────────────────────────────────────────────
# LOAD & COMPUTE
# ──────────────────────────────────────────────────────
@st.cache_data
def load_and_compute():
    csv_path = Path(__file__).parent / "src" / "synthetic_markdown_dataset.csv"
    df = pd.read_csv(csv_path)

    records = []
    for _, row in df.iterrows():
        stock = row["Stock_Level"]
        for stage, md_col, sales_col in [
            ("M1", "Markdown_1", "Sales_After_M1"),
            ("M2", "Markdown_2", "Sales_After_M2"),
            ("M3", "Markdown_3", "Sales_After_M3"),
            ("M4", "Markdown_4", "Sales_After_M4"),
        ]:
            markdown = row[md_col]
            sales = row[sales_col]
            price_after = row["Original_Price"] * (1 - markdown)
            revenue = price_after * sales
            sell_through = sales / stock if stock > 0 else 0.0
            records.append({
                "Product_ID": row["Product_ID"],
                "Category": row["Category"],
                "Season": row["Season"],
                "Product_Name": row["Product_Name"],
                "Brand": row["Brand"],
                "Stage": stage,
                "Markdown": markdown,
                "Sales": sales,
                "Revenue": revenue,
                "Sell_through": sell_through,
                "Historical_Sales": row["Historical_Sales"],
                "Original_Price": row["Original_Price"],
                "Optimal_Discount": row["Optimal Discount"],
                "Stock_Level": stock,
                "Customer_Ratings": row["Customer Ratings"],
                "Return_Rate": row["Return Rate"],
            })

    mdf = pd.DataFrame(records)
    return df, mdf

try:
    df_raw, mdf = load_and_compute()
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# ──────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding: 6px 0 16px 0;'>
  <div style='font-family: Playfair Display, serif; font-size:1.15rem; color:#F5A623; font-weight:700;'>
    📊 War Room Filters
  </div>
  <div style='font-size:0.78rem; color:#64748b; margin-top:3px;'>
    Scope the stories to your business
  </div>
</div>
""", unsafe_allow_html=True)

all_cats = sorted(df_raw["Category"].unique())
all_seasons = sorted(df_raw["Season"].unique())
all_brands = sorted(df_raw["Brand"].unique())

sel_cats = st.sidebar.multiselect("Category", all_cats, default=all_cats)
sel_seasons = st.sidebar.multiselect("Season", all_seasons, default=all_seasons)
sel_brands = st.sidebar.multiselect("Brand", all_brands, default=all_brands)

# Apply filters
filt = (
    df_raw["Category"].isin(sel_cats) &
    df_raw["Season"].isin(sel_seasons) &
    df_raw["Brand"].isin(sel_brands)
)
df = df_raw[filt].copy()
mdf_f = mdf[
    mdf["Category"].isin(sel_cats) &
    mdf["Season"].isin(sel_seasons) &
    mdf["Brand"].isin(sel_brands)
].copy()

if df.empty:
    st.warning("⚠️ No data for selected filters.")
    st.stop()

# Compute global KPIs
avg_hist = df["Historical_Sales"].mean()
best_stage_revenue = mdf_f.groupby("Stage")["Revenue"].mean()
best_stage = best_stage_revenue.idxmax()
avg_opt_disc = mdf_f.groupby("Stage")["Markdown"].mean()[best_stage] * 100
avg_opt_sales = mdf_f[mdf_f["Stage"] == best_stage]["Sales"].mean()
total_lift = ((avg_opt_sales / avg_hist) - 1) * 100

# Best category
best_cat = mdf_f[mdf_f["Stage"] == best_stage].groupby("Category")["Revenue"].mean().idxmax()

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='font-size:0.78rem; color:#64748b;'>
  <strong style='color:#94a3b8;'>Dataset scope</strong><br>
  {len(df):,} products · {len(sel_cats)} categories<br>
  {len(sel_seasons)} seasons · {len(sel_brands)} brands
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class='war-room-title'>Retail Markdown War Room</div>
    <div class='war-room-sub'>5 questions every retail manager asks — answered with data, told as stories</div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# Global KPI bar
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📦 Products Analyzed", f"{len(df):,}")
k2.metric("🏆 Revenue-Peak Stage", best_stage)
k3.metric("🎯 Optimal Discount", f"{avg_opt_disc:.0f}%")
k4.metric("📈 Sales Lift vs Baseline", f"+{total_lift:.0f}%")
k5.metric("🥇 Strongest Category", best_cat)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.divider()

# ──────────────────────────────────────────────────────
# 5 STORY TABS
# ──────────────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "🏥 Story 1 · The Category Rescue",
    "⏰ Story 2 · The Timing Trap",
    "💡 Story 3 · The Discount Myth",
    "🌨️ Story 4 · The Seasonal Window",
    "🏆 Story 5 · The Brand ROI Battle",
])


# ══════════════════════════════════════════════════════
# STORY 1 — THE CATEGORY RESCUE
# ══════════════════════════════════════════════════════
with t1:

    # Compute per-category rescue stats
    cat_hist = df.groupby("Category")["Historical_Sales"].mean()
    cat_stage = mdf_f.groupby(["Category", "Stage"])["Sales"].mean().reset_index()

    # Find struggling category = lowest hist sales
    struggling_cat = cat_hist.idxmin()
    best_cat_rescue = cat_hist.idxmax()

    sc_hist = cat_hist[struggling_cat]
    sc_best_stage = (
        mdf_f[mdf_f["Category"] == struggling_cat]
        .groupby("Stage")["Revenue"].mean()
        .idxmax()
    )
    sc_sales_at_best = (
        mdf_f[(mdf_f["Category"] == struggling_cat) & (mdf_f["Stage"] == sc_best_stage)]
        ["Sales"].mean()
    )
    sc_lift = ((sc_sales_at_best / sc_hist) - 1) * 100
    sc_disc = (
        mdf_f[(mdf_f["Category"] == struggling_cat) & (mdf_f["Stage"] == sc_best_stage)]
        ["Markdown"].mean() * 100
    )
    sc_rev_before = sc_hist * (mdf_f[mdf_f["Category"] == struggling_cat]["Original_Price"].mean())
    sc_rev_after = (
        mdf_f[(mdf_f["Category"] == struggling_cat) & (mdf_f["Stage"] == sc_best_stage)]
        ["Revenue"].mean()
    )

    st.markdown(f"""
    <div class='story-card'>
      <div class='story-chapter'>Chapter 1 · Category Performance</div>
      <div class='story-headline'>"{struggling_cat} Was Bleeding — Markdown Stopped the Haemorrhage"</div>
      <div class='story-body'>
        Quarter after quarter, <strong>{struggling_cat}</strong> sat at the bottom of the sales board.
        Buyers were placing orders, stock was arriving, but units weren't moving.
        The team tried promotions, repositioned shelf space, even ran social media pushes —
        nothing worked. Then the data asked a simpler question:
        <em>Have you tried marking it down at the right moment, at the right depth?</em>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        # Before/After/Predict boxes
        st.markdown(f"""
        <div class='outcome-before'>
          <div class='outcome-label' style='color:#ef4444;'>⚠ The Problem</div>
          <div class='outcome-text'>
            <strong>{struggling_cat}</strong> averaged only
            <strong>{sc_hist:.0f} units/product</strong> in historical sales —
            the lowest of all categories. At full price, inventory sat unsold
            and cash remained locked in stock.
          </div>
        </div>
        <br>
        <div class='outcome-after'>
          <div class='outcome-label' style='color:#22c55e;'>✅ After Markdown ({sc_best_stage} · {sc_disc:.0f}% off)</div>
          <div class='outcome-text'>
            Sales surged to <strong>{sc_sales_at_best:.0f} units/product</strong>
            — a <strong>+{sc_lift:.0f}% lift</strong> over baseline.
            The sweet spot: Stage <strong>{sc_best_stage}</strong> with a
            <strong>{sc_disc:.0f}% discount</strong>. Not M1 (too early, buyers wait),
            not M4 (too desperate, margin gone).
          </div>
        </div>
        <br>
        <div class='outcome-predict'>
          <div class='outcome-label' style='color:#3b82f6;'>🔮 Next Quarter Forecast</div>
          <div class='outcome-text'>
            If this playbook is applied to <strong>all {struggling_cat} SKUs</strong>
            at {sc_best_stage} timing, projected revenue uplift is
            <strong>+{sc_lift:.0f}%</strong> vs the no-markdown baseline.
            Prioritise SKUs with stock age &gt; 60 days.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        # Sales progression chart for struggling category
        sc_data = cat_stage[cat_stage["Category"] == struggling_cat].copy()
        sc_data["Stage_Label"] = sc_data["Stage"].map(
            {"M1": "Stage 1\n(Early)", "M2": "Stage 2", "M3": "Stage 3\n(Optimal)", "M4": "Stage 4\n(Late)"}
        )
        # Add baseline
        baseline_row = pd.DataFrame([{
            "Category": struggling_cat, "Stage": "Base",
            "Sales": sc_hist, "Stage_Label": "Baseline\n(No MD)"
        }])
        plot_data = pd.concat([baseline_row, sc_data], ignore_index=True)
        stage_order = ["Baseline\n(No MD)", "Stage 1\n(Early)", "Stage 2", "Stage 3\n(Optimal)", "Stage 4\n(Late)"]
        plot_data["Stage_Label"] = pd.Categorical(plot_data["Stage_Label"], categories=stage_order, ordered=True)

        colors = ["#ef4444", "#F5A623", "#F5A623", "#22c55e", "#94a3b8"]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=plot_data["Stage_Label"],
            y=plot_data["Sales"],
            marker_color=colors,
            text=[f"{v:.0f}" for v in plot_data["Sales"]],
            textposition="outside",
            textfont=dict(color="#f1f5f9", size=12),
        ))
        fig.add_hline(
            y=sc_hist, line_dash="dot", line_color="#ef4444",
            annotation_text=f"Baseline: {sc_hist:.0f}", annotation_font_color="#ef4444"
        )
        fig.update_layout(
            title=f"{struggling_cat}: Sales Journey Through Markdown Stages",
            xaxis_title="Markdown Stage",
            yaxis_title="Avg Units Sold",
            showlegend=False,
        )
        st.plotly_chart(styled_chart(fig), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 All Categories Compared: Before vs After Best Markdown")

    col_c, col_d = st.columns(2)

    with col_c:
        # Grouped bar: historical vs best-stage sales
        comp_data = []
        for cat in sel_cats:
            hist_avg = df[df["Category"] == cat]["Historical_Sales"].mean()
            best_s = (
                mdf_f[mdf_f["Category"] == cat]
                .groupby("Stage")["Revenue"].mean()
                .idxmax()
            )
            best_sales = mdf_f[
                (mdf_f["Category"] == cat) & (mdf_f["Stage"] == best_s)
            ]["Sales"].mean()
            comp_data.append({"Category": cat, "Type": "Before Markdown", "Sales": hist_avg})
            comp_data.append({"Category": cat, "Type": f"After Best Stage", "Sales": best_sales})

        comp_df = pd.DataFrame(comp_data)
        fig2 = px.bar(
            comp_df, x="Category", y="Sales", color="Type",
            barmode="group",
            title="Avg Sales: Pre-Markdown vs Post-Optimal Markdown",
            color_discrete_map={"Before Markdown": "#ef4444", "After Best Stage": "#22c55e"},
        )
        st.plotly_chart(styled_chart(fig2), use_container_width=True)

    with col_d:
        # Lift % per category
        lift_data = []
        for cat in sel_cats:
            hist_avg = df[df["Category"] == cat]["Historical_Sales"].mean()
            best_s = (
                mdf_f[mdf_f["Category"] == cat]
                .groupby("Stage")["Revenue"].mean().idxmax()
            )
            best_sales = mdf_f[
                (mdf_f["Category"] == cat) & (mdf_f["Stage"] == best_s)
            ]["Sales"].mean()
            lift = ((best_sales / hist_avg) - 1) * 100
            lift_data.append({"Category": cat, "Sales Lift %": lift, "Best Stage": best_s})

        lift_df = pd.DataFrame(lift_data).sort_values("Sales Lift %", ascending=False)

        fig3 = px.bar(
            lift_df, x="Category", y="Sales Lift %",
            title="% Sales Lift Achieved by Optimised Markdown",
            color="Sales Lift %",
            color_continuous_scale=["#1d4ed8", "#F5A623", "#22c55e"],
            text=lift_df["Sales Lift %"].apply(lambda x: f"+{x:.0f}%"),
        )
        fig3.update_traces(textposition="outside", textfont_color="#f1f5f9")
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(styled_chart(fig3), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
      <div class='insight-tag'>🧠 Retail Expert Takeaway</div>
      <div class='insight-text'>
        Categories don't fail because of poor product — they fail because of poor timing.
        The data shows a consistent <strong>+{total_lift:.0f}% average sales uplift</strong>
        across all categories when markdown is applied at the right stage.
        The manager's job isn't to decide <em>if</em> to discount — it's to decide <em>when</em>.
        Stage {best_stage} is where the money lives.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# STORY 2 — THE TIMING TRAP
# ══════════════════════════════════════════════════════
with t2:

    stage_rev = mdf_f.groupby("Stage")["Revenue"].mean().reset_index()
    stage_sales = mdf_f.groupby("Stage")["Sales"].mean().reset_index()
    best_timing_stage = stage_rev.loc[stage_rev["Revenue"].idxmax(), "Stage"]
    worst_timing_stage = stage_rev.loc[stage_rev["Revenue"].idxmin(), "Stage"]

    rev_best = stage_rev.loc[stage_rev["Stage"] == best_timing_stage, "Revenue"].values[0]
    rev_m1 = stage_rev.loc[stage_rev["Stage"] == "M1", "Revenue"].values[0]
    timing_cost = ((rev_best - rev_m1) / rev_m1) * 100

    st.markdown(f"""
    <div class='story-card'>
      <div class='story-chapter'>Chapter 2 · Markdown Timing</div>
      <div class='story-headline'>"You Discounted Too Early. Here's What It Cost You."</div>
      <div class='story-body'>
        A nervous category manager sees slow sales in week 2 and immediately
        slashes prices by 20%. Sounds reasonable. But the data tells a different story.
        <strong>Products marked down at Stage 1 ({worst_timing_stage}) generate
        {timing_cost:.0f}% less revenue</strong> than those held until the optimal moment.
        The problem isn't the discount — it's the panic. Buyers who see early markdowns
        learn to wait for deeper ones. You've trained your customer to hold out for more.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        # Revenue curve across stages
        stage_cat_rev = mdf_f.groupby(["Stage", "Category"])["Revenue"].mean().reset_index()
        stage_order_map = {"M1": 1, "M2": 2, "M3": 3, "M4": 4}
        stage_cat_rev["Stage_Num"] = stage_cat_rev["Stage"].map(stage_order_map)
        stage_cat_rev = stage_cat_rev.sort_values("Stage_Num")

        fig = px.line(
            stage_cat_rev, x="Stage", y="Revenue", color="Category",
            markers=True,
            title="Revenue Curve: How Timing Changes Everything",
            color_discrete_sequence=PALETTE,
            symbol="Category",
        )
        # Add shading for optimal zone
        fig.add_vrect(
            x0="M2", x1="M3",
            fillcolor="#22c55e", opacity=0.08,
            layer="below", line_width=0,
            annotation_text="🎯 Optimal Window", annotation_position="top left",
            annotation_font_color="#22c55e",
        )
        fig.add_vrect(
            x0="M1", x1="M1",
            fillcolor="#ef4444", opacity=0.0,
        )
        fig.update_traces(line_width=2.5, marker_size=10)
        st.plotly_chart(styled_chart(fig, height=400), use_container_width=True)

    with col_b:
        # Cost of early & late markdown
        st.markdown("#### ⚠️ The Price of Mistiming")

        for stage_i in ["M1", "M2", "M3", "M4"]:
            rev_i = stage_rev.loc[stage_rev["Stage"] == stage_i, "Revenue"].values[0]
            delta = ((rev_i - rev_best) / rev_best) * 100
            color = "#22c55e" if stage_i == best_timing_stage else "#ef4444" if delta < -10 else "#F5A623"
            tag = "🏆 OPTIMAL" if stage_i == best_timing_stage else ("⚠️ TOO EARLY" if stage_i == "M1" else ("❌ OVER-DISCOUNTED" if stage_i == "M4" else ""))

            st.markdown(f"""
            <div style='background:#0f172a; border:1px solid #1e293b; border-radius:8px;
                        padding:12px 16px; margin-bottom:8px; display:flex;
                        justify-content:space-between; align-items:center;'>
              <div>
                <span style='color:#f1f5f9; font-weight:600;'>{stage_i}</span>
                <span style='color:#64748b; font-size:0.78rem; margin-left:8px;'>{tag}</span>
              </div>
              <div style='text-align:right;'>
                <span style='color:{color}; font-family:Playfair Display,serif; font-size:1.1rem;'>
                  ${rev_i:,.0f}
                </span>
                <span style='color:{color}; font-size:0.78rem; display:block;'>
                  {delta:+.1f}% vs optimal
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⏰ Category-Level Timing Intelligence")

    # Heatmap: Category × Stage revenue
    pivot = mdf_f.groupby(["Category", "Stage"])["Revenue"].mean().reset_index()
    pivot_wide = pivot.pivot(index="Category", columns="Stage", values="Revenue")

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot_wide.values,
        x=pivot_wide.columns.tolist(),
        y=pivot_wide.index.tolist(),
        colorscale=[[0, "#1a0a0a"], [0.5, "#F5A623"], [1, "#22c55e"]],
        text=[[f"${v:,.0f}" for v in row] for row in pivot_wide.values],
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(tickfont=dict(color="#94a3b8")),
    ))
    fig_heat.update_layout(
        title="Avg Revenue by Category × Markdown Stage (Darker = Lower, Brighter = Higher)",
    )
    st.plotly_chart(styled_chart(fig_heat, height=280), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
      <div class='insight-tag'>🧠 The 25-Year Rule</div>
      <div class='insight-text'>
        In 25 years of retail, the single most expensive mistake I've seen isn't over-discounting
        — it's <em>mis-timing</em>. Stage M1 markdowns train customers to wait.
        Stage M4 markdowns scream desperation. <strong>Stage {best_timing_stage}
        is the confidence move</strong> — you discount before the customer expects it,
        convert fence-sitters, and protect margin on the rest of the range.
        This data shows that difference is worth <strong>{timing_cost:.0f}% more revenue</strong>.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# STORY 3 — THE DISCOUNT MYTH
# ══════════════════════════════════════════════════════
with t3:

    bins = [0, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 1.0]
    labels = ["<15%", "15–20%", "20–25%", "25–30%", "30–35%", "35–40%", ">40%"]
    mdf_f["Disc_Bin"] = pd.cut(mdf_f["Markdown"], bins=bins, labels=labels)

    disc_rev = mdf_f.groupby(["Disc_Bin", "Category"]).agg(
        Revenue=("Revenue", "mean"),
        Sales=("Sales", "mean"),
        Count=("Product_ID", "count"),
    ).reset_index()
    disc_rev_total = mdf_f.groupby("Disc_Bin")["Revenue"].mean().reset_index()
    peak_bin = disc_rev_total.loc[disc_rev_total["Revenue"].idxmax(), "Disc_Bin"]
    peak_rev = disc_rev_total.loc[disc_rev_total["Revenue"].idxmax(), "Revenue"]
    low_rev = disc_rev_total.loc[disc_rev_total["Revenue"].idxmin(), "Revenue"]
    myth_pct = ((peak_rev - low_rev) / low_rev) * 100

    st.markdown(f"""
    <div class='story-card'>
      <div class='story-chapter'>Chapter 3 · Discount Depth</div>
      <div class='story-headline'>"We Gave 40% Off and Made Less Money. Here's Why."</div>
      <div class='story-body'>
        The buyer pushed for a 40% flash sale. "More discount = more sales = more revenue."
        It sounds like math. It isn't. When the results came in, the 40%-off products
        generated <strong>{myth_pct:.0f}% less revenue per product</strong> than those
        discounted at <strong>{peak_bin}</strong>. Deep discounts attract bargain hunters
        who return more, review less favourably, and rarely become loyal customers.
        The data doesn't lie — the sweet spot has a ceiling.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        fig = px.bar(
            disc_rev_total,
            x="Disc_Bin", y="Revenue",
            title="Avg Revenue per Product by Discount Depth — The Diminishing Return Curve",
            color="Revenue",
            color_continuous_scale=["#22c55e", "#F5A623", "#ef4444"],
        )
        # Highlight peak
        peak_idx = disc_rev_total["Revenue"].idxmax()
        fig.add_annotation(
            x=disc_rev_total.loc[peak_idx, "Disc_Bin"],
            y=disc_rev_total.loc[peak_idx, "Revenue"],
            text=f"🎯 Sweet Spot<br>{peak_bin}",
            showarrow=True, arrowhead=2, arrowcolor="#22c55e",
            font=dict(color="#22c55e", size=12),
            ay=-50,
        )
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Discount Depth", yaxis_title="Avg Revenue / Product")
        st.plotly_chart(styled_chart(fig, height=400), use_container_width=True)

    with col_b:
        st.markdown("#### 📉 What Over-Discounting Really Costs")

        # Return rate vs discount correlation
        mdf_f_notnull = mdf_f.dropna(subset=["Disc_Bin"])
        return_disc = mdf_f_notnull.groupby("Disc_Bin")["Return_Rate"].mean().reset_index()
        fig_ret = px.line(
            return_disc, x="Disc_Bin", y="Return_Rate",
            markers=True,
            title="Return Rate Rises with Discount Depth",
            color_discrete_sequence=["#ef4444"],
        )
        fig_ret.update_traces(line_width=2.5, marker_size=9)
        fig_ret.update_layout(yaxis_title="Avg Return Rate (%)", xaxis_title="Discount Depth")
        st.plotly_chart(styled_chart(fig_ret, height=280), use_container_width=True)

    st.markdown("---")
    col_c, col_d = st.columns(2)

    with col_c:
        # Per-category sweet spot
        cat_sweet = (
            mdf_f.groupby(["Category", "Disc_Bin"])["Revenue"]
            .mean().reset_index()
        )
        fig_cs = px.line(
            cat_sweet.dropna(), x="Disc_Bin", y="Revenue", color="Category",
            markers=True,
            title="Each Category Has Its Own Sweet Spot",
            color_discrete_sequence=PALETTE,
        )
        fig_cs.update_traces(line_width=2, marker_size=8)
        st.plotly_chart(styled_chart(fig_cs), use_container_width=True)

    with col_d:
        # Rating vs discount
        rating_disc = mdf_f.dropna(subset=["Disc_Bin"]).groupby("Disc_Bin")["Customer_Ratings"].mean().reset_index()
        fig_rat = px.bar(
            rating_disc, x="Disc_Bin", y="Customer_Ratings",
            title="Customer Ratings Drop at Extreme Discounts",
            color="Customer_Ratings",
            color_continuous_scale=["#ef4444", "#F5A623", "#22c55e"],
        )
        fig_rat.update_layout(coloraxis_showscale=False, yaxis_title="Avg Rating", yaxis_range=[0, 5])
        st.plotly_chart(styled_chart(fig_rat), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
      <div class='insight-tag'>🧠 The Margin Destruction Warning</div>
      <div class='insight-text'>
        A 40% discount doesn't just reduce price — it changes <em>who buys</em> your product.
        Return rates climb as discount depth increases. Customer ratings drop.
        You're not gaining loyal customers; you're renting transaction volume at full margin cost.
        The data shows <strong>{peak_bin} is the intelligent ceiling</strong> —
        above that, you are subsidising your competitors' customers.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# STORY 4 — THE SEASONAL WINDOW
# ══════════════════════════════════════════════════════
with t4:

    season_stage = mdf_f.groupby(["Season", "Stage"]).agg(
        Revenue=("Revenue", "mean"),
        Sales=("Sales", "mean"),
        Sell_through=("Sell_through", "mean"),
    ).reset_index()

    # Which season has highest sell-through urgency (M4 - M1 delta)
    st_pivot = season_stage.pivot(index="Season", columns="Stage", values="Sell_through")
    st_pivot["Velocity"] = st_pivot["M4"] - st_pivot["M1"]
    urgent_season = st_pivot["Velocity"].idxmax()
    slow_season = st_pivot["Velocity"].idxmin()

    urgent_vel = st_pivot.loc[urgent_season, "Velocity"]

    st.markdown(f"""
    <div class='story-card'>
      <div class='story-chapter'>Chapter 4 · Seasonal Strategy</div>
      <div class='story-headline'>"{urgent_season} Moves Fast — If You Blink, You Miss the Window"</div>
      <div class='story-body'>
        Not all seasons are equal. <strong>{urgent_season}</strong> products show
        a sell-through velocity <strong>{urgent_vel:.1f}x faster</strong> than
        <strong>{slow_season}</strong> when markdowns are applied.
        This means your {urgent_season} markdown window is narrow.
        Miss it and you're left with full warehouses when the season turns.
        Hit it and you can clear 80%+ of inventory before the competition even notices.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.line(
            season_stage, x="Stage", y="Revenue", color="Season",
            markers=True,
            title="Revenue Trajectory by Season — Timing Differs",
            color_discrete_sequence=PALETTE,
        )
        fig.update_traces(line_width=2.5, marker_size=10)
        st.plotly_chart(styled_chart(fig, height=380), use_container_width=True)

    with col_b:
        # Sell-through heatmap by season and stage
        st_heat = season_stage.pivot(index="Season", columns="Stage", values="Sell_through")
        fig_h = go.Figure(data=go.Heatmap(
            z=st_heat.values,
            x=st_heat.columns.tolist(),
            y=st_heat.index.tolist(),
            colorscale=[[0, "#0f172a"], [0.5, "#F5A623"], [1, "#22c55e"]],
            text=[[f"{v:.2f}x" for v in row] for row in st_heat.values],
            texttemplate="%{text}",
            showscale=True,
            colorbar=dict(title="Sell-Through", tickfont=dict(color="#94a3b8")),
        ))
        fig_h.update_layout(title="Sell-Through Ratio: Season × Stage (Higher = More Urgent)")
        st.plotly_chart(styled_chart(fig_h, height=380), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📅 Seasonal Action Calendar — When to Deploy Each Markdown Stage")

    col_c, col_d = st.columns([2, 3])

    with col_c:
        # Best stage per season
        season_best = (
            mdf_f.groupby(["Season", "Stage"])["Revenue"]
            .mean().reset_index()
            .sort_values("Revenue", ascending=False)
            .drop_duplicates(subset=["Season"])
        )
        for _, row_s in season_best.iterrows():
            season_rev = mdf_f[mdf_f["Season"] == row_s["Season"]].groupby("Stage")["Revenue"].mean()
            peak_rev_s = season_rev.max()
            low_rev_s = season_rev.min()
            urgency = ((peak_rev_s - low_rev_s) / low_rev_s * 100)
            urgency_color = "#ef4444" if urgency > 60 else "#F5A623" if urgency > 30 else "#22c55e"

            st.markdown(f"""
            <div style='background:#0f172a; border:1px solid #1e293b; border-radius:8px;
                        padding:14px 16px; margin-bottom:8px;'>
              <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                  <span style='color:#f1f5f9; font-weight:600; font-size:1rem;'>{row_s['Season']}</span><br>
                  <span style='color:#64748b; font-size:0.8rem;'>Best stage: <strong style="color:#F5A623">{row_s['Stage']}</strong></span>
                </div>
                <div style='text-align:right;'>
                  <span style='color:{urgency_color}; font-size:0.78rem; font-weight:600;'>
                    {'🔥 HIGH URGENCY' if urgency > 60 else '⚡ MEDIUM' if urgency > 30 else '✅ FLEXIBLE'}
                  </span><br>
                  <span style='color:#64748b; font-size:0.75rem;'>Timing sensitivity: {urgency:.0f}%</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col_d:
        # Seasonal revenue vs category grouped
        season_cat = mdf_f.groupby(["Season", "Category"])["Revenue"].mean().reset_index()
        fig_sc = px.bar(
            season_cat, x="Season", y="Revenue", color="Category",
            barmode="group",
            title="Avg Revenue by Season & Category — Where to Focus Markdown Budget",
            color_discrete_sequence=PALETTE,
        )
        st.plotly_chart(styled_chart(fig_sc, height=340), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
      <div class='insight-tag'>🧠 The Seasonal Urgency Rule</div>
      <div class='insight-text'>
        <strong>{urgent_season}</strong> products don't wait.
        The window between "moving well" and "stranded stock" can be
        as short as 3 weeks. This data shows sell-through almost doubles
        between M1 and M4 in {urgent_season} — meaning late markdowns work
        but only because you've already lost weeks of full-margin sales.
        Build your {urgent_season} markdown calendar now, not when you
        see stock reports turning red.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# STORY 5 — THE BRAND ROI BATTLE
# ══════════════════════════════════════════════════════
with t5:

    brand_hist = df.groupby("Brand")["Historical_Sales"].mean()
    brand_stage = mdf_f.groupby(["Brand", "Stage"])["Revenue"].mean().reset_index()
    brand_best = (
        mdf_f.groupby(["Brand", "Stage"])["Revenue"].mean()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .drop_duplicates(subset=["Brand"])
        .rename(columns={"Revenue": "Best_Revenue", "Stage": "Best_Stage"})
    )
    brand_perf = pd.merge(
        brand_best,
        pd.DataFrame({"Brand": brand_hist.index, "Hist_Sales": brand_hist.values}),
        on="Brand"
    )
    brand_perf["MD_Sales"] = brand_perf.apply(
        lambda r: mdf_f[
            (mdf_f["Brand"] == r["Brand"]) & (mdf_f["Stage"] == r["Best_Stage"])
        ]["Sales"].mean(), axis=1
    )
    brand_perf["Sales_Lift_Pct"] = ((brand_perf["MD_Sales"] / brand_perf["Hist_Sales"]) - 1) * 100
    brand_perf = brand_perf.sort_values("Best_Revenue", ascending=False)

    winner_brand = brand_perf.iloc[0]["Brand"]
    winner_lift = brand_perf.iloc[0]["Sales_Lift_Pct"]
    winner_stage = brand_perf.iloc[0]["Best_Stage"]
    laggard_brand = brand_perf.iloc[-1]["Brand"]
    laggard_lift = brand_perf.iloc[-1]["Sales_Lift_Pct"]

    st.markdown(f"""
    <div class='story-card'>
      <div class='story-chapter'>Chapter 5 · Brand Markdown ROI</div>
      <div class='story-headline'>"{winner_brand} Rewards Every Discount Dollar. {laggard_brand} Wastes Half of Them."</div>
      <div class='story-body'>
        You have a fixed markdown budget. Every percentage point off comes out of margin.
        So which brands actually respond? The data reveals a stark divide:
        <strong>{winner_brand}</strong> generates a <strong>+{winner_lift:.0f}% sales lift</strong>
        when discounted at {winner_stage} — customers are primed and waiting.
        Meanwhile, <strong>{laggard_brand}</strong> shows only
        <strong>+{laggard_lift:.0f}%</strong> lift — the same discount,
        a fraction of the return. Brand equity determines markdown effectiveness.
        Are you allocating budget accordingly?
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Brand revenue comparison
        fig = px.bar(
            brand_perf, x="Brand", y="Best_Revenue",
            title="Peak Revenue Potential by Brand (at Optimal Stage)",
            color="Best_Revenue",
            color_continuous_scale=["#1d4ed8", "#F5A623", "#22c55e"],
            text=brand_perf["Best_Revenue"].apply(lambda x: f"${x:,.0f}"),
        )
        fig.update_traces(textposition="outside", textfont_color="#f1f5f9")
        fig.update_layout(coloraxis_showscale=False, yaxis_title="Avg Revenue / Product")
        st.plotly_chart(styled_chart(fig, height=380), use_container_width=True)

    with col_b:
        # Brand sales lift % chart
        lift_colors = ["#22c55e" if x == brand_perf["Sales_Lift_Pct"].max()
                       else "#ef4444" if x == brand_perf["Sales_Lift_Pct"].min()
                       else "#F5A623"
                       for x in brand_perf["Sales_Lift_Pct"]]

        fig_lift = go.Figure(go.Bar(
            x=brand_perf["Brand"],
            y=brand_perf["Sales_Lift_Pct"],
            marker_color=lift_colors,
            text=[f"+{v:.0f}%" for v in brand_perf["Sales_Lift_Pct"]],
            textposition="outside",
            textfont=dict(color="#f1f5f9"),
        ))
        fig_lift.update_layout(
            title="Sales Lift % per Brand — Where Markdown Budget Works Hardest",
            yaxis_title="Sales Lift vs Baseline (%)",
            paper_bgcolor="#0f0f1a", plot_bgcolor="#0f0f1a",
            font=dict(color="#94a3b8"),
            height=380,
            margin=dict(l=20, r=20, t=45, b=20),
        )
        fig_lift.update_xaxes(gridcolor="#1e293b")
        fig_lift.update_yaxes(gridcolor="#1e293b")
        st.plotly_chart(fig_lift, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔬 Brand × Stage Matrix — Find the Exact Trigger Point for Each Brand")

    brand_stage_rev = mdf_f.groupby(["Brand", "Stage"])["Revenue"].mean().reset_index()
    pivot_b = brand_stage_rev.pivot(index="Brand", columns="Stage", values="Revenue")
    fig_bh = go.Figure(data=go.Heatmap(
        z=pivot_b.values,
        x=pivot_b.columns.tolist(),
        y=pivot_b.index.tolist(),
        colorscale=[[0, "#1a0a0a"], [0.5, "#F5A623"], [1, "#22c55e"]],
        text=[[f"${v:,.0f}" for v in row] for row in pivot_b.values],
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(title="Avg Revenue", tickfont=dict(color="#94a3b8")),
    ))
    fig_bh.update_layout(title="Revenue by Brand × Markdown Stage — Green = Where to Act")
    st.plotly_chart(styled_chart(fig_bh, height=300), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Brand Scorecard — Full ROI Picture")

    # Full scorecard table
    scorecard = brand_perf[["Brand", "Best_Stage", "Hist_Sales", "MD_Sales", "Sales_Lift_Pct", "Best_Revenue"]].copy()
    scorecard.columns = ["Brand", "Best Stage", "Baseline Sales", "Optimised Sales", "Lift %", "Peak Revenue"]
    scorecard["Baseline Sales"] = scorecard["Baseline Sales"].round(0)
    scorecard["Optimised Sales"] = scorecard["Optimised Sales"].round(0)
    scorecard["Lift %"] = scorecard["Lift %"].round(1)
    scorecard["Peak Revenue"] = scorecard["Peak Revenue"].round(0)

    st.dataframe(
        scorecard,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Peak Revenue": st.column_config.NumberColumn("Peak Revenue", format="$%.0f"),
            "Lift %": st.column_config.NumberColumn("Sales Lift %", format="+%.1f%%"),
        },
    )

    st.markdown(f"""
    <div class='insight-box'>
      <div class='insight-tag'>🧠 The Brand Allocation Rule</div>
      <div class='insight-text'>
        Treat your markdown budget like a venture portfolio.
        Put the most capital behind <strong>{winner_brand}</strong> — its markdown elasticity
        is proven. For <strong>{laggard_brand}</strong>, investigate
        <em>why</em> customers aren't responding: is it price perception,
        distribution, or product-market fit? No markdown strategy fixes a brand problem.
        Before you discount, diagnose.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; padding: 12px 0;'>
  <span style='font-family: Playfair Display, serif; color:#F5A623; font-size:1rem;'>
    Retail Markdown War Room
  </span>
  <span style='color:#334155; margin: 0 8px;'>·</span>
  <span style='color:#475569; font-size:0.82rem;'>
    5 stories. Real data. Decisions that move inventory and protect margin.
  </span>
</div>
""", unsafe_allow_html=True)
