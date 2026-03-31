# UAE PASS Digital Documents - Sharing Request Analytics Dashboard

## Overview

This dashboard analyzes document sharing requests in the UAE PASS Digital Documents system, tracking the complete user journey from request creation to final outcome.

## Data Analysis Results

**Dataset Summary:**
- Total Requests: 350,802
- Date Range: November 12-18, 2025 (7 days)
- Service Providers: 55
- Overall Success Rate: 67.4%

## Key Findings

### 1. Document Availability is Critical
- **With Documents Available**: 84.9% success rate (236,426 / 278,604 requests)
- **Without Documents**: 0.0% success rate (0 / 72,198 requests)
- **Impact**: Missing documents account for 20.6% of all requests and 100% failure rate

### 2. Funnel Drop-off Points
The request flow shows significant drop-offs at:
1. **Document Availability Check**: 20.6% lost due to missing documents
2. **Notification Read → Consent**: Users who don't review the request
3. **Consent → PIN Entry**: Users who consent but don't complete authentication

### 3. Success vs. Failure Breakdown
- Successful Shares: 236,426 (67.4%)
- Failed: Various system failures
- User Rejected: User declined sharing
- No Action Taken: Incomplete flows
- Saved For Later: Deferred decisions

## Available Dashboards

### Option 1: Interactive Web Dashboard (Recommended)
**File**: `uaepass_dashboard.py`

**Features:**
- Real-time filtering by Service Provider, Request Type, Platform, Date Range
- Interactive charts with hover details
- Drill-down capabilities
- Live data updates

**To Run:**
```bash
# Install dependencies (one-time)
pip install -r requirements.txt

# Run the dashboard
python uaepass_dashboard.py

# Open in browser
http://127.0.0.1:8050/
```

**System Requirements:**
- Python 3.7+
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Option 2: Static HTML Report
**File**: `uaepass_dashboard_report.html`

**Features:**
- No server required - opens directly in browser
- All visualizations embedded
- Portable - can be shared via email
- Read-only snapshot of data

**To View:**
- Double-click `uaepass_dashboard_report.html`
- Or drag and drop into browser
- Or right-click → Open With → Your Browser

**To Regenerate:**
```bash
python uaepass_static_report.py
```

## Dashboard Visualizations

### 1. Sharing Request Funnel
Shows the complete user journey with drop-off rates:
- Request Created (100%)
- Documents Available (79.4%)
- Notification Read
- Consent Given
- PIN Entered
- Successfully Shared (67.4%)

**Key Metrics:**
- Conversion rates at each stage
- Absolute numbers lost at each step
- Percentage of initial requests

### 2. Outcome Distribution (Pie Chart)
Breakdown of final request statuses:
- Shared (Success)
- Failed (System errors)
- User Rejected (User declined)
- No Action Taken (Incomplete)
- Saved For Later (Deferred)

### 3. Document Availability Impact
Compares success rates between:
- Requests with all required documents available
- Requests with missing documents

**Insight**: Document availability is the single biggest predictor of success.

### 4. Failure Breakdown
Details of unsuccessful requests:
- System failures by type (ISSUER_DOCUMENT_RETRIEVAL_FAILURE, etc.)
- User rejections
- Authentication failures
- Timeout issues

### 5. Daily Request Volume & Success Rate
Time series showing:
- Daily request count (bar chart)
- Daily success rate % (line chart)
- Trends and patterns over the week

### 6. User Journey Conversion Rates
Stage-to-stage conversion showing:
- Notification Read → Consent Given
- Consent Given → PIN Entered
- PIN Entered → Successfully Shared

### 7. Service Provider Performance
Horizontal bar chart comparing:
- Total requests per SP
- Successful shares per SP
- Success rate percentage overlay

### 8. Platform Comparison
Android vs. iOS vs. Other:
- Request volume by platform
- Success/failure breakdown
- Platform-specific issues

## Interactive Dashboard Features

### Filters (Interactive Version Only)

1. **Service Provider Filter**
   - Analyze specific SP performance
   - Compare SPs side-by-side

2. **Request Type Filter**
   - Pull vs. Push notifications
   - Different authentication flows

3. **Platform Filter**
   - Android vs. iOS analysis
   - Platform-specific issues

4. **Date Range Picker**
   - Custom date ranges
   - Week-over-week comparisons

### How to Use Filters

1. Select filters at the top of the dashboard
2. All charts update automatically
3. Choose "All" to reset any filter
4. Combine filters for detailed analysis

