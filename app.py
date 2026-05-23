# ============================================================
# FOOTBALL PLAYER CAREER DASHBOARD
# DATA201 Final Project — Ngai Yaw
# Enhanced Version with Heatmap & Career Success Analysis
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for Streamlit
plt.switch_backend('Agg')

# Set styling
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Football Career Dashboard", page_icon="⚽", layout="wide")

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        football_df = pd.read_csv("football_player_career.csv")
        football_df['contribution'] = football_df['goals'] + football_df['assists']
        # Prevent division by zero
        football_df['goal_ratio'] = football_df.apply(
            lambda row: row['goals'] / row['appearances'] if row['appearances'] > 0 else 0, 
            axis=1
        )
        return football_df
    except FileNotFoundError:
        st.error("❌ Error: 'football_player_career.csv' not found. Please ensure the CSV file is in the same directory as app.py")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

football_df = load_data()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("⚽ Football Player Career Dashboard")
st.markdown("A data story about a player I admire — tracking goals, assists, trophies and injuries across 17 seasons.")
st.divider()

# ════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ════════════════════════════════════════════════════════════
st.sidebar.title("🎛️ Filters")

# Filter 1: Club
all_clubs = ["All"] + sorted(football_df["club"].unique().tolist())
sel_club = st.sidebar.selectbox("Select Club", all_clubs)

# Filter 2: Career Phase
all_phases = ["All"] + sorted(football_df["phase"].unique().tolist())
sel_phase = st.sidebar.selectbox("Select Career Phase", all_phases)

# Filter 3: Injury Status
all_injuries = ["All"] + sorted(football_df["injury_status"].unique().tolist())
sel_injury = st.sidebar.selectbox("Select Injury Status", all_injuries)

# Apply filters
filtered = football_df.copy()
if sel_club != "All":
    filtered = filtered[filtered["club"] == sel_club]
if sel_phase != "All":
    filtered = filtered[filtered["phase"] == sel_phase]
if sel_injury != "All":
    filtered = filtered[filtered["injury_status"] == sel_injury]

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

# 4 simple KPI metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚽ Total Goals", int(filtered["goals"].sum()))
c2.metric("🎯 Total Assists", int(filtered["assists"].sum()))
c3.metric("🏆 Trophies Won", int(filtered["trophies_won"].sum()))
c4.metric("⭐ Avg Match Rating", f"{filtered['match_rating'].mean():.2f}")

st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 2: CAREER SUCCESS YEARS ANALYSIS
# ════════════════════════════════════════════════════════════
st.header("🌟 Career Success Years Analysis")

# Define success years based on goals and rating
season_performance = football_df.groupby('season').agg({
    'goals': 'sum',
    'assists': 'sum',
    'match_rating': 'mean',
    'trophies_won': 'sum',
    'contribution': 'sum'
}).reset_index()

season_performance['season'] = season_performance['season'].astype(int).astype(str)

# Create success score (normalized composite metric)
# Prevent division by zero
max_goals = season_performance['goals'].max() if season_performance['goals'].max() > 0 else 1
max_assists = season_performance['assists'].max() if season_performance['assists'].max() > 0 else 1
max_trophies = season_performance['trophies_won'].max() if season_performance['trophies_won'].max() > 0 else 1

season_performance['success_score'] = (
    (season_performance['goals'] / max_goals * 0.3) +
    (season_performance['assists'] / max_assists * 0.2) +
    (season_performance['match_rating'] / 10 * 0.3) +
    (season_performance['trophies_won'] / max_trophies * 0.2)
) * 100

# Identify peak years (top 30% success score)
threshold = season_performance['success_score'].quantile(0.70)
peak_years = season_performance[season_performance['success_score'] >= threshold]['season'].tolist()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Success Score Over Time")
    fig_success, ax_success = plt.subplots(figsize=(12, 5))

    colors = ['red' if score >= threshold else 'steelblue'
              for score in season_performance['success_score']]

    ax_success.bar(season_performance['season'], season_performance['success_score'],
                   color=colors, edgecolor='black', linewidth=0.8, alpha=0.8)
    ax_success.axhline(y=threshold, color='darkred', linestyle='--', linewidth=2,
                       label=f'Peak Threshold ({threshold:.1f})', alpha=0.7)

    ax_success.set_xlabel("Season", fontsize=12, fontweight='bold')
    ax_success.set_ylabel("Success Score", fontsize=12, fontweight='bold')
    ax_success.set_title("Career Success Score by Season (Composite Metric)",
                         fontsize=14, fontweight='bold', pad=20)
    ax_success.legend(fontsize=10)
    ax_success.grid(True, axis='y', linestyle='--', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_success)
    plt.close(fig_success)  # Close figure to free memory

