"""
analyze_loader_telemetry.py
===========================
UAE PASS DV — Loader Telemetry Analysis
Infinite Loaders Detection Initiative (S70 / 2026 Roadmap)

Data: LoaderTelemetryData.xlsx
Period: 2026-04-22 to 2026-06-04 (44 days)
Granularity: Daily × LOADER_CASE × DEVICE_INFO × APP_VERSION × DURATION_RANGE → RECORD_COUNT

Run: py -3 deliverables/loader_telemetry/analyze_loader_telemetry.py
Outputs: deliverables/loader_telemetry/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO = Path('C:/Users/2065726/mainclaude')
SRC  = REPO / 'LoaderTelemetryData.xlsx'
OUT  = REPO / 'deliverables/loader_telemetry'
OUT.mkdir(parents=True, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
BRAND_GOLD   = '#a89030'
BRAND_GREEN  = '#11a56f'
BRAND_TEAL   = '#3fcaa7'
RED          = '#d94f3d'
ORANGE       = '#e07b39'
BLUE         = '#3a7abf'
GREY         = '#888888'

plt.rcParams.update({
    'figure.facecolor': '#f9f9f9',
    'axes.facecolor':   '#ffffff',
    'axes.edgecolor':   '#cccccc',
    'axes.labelcolor':  '#333333',
    'text.color':       '#333333',
    'xtick.color':      '#555555',
    'ytick.color':      '#555555',
    'font.family':      'DejaVu Sans',
    'font.size':        11,
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
})

FIG_SIZE = (16, 9)

# ── Duration bucket ordering & midpoints ─────────────────────────────────────
DUR_ORDER = [
    '< 0 ms', '= 0 ms', '1-50 ms', '51-100 ms',
    '101-500 ms', '501-1000 ms', '1001-5000 ms',
    '5001-10000 ms', '10000+ ms'
]
DUR_MIDPOINT = {
    '< 0 ms':         -1,
    '= 0 ms':          0,
    '1-50 ms':        25,
    '51-100 ms':      75,
    '101-500 ms':    300,
    '501-1000 ms':   750,
    '1001-5000 ms': 3000,
    '5001-10000 ms':7500,
    '10000+ ms':   15000,
}

# DV flow mapping  (loader case → user-facing screen / flow)
DV_FLOW = {
    'DOCUMENTS_LIST':                  'Document Vault (home) — all docs fetch',
    'NOTIFICATIONS_LIST':              'Notifications list screen',
    'NON_ACTIONABLE_NOTIFICATION_DETAILS': 'Info notification detail',
    'ISSUED_DOCUMENT_DETAILS':         'Document detail screen — issued doc',
    'ACTIONABLE_NOTIFICATION_DETAILS': 'Sharing-request notification tap',
    'ISSUED_DOCUMENT_EVIDENCE':        'eSeal / evidence fetch for issued doc',
    'ISSUERS_LIST':                    'Issuers catalogue screen',
    'QR_VERIFICATION':                 'QR-based SSO / sharing-request scan',
    'UPLOADED_DOCUMENT_EVIDENCE':      'Evidence fetch for user-uploaded doc',
    'DOWNLOAD_DOCUMENT':               'Document download (PDF/render)',
    'SHARE_DOCUMENT':                  'Consent + verifiable-presentation POST',
    'DOWNLOAD_SELF_SIGN_DOCUMENT':     'Self-signed document download',
    'DOCUMENT_SELECTION_ISSUED_LIST':  'Document selection during sharing flow',
    'DOCUMENT_SELECTION_UPLOADED_LIST':'Uploaded-doc selection during sharing',
}

# ── Load data ─────────────────────────────────────────────────────────────────
print('Loading data...')
df = pd.read_excel(SRC, sheet_name='data', engine='openpyxl')
df.columns = [c.strip() for c in df.columns]
df = df[df['LOADER_CASE'].notna()].copy()
df['DEVICE_INFO']     = df['DEVICE_INFO'].astype(str).str.strip()
df['APP_VERSION']     = df['APP_VERSION'].astype(str).str.strip()
df['DURATION_RANGE']  = df['DURATION_RANGE'].astype(str).str.strip()
df['RECORD_COUNT']    = df['RECORD_COUNT'].fillna(0).astype(int)
df['CREATEDAT']       = pd.to_datetime(df['CREATEDAT'])
df['DATE']            = df['CREATEDAT'].dt.date
df['DATE']            = pd.to_datetime(df['DATE'])
df['DUR_CAT']         = pd.Categorical(df['DURATION_RANGE'], categories=DUR_ORDER, ordered=True)
df['IS_SLOW']         = df['DURATION_RANGE'] == '10000+ ms'
df['IS_5_10K']        = df['DURATION_RANGE'] == '5001-10000 ms'
df['DV_FLOW']         = df['LOADER_CASE'].map(DV_FLOW)
df['DUR_MIDPOINT']    = df['DURATION_RANGE'].map(DUR_MIDPOINT)

# Normalise device: anything not iOS/Android → 'Other/Backend'
df['DEVICE'] = df['DEVICE_INFO'].apply(
    lambda x: x if x in ('IOS', 'ANDROID') else 'Other/Backend'
)

print(f'Rows: {len(df):,} | Date range: {df.DATE.min().date()} to {df.DATE.max().date()}')
print(f'Total events: {df.RECORD_COUNT.sum():,.0f}')
print(f'Loader cases: {df.LOADER_CASE.nunique()}')
print()

# ── Aggregates ────────────────────────────────────────────────────────────────
# Per loader case
case_agg = (df.groupby('LOADER_CASE')
              .agg(total=('RECORD_COUNT','sum'),
                   slow_10k=('RECORD_COUNT', lambda x: x[df.loc[x.index,'IS_SLOW']].sum()),
                   slow_5_10k=('RECORD_COUNT', lambda x: x[df.loc[x.index,'IS_5_10K']].sum()))
              .reset_index())
case_agg['slow_pct']  = case_agg['slow_10k']  / case_agg['total'] * 100
case_agg['slow_5pct'] = case_agg['slow_5_10k'] / case_agg['total'] * 100
case_agg['slow_5plus_pct'] = (case_agg['slow_10k'] + case_agg['slow_5_10k']) / case_agg['total'] * 100
case_agg['dv_flow']   = case_agg['LOADER_CASE'].map(DV_FLOW)
case_agg = case_agg.sort_values('slow_pct', ascending=False)

# Per loader case x device
case_dev = (df.groupby(['LOADER_CASE','DEVICE'])
              .agg(total=('RECORD_COUNT','sum'),
                   slow_10k=('RECORD_COUNT', lambda x: x[df.loc[x.index,'IS_SLOW']].sum()))
              .reset_index())
case_dev['slow_pct'] = case_dev['slow_10k'] / case_dev['total'] * 100

# Per loader case x app version
case_ver = (df.groupby(['LOADER_CASE','APP_VERSION'])
              .agg(total=('RECORD_COUNT','sum'),
                   slow_10k=('RECORD_COUNT', lambda x: x[df.loc[x.index,'IS_SLOW']].sum()))
              .reset_index())
case_ver['slow_pct'] = case_ver['slow_10k'] / case_ver['total'] * 100

# Duration distribution per case
dur_dist = (df.groupby(['LOADER_CASE','DURATION_RANGE'])['RECORD_COUNT'].sum()
              .reset_index()
              .rename(columns={'RECORD_COUNT':'count'}))
dur_dist['DUR_CAT'] = pd.Categorical(dur_dist['DURATION_RANGE'], categories=DUR_ORDER, ordered=True)
dur_dist = dur_dist.sort_values(['LOADER_CASE','DUR_CAT'])

# Save aggregations as CSV
case_agg.to_csv(OUT / 'case_agg.csv', index=False)
case_dev.to_csv(OUT / 'case_device_agg.csv', index=False)
case_ver.to_csv(OUT / 'case_version_agg.csv', index=False)
dur_dist.to_csv(OUT / 'duration_distribution.csv', index=False)
print('Aggregation CSVs saved.')

# ── CHART 1: Ranked bar — % of events >= 10s per loader case ─────────────────
print('Chart 1: Ranked bar...')
fig, ax = plt.subplots(figsize=FIG_SIZE)
df_plot = case_agg.sort_values('slow_pct')
colors = [RED if p >= 15 else ORANGE if p >= 7 else BRAND_GOLD for p in df_plot.slow_pct]
bars = ax.barh(df_plot.LOADER_CASE, df_plot.slow_pct, color=colors, edgecolor='white', height=0.65)

for bar, val, total in zip(bars, df_plot.slow_pct, df_plot.total):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%  ({total/1e6:.1f}M events)', va='center', fontsize=9.5, color='#333')

ax.set_xlabel('% of loader events taking >10 seconds (infinite loader risk)', labelpad=8)
ax.set_xlim(0, 42)
ax.axvline(10, color=ORANGE, linestyle='--', linewidth=1, alpha=0.7, label='10% alert threshold')
ax.set_title('Loader Hotspots: % of Events Exceeding 10 s, by Screen/API\n'
             'UAE PASS DV App — 22 Apr to 4 Jun 2026 (28.1M events total)', pad=14)

legend_handles = [
    mpatches.Patch(color=RED,        label='Critical: >=15% infinite-loader rate'),
    mpatches.Patch(color=ORANGE,     label='Warning:  7-14%'),
    mpatches.Patch(color=BRAND_GOLD, label='Acceptable: <7%'),
]
ax.legend(handles=legend_handles, loc='lower right', fontsize=9.5)
ax.set_yticklabels(df_plot.LOADER_CASE, fontsize=10)
plt.tight_layout()
fig.savefig(OUT / 'fig1_ranked_bar_slow_loaders.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig1_ranked_bar_slow_loaders.png')

# ── CHART 2: Latency distribution histograms (stacked bar by duration bucket) ─
print('Chart 2: Distribution histograms...')
top_cases_by_vol = case_agg.sort_values('total', ascending=False).head(8).LOADER_CASE.tolist()

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()

DUR_COLORS = {
    '< 0 ms':         '#aaaaaa',
    '= 0 ms':         '#dddddd',
    '1-50 ms':        BRAND_TEAL,
    '51-100 ms':      BRAND_TEAL,
    '101-500 ms':     BRAND_GREEN,
    '501-1000 ms':    BRAND_GOLD,
    '1001-5000 ms':   ORANGE,
    '5001-10000 ms':  '#c06030',
    '10000+ ms':      RED,
}

for i, lc in enumerate(top_cases_by_vol):
    ax = axes[i]
    sub = dur_dist[dur_dist.LOADER_CASE == lc].copy()
    case_total = sub['count'].sum()
    sub['pct'] = sub['count'] / case_total * 100
    sub = sub.sort_values('DUR_CAT')

    x = range(len(sub))
    bar_colors = [DUR_COLORS.get(d, GREY) for d in sub.DURATION_RANGE]
    bars = ax.bar(x, sub.pct, color=bar_colors, edgecolor='white', width=0.75)
    ax.set_xticks(list(x))
    ax.set_xticklabels([d.replace(' ms','') for d in sub.DURATION_RANGE], rotation=40, ha='right', fontsize=7.5)
    ax.set_ylabel('%', fontsize=9)
    slow_pct = sub[sub.DURATION_RANGE == '10000+ ms']['pct'].sum()
    ax.set_title(f'{lc}\n(10k+: {slow_pct:.1f}%, n={case_total/1e6:.1f}M)', fontsize=9.5, fontweight='bold')
    ax.set_ylim(0, max(sub.pct)*1.15 + 1)

fig.suptitle('Duration Distribution by Loader Case (Top 8 by Volume)\n'
             'UAE PASS DV — 28.1M Events, 22 Apr to 4 Jun 2026', fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
fig.savefig(OUT / 'fig2_duration_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig2_duration_distributions.png')

# ── CHART 3: Heatmap — loader case × device (iOS / Android) ──────────────────
print('Chart 3: Heatmap loader x device...')
pivot_dev = case_dev[case_dev.DEVICE.isin(['IOS','ANDROID'])].pivot(
    index='LOADER_CASE', columns='DEVICE', values='slow_pct'
).fillna(0)
pivot_dev = pivot_dev.sort_values('ANDROID', ascending=False)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pivot_dev, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=0.5, linecolor='#eee', ax=ax,
            cbar_kws={'label': '% of events >10s'})
ax.set_title('Infinite Loader Rate (% events >10s): Screen vs Platform\n'
             'Android Consistently Worse — ISSUED_DOCUMENT_EVIDENCE Worst Gap (+14pp)', pad=12)
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(axis='y', labelsize=9.5)
plt.tight_layout()
fig.savefig(OUT / 'fig3_heatmap_loader_device.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig3_heatmap_loader_device.png')

# ── CHART 4: Heatmap — loader case × app version ──────────────────────────────
print('Chart 4: Heatmap loader x version...')
real_versions = ['6.5.0','6.5.1','6.6.0','6.6.1','6.6.2','6.7.0']
cv_filt = case_ver[case_ver.APP_VERSION.isin(real_versions) &
                   case_ver.LOADER_CASE.isin([
                       'ISSUED_DOCUMENT_EVIDENCE','ISSUED_DOCUMENT_DETAILS',
                       'ACTIONABLE_NOTIFICATION_DETAILS','SHARE_DOCUMENT',
                       'QR_VERIFICATION','DOCUMENTS_LIST','ISSUERS_LIST',
                       'DOWNLOAD_DOCUMENT','DOCUMENT_SELECTION_ISSUED_LIST'])]

pivot_ver = cv_filt.pivot(index='LOADER_CASE', columns='APP_VERSION', values='slow_pct').fillna(0)
# Sort by latest version's rate
if '6.7.0' in pivot_ver.columns:
    pivot_ver = pivot_ver.sort_values('6.7.0', ascending=False)

fig, ax = plt.subplots(figsize=(13, 7))
sns.heatmap(pivot_ver, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.5, linecolor='#eee', ax=ax,
            cbar_kws={'label': '% of events >10s'})
ax.set_title('Infinite Loader Rate (%) by Loader Case × App Version\n'
             'Green = improving, Red = worsening across versions', pad=12)
ax.set_xlabel('App Version', labelpad=8)
ax.set_ylabel('')
ax.tick_params(axis='y', labelsize=9.5)
plt.tight_layout()
fig.savefig(OUT / 'fig4_heatmap_loader_version.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig4_heatmap_loader_version.png')

# ── CHART 5: Time-series — daily 10k+ rate for top 5 offenders ───────────────
print('Chart 5: Time series p95 by loader case...')
daily = (df.groupby(['DATE','LOADER_CASE'])
           .agg(total=('RECORD_COUNT','sum'),
                slow=('RECORD_COUNT', lambda x: x[df.loc[x.index,'IS_SLOW']].sum()))
           .reset_index())
daily['slow_pct'] = daily['slow'] / daily['total'] * 100

top5_slow = case_agg.sort_values('slow_pct', ascending=False).head(5).LOADER_CASE.tolist()
palette = [RED, ORANGE, BRAND_GOLD, BLUE, BRAND_GREEN]

fig, ax = plt.subplots(figsize=FIG_SIZE)
for lc, color in zip(top5_slow, palette):
    sub = daily[daily.LOADER_CASE == lc].sort_values('DATE')
    ax.plot(sub.DATE, sub.slow_pct, label=lc, color=color, linewidth=2, alpha=0.9)

ax.axhline(15, color=RED, linestyle='--', linewidth=1, alpha=0.5, label='15% critical threshold')
ax.axhline(7,  color=ORANGE, linestyle=':', linewidth=1, alpha=0.5, label='7% warning threshold')
ax.set_ylabel('% of events taking >10 seconds', labelpad=8)
ax.set_xlabel('Date (UAE local time, GMT+4)', labelpad=8)
ax.set_title('Daily Infinite Loader Rate (>10s) — Top 5 Offending Screens\n'
             'ACTIONABLE_NOTIFICATION_DETAILS shows alarming upward trend (+21pp in 6 weeks)', pad=12)
ax.legend(fontsize=9, loc='upper left')
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_xlim(daily.DATE.min(), daily.DATE.max())
plt.xticks(rotation=30)
plt.tight_layout()
fig.savefig(OUT / 'fig5_timeseries_slow_rate.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig5_timeseries_slow_rate.png')

# ── CHART 6: iOS vs Android delta bar chart ───────────────────────────────────
print('Chart 6: iOS vs Android delta...')
dev_pivot = case_dev[case_dev.DEVICE.isin(['IOS','ANDROID'])].pivot(
    index='LOADER_CASE', columns='DEVICE', values='slow_pct'
).fillna(0).reset_index()
dev_pivot['delta'] = dev_pivot['ANDROID'] - dev_pivot['IOS']
dev_pivot = dev_pivot.sort_values('delta', ascending=False)

fig, ax = plt.subplots(figsize=(14, 7))
colors_delta = [RED if d > 5 else ORANGE if d > 0 else BRAND_GREEN for d in dev_pivot.delta]
bars = ax.barh(dev_pivot.LOADER_CASE, dev_pivot.delta, color=colors_delta, edgecolor='white', height=0.6)

for bar, val in zip(bars, dev_pivot.delta):
    label = f'+{val:.1f}pp' if val >= 0 else f'{val:.1f}pp'
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            label, va='center', fontsize=9.5)

ax.axvline(0, color='#333', linewidth=1)
ax.set_xlabel('Android 10s-rate minus iOS 10s-rate (percentage points)\nPositive = Android worse', labelpad=8)
ax.set_title('Platform Gap: Android vs iOS Infinite-Loader Rate Difference by Screen\n'
             'ISSUED_DOCUMENT_EVIDENCE is 14pp worse on Android — biggest single gap', pad=12)
plt.tight_layout()
fig.savefig(OUT / 'fig6_ios_android_delta.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig6_ios_android_delta.png')

# ── CHART 7: Volume-weighted impact bubble chart ──────────────────────────────
print('Chart 7: Volume x slow rate bubble...')
fig, ax = plt.subplots(figsize=FIG_SIZE)
x = case_agg['total'] / 1e6
y = case_agg['slow_pct']
sizes = np.sqrt(case_agg['slow_10k']) * 0.3

scatter_colors = [RED if p >= 15 else ORANGE if p >= 7 else BRAND_GREEN for p in y]
sc = ax.scatter(x, y, s=sizes*2, c=scatter_colors, alpha=0.75, edgecolors='white', linewidths=0.8)

for _, row in case_agg.iterrows():
    ax.annotate(row.LOADER_CASE.replace('_', '\n'),
                xy=(row.total/1e6, row.slow_pct),
                xytext=(6, 0), textcoords='offset points',
                fontsize=7.5, color='#333', va='center')

ax.set_xlabel('Total Events (millions) — proxy for user exposure', labelpad=8)
ax.set_ylabel('% of events taking >10 seconds', labelpad=8)
ax.axhline(15, color=RED, linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(7,  color=ORANGE, linestyle=':', linewidth=1, alpha=0.5)
ax.set_title('Loader Impact Map: Volume vs Severity\n'
             'Bubble size = absolute count of infinite-loader events (n slow events)', pad=12)
legend_handles = [
    mpatches.Patch(color=RED,        label='Critical (>=15% rate)'),
    mpatches.Patch(color=ORANGE,     label='Warning (7-14% rate)'),
    mpatches.Patch(color=BRAND_GREEN,label='Acceptable (<7%)'),
]
ax.legend(handles=legend_handles, fontsize=9.5)
plt.tight_layout()
fig.savefig(OUT / 'fig7_volume_vs_severity_bubble.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig7_volume_vs_severity_bubble.png')

# ── CHART 8: Daily volume trend (total events) ────────────────────────────────
print('Chart 8: Daily volume trend...')
daily_total = df.groupby('DATE')['RECORD_COUNT'].sum().reset_index()
daily_slow  = df[df.IS_SLOW].groupby('DATE')['RECORD_COUNT'].sum().reset_index()
daily_merged = daily_total.merge(daily_slow, on='DATE', suffixes=('_total','_slow'))
daily_merged['slow_pct'] = daily_merged['RECORD_COUNT_slow'] / daily_merged['RECORD_COUNT_total'] * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
ax1.fill_between(daily_merged.DATE, daily_merged.RECORD_COUNT_total/1e6,
                 alpha=0.3, color=BLUE, label='Total events (M)')
ax1.plot(daily_merged.DATE, daily_merged.RECORD_COUNT_total/1e6, color=BLUE, linewidth=2)
ax1.set_ylabel('Daily events (millions)')
ax1.set_title('UAE PASS DV — Daily Loader Event Volume\n22 Apr – 4 Jun 2026 (GMT+4)')
ax1.legend()

ax2.plot(daily_merged.DATE, daily_merged.slow_pct, color=RED, linewidth=2)
ax2.fill_between(daily_merged.DATE, daily_merged.slow_pct, alpha=0.2, color=RED)
ax2.axhline(daily_merged.slow_pct.mean(), color=GREY, linestyle='--',
            label=f'Mean {daily_merged.slow_pct.mean():.1f}%')
ax2.set_ylabel('% of all events >10s')
ax2.set_xlabel('Date (UTC+4)')
ax2.legend()
plt.xticks(rotation=30)
plt.tight_layout()
fig.savefig(OUT / 'fig8_daily_volume_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print('  saved fig8_daily_volume_trend.png')

# ── Print summary table ───────────────────────────────────────────────────────
print()
print('='*90)
print('SUMMARY TABLE — Per-Loader-Case Statistics')
print('='*90)
print(f'{"LOADER_CASE":<45} {"Volume":>10} {"10k+ count":>12} {"10k+ %":>8} {"Severity":>12}')
print('-'*90)
for _, row in case_agg.iterrows():
    sev = 'CRITICAL' if row.slow_pct >= 15 else ('WARNING' if row.slow_pct >= 7 else 'OK')
    print(f'{row.LOADER_CASE:<45} {row.total:>10,.0f} {row.slow_10k:>12,.0f} {row.slow_pct:>7.1f}% {sev:>12}')
print()
grand_total = case_agg.total.sum()
grand_slow  = case_agg.slow_10k.sum()
print(f'Grand total: {grand_total:,.0f} events | Infinite loaders: {grand_slow:,.0f} ({grand_slow/grand_total*100:.2f}%)')
print()
print('All charts saved to:', OUT)
print('Done.')
