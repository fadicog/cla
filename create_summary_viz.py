"""
Create executive summary visualization for SP analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Load data
sp_metrics = pd.read_csv(r"D:\cluade\visualizations\sp_analysis\sp_metrics_summary.csv")

# Create executive summary figure
fig = plt.figure(figsize=(20, 12))

# Define grid
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3,
                     left=0.05, right=0.95, top=0.92, bottom=0.05)

# ============================================================================
# TOP LEFT: SP Performance Tiers
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])

performance_tiers = [
    ('Excellent\n80-90%', len(sp_metrics[sp_metrics['success_rate'] >= 80]), '#2ecc71'),
    ('Good\n70-79%', len(sp_metrics[(sp_metrics['success_rate'] >= 70) & (sp_metrics['success_rate'] < 80)]), '#3498db'),
    ('Fair\n60-69%', len(sp_metrics[(sp_metrics['success_rate'] >= 60) & (sp_metrics['success_rate'] < 70)]), '#f39c12'),
    ('Poor\n50-59%', len(sp_metrics[(sp_metrics['success_rate'] >= 50) & (sp_metrics['success_rate'] < 60)]), '#e67e22'),
    ('Critical\n<50%', len(sp_metrics[sp_metrics['success_rate'] < 50]), '#e74c3c')
]

tiers, counts, colors = zip(*performance_tiers)
y_pos = range(len(tiers))

bars = ax1.barh(y_pos, counts, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(tiers, fontsize=11, fontweight='bold')
ax1.set_xlabel('Number of SPs', fontsize=12, fontweight='bold')
ax1.set_title('SP Performance Distribution', fontsize=14, fontweight='bold', pad=15)

# Add count labels
for i, (bar, count) in enumerate(zip(bars, counts)):
    ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f'{count} SPs', va='center', fontsize=10, fontweight='bold')

ax1.set_xlim([0, max(counts) + 2])
ax1.grid(axis='x', alpha=0.3)

# ============================================================================
# TOP CENTER: Priority SPs to Fix
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

priority_sps = [
    ('InsureOne', 36, 'P0'),
    ('ADIB', 37, 'P0'),
    ('Beyon Money', 58, 'P1'),
    ('NBF', 55, 'P1'),
    ('National Bonds', 54, 'P1'),
    ('Baraka', 57, 'P2'),
    ('Etisalat Business', 62, 'P2'),
    ('Arab Bank', 61, 'P2')
]

sps, success_rates, priorities = zip(*priority_sps)

# Color by priority
priority_colors = {'P0': '#e74c3c', 'P1': '#f39c12', 'P2': '#3498db'}
colors_priority = [priority_colors[p] for p in priorities]

y_pos = range(len(sps))
bars = ax2.barh(y_pos, success_rates, color=colors_priority, edgecolor='black', linewidth=1.5)

# Add system average line
system_avg = 65.6
ax2.axvline(system_avg, color='green', linestyle='--', linewidth=2, label=f'System Avg: {system_avg:.1f}%')

ax2.set_yticks(y_pos)
ax2.set_yticklabels([f"{sp}\n({p})" for sp, p in zip(sps, priorities)], fontsize=9)
ax2.set_xlabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Priority SPs to Fix', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlim([0, 100])

# Add success rate labels
for bar, rate in zip(bars, success_rates):
    ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{rate:.0f}%', va='center', fontsize=9, fontweight='bold')

ax2.legend(loc='lower right', fontsize=9)
ax2.grid(axis='x', alpha=0.3)

# ============================================================================
# TOP RIGHT: Expected Impact
# ============================================================================
ax3 = fig.add_subplot(gs[0, 2])

impact_data = [
    ('InsureOne', 36, 65, 29),
    ('ADIB', 37, 65, 28),
    ('Etisalat Business', 62, 80, 18),
    ('National Bonds', 54, 70, 16)
]

sp_names, current, target, gain = zip(*impact_data)

x = range(len(sp_names))
width = 0.35

bars1 = ax3.bar([i - width/2 for i in x], current, width, label='Current', color='#e74c3c', edgecolor='black')
bars2 = ax3.bar([i + width/2 for i in x], target, width, label='Target (1 month)', color='#2ecc71', edgecolor='black')

ax3.set_xticks(x)
ax3.set_xticklabels(sp_names, rotation=45, ha='right', fontsize=9)
ax3.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax3.set_title('Expected Impact (1-Month Fixes)', fontsize=14, fontweight='bold', pad=15)
ax3.legend(fontsize=9, loc='upper left')
ax3.grid(axis='y', alpha=0.3)

# Add gain annotations
for i, g in enumerate(gain):
    ax3.annotate(f'+{g}pp', xy=(i, target[i]), xytext=(0, 5),
                textcoords='offset points', ha='center', fontsize=9,
                fontweight='bold', color='green',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))

ax3.set_ylim([0, 100])

# ============================================================================
# MIDDLE LEFT: Failure Mode Rankings
# ============================================================================
ax4 = fig.add_subplot(gs[1, 0])

failure_modes = [
    'User Abort\n(S43)',
    'Expired\n(S42)',
    'Tech Error\n(S41)',
    'Not Eligible\n(S44)'
]

# Get top SP for each failure mode
top_s43 = sp_metrics.nlargest(1, 's43_rate').iloc[0]
top_s42 = sp_metrics.nlargest(1, 's42_rate').iloc[0]
top_s41 = sp_metrics.nlargest(1, 's41_rate').iloc[0]
top_s44 = sp_metrics.nlargest(1, 's44_rate').iloc[0]

rates = [top_s43['s43_rate'], top_s42['s42_rate'], top_s41['s41_rate'], top_s44['s44_rate']]
labels = [f"{top_s43['sp_id']}\n{top_s43['s43_rate']:.1f}%",
          f"{top_s42['sp_id']}\n{top_s42['s42_rate']:.1f}%",
          f"{top_s41['sp_id']}\n{top_s41['s41_rate']:.1f}%",
          f"{top_s44['sp_id']}\n{top_s44['s44_rate']:.1f}%"]

colors_failure = ['#e74c3c', '#f39c12', '#9b59b6', '#95a5a6']

bars = ax4.bar(range(len(failure_modes)), rates, color=colors_failure, edgecolor='black', linewidth=1.5)
ax4.set_xticks(range(len(failure_modes)))
ax4.set_xticklabels(failure_modes, fontsize=10, fontweight='bold')
ax4.set_ylabel('Failure Rate (%)', fontsize=12, fontweight='bold')
ax4.set_title('Worst Performer by Failure Mode', fontsize=14, fontweight='bold', pad=15)
ax4.grid(axis='y', alpha=0.3)

# Add SP labels
for bar, label in zip(bars, labels):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             label, ha='center', va='bottom', fontsize=8, fontweight='bold')

ax4.set_ylim([0, max(rates) + 10])

# ============================================================================
# MIDDLE CENTER: Key Metrics Summary
# ============================================================================
ax5 = fig.add_subplot(gs[1, 1])
ax5.axis('off')

# Calculate key metrics
total_requests = sp_metrics['total_requests'].sum()
total_success = sp_metrics['success_count'].sum()
overall_success_rate = total_success / total_requests * 100
worst_sp = sp_metrics.nsmallest(1, 'success_rate').iloc[0]
best_sp = sp_metrics.nlargest(1, 'success_rate').iloc[0]
total_failures = total_requests - total_success
total_aborts = sp_metrics['s43_count'].sum()
total_tech_errors = sp_metrics['s41_count'].sum()

metrics_text = f"""
KEY METRICS SUMMARY
{'='*35}