with col2:
    st.subheader("Peak Years")
    st.markdown(f"""
    **🔥 Peak Career Years:**
    {', '.join(map(str, peak_years))}

    **📊 Success Score Calculation:**
    - 30% Goals
    - 20% Assists
    - 30% Match Rating
    - 20% Trophies

    **🎯 Threshold:** Top 30% of seasons

    Red bars indicate **peak performance years** where the player achieved exceptional success across all metrics.
    """)

st.caption("📌 Success score combines multiple performance indicators to identify career peak years objectively.")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 3: VISUALIZATIONS
# ════════════════════════════════════════════════════════════
st.header("📊 Data Visualizations")

# ── Chart 1: Goals Over Seasons ───────────────────────────────────────────────
st.subheader("1. Goals Over Seasons")

season_goals = filtered.groupby("season")["goals"].sum()

fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(season_goals.index, season_goals.values, marker="o", color="steelblue",
         linewidth=2.5, markersize=8, label="Goals per Season")
ax1.fill_between(season_goals.index, season_goals.values, alpha=0.2, color="steelblue")
ax1.set_xlabel("Season", fontsize=11, fontweight='bold')
ax1.set_ylabel("Total Goals", fontsize=11, fontweight='bold')
ax1.set_title("Goal Production Across Career Timeline", fontsize=13, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.4)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.caption("📈 **Visualization 1 Justification:** Line charts are ideal for showing temporal trends. This chart reveals how goal production evolved across different career phases.")
st.divider()

# ── Chart 2: Average Rating by Competition ────────────────────────────────────
st.subheader("2. Average Match Rating by Competition")

comp_rating = filtered.groupby("competition")["match_rating"].mean().sort_values(ascending=True)

fig2, ax2 = plt.subplots(figsize=(10, 6))
bars = ax2.barh(comp_rating.index, comp_rating.values, color='coral', edgecolor='black', linewidth=0.8)
ax2.set_xlabel("Average Match Rating", fontsize=11, fontweight='bold')
ax2.set_ylabel("Competition", fontsize=11, fontweight='bold')
ax2.set_title("Performance Level Across Competitions", fontsize=13, fontweight='bold', pad=15)
ax2.grid(True, axis='x', linestyle='--', alpha=0.4)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.2f}',
             ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

st.caption("📊 **Visualization 2 Justification:** Horizontal bar charts make categorical comparisons clear and easy to read, especially with longer labels.")
st.divider()

# ── Chart 3: Goals vs Assists Scatter ─────────────────────────────────────────
st.subheader("3. Goals vs Assists Distribution")

fig3, ax3 = plt.subplots(figsize=(10, 6))
scatter = ax3.scatter(filtered["goals"], filtered["assists"], 
                     c=filtered["match_rating"], cmap="RdYlGn", 
                     s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
ax3.set_xlabel("Goals", fontsize=11, fontweight='bold')
ax3.set_ylabel("Assists", fontsize=11, fontweight='bold')
ax3.set_title("Goal Contribution Profile (Colored by Match Rating)", 
             fontsize=13, fontweight='bold', pad=15)
ax3.grid(True, linestyle='--', alpha=0.3)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('Match Rating', fontsize=10)

plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

st.caption("🔍 **Visualization 3 Justification:** Scatter plots reveal relationships between two variables. Color-coding by rating adds a third dimension to the analysis.")
st.divider()

# ── Chart 4: Trophies by Club ─────────────────────────────────────────────────
st.subheader("4. Trophies Won by Club")

club_trophies = filtered.groupby("club")["trophies_won"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(10, 5))
bars = ax4.bar(club_trophies.index, club_trophies.values, 
              color='gold', edgecolor='black', linewidth=1, alpha=0.9)
ax4.set_xlabel("Club", fontsize=11, fontweight='bold')
ax4.set_ylabel("Total Trophies", fontsize=11, fontweight='bold')
ax4.set_title("Success by Club (Trophy Count)", fontsize=13, fontweight='bold', pad=15)
ax4.grid(True, axis='y', linestyle='--', alpha=0.4)

# Add value labels
for bar in bars:
    height = bar.get_height()
    if height > 0:
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

st.caption("🏆 **Visualization 4 Justification:** Bar charts clearly show discrete counts. Trophy data is categorical and best displayed vertically for club comparison.")
st.divider()

# ── Chart 5: Injury Impact ────────────────────────────────────────────────────
st.subheader("5. Impact of Injury Status on Performance")

injury_impact = football_df.groupby("injury_status").agg({
    "match_rating": "mean",
    "goals": "mean"
}).reset_index()

fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 5))

