# ============================================================
# FOOTBALL PLAYER CAREER DASHBOARD
# DATA201 Final Project — Ngai Yaw
# ✅ Ready for https://share.streamlit.io/deploy
# ✅ No seaborn — all charts use matplotlib only
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')
plt.switch_backend('Agg')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = 'white'

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Football Career Dashboard",
    page_icon="⚽",
    layout="wide"
)

# ── Load Data ──────────────────────
@st.cache_data
def load_data():
    try:
        football_df = pd.read_csv("football_player_career.csv")
        football_df['contribution'] = football_df['goals'] + football_df['assists']    # Cell 22
        football_df['goal_ratio']   = football_df.apply(                               # Cell 23
            lambda row: row['goals'] / row['appearances'] if row['appearances'] > 0 else 0,
            axis=1
        )
        return football_df
    except FileNotFoundError:
        st.error("❌ 'football_player_career.csv' not found. Upload it to the same GitHub repo as app.py")
        st.stop()

football_df = load_data()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("⚽ Football Player Career Dashboard")
st.markdown("A data story about a player I admire — tracking goals, assists, trophies and injuries across **17 seasons**.")
st.divider()

# ════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ════════════════════════════════════════════════════════════
st.sidebar.title("🎛️ Filters")

all_clubs    = ["All"] + sorted(football_df["club"].unique().tolist())
all_competitions = ["All"] + sorted(football_df["competition"].unique().tolist())  
all_phases   = ["All"] + sorted(football_df["phase"].unique().tolist())
all_injuries = ["All"] + sorted(football_df["injury_status"].unique().tolist())
all_seasons = ["All"] + sorted(football_df["season"].astype(str).unique().tolist())


sel_season = st.sidebar.selectbox("📅 Select Season", all_seasons)
sel_club   = st.sidebar.selectbox("🏟️ Select Club",  all_clubs)
sel_comp       = st.sidebar.selectbox("🏆 Select Competition",  all_competitions) 
sel_phase  = st.sidebar.selectbox("📈 Select Career Phase",  all_phases)
sel_injury = st.sidebar.selectbox("🏥 Select Injury Status", all_injuries)


filtered = football_df.copy()
if sel_club   != "All": filtered = filtered[filtered["club"]          == sel_club]
if sel_season != "All":
    filtered = filtered[filtered["season"].astype(str) == sel_season]
if sel_comp   != "All": filtered = filtered[filtered["competition"]   == sel_comp]  
if sel_phase  != "All": filtered = filtered[filtered["phase"]         == sel_phase]
if sel_injury != "All": filtered = filtered[filtered["injury_status"] == sel_injury]

st.sidebar.divider()
st.sidebar.write(f"📋 Showing **{len(filtered)}** rows out of {len(football_df)}")

# ════════════════════════════════════════════════════════════
# SECTION 1 — STORY OVERVIEW
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
c1.metric("⚽ Total Goals",      int(filtered["goals"].sum()))
c2.metric("🎯 Total Assists",    int(filtered["assists"].sum()))
c3.metric("🏆 Trophies Won",     int(filtered["trophies_won"].sum()))
c4.metric("⭐ Avg Match Rating", f"{filtered['match_rating'].mean():.2f}" if not filtered.empty else "—")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 2 — CAREER SUCCESS YEARS ANALYSIS
# ════════════════════════════════════════════════════════════
st.header("🌟 Career Success Years Analysis")

season_performance = football_df.groupby('season').agg(
    goals=('goals','sum'), assists=('assists','sum'),
    match_rating=('match_rating','mean'),
    trophies_won=('trophies_won','sum'),
    contribution=('contribution','sum')
).reset_index()
season_performance['season'] = season_performance['season'].astype(int).astype(str)
mg = max(season_performance['goals'].max(), 1)
ma = max(season_performance['assists'].max(), 1)
mt = max(season_performance['trophies_won'].max(), 1)

season_performance['success_score'] = (
    (season_performance['goals']        / mg * 0.30) +
    (season_performance['assists']      / ma * 0.20) +
    (season_performance['match_rating'] / 10 * 0.30) +
    (season_performance['trophies_won'] / mt * 0.20)
) * 100