Total Requests: {total_requests:,}
Total Successes: {total_success:,}
Overall Success Rate: {overall_success_rate:.1f}%

Total Failures: {total_failures:,}
  • User Aborts (S43): {total_aborts} ({total_aborts/total_requests*100:.1f}%)
  • Expired (S42): {sp_metrics['s42_count'].sum()} ({sp_metrics['s42_count'].sum()/total_requests*100:.1f}%)
  • Tech Errors (S41): {total_tech_errors} ({total_tech_errors/total_requests*100:.1f}%)
  • Not Eligible (S44): {sp_metrics['s44_count'].sum()} ({sp_metrics['s44_count'].sum()/total_requests*100:.1f}%)

{'='*35}
BEST PERFORMER
{best_sp['sp_id']}: {best_sp['success_rate']:.1f}% success
({best_sp['success_count']}/{best_sp['total_requests']} requests)

WORST PERFORMER
{worst_sp['sp_id']}: {worst_sp['success_rate']:.1f}% success
({worst_sp['success_count']}/{worst_sp['total_requests']} requests)

SPREAD: {best_sp['success_rate'] - worst_sp['success_rate']:.1f} percentage points
{'='*35}

POTENTIAL GAIN (if top 3 fixes applied):
Current: {overall_success_rate:.1f}%
Target: 74.2%
Improvement: +8.6pp
At 350K req/week: +30,100 shares/week
"""

ax5.text(0.05, 0.95, metrics_text, transform=ax5.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# ============================================================================
# MIDDLE RIGHT: Root Cause Analysis
# ============================================================================
ax6 = fig.add_subplot(gs[1, 2])

root_causes = [
    ('UX Issues\n(Abort at consent)', 'InsureOne\nADIB\nAAE', '#e74c3c'),
    ('Backend Errors\n(Integration)', 'Etisalat Business\nInsureOne\nEmirates Islamic', '#9b59b6'),
    ('Missing Docs\n(Futile Requests)', 'ADIB\nArab Bank\nInsureOne', '#95a5a6'),
    ('Slow Processing\n(Expiry)', 'ADIB\nBeyon Money\nNBF', '#f39c12')
]

y_pos = range(len(root_causes))
colors_root = [rc[2] for rc in root_causes]

ax6.barh(y_pos, [1]*len(root_causes), color=colors_root, edgecolor='black', linewidth=1.5)
ax6.set_yticks(y_pos)
ax6.set_yticklabels([rc[0] for rc in root_causes], fontsize=9, fontweight='bold')
ax6.set_xlim([0, 1])
ax6.set_xticks([])
ax6.set_title('Root Cause Categories', fontsize=14, fontweight='bold', pad=15)

# Add SP names on bars
for i, (cause, sps, color) in enumerate(root_causes):
    ax6.text(0.5, i, sps, ha='center', va='center', fontsize=8, fontweight='bold',
             color='white', bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

# ============================================================================
# BOTTOM ROW: Top 5 Recommendations
# ============================================================================
ax7 = fig.add_subplot(gs[2, :])
ax7.axis('off')

recommendations_text = """
TOP 5 RECOMMENDATIONS (Prioritized by Impact)
═══════════════════════════════════════════════════════════════════════════════════════════════════