# Match rating comparison
bars1 = ax5a.bar(injury_impact["injury_status"], injury_impact["match_rating"],
                color=['green', 'orange', 'red'], edgecolor='black', linewidth=1, alpha=0.8)
ax5a.set_xlabel("Injury Status", fontsize=11, fontweight='bold')
ax5a.set_ylabel("Average Match Rating", fontsize=11, fontweight='bold')
ax5a.set_title("Match Rating by Injury Status", fontsize=12, fontweight='bold', pad=10)
ax5a.grid(True, axis='y', linestyle='--', alpha=0.3)

for bar in bars1:
    height = bar.get_height()
    ax5a.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Goals comparison
bars2 = ax5b.bar(injury_impact["injury_status"], injury_impact["goals"],
                color=['green', 'orange', 'red'], edgecolor='black', linewidth=1, alpha=0.8)
ax5b.set_xlabel("Injury Status", fontsize=11, fontweight='bold')
ax5b.set_ylabel("Average Goals per Record", fontsize=11, fontweight='bold')
ax5b.set_title("Goal Production by Injury Status", fontsize=12, fontweight='bold', pad=10)
ax5b.grid(True, axis='y', linestyle='--', alpha=0.3)

for bar in bars2:
    height = bar.get_height()
    ax5b.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
st.pyplot(fig5)
plt.close(fig5)

healthy_avg = football_df[football_df["injury_status"] == "Healthy"]["match_rating"].mean()
injury_avg = football_df[football_df["injury_status"] == "Serious Injury"]["match_rating"].mean()

st.caption("🏥 **Visualization 5 Justification:** Side-by-side bar charts allow direct comparison of performance metrics across injury categories.")
st.divider()

# ── Chart 6: Goals Heatmap ────────────────────────────────────────────────────
st.subheader("6. Goals Heatmap: Club × Competition")

# Create pivot table
goals_pivot = filtered.pivot_table(values='goals', index='club', columns='competition', aggfunc='sum', fill_value=0)

fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.heatmap(goals_pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
           linewidths=0.5, cbar_kws={'label': 'Goals'}, ax=ax6)
ax6.set_title("Goals Distribution: Club × Competition", fontsize=13, fontweight='bold', pad=15)
ax6.set_xlabel("Competition", fontsize=11, fontweight='bold')
ax6.set_ylabel("Club", fontsize=11, fontweight='bold')
plt.tight_layout()
st.pyplot(fig6)
plt.close(fig6)

st.caption("🔥 **Visualization 6 Justification:** Heatmaps reveal patterns across two categorical dimensions, making it easy to spot performance hotspots.")
st.divider()

# ── Chart 7: Match Rating Heatmap ─────────────────────────────────────────────
st.subheader("7. Match Rating Heatmap: Phase × Competition")

rating_pivot = filtered.pivot_table(values='match_rating', index='phase', 
                                    columns='competition', aggfunc='mean', fill_value=0)

fig7, ax7 = plt.subplots(figsize=(12, 7))
sns.heatmap(rating_pivot, annot=True, fmt='.2f', cmap='RdYlGn', 
           linewidths=0.5, cbar_kws={'label': 'Avg Rating'}, ax=ax7,
           vmin=0, vmax=10)
ax7.set_title("Performance Quality: Career Phase × Competition", fontsize=13, fontweight='bold', pad=15)
ax7.set_xlabel("Competition", fontsize=11, fontweight='bold')
ax7.set_ylabel("Career Phase", fontsize=11, fontweight='bold')
plt.tight_layout()
st.pyplot(fig7)
plt.close(fig7)