Example queries:
- "Show me Arab Bank on Android only"
- "What's the success rate for AAE last week?"
- "Compare Push vs. Pull notification success rates"

## Technical Details

### Data Structure

**Input**: `csvdata-2.csv`

**Key Columns:**
- `CREATED_AT`: Request timestamp
- `STATUS`: Final outcome (Shared, Failed, User Rejected, etc.)
- `ALIAS_NAME`: Service Provider name
- `VIZ_TYPE`: Push or Pull request
- `MANDATORY_DOCS_AVAILABLE`: Yes/No
- `CONSENT_GIVEN`: Yes/No
- `PIN_GIVEN`: Yes/No
- `FAILURE_REASON`: Error details for failures
- `COUNT`: Aggregated request count

### Status Flow Mapping

```
Request Created (100)
    ↓
Docs Available?
    ↓ Yes (200-240)          ↓ No
Ready for Review (300-340)   Failed
    ↓
Consent Given?
    ↓ Yes                    ↓ No
PIN Entry                    User Rejected (600)
    ↓
Success (400) / Failure (500-560)
```

## Files Included

1. **uaepass_dashboard.py** - Interactive Dash web application
2. **uaepass_static_report.py** - HTML report generator
3. **uaepass_dashboard_report.html** - Pre-generated static report
4. **requirements.txt** - Python dependencies
5. **DASHBOARD_README.md** - This file
6. **csvdata-2.csv** - Source data (3.8MB)

## Dependencies

```
dash==2.14.2
plotly==5.18.0
pandas==2.1.4
dash-bootstrap-components==1.5.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Issue: Dashboard won't start
**Solution**: Check Python version (3.7+ required) and install dependencies

### Issue: Port 8050 already in use
**Solution**: Edit `uaepass_dashboard.py` line 560, change port to 8051

### Issue: Data not loading
**Solution**: Ensure `csvdata-2.csv` is in `D:\cluade\` directory

### Issue: Charts not rendering
**Solution**:
- Clear browser cache
- Try different browser
- Check JavaScript is enabled

### Issue: Static report is blank
**Solution**: Regenerate with `python uaepass_static_report.py`

## Recommendations Based on Analysis

### 1. Improve Document Availability (Priority: HIGH)
- 72,198 requests (20.6%) fail due to missing documents
- **Action**: Implement pre-request document availability check
- **Expected Impact**: Could improve overall success rate from 67.4% to 84.9%

### 2. Reduce Notification-to-Consent Drop-off (Priority: MEDIUM)
- Significant users read notifications but don't consent
- **Action**: Improve consent UI, clarify what will be shared
- **Expected Impact**: 5-10% improvement in conversion

### 3. Simplify PIN Entry (Priority: MEDIUM)
- Drop-off between consent and PIN completion
- **Action**: Biometric authentication as alternative to PIN
- **Expected Impact**: 3-5% improvement in completion rate

### 4. Investigate System Failures (Priority: HIGH)
- Analyze specific failure reasons (ISSUER_DOCUMENT_RETRIEVAL_FAILURE, etc.)
- **Action**: Improve error handling and retry logic
- **Expected Impact**: Reduce system failures by 50%

### 5. Service Provider Onboarding
- Performance varies significantly across SPs
- **Action**: Share best practices from top-performing SPs
- **Expected Impact**: Standardize success rates across SPs

## Future Enhancements

Potential additions to the dashboard:

1. **Real-time Monitoring**
   - Live data feed from production
   - Alert system for success rate drops

2. **Cohort Analysis**
   - Track user behavior over time
   - Identify power users vs. first-time users

3. **A/B Test Analysis**
   - Compare different UX flows
   - Measure feature impact

4. **Predictive Analytics**
   - Predict likelihood of success
   - Identify at-risk requests early

5. **Document-Level Drill-down**
   - Which specific documents cause issues?
   - Emirates ID vs. Visa vs. Passport analysis

## Contact & Support

For questions about this dashboard:
- Check this README first
- Review the inline code comments
- Examine the static HTML report for examples

For UAE PASS DV product questions:
- Refer to `uae_pass_knowledge_base.md`
- Check `pm_dv_working_doc.md` for roadmap

## Version History

**v1.0** (2025-11-25)
- Initial dashboard creation
- 8 core visualizations
- Interactive and static versions
- Comprehensive data analysis

---

**Generated**: 2025-11-25
**Dataset**: November 12-18, 2025 (350,802 requests)
**Success Rate**: 67.4%
**Key Finding**: Document availability increases success rate from 0% to 84.9%
