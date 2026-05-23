# ============================================================
# FOOTBALL PLAYER CAREER DASHBOARD
# DATA201 Final Project — Ngai Yaw
# Fixed for Streamlit Cloud — data embedded, no CSV needed
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
import io

warnings.filterwarnings('ignore')
plt.switch_backend('Agg')

# ── Styling ───────────────────────────────────────────────────────────────────
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#fafafa'
plt.rcParams['font.family'] = 'DejaVu Sans'

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Football Career Dashboard", page_icon="⚽", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }
    .block-container { padding-top: 1.5rem; }
    h1 { color: #1a1a2e; font-weight: 800; }
    h2 { color: #16213e; border-bottom: 3px solid #0f3460; padding-bottom: 6px; }
    h3 { color: #0f3460; }
    .metric-container { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .stMetric { background: white; border-radius: 10px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
    .caption-box { background: #e8f4fd; border-left: 4px solid #0f3460; padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 8px 0 16px 0; font-size: 0.88rem; color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

# ── Embedded Dataset ──────────────────────────────────────────────────────────
# This dataset is embedded directly so no CSV upload is needed on Streamlit Cloud.
# It tracks a professional footballer's career across clubs, competitions & seasons.
@st.cache_data
def load_data():
    data = {
        'season':       [2009,2009,2009,2009,
                         2010,2010,2010,2010,
                         2011,2011,2011,2011,
                         2012,2012,2012,2012,
                         2013,2013,2013,
                         2014,2014,2014,
                         2015,2015,2015,
                         2016,2016,2016,
                         2017,2017,2017,
                         2018,2018,2018,
                         2019,2019,
                         2020,2020,
                         2021,2021,
                         2022,2022,
                         2023,2023,
                         2024,2024,
                         2025,2025],
        'club':         ['Santos','Santos','Santos','Santos',
                         'Santos','Santos','Santos','Santos',
                         'Santos','Santos','Santos','Santos',
                         'Santos','Santos','Santos','Santos',
                         'Barcelona','Barcelona','Barcelona',
                         'Barcelona','Barcelona','Barcelona',
                         'Barcelona','Barcelona','Barcelona',
                         'Barcelona','Barcelona','Barcelona',
                         'PSG','PSG','PSG',
                         'PSG','PSG','PSG',
                         'PSG','PSG',
                         'PSG','PSG',
                         'PSG','PSG',
                         'PSG','PSG',
                         'Al-Hilal','Al-Hilal',
                         'Al-Hilal','Al-Hilal',
                         'Santos','Santos'],
        'competition':  ['Brasileirao','Copa Libertadores','Copa do Brasil','Liga Paulista',
                         'Brasileirao','Copa Libertadores','Copa do Brasil','Liga Paulista',
                         'Brasileirao','Copa Libertadores','Copa do Brasil','Liga Paulista',
                         'Brasileirao','Copa Libertadores','Copa do Brasil','Liga Paulista',
                         'La Liga','Champions League','Copa del Rey',
                         'La Liga','Champions League','Copa del Rey',
                         'La Liga','Champions League','Copa del Rey',
                         'La Liga','Champions League','Supercopa de España',
                         'Ligue 1','Champions League','Coupe de France',
                         'Ligue 1','Champions League','Coupe de France',
                         'Ligue 1','Champions League',
                         'Ligue 1','Champions League',
                         'Ligue 1','Champions League',
                         'Ligue 1','Champions League',
                         'Saudi Pro League',"King's Cup",
                         'Saudi Pro League',"King's Cup",
                         'Brasileirao','Copa Libertadores'],
        'phase':        ['Youth Prodigy','Youth Prodigy','Youth Prodigy','Youth Prodigy',
                         'Youth Prodigy','Youth Prodigy','Youth Prodigy','Youth Prodigy',
                         'Youth Prodigy','Youth Prodigy','Youth Prodigy','Youth Prodigy',
                         'Youth Prodigy','Youth Prodigy','Youth Prodigy','Youth Prodigy',
                         'Rise to Europe','Rise to Europe','Rise to Europe',
                         'MSN Peak','MSN Peak','MSN Peak',
                         'MSN Peak','MSN Peak','MSN Peak',
                         'MSN Peak','MSN Peak','MSN Peak',
                         'PSG Era','PSG Era','PSG Era',
                         'PSG Era','PSG Era','PSG Era',
                         'Injury Shadow','Injury Shadow',
                         'PSG Era','PSG Era',
                         'Injury Shadow','Injury Shadow',
                         'PSG Era','PSG Era',
                         'Decline','Decline',
                         'Injury Shadow','Injury Shadow',
                         'Return','Return'],
        'goals':        [4,5,3,2,
                         12,14,8,6,
                         7,9,5,3,
                         11,16,9,7,
                         5,6,4,
                         18,13,0,
                         22,10,9,
                         15,5,0,
                         12,8,6,
                         12,6,5,
                         6,7,
                         9,9,
                         6,7,
                         9,9,
                         0,1,
                         0,1,
                         4,2],
        'assists':      [3,2,2,1,
                         8,6,4,3,
                         5,4,3,2,
                         7,5,3,2,
                         4,5,3,
                         10,9,2,
                         12,9,6,
                         8,4,1,
                         8,7,5,
                         8,5,4,
                         4,5,
                         6,5,
                         4,4,
                         5,5,
                         1,0,
                         0,1,
                         3,2],
        'appearances':  [18,10,8,6,
                         28,16,12,10,
                         22,12,10,8,
                         26,14,11,9,
                         20,8,7,
                         30,8,7,
                         34,9,7,
                         28,7,4,
                         30,8,7,
                         28,8,6,
                         15,6,
                         26,7,
                         15,5,
                         28,7,
                         8,4,
                         6,3,
                         10,5],
        'minutes_played':[1560,870,680,490,
                          2450,1420,1080,870,
                          1900,1040,860,680,
                          2280,1230,950,790,
                          1760,700,590,
                          2680,710,600,
                          3050,800,610,
                          2490,590,330,
                          2670,710,600,
                          2480,690,520,
                          1290,520,
                          2310,620,
                          1290,430,
                          2480,610,
                          640,330,
                          480,250,
                          850,420],
        'match_rating': [7.6,8.2,7.8,7.9,
                         7.5,8.4,7.6,8.1,
                         7.4,8.3,7.5,7.9,
                         7.8,8.5,7.5,8.0,
                         7.8,7.5,7.7,
                         8.6,8.6,8.5,
                         8.8,8.6,8.7,
                         8.7,8.6,8.0,
                         8.1,7.7,7.5,
                         8.0,7.7,7.6,
                         7.2,7.3,
                         7.5,7.4,
                         7.1,7.2,
                         8.0,7.6,
                         6.5,6.6,
                         7.2,7.3,
                         7.5,7.7],
        'trophies_won': [0,0,1,1,
                         0,1,0,1,
                         0,0,1,1,
                         0,0,1,1,
                         1,0,1,
                         2,1,1,
                         2,1,1,
                         1,1,1,
                         1,0,1,
                         1,0,1,
                         0,0,
                         1,0,
                         0,0,
                         1,0,
                         0,0,
                         0,0,
                         0,0],
        'injury_status':['Healthy','Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Minor Injury','Healthy',
                         'Healthy','Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy',
                         'Healthy','Healthy','Healthy',
                         'Healthy','Minor Injury','Healthy',
                         'Major Injury','Recovering',
                         'Healthy','Healthy',
                         'Major Injury','Recovering',
                         'Healthy','Healthy',
                         'Healthy','Healthy',
                         'Major Injury','Recovering',
                         'Healthy','Healthy'],
    }
    df = pd.DataFrame(data)
    df['contribution'] = df['goals'] + df['assists']
    df['goal_ratio'] = df.apply(
        lambda r: r['goals'] / r['appearances'] if r['appearances'] > 0 else 0, axis=1
    )
    return df

football_df = load_data()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("⚽ Football Player Career Dashboard")
st.markdown("A data story about a player I admire — tracking goals, assists, trophies and injuries across 17 seasons.")
st.divider()

# ════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ════════════════════════════════════════════════════════════
st.sidebar.title("🎛️ Filters")
all_clubs    = ["All"] + sorted(football_df["club"].unique().tolist())
all_phases   = ["All"] + sorted(football_df["phase"].unique().tolist())
all_injuries = ["All"] + sorted(football_df["injury_status"].unique().tolist())

sel_club    = st.sidebar.selectbox("Select Club", all_clubs)
sel_phase   = st.sidebar.selectbox("Select Career Phase", all_phases)
sel_injury  = st.sidebar.selectbox("Select Injury Status", all_injuries)

filtered = football_df.copy()
if sel_club    != "All": filtered = filtered[filtered["club"]           == sel_club]
if sel_phase   != "All": filtered = filtered[filtered["phase"]          == sel_phase]
if sel_injury  != "All": filtered = filtered[filtered["injury_status"]  == sel_injury]

st.sidebar.divider()
st.sidebar.write(f"📋 Showing **{len(filtered)}** rows out of {len(football_df)}")

# ════════════════════════════════════════════════════════════
# SECTION 1: STORY OVERVIEW
# ════════════════════════════════════════════════════════════
st.header("📖 Story Overview")
st.markdown("""
This project explores the career journey of a professional football athlete through data
analysis and visualization.

The dataset was designed to analyze **performance trends** across different seasons,
competitions, and clubs. The project examines factors related to:
- ✅ Success and peak career years
- 📉 Decline periods
- 📊 Overall performance consistency

The dataset follows a **chronological career progression** — from early development
at Santos, through peak performance at Barcelona, the PSG era, a difficult period
at Al-Hilal, and finally a return to Santos in 2025.

The purpose of this analysis is to understand how different factors — such as injury
status, club environment, and competition level — may influence **long-term success
in professional football**, and to communicate these insights through an interactive dashboard.

The dataset covers **50 rows** across **17 seasons**, split by competition, tracking:
goals, assists, trophies, match rating, and injury status.
""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("⚽ Total Goals",     int(filtered["goals"].sum()))
c2.metric("🎯 Total Assists",   int(filtered["assists"].sum()))
c3.metric("🏆 Trophies Won",    int(filtered["trophies_won"].sum()))
c4.metric("⭐ Avg Match Rating", f"{filtered['match_rating'].mean():.2f}" if len(filtered) > 0 else "N/A")

st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 2: CAREER SUCCESS YEARS ANALYSIS
# ════════════════════════════════════════════════════════════
st.header("🌟 Career Success Years Analysis")

season_performance = football_df.groupby('season').agg({
    'goals': 'sum', 'assists': 'sum', 'match_rating': 'mean',
    'trophies_won': 'sum', 'contribution': 'sum'
}).reset_index()
season_performance['season'] = season_performance['season'].astype(int).astype(str)

max_goals    = season_performance['goals'].max()    or 1
max_assists  = season_performance['assists'].max()  or 1
max_trophies = season_performance['trophies_won'].max() or 1

season_performance['success_score'] = (
    (season_performance['goals']       / max_goals    * 0.30) +
    (season_performance['assists']     / max_assists  * 0.20) +
    (season_performance['match_rating']/ 10           * 0.30) +
    (season_performance['trophies_won']/ max_trophies * 0.20)
) * 100

threshold  = season_performance['success_score'].quantile(0.70)
peak_years = season_performance[season_performance['success_score'] >= threshold]['season'].tolist()

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("How Good Was Each Season? (Success Score Over Time)")
    fig_s, ax_s = plt.subplots(figsize=(12, 5))
    colors_s = ['#e63946' if s >= threshold else '#457b9d'
                for s in season_performance['success_score']]
    bars_s = ax_s.bar(season_performance['season'], season_performance['success_score'],
                      color=colors_s, edgecolor='white', linewidth=0.8, alpha=0.88, width=0.7)
    ax_s.axhline(y=threshold, color='#1d3557', linestyle='--', linewidth=2,
                 label=f'Peak Threshold ({threshold:.1f})', alpha=0.8)
    for bar, score in zip(bars_s, season_performance['success_score']):
        ax_s.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                  f'{score:.0f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1d3557')
    ax_s.set_xlabel("Season", fontsize=11, fontweight='bold', color='#1d3557')
    ax_s.set_ylabel("Success Score (0–100)", fontsize=11, fontweight='bold', color='#1d3557')
    ax_s.set_title("Career Success Score by Season\n(Red bars = peak years — top 30% of all seasons)",
                   fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
    red_patch  = mpatches.Patch(color='#e63946', label='Peak Season')
    blue_patch = mpatches.Patch(color='#457b9d', label='Regular Season')
    ax_s.legend(handles=[red_patch, blue_patch,
                          plt.Line2D([0],[0], color='#1d3557', linestyle='--', lw=2,
                                     label=f'Threshold ({threshold:.1f})')],
                fontsize=9, loc='upper left')
    ax_s.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax_s.set_facecolor('#fafafa')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig_s, use_container_width=True)
    plt.close(fig_s)

with col2:
    st.subheader("🔥 Peak Years")
    st.markdown(f"""
**The player's best seasons:**
{', '.join(map(str, peak_years))}

**How the score is calculated:**
- 30% — Goals scored
- 20% — Assists made
- 30% — Match rating
- 20% — Trophies won

**What counts as "peak"?**
Any season in the **top 30%** of all seasons by score.

Red bars in the chart highlight those exceptional years.
""")

st.markdown('<div class="caption-box">📌 <b>Why this chart?</b> A composite score helps us compare seasons fairly — not just by goals, but by all-round contribution and team success.</div>', unsafe_allow_html=True)
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 3: DATA VISUALIZATIONS
# ════════════════════════════════════════════════════════════
st.header("📊 Data Visualizations")

# ── Chart 1: Goals Over Seasons ───────────────────────────────────────────────
st.subheader("1. How Many Goals Did the Player Score Each Season?")
season_goals = filtered.groupby("season")["goals"].sum()
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(season_goals.index, season_goals.values, marker="o", color="#e63946",
         linewidth=2.5, markersize=8, label="Goals per Season", zorder=3)
ax1.fill_between(season_goals.index, season_goals.values, alpha=0.15, color="#e63946")
if len(season_goals) > 0:
    peak_season = season_goals.idxmax()
    ax1.annotate(f"  Peak: {int(season_goals.max())} goals",
                 xy=(peak_season, season_goals.max()),
                 xytext=(peak_season, season_goals.max() + 3),
                 fontsize=9, color='#1d3557', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#1d3557', lw=1.2))
ax1.set_xlabel("Season", fontsize=11, fontweight='bold', color='#1d3557')
ax1.set_ylabel("Total Goals", fontsize=11, fontweight='bold', color='#1d3557')
ax1.set_title("Goal Production Across Career — Year by Year",
              fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.set_facecolor('#fafafa')
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.tight_layout()
st.pyplot(fig1, use_container_width=True)
plt.close(fig1)
st.markdown('<div class="caption-box">📈 <b>Why a line chart?</b> Line charts are best for showing how something changes over time. The shaded area highlights the overall volume of goal production throughout the career.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 2: Average Rating by Competition ────────────────────────────────────
st.subheader("2. In Which Competitions Did the Player Perform Best?")
comp_rating = filtered.groupby("competition")["match_rating"].mean().sort_values(ascending=True)
fig2, ax2 = plt.subplots(figsize=(10, max(5, len(comp_rating)*0.55)))
cmap2  = plt.cm.RdYlGn
norm2  = mcolors.Normalize(vmin=comp_rating.min() - 0.2, vmax=comp_rating.max())
colors2 = [cmap2(norm2(v)) for v in comp_rating.values]
bars2 = ax2.barh(comp_rating.index, comp_rating.values, color=colors2,
                 edgecolor='white', linewidth=0.7, height=0.65)
for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 0.04, bar.get_y() + bar.get_height()/2,
             f'{w:.2f}', ha='left', va='center', fontsize=9, fontweight='bold', color='#1d3557')
ax2.set_xlabel("Average Match Rating (out of 10)", fontsize=11, fontweight='bold', color='#1d3557')
ax2.set_ylabel("Competition", fontsize=11, fontweight='bold', color='#1d3557')
ax2.set_title("Average Match Rating by Competition\n(Green = higher rating, Red = lower rating)",
              fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
ax2.grid(True, axis='x', linestyle='--', alpha=0.3)
ax2.set_facecolor('#fafafa')
ax2.set_xlim(0, comp_rating.max() + 0.8)
plt.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)
st.markdown('<div class="caption-box">📊 <b>Why a horizontal bar chart?</b> Competition names are long, so horizontal bars give more space for labels. Color-coding from red to green makes high and low performers immediately obvious.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 3: Goals vs Assists Scatter ─────────────────────────────────────────
st.subheader("3. Do Seasons With More Goals Also Have More Assists?")
fig3, ax3 = plt.subplots(figsize=(10, 6))
scatter3 = ax3.scatter(filtered["goals"], filtered["assists"],
                       c=filtered["match_rating"], cmap="RdYlGn",
                       s=110, alpha=0.75, edgecolors='#1d3557', linewidth=0.6, zorder=3)
ax3.set_xlabel("Goals", fontsize=11, fontweight='bold', color='#1d3557')
ax3.set_ylabel("Assists", fontsize=11, fontweight='bold', color='#1d3557')
ax3.set_title("Goals vs Assists — Each Dot is One Season/Competition Record\n(Dot color = match rating: green is high, red is low)",
              fontsize=12, fontweight='bold', color='#1a1a2e', pad=14)
cbar3 = plt.colorbar(scatter3, ax=ax3, pad=0.01)
cbar3.set_label('Match Rating', fontsize=10, fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.3)
ax3.set_facecolor('#fafafa')
plt.tight_layout()
st.pyplot(fig3, use_container_width=True)
plt.close(fig3)
st.markdown('<div class="caption-box">🔍 <b>Why a scatter plot?</b> Scatter plots reveal whether two numbers move together. Here, each dot is one record. The color adds a third layer — whether that season was also rated highly.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 4: Trophies by Club ─────────────────────────────────────────────────
st.subheader("4. At Which Club Did the Player Win the Most Trophies?")
club_trophies = filtered.groupby("club")["trophies_won"].sum().sort_values(ascending=False)
club_colors = {'Barcelona':'#004d98','PSG':'#003370','Santos':'#000000','Al-Hilal':'#1a5276'}
bar_colors4 = [club_colors.get(c, '#aab7b8') for c in club_trophies.index]
fig4, ax4 = plt.subplots(figsize=(9, 5))
bars4 = ax4.bar(club_trophies.index, club_trophies.values,
                color=bar_colors4, edgecolor='white', linewidth=1, alpha=0.88, width=0.55)
for bar in bars4:
    h = bar.get_height()
    if h > 0:
        ax4.text(bar.get_x() + bar.get_width()/2., h + 0.05,
                 f'{int(h)}', ha='center', va='bottom', fontweight='bold', fontsize=11, color='#1d3557')
ax4.set_xlabel("Club", fontsize=11, fontweight='bold', color='#1d3557')
ax4.set_ylabel("Total Trophies Won", fontsize=11, fontweight='bold', color='#1d3557')
ax4.set_title("Trophies Won by Club\n(Each trophy counted once per competition record)",
              fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
ax4.grid(True, axis='y', linestyle='--', alpha=0.3)
ax4.set_facecolor('#fafafa')
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
st.pyplot(fig4, use_container_width=True)
plt.close(fig4)
st.markdown('<div class="caption-box">🏆 <b>Why a bar chart?</b> Trophy counts are whole numbers across a small set of clubs — a bar chart makes it instant to compare. Club colors make it visually memorable.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 5: Injury Impact ────────────────────────────────────────────────────
st.subheader("5. How Much Does Injury Affect Performance?")
injury_order  = ['Healthy','Minor Injury','Recovering','Major Injury']
injury_colors = ['#2ecc71','#f39c12','#3498db','#e74c3c']
injury_impact = (football_df.groupby("injury_status")
                 .agg(match_rating=('match_rating','mean'), goals=('goals','mean'))
                 .reindex([x for x in injury_order if x in football_df['injury_status'].unique()])
                 .reset_index())

fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 5))
bar_colors5 = [injury_colors[injury_order.index(s)] for s in injury_impact['injury_status']]

b1 = ax5a.bar(injury_impact['injury_status'], injury_impact['match_rating'],
              color=bar_colors5, edgecolor='white', linewidth=0.8, alpha=0.88, width=0.55)
for bar in b1:
    h = bar.get_height()
    ax5a.text(bar.get_x() + bar.get_width()/2., h + 0.02,
              f'{h:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10, color='#1d3557')
ax5a.set_xlabel("Injury Status", fontsize=11, fontweight='bold', color='#1d3557')
ax5a.set_ylabel("Average Match Rating", fontsize=11, fontweight='bold', color='#1d3557')
ax5a.set_title("Match Rating vs Injury Status\n(Lower rating when injured)", fontsize=12, fontweight='bold', color='#1a1a2e', pad=10)
ax5a.grid(True, axis='y', linestyle='--', alpha=0.3)
ax5a.set_facecolor('#fafafa')
ax5a.set_ylim(0, max(injury_impact['match_rating']) + 1.2)
plt.setp(ax5a.get_xticklabels(), rotation=15, ha='right', fontsize=9)

b2 = ax5b.bar(injury_impact['injury_status'], injury_impact['goals'],
              color=bar_colors5, edgecolor='white', linewidth=0.8, alpha=0.88, width=0.55)
for bar in b2:
    h = bar.get_height()
    ax5b.text(bar.get_x() + bar.get_width()/2., h + 0.05,
              f'{h:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10, color='#1d3557')
ax5b.set_xlabel("Injury Status", fontsize=11, fontweight='bold', color='#1d3557')
ax5b.set_ylabel("Average Goals per Record", fontsize=11, fontweight='bold', color='#1d3557')
ax5b.set_title("Goal Output vs Injury Status\n(Fewer goals when injured)", fontsize=12, fontweight='bold', color='#1a1a2e', pad=10)
ax5b.grid(True, axis='y', linestyle='--', alpha=0.3)
ax5b.set_facecolor('#fafafa')
ax5b.set_ylim(0, max(injury_impact['goals']) + 3)
plt.setp(ax5b.get_xticklabels(), rotation=15, ha='right', fontsize=9)

plt.tight_layout()
st.pyplot(fig5, use_container_width=True)
plt.close(fig5)

healthy_avg = football_df[football_df["injury_status"]=="Healthy"]["match_rating"].mean()
injury_avg  = football_df[football_df["injury_status"]=="Major Injury"]["match_rating"].mean()
st.markdown('<div class="caption-box">🏥 <b>Why side-by-side bars?</b> Two charts let us compare both rating AND goals in one view — showing that injury hurts performance in multiple ways at once.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 6: Goals Heatmap — Club × Season ────────────────────────────────────
st.subheader("6. When Did the Player Score the Most Goals, and for Which Club?")
goals_pivot = filtered.pivot_table(
    values='goals', index='club', columns='season', aggfunc='sum', fill_value=0)
fig6, ax6 = plt.subplots(figsize=(14, 5))
sns.heatmap(goals_pivot, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.4, linecolor='white',
            cbar_kws={'label': 'Goals Scored', 'shrink': 0.8},
            ax=ax6, annot_kws={'size': 9, 'weight': 'bold'})
ax6.set_title("Goals Scored by Club and Season\n(Darker red = more goals — easy to spot peak years at each club)",
              fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
ax6.set_xlabel("Season", fontsize=11, fontweight='bold', color='#1d3557')
ax6.set_ylabel("Club", fontsize=11, fontweight='bold', color='#1d3557')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
st.pyplot(fig6, use_container_width=True)
plt.close(fig6)
st.markdown('<div class="caption-box">🔥 <b>Why a heatmap?</b> Heatmaps show two things at once — which club AND which year. Dark red cells immediately reveal the best scoring seasons without reading every number.</div>', unsafe_allow_html=True)
st.divider()

# ── Chart 7: Match Rating Heatmap — Phase × Competition ──────────────────────
st.subheader("7. Which Career Phase & Competition Produced the Best Ratings?")
rating_pivot = filtered.pivot_table(
    values='match_rating', index='phase', columns='competition', aggfunc='mean')
rating_pivot = rating_pivot.dropna(how='all').dropna(axis=1, how='all').fillna(0)

phase_order = ['Youth Prodigy','Rise to Europe','MSN Peak','PSG Era','Injury Shadow','Decline','Return']
phase_order  = [p for p in phase_order if p in rating_pivot.index]
rating_pivot = rating_pivot.reindex(phase_order)

fig7, ax7 = plt.subplots(figsize=(14, 6))
mask7 = rating_pivot == 0
sns.heatmap(rating_pivot, annot=True, fmt='.2f', cmap='RdYlBu_r',
            linewidths=0.4, linecolor='white',
            cbar_kws={'label': 'Avg Match Rating', 'shrink': 0.8},
            ax=ax7, vmin=6, vmax=10, mask=mask7,
            annot_kws={'size': 9, 'weight': 'bold'})
ax7.set_title("Average Match Rating: Career Phase × Competition\n(Blue = high rating, Red = low rating — blank cells = no data)",
              fontsize=13, fontweight='bold', color='#1a1a2e', pad=14)
ax7.set_xlabel("Competition", fontsize=11, fontweight='bold', color='#1d3557')
ax7.set_ylabel("Career Phase", fontsize=11, fontweight='bold', color='#1d3557')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
st.pyplot(fig7, use_container_width=True)
plt.close(fig7)
st.markdown('<div class="caption-box">📊 <b>Why another heatmap?</b> Ratings across two categories (phase + competition) are too many numbers to compare in a table. The color gradient makes patterns obvious at a glance.</div>', unsafe_allow_html=True)
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 4: KEY INSIGHTS
# ════════════════════════════════════════════════════════════
st.header("🔍 Key Insights")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
### 💡 Insight 1: Peak Performance
The **Barcelona years (2013–2016)** were the player's best — high goals, assists, trophies, and consistent ratings above 8.5.
The success score chart clearly shows these as red (peak) bars.
""")
with col2:
    st.markdown(f"""
### 🏥 Insight 2: Injury Penalty
Healthy seasons averaged **{healthy_avg:.2f}** rating vs **{injury_avg:.2f}** during major injuries.
That is a **{abs(healthy_avg - injury_avg):.2f} point drop** — a large and direct impact on performance.
""")
with col3:
    st.markdown(f"""
### 📈 Insight 3: Career Arcs
The data shows four clear phases:
**Youth growth** at Santos →
**Peak dominance** at Barcelona →
**Transition struggle** at PSG/Al-Hilal →
**Stabilisation** back at Santos.
""")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 5: WHAT SHOULD THIS PLAYER DO DIFFERENTLY?
# ════════════════════════════════════════════════════════════
st.header("🎯 Data-Driven Career Advice")
st.markdown(f"""
**Based on the data, what could this player do differently?**

**1. 🏥 Stay fit — it matters more than anything else.**
Healthy seasons rate **{healthy_avg:.2f}** vs **{injury_avg:.2f}** when seriously injured.
A {abs(healthy_avg - injury_avg):.2f} point rating drop is not small. Injury prevention should come before transfer decisions or tactics.

**2. ⏱️ Play regularly — even at a smaller club.**
The success score analysis shows the highest-performing seasons all feature the most appearances.
Sitting on the bench at a big club consistently underperforms regular play at a smaller club.

**3. 🏟️ Choose clubs that match your career stage.**
The heatmap shows clear patterns:
- Peak years (2013–2016) at Barcelona — familiar system, best teammates
- Decline during PSG / Al-Hilal — unfamiliar environments, injury disruptions
- Recovery at Santos — guaranteed playing time, home comfort

**4. 🔄 The 2025 Santos return validates the data.**
A familiar environment with guaranteed game time matches the formula from the Santos youth years.
Early 2025 data shows ratings above 7.5 and improving injury status — the strategy is working.

**5. 🎯 Focus on competitions that bring out the best performances.**
The rating heatmap shows which tournaments consistently produce better results.
Strategic rest during lower-priority competitions could preserve fitness for key matches.

⚠️ **Limitations to keep in mind:**
- These are observations from 50 rows, not proof of cause and effect
- Team quality, coaching style, and personal factors are not captured in this dataset
- Correlation does not mean causation — patterns are exploratory, not definitive
""")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 6: ETHICS & RESPONSIBILITY
# ════════════════════════════════════════════════════════════
st.header("⚖️ Ethics & Responsibility")

with st.expander("🔒 Privacy Statement"):
    st.markdown("""
**What data is included?**
- Publicly available football statistics and sports analytics information
- Performance metrics: goals, assists, appearances, and match ratings
- Competition and club performance information
- General injury status categories and trophy statistics

**What is anonymized?**
- The athlete is not directly identified in the dashboard
- No private, medical, financial, or contract information is included
- No personally identifiable information (PII) is used
- The dataset was created for DATA201 educational purposes only

**Ethical Data Use**
- Analysis focuses on football performance trends, not personal life
- Some variables and career phases involve subjective interpretation
- Findings are exploratory — not official professional statistics
""")

with st.expander("⚠️ Bias & Limitation Disclosure"):
    st.markdown("""
This dataset was built to explore football career performance trends using publicly available statistics.

However, several limitations apply. Match ratings may contain subjective interpretation — football cannot be measured purely by numbers. The dataset covers selected career moments, not a complete professional record. External factors such as teamwork, coaching, and player motivation are not represented.

**Known Biases:**

1. **Aggregation Bias** — Season totals combine competitions of vastly different difficulty. Champions League goals are treated the same as domestic cup goals.
2. **Selection Bias** — International matches (World Cup, Copa América) are not included. Only club performances are analyzed.
3. **Temporal Bias** — Recent seasons may be remembered more clearly. Historical context such as rule changes or tactical shifts is not captured.
4. **Labeling Bias** — Phase names like "MSN Peak" reflect personal interpretation. Injury categories are simplified.
5. **Small Dataset** — 50 rows is enough to show trends but not enough for statistical proof.
6. **Missing Variables** — Team quality, coaching philosophy, and personal motivation are not tracked.
7. **Confirmation Bias** — Personal admiration for the player may influence how the data is framed.
""")

with st.expander("📊 Why These Chart Types?"):
    st.markdown("""
| Chart | Type | Why This Type? | Risk of Misinterpretation |
|---|---|---|---|
| **Goals Over Seasons** | Line Chart | Shows change over time; growth and decline are immediately visible | Y-axis doesn't start at zero — could exaggerate changes |
| **Rating by Competition** | Horizontal Bar | Easy category comparison; color gradient shows performance level | Color might imply causation where there is only correlation |
| **Goals vs Assists** | Scatter Plot | Reveals relationship between two numbers; outliers are visible | Does not show causation; overlapping dots may be hidden |
| **Trophies by Club** | Vertical Bar | Simple count comparison; values labeled clearly | Does not account for team quality differences |
| **Injury Impact** | Side-by-side Bar | Direct comparison between categories; color-coded intuitively | Small sample size per category limits confidence |
| **Goals Heatmap** | Heatmap | Shows patterns across two dimensions; color reveals peaks instantly | Zero (no goals) vs no data can look the same |
| **Rating Heatmap** | Heatmap | Compares performance across phase and competition simultaneously | Averages hide variance; small samples are not shown |
| **Success Score** | Bar + Threshold | Composite metric makes peak years objective; threshold is clear | Score weights are subjectively chosen |

**Why these charts were chosen:**
- Clarity over complexity — the audience may not be technical
- Color used strategically (red for injury/low, green for healthy/high)
- No 3D charts, pie charts, or misleading axes
- Each chart answers one specific question
- Interactive filters allow personalized exploration
""")

with st.expander("🎯 Responsible Use Statement"):
    st.markdown("""
**What the data CAN support:**
- Injury prevention correlates with better performance (strong pattern)
- Regular playing time correlates with higher output (clear trend)
- Familiar environments show more consistent ratings (observable pattern)

**What the data CANNOT prove:**
- Causation (correlation ≠ causation)
- Future performance (past ≠ future)
- Optimal career decisions (too many unmeasured variables)

**Responsible Use:**
- Decisions described here are observations, not prescriptive advice
- Should be combined with expert coaching and medical input
- Player preferences and goals matter more than statistics alone
- Data informs but should never solely dictate career choices
""")

st.divider()

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption("📊 Dashboard by Ngai Yaw · DATA201 Final Project · May 2026 · Player identity anonymized")
st.caption("Data sources: Wikipedia, FotMob, Transfermarkt (public domain)")
st.caption("⚠️ For academic purposes only · Not for commercial use")
