import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Markdown Insights",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# COLOR PALETTE  — dark background, blue accent
# ─────────────────────────────────────────────
C = {
    "primary":   "#3B82F6",   # bright blue — main accent
    "accent":    "#60A5FA",   # lighter blue — secondary
    "warn":      "#F59E0B",   # amber — caution
    "danger":    "#EF4444",   # red — problem state
    "bg_page":   "#0A0F1E",   # very dark navy — page bg
    "bg_card":   "#111827",   # dark card bg
    "bg_subtle": "#1A2235",   # slightly lighter — subtle sections
    "border":    "#1E2D45",   # dark blue border
    "text_main": "#F1F5F9",   # near-white — primary text
    "text_sub":  "#333333",   # grey — secondary text
    "text_mute": "#475569",   # muted grey
}

CHART_COLORS = ["#3B82F6", "#60A5FA", "#93C5FD", "#1D4ED8", "#BFDBFE"]

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {C['bg_page']};
    color: {C['text_main']};
  }}

  /* Force Streamlit's own backgrounds dark */
  .stApp {{ background-color: {C['bg_page']} !important; }}
  section[data-testid="stSidebar"] {{ background-color: #0D1424 !important; }}
  .stTabs [data-baseweb="tab-list"] {{ background-color: {C['bg_card']} !important; border-radius: 8px; }}
  .stTabs [data-baseweb="tab"] {{ color: {C['text_sub']} !important; }}
  .stTabs [aria-selected="true"] {{ color: {C['primary']} !important; }}
  hr {{ border-color: {C['border']} !important; }}

  .page-title {{
    font-size: 1.75rem; font-weight: 700;
    color: {C['text_main']}; margin-bottom: 2px;
  }}
  .page-subtitle {{
    font-size: 0.95rem; color: {C['text_sub']};
    font-weight: 400; margin-bottom: 0;
  }}

  .story-intro {{
    background: {C['bg_card']};
    border: 1px solid {C['border']};
    border-left: 4px solid {C['primary']};
    border-radius: 8px;
    padding: 20px 24px; margin-bottom: 20px;
  }}
  .story-label {{
    font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: {C['primary']}; margin-bottom: 4px;
  }}
  .story-title {{
    font-size: 1.2rem; font-weight: 700;
    color: {C['text_main']}; margin-bottom: 8px; line-height: 1.4;
  }}
  .story-body {{
    font-size: 0.9rem; color: #FFFFFF; line-height: 1.7;
  }}
  .story-body strong {{ color: {C['text_main']}; }}

  .box-row {{ display: flex; gap: 12px; margin: 16px 0; }}
  .box-problem {{
    flex: 1; background: #0D0D0D;
    border: 1px solid #EF4444; border-radius: 8px; padding: 14px 16px;
  }}
  .box-result {{
    flex: 1; background: #0D0D0D;
    border: 1px solid #3B82F6; border-radius: 8px; padding: 14px 16px;
  }}
  .box-recommend {{
    flex: 1; background: #0D0D0D;
    border: 1px solid #3B82F6; border-radius: 8px; padding: 14px 16px;
  }}
  .box-label {{
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px;
  }}
  .box-text {{
    font-size: 0.85rem; line-height: 1.6; color: #FFFFFF;
  }}
  .box-text strong {{ font-weight: 600; color: {C['text_main']}; }}

  .insight {{
    background: #0D0D0D;
    border: 1px solid #222222;
    border-left: 3px solid {C['primary']};
    border-radius: 0 8px 8px 0;
    padding: 14px 18px; margin-top: 16px;
  }}
  .insight-label {{
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: {C['primary']}; margin-bottom: 4px;
  }}
  .insight-text {{
    font-size: 0.88rem; color: #FFFFFF; line-height: 1.6;
  }}
  .insight-text strong {{ color: {C['text_main']}; }}

  .stage-pill {{
    display: inline-block;
    background: {C['primary']}25; color: {C['accent']};
    font-size: 0.75rem; font-weight: 600;
    padding: 2px 10px; border-radius: 20px; margin: 2px;
  }}

  div[data-testid="metric-container"] {{
    background: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 8px; padding: 12px 16px;
  }}
  [data-testid="stMetricValue"] {{ color: {C['accent']} !important; font-weight: 700; }}
  [data-testid="stMetricLabel"] {{ color: {C['text_sub']}; font-size: 0.8rem; }}

  /* Dataframe dark override */
  .stDataFrame {{ background: {C['bg_card']} !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def chart(fig, height=360):
    fig.update_layout(
        paper_bgcolor=C["bg_card"], plot_bgcolor=C["bg_card"],
        font=dict(color=C["text_sub"], family="Inter", size=12),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        title_font=dict(color=C["text_main"], size=13, family="Inter"),
        legend=dict(font=dict(color=C["text_sub"])),
    )
    fig.update_xaxes(gridcolor=C["border"], zeroline=False,
                     linecolor=C["border"], tickfont=dict(color=C["text_sub"]))
    fig.update_yaxes(gridcolor=C["border"], zeroline=False,
                     linecolor=C["border"], tickfont=dict(color=C["text_sub"]))
    return fig

def slabel(s):
    return {"M1":"Stage 1","M2":"Stage 2","M3":"Stage 3","M4":"Stage 4"}.get(s, s)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load():
    path = Path(__file__).parent / "src" / "synthetic_markdown_dataset.csv"
    df = pd.read_csv(path)
    rows = []
    for _, r in df.iterrows():
        stock = r["Stock_Level"]
        for stage, mc, sc in [
            ("M1","Markdown_1","Sales_After_M1"),
            ("M2","Markdown_2","Sales_After_M2"),
            ("M3","Markdown_3","Sales_After_M3"),
            ("M4","Markdown_4","Sales_After_M4"),
        ]:
            md = r[mc]; sales = r[sc]
            rev = r["Original_Price"] * (1 - md) * sales
            rows.append({
                "Product_ID": r["Product_ID"],
                "Category": r["Category"],
                "Season": r["Season"],
                "Product_Name": r["Product_Name"],
                "Brand": r["Brand"],
                "Stage": stage,
                "Markdown": md,
                "Sales": sales,
                "Revenue": rev,
                "Sell_through": sales / stock if stock > 0 else 0,
                "Historical_Sales": r["Historical_Sales"],
                "Original_Price": r["Original_Price"],
                "Optimal_Discount": r["Optimal Discount"],
                "Stock_Level": stock,
                "Customer_Ratings": r["Customer Ratings"],
                "Return_Rate": r["Return Rate"],
            })
    return df, pd.DataFrame(rows)

try:
    df_raw, mdf_all = load()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.markdown("### Filters")
sel_cats    = st.sidebar.multiselect("Category", sorted(df_raw["Category"].unique()), default=sorted(df_raw["Category"].unique()))
sel_seasons = st.sidebar.multiselect("Season",   sorted(df_raw["Season"].unique()),   default=sorted(df_raw["Season"].unique()))
sel_brands  = st.sidebar.multiselect("Brand",    sorted(df_raw["Brand"].unique()),    default=sorted(df_raw["Brand"].unique()))

df  = df_raw[df_raw["Category"].isin(sel_cats) & df_raw["Season"].isin(sel_seasons) & df_raw["Brand"].isin(sel_brands)].copy()
mdf = mdf_all[mdf_all["Category"].isin(sel_cats) & mdf_all["Season"].isin(sel_seasons) & mdf_all["Brand"].isin(sel_brands)].copy()

if df.empty:
    st.warning("No data for the selected filters. Please adjust your selection.")
    st.stop()

# ─────────────────────────────────────────────
# GLOBAL KPIs
# ─────────────────────────────────────────────
avg_hist      = df["Historical_Sales"].mean()
stage_rev_avg = mdf.groupby("Stage")["Revenue"].mean()
best_stage    = stage_rev_avg.idxmax()
best_disc     = mdf[mdf["Stage"] == best_stage]["Markdown"].mean() * 100
best_sales    = mdf[mdf["Stage"] == best_stage]["Sales"].mean()
total_lift    = ((best_sales / avg_hist) - 1) * 100
best_cat      = mdf[mdf["Stage"] == best_stage].groupby("Category")["Revenue"].mean().idxmax()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("<div class='page-title'>📦 Retail Markdown Insights</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Five questions retail managers ask most — answered with data from your product range.</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Products Analysed",       f"{len(df):,}")
k2.metric("Best Markdown Stage",     slabel(best_stage))
k3.metric("Recommended Discount",    f"{best_disc:.0f}%")
k4.metric("Sales Increase vs No MD", f"+{total_lift:.0f}%")
k5.metric("Top Performing Category", best_cat)
st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "1 · Category Performance",
    "2 · Markdown Timing",
    "3 · Discount Depth",
    "4 · Seasonal Patterns",
    "5 · Brand Comparison",
])

# ══════════════════════════════════════════════
# TAB 1 — CATEGORY PERFORMANCE
# ══════════════════════════════════════════════
with t1:
    cat_hist    = df.groupby("Category")["Historical_Sales"].mean()
    focus_cat   = cat_hist.idxmin()
    focus_hist  = cat_hist[focus_cat]
    focus_best  = mdf[mdf["Category"] == focus_cat].groupby("Stage")["Revenue"].mean().idxmax()
    focus_sales = mdf[(mdf["Category"]==focus_cat) & (mdf["Stage"]==focus_best)]["Sales"].mean()
    focus_disc  = mdf[(mdf["Category"]==focus_cat) & (mdf["Stage"]==focus_best)]["Markdown"].mean() * 100
    focus_lift  = ((focus_sales / focus_hist) - 1) * 100

    st.markdown(f"""
    <div class='story-intro'>
      <div class='story-label'>Question 1</div>
      <div class='story-title'>Why are some categories selling less, and what can a markdown do?</div>
      <div class='story-body'>
        Looking across all categories, <strong>{focus_cat}</strong> had the lowest average
        sales before any markdown was applied — <strong>{focus_hist:.0f} units per product</strong>.
        Stock was available, but sales were not moving at the original price.
        When a <strong>{focus_disc:.0f}% markdown was applied at {slabel(focus_best)}</strong>,
        the outcome showed a clear and measurable improvement.
      </div>
    </div>

    <div class='box-row'>
      <div class='box-problem'>
        <div class='box-label' style='color:#B91C1C;'>Situation Before Markdown</div>
        <div class='box-text'>
          <strong>{focus_cat}</strong> averaged <strong>{focus_hist:.0f} units sold per product</strong>
          at the original price. This was the lowest across all categories,
          suggesting that the price point was reducing customer conversion.
        </div>
      </div>
      <div class='box-result'>
        <div class='box-label' style='color:#15803D;'>Result After Markdown</div>
        <div class='box-text'>
          At <strong>{slabel(focus_best)} with a {focus_disc:.0f}% discount</strong>,
          average sales rose to <strong>{focus_sales:.0f} units</strong>
          — a <strong>+{focus_lift:.0f}% increase</strong> over the baseline figure.
        </div>
      </div>
      <div class='box-recommend'>
        <div class='box-label' style='color:#1D4ED8;'>Recommended Action</div>
        <div class='box-text'>
          Apply a <strong>{focus_disc:.0f}% markdown at {slabel(focus_best)}</strong>
          for all {focus_cat} products with more than 60 days of stock on hand.
          Projected improvement: <strong>+{focus_lift:.0f}% in units sold</strong>.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sd = mdf[mdf["Category"]==focus_cat].groupby("Stage")["Sales"].mean().reset_index()
        sd["Stage_Label"] = sd["Stage"].map({"M1":"Stage 1","M2":"Stage 2","M3":"Stage 3","M4":"Stage 4"})
        base = pd.DataFrame([{"Stage":"Base","Sales":focus_hist,"Stage_Label":"No Markdown"}])
        plot_df = pd.concat([base, sd], ignore_index=True)
        order = ["No Markdown","Stage 1","Stage 2","Stage 3","Stage 4"]
        plot_df["Stage_Label"] = pd.Categorical(plot_df["Stage_Label"], categories=order, ordered=True)
        plot_df = plot_df.sort_values("Stage_Label")

        bar_cols = [C["danger"]] + [C["primary"]] * 4
        fig = go.Figure(go.Bar(
            x=plot_df["Stage_Label"], y=plot_df["Sales"],
            marker_color=bar_cols,
            text=[f"{v:.0f}" for v in plot_df["Sales"]],
            textposition="outside",
        ))
        fig.add_hline(y=focus_hist, line_dash="dot", line_color=C["danger"],
                      annotation_text=f"Baseline: {focus_hist:.0f} units",
                      annotation_font_color=C["danger"])
        fig.update_layout(title=f"{focus_cat}: Average Units Sold at Each Markdown Stage",
                          yaxis_title="Avg Units Sold", showlegend=False)
        st.plotly_chart(chart(fig), use_container_width=True)

    with col2:
        lift_rows = []
        for cat in sel_cats:
            h  = df[df["Category"]==cat]["Historical_Sales"].mean()
            bs = mdf[mdf["Category"]==cat].groupby("Stage")["Revenue"].mean().idxmax()
            s  = mdf[(mdf["Category"]==cat) & (mdf["Stage"]==bs)]["Sales"].mean()
            lift_rows.append({"Category": cat, "Sales Increase %": ((s/h)-1)*100})
        lift_df = pd.DataFrame(lift_rows).sort_values("Sales Increase %", ascending=False)

        fig2 = px.bar(lift_df, x="Category", y="Sales Increase %",
                      title="Sales Increase (%) After Applying Optimal Markdown — by Category",
                      color_discrete_sequence=[C["primary"]],
                      text=lift_df["Sales Increase %"].apply(lambda x: f"+{x:.0f}%"))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(chart(fig2), use_container_width=True)

    st.markdown(f"""
    <div class='insight'>
      <div class='insight-label'>Key Takeaway</div>
      <div class='insight-text'>
        Every category in the range responded positively to a well-timed markdown.
        The average sales increase across all categories is <strong>+{total_lift:.0f}%</strong>.
        A category that appears to be underperforming is often a pricing problem,
        not a product problem.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — MARKDOWN TIMING
# ══════════════════════════════════════════════
with t2:
    stage_rev  = mdf.groupby("Stage")["Revenue"].mean()
    best_t     = stage_rev.idxmax()
    rev_best   = stage_rev[best_t]
    timing_gap = ((rev_best - stage_rev["M1"]) / stage_rev["M1"]) * 100

    st.markdown(f"""
    <div class='story-intro'>
      <div class='story-label'>Question 2</div>
      <div class='story-title'>Does it matter when you apply the markdown — and by how much?</div>
      <div class='story-body'>
        Yes — significantly. Products marked down at <strong>{slabel(best_t)}</strong> generate
        <strong>{timing_gap:.0f}% more revenue on average</strong> compared to products
        marked down at Stage 1.
        The data shows a consistent revenue peak in the middle of the markdown journey.
        Acting too early or leaving it too late both reduce the outcome.
      </div>
    </div>

    <div class='box-row'>
      <div class='box-problem'>
        <div class='box-label' style='color:#B91C1C;'>Stage 1 — Lower Revenue</div>
        <div class='box-text'>
          Applying a markdown immediately results in reduced-price sales
          before demand has had time to build naturally.
          Average revenue at Stage 1: <strong>${stage_rev['M1']:,.0f}</strong> per product.
        </div>
      </div>
      <div class='box-result'>
        <div class='box-label' style='color:#15803D;'>{slabel(best_t)} — Highest Revenue</div>
        <div class='box-text'>
          Revenue is highest at <strong>{slabel(best_t)}</strong>,
          averaging <strong>${rev_best:,.0f}</strong> per product.
          Customers who were considering the product at full price convert here,
          while margin remains above the floor.
        </div>
      </div>
      <div class='box-recommend'>
        <div class='box-label' style='color:#1D4ED8;'>Stage 4 — Margin Reduces Further</div>
        <div class='box-text'>
          Waiting until Stage 4 typically requires a deeper discount to shift
          remaining stock. Average revenue at Stage 4:
          <strong>${stage_rev['M4']:,.0f}</strong> per product.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        sc = mdf.groupby(["Stage","Category"])["Revenue"].mean().reset_index()
        sc["Stage_Label"] = sc["Stage"].map({"M1":"Stage 1","M2":"Stage 2","M3":"Stage 3","M4":"Stage 4"})
        fig = px.line(sc, x="Stage_Label", y="Revenue", color="Category",
                      markers=True,
                      title="Average Revenue at Each Markdown Stage — by Category",
                      color_discrete_sequence=CHART_COLORS)
        fig.add_vrect(x0="Stage 2", x1="Stage 3",
                      fillcolor=C["primary"], opacity=0.06, layer="below", line_width=0,
                      annotation_text="Recommended window",
                      annotation_position="top left",
                      annotation_font_color=C["primary"])
        fig.update_traces(line_width=2, marker_size=8)
        fig.update_layout(xaxis_title="Markdown Stage", yaxis_title="Avg Revenue per Product")
        st.plotly_chart(chart(fig, height=380), use_container_width=True)

    with col2:
        st.markdown("#### Revenue by Stage")
        for sk in ["M1","M2","M3","M4"]:
            rv    = stage_rev[sk]
            delta = ((rv - rev_best) / rev_best) * 100
            is_b  = sk == best_t
            row_bg = f"background:{C['primary']}10; border:1px solid {C['primary']}30;" if is_b \
                     else f"background:{C['bg_subtle']}; border:1px solid {C['border']};"
            tag    = "  ✓ Best" if is_b else ""
            vc     = C["primary"] if is_b else (C["danger"] if delta < -8 else C["warn"])
            st.markdown(f"""
            <div style='{row_bg} border-radius:6px; padding:10px 14px; margin-bottom:6px;
                        display:flex; justify-content:space-between; align-items:center;'>
              <span style='font-weight:600; color:{C["text_main"]};'>{slabel(sk)}{tag}</span>
              <div style='text-align:right;'>
                <span style='color:{vc}; font-weight:700;'>${rv:,.0f}</span><br>
                <span style='color:{C["text_mute"]}; font-size:0.75rem;'>{delta:+.1f}% vs best</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    pivot = mdf.groupby(["Category","Stage"])["Revenue"].mean().reset_index()
    pw = pivot.pivot(index="Category", columns="Stage", values="Revenue")
    pw.columns = [slabel(c) for c in pw.columns]
    fig_h = go.Figure(data=go.Heatmap(
        z=pw.values, x=pw.columns.tolist(), y=pw.index.tolist(),
        colorscale=[[0,"#000000"],[0.5,"#7DE1D8"],[1,C["primary"]]],
        text=[[f"${v:,.0f}" for v in row] for row in pw.values],
        texttemplate="%{text}", showscale=True,
    ))
    fig_h.update_layout(title="Average Revenue by Category and Markdown Stage — Darker = Higher Revenue")
    st.plotly_chart(chart(fig_h, height=250), use_container_width=True)

    st.markdown(f"""
    <div class='insight'>
      <div class='insight-label'>Key Takeaway</div>
      <div class='insight-text'>
        Changing the timing of a markdown — without changing the discount amount —
        can be worth up to <strong>{timing_gap:.0f}% more revenue</strong>.
        The recommended approach is to plan your markdown calendar in advance
        and use <strong>{slabel(best_t)}</strong> as the standard trigger point.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — DISCOUNT DEPTH
# ══════════════════════════════════════════════
with t3:
    bins   = [0, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 1.0]
    labels = ["<15%","15–20%","20–25%","25–30%","30–35%","35–40%",">40%"]
    mdf["Disc_Bin"] = pd.cut(mdf["Markdown"], bins=bins, labels=labels)

    disc_total = mdf.groupby("Disc_Bin", observed=True)["Revenue"].mean().reset_index()
    peak_bin   = disc_total.loc[disc_total["Revenue"].idxmax(), "Disc_Bin"]
    peak_rev   = disc_total["Revenue"].max()
    low_rev    = disc_total["Revenue"].min()
    depth_gap  = ((peak_rev - low_rev) / low_rev) * 100

    ret_disc   = mdf.dropna(subset=["Disc_Bin"]).groupby("Disc_Bin", observed=True)["Return_Rate"].mean().reset_index()
    rate_low   = ret_disc.iloc[0]["Return_Rate"]
    rate_high  = ret_disc.iloc[-1]["Return_Rate"]

    st.markdown(f"""
    <div class='story-intro'>
      <div class='story-label'>Question 3</div>
      <div class='story-title'>Is a larger discount always better for revenue?</div>
      <div class='story-body'>
        The data shows that the highest average revenue per product is achieved at a
        <strong>{peak_bin} discount</strong> — not at 40% or above.
        Beyond this point, the additional units sold are not enough to compensate for
        the lower price per unit. Product return rates also increase at higher discount levels,
        which further reduces net revenue.
      </div>
    </div>

    <div class='box-row'>
      <div class='box-problem'>
        <div class='box-label' style='color:#B91C1C;'>What Happens Above {peak_bin}</div>
        <div class='box-text'>
          At discounts above <strong>{peak_bin}</strong>, average revenue per product
          starts to decline. Return rates rise from <strong>{rate_low:.1f}%</strong>
          at lower discounts to <strong>{rate_high:.1f}%</strong> at the highest levels,
          reducing the net benefit of the additional sales volume.
        </div>
      </div>
      <div class='box-result'>
        <div class='box-label' style='color:#15803D;'>The Recommended Range</div>
        <div class='box-text'>
          A discount of <strong>{peak_bin}</strong> produces the highest average revenue.
          This range brings in price-sensitive customers without reducing the
          perceived value of the product.
        </div>
      </div>
      <div class='box-recommend'>
        <div class='box-label' style='color:#1D4ED8;'>Recommended Action</div>
        <div class='box-text'>
          Use <strong>{peak_bin}</strong> as the default markdown range for most products.
          Only go beyond this for products that have been unsold for more than 90 days
          and require clearance.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        peak_idx  = disc_total["Revenue"].idxmax()
        bar_cols3 = [C["primary"] if i == peak_idx else "#333333" for i in range(len(disc_total))]
        fig = go.Figure(go.Bar(
            x=disc_total["Disc_Bin"].astype(str), y=disc_total["Revenue"],
            marker_color=bar_cols3,
            text=[f"${v:,.0f}" for v in disc_total["Revenue"]],
            textposition="outside",
        ))
        fig.add_annotation(
            x=str(peak_bin), y=peak_rev,
            text="Best range",
            showarrow=True, arrowhead=2, arrowcolor=C["primary"],
            font=dict(color=C["primary"], size=11), ay=-45,
        )
        fig.update_layout(title="Average Revenue per Product by Discount Depth",
                          xaxis_title="Discount Range", yaxis_title="Avg Revenue", showlegend=False)
        st.plotly_chart(chart(fig), use_container_width=True)

    with col2:
        fig2 = px.line(ret_disc, x="Disc_Bin", y="Return_Rate", markers=True,
                       title="Return Rate by Discount Depth",
                       color_discrete_sequence=[C["warn"]])
        fig2.update_traces(line_width=2, marker_size=8)
        fig2.update_layout(yaxis_title="Return Rate (%)", xaxis_title="Discount Range")
        st.plotly_chart(chart(fig2), use_container_width=True)

    cat_disc = mdf.dropna(subset=["Disc_Bin"]).groupby(["Category","Disc_Bin"], observed=True)["Revenue"].mean().reset_index()
    fig3 = px.line(cat_disc, x="Disc_Bin", y="Revenue", color="Category", markers=True,
                   title="Average Revenue by Discount Depth — by Category",
                   color_discrete_sequence=CHART_COLORS)
    fig3.update_traces(line_width=2, marker_size=7)
    fig3.update_layout(xaxis_title="Discount Range", yaxis_title="Avg Revenue")
    st.plotly_chart(chart(fig3, height=320), use_container_width=True)

    st.markdown(f"""
    <div class='insight'>
      <div class='insight-label'>Key Takeaway</div>
      <div class='insight-text'>
        A larger discount does not automatically generate more revenue.
        The data shows a <strong>{depth_gap:.0f}% revenue difference</strong>
        between the best and lowest performing discount ranges.
        Setting a clear upper limit on discount depth — and reviewing exceptions individually —
        is a straightforward way to protect margin.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — SEASONAL PATTERNS
# ══════════════════════════════════════════════
with t4:
    season_stage = mdf.groupby(["Season","Stage"]).agg(
        Revenue=("Revenue","mean"),
        Sell_through=("Sell_through","mean"),
    ).reset_index()

    st_pivot     = season_stage.pivot(index="Season", columns="Stage", values="Sell_through")
    st_pivot["Range"] = st_pivot["M4"] - st_pivot["M1"]
    fast_season  = st_pivot["Range"].idxmax()
    fast_vel     = st_pivot.loc[fast_season, "Range"]

    season_best = (
        mdf.groupby(["Season","Stage"])["Revenue"].mean().reset_index()
        .sort_values("Revenue", ascending=False)
        .drop_duplicates(subset=["Season"])
    )

    st.markdown(f"""
    <div class='story-intro'>
      <div class='story-label'>Question 4</div>
      <div class='story-title'>Should the markdown approach change depending on the season?</div>
      <div class='story-body'>
        Yes — different seasons show different sell-through patterns.
        <strong>{fast_season}</strong> products show the highest sell-through improvement
        once a markdown is applied, with the rate improving by
        <strong>{fast_vel:.1f}x</strong> between Stage 1 and Stage 4.
        This means the markdown window in <strong>{fast_season}</strong> delivers strong results,
        but requires a more timely decision to capture the full benefit.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        season_stage["Stage_Label"] = season_stage["Stage"].map(
            {"M1":"Stage 1","M2":"Stage 2","M3":"Stage 3","M4":"Stage 4"}
        )
        fig = px.line(season_stage, x="Stage_Label", y="Revenue", color="Season",
                      markers=True, title="Average Revenue by Season and Markdown Stage",
                      color_discrete_sequence=CHART_COLORS)
        fig.update_traces(line_width=2, marker_size=8)
        fig.update_layout(xaxis_title="Stage", yaxis_title="Avg Revenue")
        st.plotly_chart(chart(fig, height=360), use_container_width=True)

    with col2:
        st_wide = season_stage.pivot(index="Season", columns="Stage_Label", values="Sell_through")
        fig_h   = go.Figure(data=go.Heatmap(
            z=st_wide.values, x=st_wide.columns.tolist(), y=st_wide.index.tolist(),
            colorscale=[[0,"#000000"],[0.5,"#7DE1D8"],[1,C["primary"]]],
            text=[[f"{v:.2f}x" for v in row] for row in st_wide.values],
            texttemplate="%{text}", showscale=True,
        ))
        fig_h.update_layout(
            title="Sell-Through Rate by Season and Stage — Darker = Faster Stock Movement",
            height=360,
        )
        st.plotly_chart(chart(fig_h), use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns([1, 2])

    with col3:
        st.markdown("#### Recommended Stage by Season")
        for _, row_s in season_best.iterrows():
            sv = mdf[mdf["Season"]==row_s["Season"]].groupby("Stage")["Revenue"].mean()
            sensitivity = ((sv.max() - sv.min()) / sv.min() * 100)
            note = "Plan markdown early" if sensitivity > 60 else ("Some flexibility" if sensitivity > 30 else "Flexible timing")
            nc   = C["danger"] if sensitivity > 60 else (C["warn"] if sensitivity > 30 else C["primary"])
            st.markdown(f"""
            <div style='background:{C["bg_subtle"]}; border:1px solid {C["border"]};
                        border-radius:6px; padding:12px 14px; margin-bottom:8px;'>
              <div style='display:flex; justify-content:space-between;'>
                <div>
                  <span style='font-weight:600; color:{C["text_main"]};'>{row_s['Season']}</span><br>
                  <span style='color:{C["text_sub"]}; font-size:0.8rem;'>
                    Best stage: <span class='stage-pill'>{slabel(row_s['Stage'])}</span>
                  </span>
                </div>
                <div style='text-align:right;'>
                  <span style='color:{nc}; font-size:0.75rem; font-weight:600;'>{note}</span><br>
                  <span style='color:{C["text_mute"]}; font-size:0.72rem;'>
                    Timing sensitivity: {sensitivity:.0f}%
                  </span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        sc = mdf.groupby(["Season","Category"])["Revenue"].mean().reset_index()
        fig_sc = px.bar(sc, x="Season", y="Revenue", color="Category",
                        barmode="group",
                        title="Average Revenue by Season and Category",
                        color_discrete_sequence=CHART_COLORS)
        fig_sc.update_layout(yaxis_title="Avg Revenue")
        st.plotly_chart(chart(fig_sc, height=300), use_container_width=True)

    st.markdown(f"""
    <div class='insight'>
      <div class='insight-label'>Key Takeaway</div>
      <div class='insight-text'>
        A single markdown calendar does not work equally well across all seasons.
        <strong>{fast_season}</strong> products respond most strongly to markdowns
        and have a shorter window to act in.
        Building a season-specific markdown plan — with stage targets agreed
        before the season begins — will improve both sell-through rates and revenue.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — BRAND COMPARISON
# ══════════════════════════════════════════════
with t5:
    brand_hist = df.groupby("Brand")["Historical_Sales"].mean()
    brand_best = (
        mdf.groupby(["Brand","Stage"])["Revenue"].mean().reset_index()
        .sort_values("Revenue", ascending=False)
        .drop_duplicates(subset=["Brand"])
        .rename(columns={"Revenue":"Best_Revenue","Stage":"Best_Stage"})
    )
    brand_best["Hist_Sales"] = brand_best["Brand"].map(brand_hist)
    brand_best["Opt_Sales"]  = brand_best.apply(
        lambda r: mdf[(mdf["Brand"]==r["Brand"]) & (mdf["Stage"]==r["Best_Stage"])]["Sales"].mean(), axis=1
    )
    brand_best["Lift_Pct"] = ((brand_best["Opt_Sales"] / brand_best["Hist_Sales"]) - 1) * 100
    brand_best = brand_best.sort_values("Best_Revenue", ascending=False)

    top_brand    = brand_best.iloc[0]["Brand"]
    top_lift     = brand_best.iloc[0]["Lift_Pct"]
    top_stage    = brand_best.iloc[0]["Best_Stage"]
    low_brand    = brand_best.iloc[-1]["Brand"]
    low_lift     = brand_best.iloc[-1]["Lift_Pct"]

    st.markdown(f"""
    <div class='story-intro'>
      <div class='story-label'>Question 5</div>
      <div class='story-title'>Do all brands respond equally to markdowns — and where should budget go?</div>
      <div class='story-body'>
        The data shows a clear difference between brands.
        <strong>{top_brand}</strong> shows a <strong>+{top_lift:.0f}% sales increase</strong>
        when a markdown is applied at {slabel(top_stage)}.
        <strong>{low_brand}</strong> shows a smaller increase of
        <strong>+{low_lift:.0f}%</strong> for a comparable action.
        This means the same markdown budget produces different results
        depending on which brand it is applied to.
      </div>
    </div>

    <div class='box-row'>
      <div class='box-problem'>
        <div class='box-label' style='color:#B91C1C;'>Brands with Lower Response</div>
        <div class='box-text'>
          <strong>{low_brand}</strong> shows a <strong>+{low_lift:.0f}%</strong> sales
          response to markdown. Before increasing the discount level,
          it is worth investigating whether price is actually the main factor
          limiting sales for this brand.
        </div>
      </div>
      <div class='box-result'>
        <div class='box-label' style='color:#15803D;'>Brands with Higher Response</div>
        <div class='box-text'>
          <strong>{top_brand}</strong> shows a <strong>+{top_lift:.0f}%</strong> sales
          increase — the highest in the range — making it the most effective use
          of markdown budget at <strong>{slabel(top_stage)}</strong>.
        </div>
      </div>
      <div class='box-recommend'>
        <div class='box-label' style='color:#1D4ED8;'>Recommended Approach</div>
        <div class='box-text'>
          Prioritise markdown investment for brands where the response is highest.
          For brands with a lower response, consider whether non-price actions
          such as placement, range or availability would be more effective.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(brand_best, x="Brand", y="Best_Revenue",
                     title="Peak Revenue per Product — by Brand at Optimal Stage",
                     color_discrete_sequence=[C["primary"]],
                     text=brand_best["Best_Revenue"].apply(lambda x: f"${x:,.0f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_title="Avg Revenue per Product", showlegend=False)
        st.plotly_chart(chart(fig), use_container_width=True)

    with col2:
        bar_cols5 = [
            C["primary"] if v == brand_best["Lift_Pct"].max()
            else C["danger"] if v == brand_best["Lift_Pct"].min()
            else "#333333"
            for v in brand_best["Lift_Pct"]
        ]
        fig2 = go.Figure(go.Bar(
            x=brand_best["Brand"], y=brand_best["Lift_Pct"],
            marker_color=bar_cols5,
            text=[f"+{v:.0f}%" for v in brand_best["Lift_Pct"]],
            textposition="outside",
        ))
        fig2.update_layout(
            title="Sales Increase (%) by Brand After Applying Optimal Markdown",
            yaxis_title="Sales Increase %",
            paper_bgcolor=C["bg_card"], plot_bgcolor=C["bg_card"],
            font=dict(color=C["text_sub"]), height=360,
            margin=dict(l=10,r=10,t=40,b=10), showlegend=False,
        )
        fig2.update_xaxes(gridcolor=C["border"])
        fig2.update_yaxes(gridcolor=C["border"])
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap
    bpiv = mdf.groupby(["Brand","Stage"])["Revenue"].mean().reset_index()
    bpw  = bpiv.pivot(index="Brand", columns="Stage", values="Revenue")
    bpw.columns = [slabel(c) for c in bpw.columns]
    fig3 = go.Figure(data=go.Heatmap(
        z=bpw.values, x=bpw.columns.tolist(), y=bpw.index.tolist(),
        colorscale=[[0,"#000000"],[0.5,"#7DE1D8"],[1,C["primary"]]],
        text=[[f"${v:,.0f}" for v in row] for row in bpw.values],
        texttemplate="%{text}", showscale=True,
    ))
    fig3.update_layout(title="Average Revenue by Brand and Stage — Darker = Higher Revenue")
    st.plotly_chart(chart(fig3, height=280), use_container_width=True)

    st.markdown("---")
    st.markdown("#### Brand Summary")

    sc = brand_best[["Brand","Best_Stage","Hist_Sales","Opt_Sales","Lift_Pct","Best_Revenue"]].copy()
    sc.columns = ["Brand","Best Stage","Baseline Avg Sales","Optimised Avg Sales","Sales Increase %","Peak Revenue"]
    sc["Best Stage"]           = sc["Best Stage"].map({"M1":"Stage 1","M2":"Stage 2","M3":"Stage 3","M4":"Stage 4"})
    sc["Baseline Avg Sales"]   = sc["Baseline Avg Sales"].round(0)
    sc["Optimised Avg Sales"]  = sc["Optimised Avg Sales"].round(0)
    sc["Sales Increase %"]     = sc["Sales Increase %"].round(1)
    sc["Peak Revenue"]         = sc["Peak Revenue"].round(0)

    st.dataframe(sc, use_container_width=True, hide_index=True,
        column_config={
            "Peak Revenue":        st.column_config.NumberColumn("Peak Revenue",        format="$%.0f"),
            "Sales Increase %":    st.column_config.NumberColumn("Sales Increase %",    format="+%.1f%%"),
            "Baseline Avg Sales":  st.column_config.NumberColumn("Baseline Avg Sales",  format="%.0f units"),
            "Optimised Avg Sales": st.column_config.NumberColumn("Optimised Avg Sales", format="%.0f units"),
        })

    st.markdown(f"""
    <div class='insight'>
      <div class='insight-label'>Key Takeaway</div>
      <div class='insight-text'>
        Markdown budget should follow response rate, not just brand size.
        <strong>{top_brand}</strong> delivers the highest return on every percentage
        point of discount applied. Reviewing brand-level markdown response
        each quarter will help ensure budget is directed where it has the
        greatest measurable impact on sales.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style='text-align:center; color:{C["text_mute"]}; font-size:0.82rem; padding:8px 0;'>
  Retail Markdown Insights &nbsp;·&nbsp; {len(df):,} products across {len(sel_cats)} categories
</div>
""", unsafe_allow_html=True)