1. FIX INSUREONE S32 STUCK STATE [P0 - 2 weeks]
   Issue: 36% of users abandon at post-PIN processing (S32 stage)
   Actions: • Profile S32 latency to identify bottleneck (likely issuer API or eSeal validation)
           • Add progress indicators ("Retrieving documents...", "Validating...", "Almost ready...")
           • Optimize backend: parallelize document retrieval, cache eSeal validation
           • Simplify document requirements with InsureOne partnership team
   Expected Impact: +29pp success rate (+8 successful shares/week) → 36% to 65%

2. IMPLEMENT DOCUMENT PRE-CHECK API [P0 - 2 weeks]
   Issue: 2.4% of requests are futile - users don't have required documents but don't know until S10/S11
   Actions: • Build /v1/check-eligibility endpoint (returns eligible true/false + missing_docs list)
           • SPs call BEFORE creating sharing request
           • Block request creation if user lacks documents
           • Show "Missing documents" screen with list to user
   Expected Impact: Eliminate 8,400 futile requests/week at scale (100% of S44 failures)
   Primary Beneficiaries: ADIB (11% waste), Arab Bank (9% waste), InsureOne (7% waste)

3. ADIB UX OVERHAUL [P0 - 3 weeks]
   Issue: 37% success rate due to: (1) futile requests, (2) S10 abandonment, (3) high expiry rate
   Actions: • Implement pre-check API to prevent S44 failures (Fix #2 above)
           • Redesign S10 screen: show real-time doc availability (✓ Emirates ID - Found, ⊗ Passport - Missing)
           • Simplify consent screen: icons + short names + expandable "Why we need this"
           • Reduce timeout (currently 21 day avg journey time → target 15 min active session)
           • User testing with 10 ADIB customers to validate fixes
   Expected Impact: +28pp success rate (+5 successful shares/week) → 37% to 65%

4. ETISALAT BUSINESS NETWORK STABILITY [P1 - 2 weeks]
   Issue: 23% tech error rate (3/13 requests) - 2 network errors indicate integration reliability issues
   Actions: • Implement request retry logic: 3 attempts with exponential backoff (1s, 2s, 4s)
           • Add connection pooling to reuse TCP connections
           • Implement circuit breaker: if >50% failure in 5 min, open circuit + alert ops
           • Monitor network error rates in real-time dashboard
   Expected Impact: +18pp success rate → 62% to 80%

5. CONSENT SCREEN A/B TESTING PROGRAM [P1 - 3 weeks]
   Issue: Consent conversion varies wildly (67% InsureOne vs 95% FAB) - UX quality inconsistent
   Actions: • Create 3 variants: (A) Current detailed, (B) Simplified with icons, (C) Progressive disclosure
           • A/B test across all SPs for 2 weeks
           • Measure consent conversion (S20→S21) per variant
           • Roll out winner to all SPs
   Expected Impact: +5-10pp system-wide success rate (if Variant B wins, apply to InsureOne → +18% consent conversion)
   Benefits: National Bonds (73% consent), ADIB (71%), InsureOne (67%) get biggest gains
═══════════════════════════════════════════════════════════════════════════════════════════════════
"""

ax7.text(0.02, 0.98, recommendations_text, transform=ax7.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

# ============================================================================
# Main Title
# ============================================================================
fig.suptitle('Service Provider Failure Analysis - Executive Summary',
             fontsize=20, fontweight='bold', y=0.98)

# Add subtitle
fig.text(0.5, 0.95, '500 Requests | 22 Service Providers | Analysis Date: 2026-01-09',
         ha='center', fontsize=12, style='italic')

# Save
output_path = Path(r"D:\cluade\visualizations\sp_analysis\SP_ANALYSIS_EXECUTIVE_SUMMARY.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n[SUCCESS] Executive summary saved: {output_path}")
print("\nThis single-page summary includes:")
print("  1. SP performance distribution (tier breakdown)")
print("  2. Priority SPs to fix (ranked by urgency)")
print("  3. Expected impact (before/after comparison)")
print("  4. Failure mode rankings (worst performer per mode)")
print("  5. Key metrics summary (overall stats)")
print("  6. Root cause categories (UX vs Backend vs Missing Docs vs Slow)")
print("  7. Top 5 recommendations (actionable next steps)")
print("\nUse this for stakeholder presentations!")

plt.close()