threshold  = season_performance['success_score'].quantile(0.70)
peak_years = season_performance[season_performance['success_score'] >= threshold]['season'].tolist()
bar_cols_s = ['#C0392B' if sc >= threshold else 'steelblue'
              for sc in season_performance['success_score']]

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Success Score Over Time")
    fig_s, ax_s = plt.subplots(figsize=(12, 5))
    ax_s.bar(season_performance['season'], season_performance['success_score'],
             color=bar_cols_s, edgecolor='black', linewidth=0.8, alpha=0.85)
    ax_s.axhline(y=threshold, color='darkred', linestyle='--', linewidth=2,
                 label=f'Peak Threshold ({threshold:.1f})', alpha=0.8)
    ax_s.set_xlabel("Season", fontsize=12, fontweight='bold')
    ax_s.set_ylabel("Success Score", fontsize=12, fontweight='bold')
    ax_s.set_title("Career Success Score by Season (Composite Metric)",
                   fontsize=14, fontweight='bold', pad=20)
    ax_s.legend(fontsize=10)
    ax_s.grid(True, axis='y', linestyle='--', alpha=0.35)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_s)
    plt.close(fig_s)

with col2:
    st.subheader("Peak Career Years")
    st.markdown(f"""
**🔥 Peak Career Years:**
{', '.join(map(str, peak_years))}

**📊 How the score is calculated:**
- 30% Goals
- 20% Assists
- 30% Match Rating
- 20% Trophies Won

**🎯 Threshold:** Top 30% of all seasons

🔴 **Red bars** = peak seasons

🔵 **Blue bars** = regular seasons
    """)

st.caption("📌 The success score combines goals, assists, match rating, and trophies into one number to find the best career years. Red bars are the top 30% of all seasons.")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 3 — DATA VISUALIZATIONS
# ════════════════════════════════════════════════════════════
st.header("📊 Data Visualizations")
# ── Chart 1: Goals Over Seasons ── 
st.subheader("1. Goals Over Seasons")
season_goals = filtered.sort_values("season").groupby("season")["goals"].sum()
season_goals.index = season_goals.index.astype(int)

season_labels = season_goals.index.astype(str)

if season_goals.empty:
    st.warning("⚠️ No data. Please adjust the filters.")