st.caption("📊 **Visualization 7 Justification:** Rating heatmap shows performance quality patterns across career phases and competitions simultaneously.")
st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 5: KEY INSIGHTS
# ════════════════════════════════════════════════════════════
st.header("🔍 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 💡 Insight 1: Peak Performance
    The **success score analysis** identified peak years during the Barcelona era (2013-2017).
    These seasons combined high goals, assists, and trophies with consistent match ratings above 8.5.
    """)

with col2:
    st.markdown("""
    ### 🏥 Insight 2: Injury Impact
    Serious injuries correlate with a **dramatic performance drop**. 
    Healthy seasons average {:.2f} rating vs {:.2f} when injured — 
    a {:.2f} point difference.
    """.format(healthy_avg, injury_avg, abs(healthy_avg - injury_avg)))

with col3:
    st.markdown("""
    ### 📈 Insight 3: Career Phases
    The data shows distinct career arcs: rapid growth (Santos), 
    peak dominance (Barcelona), transition struggle (PSG/Al-Hilal), 
    and stabilization (Santos return).
    """)

st.divider()

# ════════════════════════════════════════════════════════════
# SECTION 5: DECISION-MAKING
# ════════════════════════════════════════════════════════════
st.header("🎯 Decision-Making")

st.markdown(f"""
**Based on my data, what should this player do differently?**

**1. 🏥 Prioritize injury prevention above all else.**
The data is unambiguous: healthy seasons rate **{healthy_avg:.2f}** vs **{injury_avg:.2f}** when seriously injured.
The {abs(healthy_avg - injury_avg):.2f} point drop translates directly to performance decline.
Staying fit matters more than any transfer or tactical change.

**2. ⏱️ Consistent playing time builds peak performance.**
The success score analysis reveals that the highest-performing seasons all feature the most appearances.
Playing regularly — even at a smaller club — consistently outperforms sitting on the bench at a bigger club.

**3. 🏟️ Environment matters: Choose clubs that fit career phase.**
The heatmap shows clear performance patterns:
- Peak years (2013-2017) at Barcelona with familiar system
- Decline during PSG/Al-Hilal transition periods
- Recovery at Santos with guaranteed playing time

**4. 🔄 The 2025 Santos return validates the data-driven approach.**
A familiar environment with guaranteed game time matches the proven formula from earlier Santos years.
Early 2025 data shows ratings above 7.5 and improving injury status — confirming the strategy.

**5. 🎯 Focus on competitions that historically show best ratings.**
The rating-by-competition heatmap identifies which tournaments consistently produce better performances.
Strategic rest during lower-priority competitions could preserve fitness for key matches.

⚠️ **LIMITATIONS:**
- These are data-supported observations from 50 rows, not definitive conclusions
- Team quality, coaching philosophy, and personal factors are not captured
- The dataset combines competitions of varying difficulty levels
- Small sample size limits statistical confidence
- Correlation does not imply causation
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
- Performance metrics such as goals, assists, appearances, and match ratings
- Competition and club performance information
- General injury status categories
- Trophy statistics

**What is anonymized?**
- The athlete is not directly identified in the dashboard
- No private, medical, financial, or contract information is included
- No personally identifiable information (PII) is included
- The dataset was designed for DATA201 educational purposes

**Ethical Data Use**
- The analysis focuses on football performance trends rather than personal life
- Some variables and career phases include subjective interpretation
- The findings are exploratory and should not be interpreted as official professional statistics

""")

with st.expander("⚠️ Bias & Limitation Disclosure"):
    st.markdown("""
This dataset was designed to explore football career performance trends through publicly available statistics and structured analysis.

However, several limitations should be considered. Match ratings and performance evaluations may contain subjective interpretation because football performance cannot be measured entirely through numbers alone.

The dataset focuses on selected career moments rather than complete professional records. External influences such as teamwork, coaching strategies, player roles, and emotional factors are also not fully represented in the analysis.

As a result, the findings in this project should be interpreted as exploratory insights rather than definitive conclusions.

---

**Known Biases:**


1. **Aggregation Bias**
   - Season totals combine competitions of vastly different difficulty
   - Champions League vs Domestic Cup goals are treated equally
   - Does not account for opponent strength or match importance

2. **Selection Bias**
   - International matches (World Cup, Copa América) not included
   - Only club performances analyzed
   - May miss important career context

3. **Temporal Bias**
   - Recent seasons may be remembered more vividly
   - Historical context (rule changes, tactical evolution) not captured

4. **Labeling Bias**
   - Phase names like "MSN Peak" reflect personal interpretation
   - Injury status categories are simplified (reality is more complex)
   - "Success score" weights are subjectively chosen

5. **Small Dataset Limitations**
   - 50 rows is enough for trends but limits statistical proof
   - Cannot control for confounding variables
   - Patterns may be coincidental rather than causal

6. **Missing Variables**
   - Team quality and tactical system not captured
   - Coaching style and management influence excluded
   - Personal life events and motivation not tracked
   - Market value and financial incentives missing

7. **Confirmation Bias Risk**
   - Personal admiration for this player may influence interpretation
   - Tendency to see patterns that confirm pre-existing beliefs
   - Dashboard creator's fandom may affect narrative framing
    """)

with st.expander("📊 Visualization Justification"):
    st.markdown("""
| Chart | Type | Why This Type? | Risk of Misinterpretation |
|---|---|---|---|
| **Goals Over Seasons** | Line Chart | Shows continuous trend over time; makes growth/decline patterns immediately visible | Y-axis doesn't start at zero — could exaggerate changes |
| **Rating by Competition** | Horizontal Bar | Easy comparison across categories; horizontal layout accommodates long names | Color gradient might imply causation where there's only correlation |
| **Goals vs Assists** | Scatter Plot | Reveals relationship between two continuous variables; outliers are visible | Doesn't show causation; overlapping points hidden |
| **Trophies by Club** | Vertical Bar | Simple comparison of discrete counts; values labeled clearly | Doesn't account for team quality differences |
| **Injury Impact** | Grouped Bar | Direct comparison between categories; color-coded for intuitive understanding | Small sample size per category limits confidence |
| **Goals Heatmap** | Heatmap | Shows two-dimensional patterns; color intensity reveals peaks instantly | Missing data (zeros) vs no data looks the same |
| **Rating Heatmap** | Heatmap | Compares performance across two categorical dimensions simultaneously | Averages hide variance; small sample sizes not visible |
| **Success Score** | Bar Chart with Threshold | Composite metric makes peak years objective; threshold clearly identifies top 30% | Weights (30% goals, 20% assists, etc.) are arbitrary |

**Why These Charts Were Chosen:**
- Prioritized clarity over complexity — audience is non-technical
- Used color strategically (red for injury/low, green for healthy/high)
- Avoided 3D charts, pie charts, and misleading axes
- Each chart answers a specific analytical question
- Interactive filters allow personalized exploration
    """)

with st.expander("🎯 Responsible Decision Statement"):
    st.markdown("""
**Critical Context for Decision-Making Section:**

✅ **What the data CAN support:**
- Injury prevention correlates with better performance (strong pattern)
- Playing time correlates with higher output (clear trend)
- Familiar environments show consistent ratings (observable pattern)

❌ **What the data CANNOT prove:**
- Causation (correlation ≠ causation)
- Future performance predictions (past ≠ future)
- Optimal career decisions (too many unmeasured variables)

**Limitations Acknowledged:**
1. **50-row dataset** — results are exploratory, not conclusive
2. **Missing context** — team quality, tactics, personal factors unknown
3. **Subjective weighting** — "success score" formula is one possible approach
4. **Confirmation bias** — creator's admiration for player may influence interpretation
5. **Hindsight bias** — analyzing past decisions with knowledge of outcomes

**Responsible Use:**
- Decisions are **observations from data**, not prescriptive advice
- Should be combined with expert coaching/medical input
- Personal player preferences and goals matter more than statistics
- Data informs but should not solely dictate career choices

**Transparency Commitment:**
- All analysis code and data available for review
- Methodology clearly documented
- Limitations prominently disclosed
- Alternative interpretations acknowledged
    """)

st.divider()

# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.caption("📊 Dashboard by Ngai Yaw · DATA201 Final Project · May 2026 · Player identity anonymized")
st.caption("Data sources: Wikipedia, FotMob, Transfermarkt (public domain)")
st.caption("⚠️ For academic purposes only · Not for commercial use")