else:
    fig1, ax1 = plt.subplots(figsize=(12, 4))

    ax1.plot(
        season_labels,
        season_goals.values,
        marker='o',
        linewidth=2.5,
        color='steelblue',
        markersize=8
    )

    for x, y in zip(season_labels, season_goals.values):
        ax1.annotate(
            str(int(y)),
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha='center',
            fontsize=8,
            fontweight='bold'
        )

    ax1.set_title("Total Goals Over Seasons", fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel("Season", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Goals", fontsize=12, fontweight='bold')
    ax1.set_ylim(bottom=0)
    ax1.grid(True, linestyle='--', alpha=0.45)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)

st.caption("📌 A line chart was used to visualize performance trends across seasons. The chart highlights periods of growth, peak performance, and decline throughout the player’s career.")
st.markdown("---")

# ── Chart 2: Average Match Rating by Competition 
st.subheader("2. Average Match Rating by Competition")

comp_rating = filtered.groupby("competition")["match_rating"].mean().sort_values()

if comp_rating.empty:
    st.warning("⚠️ No data. Please adjust the filters.")
else:
    n     = len(comp_rating)
    third = max(n // 3, 1)
    my_colors = (
        ['#e07a5f'] * third +
        ['#f4f1de'] * third +
        ['#3d5a80'] * (n - 2 * third)
    )

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bars2 = ax2.barh(comp_rating.index, comp_rating.values,
                     color=my_colors, edgecolor='none')
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 0.03, bar.get_y() + bar.get_height()/2,
                 f'{w:.2f}', va='center', fontsize=9, fontweight='bold')
    ax2.set_title("Average Match Rating by Competition",
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel("Average Match Rating", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Competition", fontsize=12, fontweight='bold')
    ax2.axvline(x=7.5, color='red', linestyle='--', linewidth=1.5,
                alpha=0.7, label='7.5 reference line')
    ax2.set_xlim(6.5, comp_rating.max() + 0.5)
    ax2.legend(fontsize=9)
    ax2.grid(True, axis='x', linestyle='--', alpha=0.45)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

st.caption("📌 This horizontal bar chart compares average performance across different competitions. The color gradient represents rating strength (red = lower ratings, blue = higher ratings).")
st.markdown("---")

col_left, col_right = st.columns(2)

# ── Chart 3: Goals vs Assists with Trend Line ──
with col_left:
    st.subheader("3. Goals vs Assists Relationship")
    if filtered.empty:
        st.warning("⚠️ No data. Please adjust the filters.")
    else:
        fig3, ax3 = plt.subplots(figsize=(6, 5))
        x = filtered["goals"].values
        y = filtered["assists"].values
        ax3.scatter(x, y, s=120, alpha=0.7,
                    edgecolors='black', linewidth=0.8,
                    color='steelblue', zorder=3)
        if len(x) > 1:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_line = np.linspace(x.min(), x.max(), 100)
            ax3.plot(x_line, p(x_line), color='red', linewidth=2,
                     label='Trend line', zorder=2)
            ax3.legend(fontsize=9)
        ax3.set_title("Goals vs Assists Relationship\nwith Trend Line",
                      fontsize=13, fontweight='bold', pad=15)
        ax3.set_xlabel("Goals", fontsize=11, fontweight='bold')
        ax3.set_ylabel("Assists", fontsize=11, fontweight='bold')
        ax3.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
    st.caption("📌  Scatter plot shows relationship between goals and assists. The red trend line shows the direction — higher goal seasons tend to also have more assists. Risk: the relationship is a pattern, not a proven cause.")

# ── Chart 4: Trophies Won by Club ── 
with col_right:
    st.subheader("4. Trophies Won by Club")
    club_trophies = filtered.groupby("club")["trophies_won"].sum().sort_values(ascending=False)
    if club_trophies.empty:
        st.warning("⚠️ No data. Please adjust the filters.")
    else:
        fig4, ax4 = plt.subplots(figsize=(6, 5))
        ax4.bar(club_trophies.index, club_trophies.values,
                color='mediumpurple', edgecolor='white', linewidth=0.8)
        for i, v in enumerate(club_trophies.values):
            ax4.text(i, v + 0.15, str(int(v)),
                     ha='center', fontweight='bold', fontsize=11)
        ax4.set_title("Trophies Won by Club", fontsize=13, fontweight='bold', pad=15)
        ax4.set_xlabel("Club", fontsize=11, fontweight='bold')
        ax4.set_ylabel("Trophies Won", fontsize=11, fontweight='bold')
        ax4.grid(True, axis='y', linestyle='--', alpha=0.5)
        ax4.set_ylim(bottom=0)
        plt.yticks(range(0, int(club_trophies.max()) + 3, 2))
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)
    st.caption("📌 Bar charts are the simplest way to compare whole numbers across clubs. Risk: PSG's trophy count can look inflated because Ligue 1 is a weaker league than La Liga or the Champions League.")

st.markdown("---")

# ── Chart 5: Injury Impact on Match Rating ── 
st.subheader("5. Injury Impact on Match Rating")

injury_order = ["Healthy", "Minor Injury", "Recovering", "Major Injury"]
avail        = [x for x in injury_order if x in football_df["injury_status"].values]
inj_rating   = football_df.groupby("injury_status")["match_rating"].mean().reindex(avail)
inj_colors5  = ["green", "orange", "steelblue", "red"][:len(avail)]

if inj_rating.empty:
    st.warning("⚠️ No data. Please adjust the filters.")
else:
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    bars5 = ax5.bar(inj_rating.index, inj_rating.values,
                    color=inj_colors5, edgecolor='black', linewidth=0.8, width=0.5)
    for bar in bars5:
        ax5.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.05,
                 f"{bar.get_height():.2f}",
                 ha='center', fontweight='bold', fontsize=11)
    ax5.set_title("Impact of Injury on Match Rating",
                  fontsize=14, fontweight='bold', pad=20)
    ax5.set_xlabel("Injury Status", fontsize=12, fontweight='bold')
    ax5.set_ylabel("Average Match Rating", fontsize=12, fontweight='bold')
    ax5.set_ylim(6.0, 9.5)
    ax5.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

healthy_avg = football_df[football_df["injury_status"] == "Healthy"]["match_rating"].mean()
injury_avg  = football_df[football_df["injury_status"] == "Major Injury"]["match_rating"].mean()
st.caption(f"📌 Bars directly compare average ratings across health categories. Clear finding: Healthy seasons average **{healthy_avg:.2f}** vs **{injury_avg:.2f}** when seriously injured — a **{abs(healthy_avg - injury_avg):.2f} point drop**. Risk: 'Recovering' label is subjective.")
st.markdown("---")

# ── Chart 6: Goals Heatmap — Club × Season ── 
st.subheader("6. Performance Heatmap: Goals by Season and Club")

heatmap_data = filtered.pivot_table(
    values='goals', index='club', columns='season',
    aggfunc='sum', fill_value=0
)

if heatmap_data.empty:
    st.warning("⚠️ Not enough data for this heatmap. Please adjust the filters.")
else:
    data6  = heatmap_data.values.astype(float)
    clubs6 = heatmap_data.index.tolist()
    szns6  = [str(int(c)) for c in heatmap_data.columns.tolist()]

    fig6, ax6 = plt.subplots(figsize=(14, max(4, len(clubs6) * 1.1)))
    im6 = ax6.imshow(data6, cmap='YlOrRd', aspect='auto', vmin=0)
    cbar6 = plt.colorbar(im6, ax=ax6)
    cbar6.set_label('Goals Scored', fontsize=10)

    ax6.set_xticks(range(len(szns6)))
    ax6.set_xticklabels(szns6, rotation=45, ha='right', fontsize=9)
    ax6.set_yticks(range(len(clubs6)))
    ax6.set_yticklabels(clubs6, fontsize=11)
    ax6.set_xlabel("Season", fontsize=12, fontweight='bold')
    ax6.set_ylabel("Club", fontsize=12, fontweight='bold')
    ax6.set_title("Goals Scored by Club and Season",
                  fontsize=14, fontweight='bold', pad=20)

    for x in range(len(szns6) + 1):
        ax6.axvline(x - 0.5, color='white', linewidth=0.8)
    for y in range(len(clubs6) + 1):
        ax6.axhline(y - 0.5, color='white', linewidth=0.8)

    for r in range(data6.shape[0]):
        for c in range(data6.shape[1]):
            val     = int(data6[r, c])
            txt_col = 'white' if data6[r, c] > data6.max() * 0.55 else 'black'
            ax6.text(c, r, str(val), ha='center', va='center',
                     fontsize=10, fontweight='bold', color=txt_col)

    plt.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

st.caption("📌 heatmap shows two categories — club and season — at the same time using colour. Darker red = more goals. You can instantly see which club-year combinations were the strongest. Risk: a zero cell could mean no games played OR zero goals — both look the same.")
st.markdown("---")

# ── Chart 7: Match Rating Heatmap — Phase × Competition  ──
st.subheader("7. Match Rating Heatmap: Career Phase vs Competition")

heatmap_rating = filtered.pivot_table(
    values='match_rating', index='phase', columns='competition',
    aggfunc='mean'
)

if heatmap_rating.empty:
    st.info("ℹ️ Not enough data for this heatmap with the current filters.")
else:
    data7   = heatmap_rating.values
    phases7 = heatmap_rating.index.tolist()
    comps7  = heatmap_rating.columns.tolist()

    fig7, ax7 = plt.subplots(figsize=(16, max(5, len(phases7) * 1.1)))
    cmap7 = plt.cm.coolwarm
    cmap7.set_bad(color='#F0F0F0')
    im7 = ax7.imshow(np.ma.masked_invalid(data7), cmap=cmap7,
                     aspect='auto', vmin=6.5, vmax=9.0)
    cbar7 = plt.colorbar(im7, ax=ax7)
    cbar7.set_label('Avg Match Rating', fontsize=10)

    ax7.set_xticks(range(len(comps7)))
    ax7.set_xticklabels(comps7, rotation=45, ha='right', fontsize=9)
    ax7.set_yticks(range(len(phases7)))
    ax7.set_yticklabels(phases7, fontsize=11)
    ax7.set_xlabel("Competition", fontsize=12, fontweight='bold')
    ax7.set_ylabel("Career Phase", fontsize=12, fontweight='bold')
    ax7.set_title(
        "Average Match Rating by Career Phase and Competition\n"
        "(Blue = lower rating · Red = higher rating · Grey = no data)",
        fontsize=13, fontweight='bold', pad=20
    )

    for x in range(len(comps7) + 1):
        ax7.axvline(x - 0.5, color='gray', linewidth=0.5, alpha=0.5)
    for y in range(len(phases7) + 1):
        ax7.axhline(y - 0.5, color='gray', linewidth=0.5, alpha=0.5)

    for r in range(data7.shape[0]):
        for c in range(data7.shape[1]):
            val = data7[r, c]
            if not np.isnan(val):
                norm_val = (val - 6.5) / (9.0 - 6.5)
                bg  = cmap7(norm_val)
                lum = 0.299*bg[0] + 0.587*bg[1] + 0.114*bg[2]
                txt_col = 'white' if lum < 0.5 else 'black'
                ax7.text(c, r, f'{val:.2f}', ha='center', va='center',
                         fontsize=9, fontweight='bold', color=txt_col)

    plt.tight_layout()
    st.pyplot(fig7)
    plt.close(fig7)

st.caption("📌  This chart shows two categories at once — career phase and competition — to find which combinations produced the best performance. MSN Peak + Champions League stands out clearly. Grey cells mean no data for that combination.")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 4 — KEY INSIGHTS
# ════════════════════════════════════════════════════════════
st.header("🔍 Key Insights")

best_row = filtered.loc[filtered["goals"].idxmax()] if not filtered.empty else None

if best_row is not None:
    st.success(f"🔥 **Best scoring period:** {int(best_row['season'])} — {best_row['competition']} at {best_row['club']} with **{int(best_row['goals'])} goals**")

st.info(f"🏥 Healthy seasons average **{healthy_avg:.2f}** rating vs **{injury_avg:.2f}** during major injuries — a **{abs(healthy_avg - injury_avg):.2f} point drop**. Injury is the biggest single factor found in this dataset.")
st.info(f"👑 Peak career years ({', '.join(map(str, peak_years))}) produced the highest combined goals, assists, ratings, and trophies.")
st.info("📈 Career growth from 2009 to 2015 is steep and consistent — goals and ratings improved every healthy season.")
st.info("🔄 The 2025 Santos return shows early signs of recovery — ratings above 7.5 and injury status is improving.")
st.info("🏆 The Barcelona era (2013–2016) produced the highest match ratings and the most trophies in the dataset.")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 5 — DECISION-MAKING
# ════════════════════════════════════════════════════════════
st.header("🎯 Decision-Making")

st.markdown(f"""
**Based on my data, what should this player do differently in the future?**

**1. 🏥 Prioritise injury prevention above everything else.**
The data is clear: healthy seasons rate **{healthy_avg:.2f}** vs **{injury_avg:.2f}** when seriously injured.
That {abs(healthy_avg - injury_avg):.2f} point drop means fewer goals, fewer trophies, and lower performance overall.
Staying fit matters more than any transfer.

**2. ⏱️ Consistent playing time builds peak performance.**
The success score shows that the best seasons all had the most appearances.
Playing regularly — even at a smaller club — is better than sitting on the bench at a bigger one.

**3. 🏟️ Choose clubs that match the current career stage.**
The heatmap shows clear patterns — best ratings during Barcelona years.
Decline at PSG and Al-Hilal may reflect an environment mismatch, not only injuries.

**4. 🔄 The 2025 Santos return is the right decision based on data.**
A familiar environment with guaranteed game time matches the formula from the best Santos years.
Early 2025 data shows ratings above 7.5 and improving injury status — confirming the strategy.

**5. 🎯 Be selective with competitions to protect fitness.**
The rating heatmap shows which competitions produced the best performances.
Resting during lower-priority matches could protect fitness for the most important games.

⚠️ **Important limitations:**
- These are observations from 50 rows of data — not definitive proof
- Team quality, coaching style, and personal factors are not captured
- Correlation does not mean causation
- Small dataset limits statistical confidence
""")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 6 — ETHICS & RESPONSIBILITY
# ════════════════════════════════════════════════════════════
st.header("⚖️ Ethics & Responsibility")

with st.expander("🔒 Privacy Statement"):
    st.markdown("""
**What data is included?**
- Publicly available football statistics (goals, assists, appearances, match ratings, trophies)
- Competition and club performance information
- General injury status categories (Healthy / Minor Injury / Recovering / Major Injury)

**What is anonymized?**
- The athlete is **not named** anywhere in this dashboard
- No private, medical, financial, or contract information is included
- No personally identifiable information (PII) is used
- Created for DATA201 educational purposes only

**Ethical data use:**
- The analysis focuses on football performance trends, not personal life
- Some variables include subjective interpretation (e.g. career phase labels)
- Findings are exploratory and should not be treated as official statistics
    """)

with st.expander("⚠️ Bias & Limitation Disclosure"):
    st.markdown("""
This dataset explores football career performance trends using publicly available statistics.
Several limitations apply:

1. **Aggregation Bias** — Season totals combine competitions of very different difficulty
2. **Selection Bias** — International matches (World Cup, Copa América) are not included
3. **Temporal Bias** — Recent seasons may be remembered more clearly than older ones
4. **Labelling Bias** — Phase names like "MSN Peak" reflect personal interpretation
5. **Small Dataset** — 50 rows is enough for trends but not for statistical proof
6. **Missing Variables** — Team quality, coaching style, and motivation are not captured
7. **Confirmation Bias** — Personal admiration for this player may affect how results are framed

All findings should be read as **exploratory observations**, not proven conclusions.
    """)

with st.expander("📊 Visualization Justification"):
    st.markdown("""
| Chart | Type | Why This Type? | Risk |
|---|---|---|---|
| Goals Over Seasons | Line Chart | Best for trends over time | Dips may reflect injury, not poor form |
| Rating by Competition | Horizontal Bar | Readable with long category names | Averages hide match count differences |
| Goals vs Assists | Scatter + Trend Line | Shows relationship between two variables | Correlation ≠ causation |
| Trophies by Club | Vertical Bar | Clear count comparison | PSG count may be inflated by weaker league |
| Injury Impact | Bar Chart | Direct comparison across health categories | 'Recovering' label is subjective |
| Goals Heatmap | Heatmap | Shows club and season at the same time | Zeros = no games OR zero goals — look identical |
| Rating Heatmap | Heatmap | Phase × competition performance map | Averages hide variance; grey = missing data |
| Success Score | Bar + Threshold | Objective peak year identification | Score weights are subjectively chosen |
    """)

with st.expander("🎯 Responsible Decision Statement"):
    st.markdown("""
**What the data CAN support:**
- Injury prevention links to better performance (strong, consistent pattern)
- More playing time links to higher output (clear trend)
- Familiar environments show more consistent ratings (observable pattern)

**What the data CANNOT prove:**
- Causation (correlation ≠ causation)
- Future performance (past ≠ future guarantee)
- Optimal career decisions (too many unmeasured factors)

**Limitations acknowledged:**
- 50-row dataset — results are exploratory, not conclusive
- Team quality, tactics, and personal factors are not captured
- Success score weights are one approach among many
- Personal admiration may create confirmation bias in interpretation

All decisions in this dashboard are **data-supported observations**, not professional advice.
    """)

st.divider()
st.caption("📊 Dashboard by Ngai Yaw · DATA201 Final Project · May 2026 · Player identity anonymized")
st.caption("Data: Wikipedia, FotMob, Transfermarkt (publicly available) · For academic purposes only")
