# UAE PASS Sharing Request Analysis - Key Insights

**Date**: 2026-01-09
**Dataset**: 500 requests, 5,068 events (Nov 1-28, 2025)
**Overall Success Rate**: 65.6%

---

## Top 10 Actionable Insights

### 1. POST-CONSENT ABANDONMENT IS THE #1 PROBLEM

**Insight**: 37 requests (7.4% of total) abort after users grant consent (S21 -> S43).

**Why It Matters**:
- Users have already approved sharing
- They've invested time in the journey
- System loses them at the last minute

**Root Cause Hypotheses**:
- App backgrounding kills session
- No loading indicator after consent creates confusion
- Unclear next steps after approval
- Network issues with no feedback
- Unexpected delay before PIN screen

**Actions**:
- Add prominent loading indicator: "Preparing your documents..."
- Show progress bar with stages
- Implement session recovery for backgrounding
- Set user expectation: "This will take ~30 seconds"
- Track exactly where S21 -> S43 happens

**Impact**: Fix this -> +7.4% success rate (+37 requests)

---

### 2. BACKEND FAILURES AFTER PIN SUCCESS (CRITICAL BUG)

**Insight**: 24 requests (4.8% of total) fail with technical error S41 immediately after successful PIN entry (S31).

**Why It Matters**:
- Users complete ALL steps correctly
- System fails them at the final stage
- Worst possible user experience

**Error Codes**:
- `dv_5xx`: 11 errors (backend server failure)
- `signing_timeout`: 6 errors (document signing timeout)
- `network_error`: 2 errors

**Root Causes**:
- Backend signing service failures
- Network timeouts during document packaging
- Race conditions in multi-step signing process

**Actions**:
- URGENT: Investigate backend logs for S31 -> S41 patterns
- Implement retry logic with exponential backoff
- Add circuit breaker for signing service
- Set up real-time alerts for S31 -> S41 failures
- Load test signing service

**Impact**: Fix this -> +4.8% success rate (+24 requests)

---

### 3. REDIRECT CHANNEL DRAMATICALLY OUTPERFORMS

**Insight**: Redirect channel achieves 83% success rate, 23% higher than notification channel (60%).

**Performance Comparison**:
- **Redirect**: 83% success, 57s avg time, 100 requests
- **QR**: 65% success, 138s avg time, 112 requests
- **Notification**: 60% success, 148s avg time, 288 requests

**Why Redirect Wins**:
- Immediate app open (no notification delay)
- No notification permission required
- Fewer steps in journey (10 vs 11)
- Users already engaged (clicked link)
- Lower expiry rate (5% vs 9-10%)

**Actions**:
- Promote redirect channel for critical transactions
- Study redirect UX best practices
- Consider redirect as default for high-value SPs
- Analyze why notification struggles
- Migrate high-volume SPs to redirect where possible

**Impact**: Shifting volume to redirect -> +10-15% overall success rate

---

### 4. CONSENT & PIN ARE NOT THE PROBLEMS

**Insight**: Consent (93.1% approval) and PIN (95.7% success) perform excellently.

**Data**:
- Consent granted: 405 out of 435 (93.1%)
- Consent denied: 0 (zero explicit denials)
- PIN success: 352 out of 368 (95.7%)
- PIN failed: 16 (4.3%)

**Why It Matters**:
- Common assumption that consent is friction point
- Data proves otherwise - users are willing to share
- Product/UX teams can stop optimizing these areas
- Focus engineering effort elsewhere

**Key Takeaway**: Don't waste time optimizing 93%+ success rates. Focus on the 7.4% post-consent abandonment and 4.8% backend failures instead.

---

### 5. FAILED REQUESTS TAKE 4.6X LONGER

**Insight**: Failed requests average 290.7 seconds vs 63.5 seconds for successful ones.

**Breakdown**:
- **Success (S40)**: Mean 63.5s, Median 59s (tight distribution)
- **Failed (All)**: Mean 290.7s, Median 63s (wide variance)

**Why the Huge Difference**:
- 47 expiries at 900 seconds (15-minute timeout) inflate mean
- Excluding expiries, failures are ~65s (similar to success)
- Users wait before abandoning (mean 13.7s at S43)

**User Experience Impact**:
- 34% of users experience slow/failed journeys
- Expiries create worst UX (15 minutes wasted)
- Users don't know if request is stuck or processing

**Actions**:
- Reduce expiry rate (9.4% is too high)
- Add progress indicators for long operations
- Push notification reminders if user stalls
- Timeout warnings: "Request expires in 5 minutes"

**Impact**: Reduce expiries -> Better UX, lower time-to-failure

---

### 6. DOCUMENT RETRIEVAL WORKS EXCELLENTLY (DON'T FIX WHAT ISN'T BROKEN)

**Insight**: When documents are missing, retrieval succeeds 86.7% of the time (117 out of 135 attempts).

**Performance**:
- Retrieval success (S13): 117 (86.7%)
- Failed - Issuer (S15): 12 (8.9%)
- Failed - Network (S14): 6 (4.4%)

**Why It Matters**:
- Document retrieval is often perceived as risky/unreliable
- Data proves it's actually very robust
- Engineering team has done excellent work here
- Should be highlighted as a strength, not improved

**Actions**:
- NO changes needed to retrieval logic
- Leverage retrieval success as competitive advantage
- Document best practices for future issuer integrations
- Monitor but don't over-optimize (86.7% is great)

**Key Takeaway**: Focus on actual problems (abandonment, backend failures), not on things that work well.

---

### 7. SURPRISING PARADOX: MISSING DOCUMENTS -> HIGHER SUCCESS

**Insight**: Requests requiring document retrieval have 86.7% success rate vs 61.5% when documents are already available.

**The Paradox**:
- **Documents ready (S10)**: 61.5% success
- **Documents missing (S11) + retrieval**: 86.7% success

**Why This Happens**:
- **Sunk Cost Effect**: Users who retrieve docs have invested more time/effort
- **Commitment Bias**: They're more motivated to complete
- **Engagement**: Retrieval process keeps users engaged
- **Self-Selection**: Only committed users attempt retrieval

**Implications**:
- Document availability is NOT the critical factor
- User engagement/commitment matters more
- Retrieval process creates "journey investment"

**Actions**:
- Leverage retrieval as engagement mechanic
- Show progress during retrieval: "Fetching your Passport... 2/3 complete"
- Apply same engagement tactics to ready-document flows
- Consider "progressive disclosure" even when docs are ready

**Impact**: Rethink document availability as problem -> Focus on user engagement

---

### 8. iOS OUTPERFORMS ANDROID BY 5.4%

**Insight**: iOS achieves 68.3% success vs Android's 62.9% (5.4 percentage point gap).

**Platform Comparison**:
| Metric | iOS | Android | Delta |
|--------|-----|---------|-------|
| Success Rate | 68.3% | 62.9% | iOS +5.4% |
| Avg Journey Time | 146s | 137s | Android 6% faster |
| Technical Errors | 4.0% | 5.6% | Android +40% higher |
| User Aborts | 16.9% | 18.7% | Android +11% higher |

**Why Android Struggles**:
- Higher technical error rate (5.6% vs 4.0%)
- More user aborts (18.7% vs 16.9%)
- Possibly background restrictions killing sessions
- Memory management issues?
- OS fragmentation (many Android versions)

**Actions**:
- **Android Performance Sprint**: Dedicated investigation
- Analyze Android-specific S41 errors
- Test background/foreground transitions across Android versions
- Improve memory management and state preservation
- Increase test coverage for Samsung, Xiaomi, Oppo, etc.

**Impact**: Close gap -> +13 successful requests (+2.6% improvement)

---

### 9. SERVICE PROVIDER INTEGRATION QUALITY VARIES WILDLY

**Insight**: SP success rates range from 89.5% (DU) to 35.7% (InsureOne).

**Top Performers**:
- DU: 89.5% (19 requests)
- ENBD: 86.4% (22 requests)
- Du Esim: 85.7% (21 requests)

**Bottom Performers**:
- InsureOne: 35.7% (28 requests) **CRITICAL**
- ADIB: 36.8% (19 requests) **CRITICAL**
- National Bonds: 53.8% (26 requests)

**Why InsureOne & ADIB Fail**:
- Likely requesting documents users don't have
- Integration misconfiguration
- No pre-check for document availability
- Possibly requesting wrong document types

**Impact on UAE PASS Reputation**:
- 28 InsureOne users (56% of volume) had bad experience
- Users blame UAE PASS, not the SP
- Damages overall platform trust

**Actions**:
- **SP Audit**: Review InsureOne and ADIB integrations immediately
- **Document Pre-check API**: Let SPs verify availability before requesting
- **Best Practices Sharing**: DU and ENBD doing it right - share their approach
- **SP Dashboard**: Real-time success rate visibility
- **SLA Requirements**: Minimum success rate for SP integrations

**Impact**: Fix bottom SPs -> +15 requests (+3% improvement)

---

### 10. EXPIRY RATE AT 9.4% IS TOO HIGH

**Insight**: 47 requests (9.4%) expire before completion - 1 in 10 requests times out.

**Where Expiries Happen**:
- **S10 -> S42** (25 requests): After docs ready, user doesn't act
- **S06 -> S42** (22 requests): QR code never scanned

**Why 9.4% is Too High**:
- Users have initiated the request (not spam)
- 15-minute TTL might be too short
- No reminders or nudges to continue
- Users distracted or unclear on urgency

**15-Minute TTL Analysis**:
- **Pro**: Security (short-lived credentials)
- **Con**: 9.4% of legitimate users can't complete in time

**Actions**:
- **Push Notification Reminders**: If no action in 5 minutes
- **Extended TTL for S10**: 30 minutes when docs are ready
- **In-App Nudges**: "Your documents are ready! Tap to continue"
- **Expiry Warning**: "Request expires in 5 minutes"
- **QR Refresh**: Allow regenerating expired QR codes

**Impact**: Reduce expiries from 9.4% to ~5% -> +22 requests (+4.4% improvement)

---

## Summary: The Big Picture

### What's Working
- Document retrieval (86.7% success)
- Consent approval (93.1%)
- PIN entry (95.7%)
- Redirect channel (83% success)
- iOS platform (68.3% success)

### What's Broken
- Post-consent abandonment (7.4% of requests)
- Backend failures after PIN (4.8% of requests)
- Notification channel (60% success)
- Android platform (62.9% success, 5.4% behind iOS)
- InsureOne & ADIB integrations (35-37% success)
- Expiry rate (9.4%)

### Maximum Improvement Potential

If top 3 issues fixed:
- **Current**: 65.6% success rate
- **After fixes**: 82.8% success rate
- **Improvement**: +17.2 percentage points
- **Weekly impact**: +1,720 successful shares (assuming 10K requests/week)

### Priority Order

1. **Fix S21 -> S43 post-consent abandonment** (+7.4%)
2. **Fix S31 -> S41 backend failures** (+4.8%)
3. **Reduce S10 -> S42 expiries** (+5.0%)
4. **Audit InsureOne & ADIB integrations** (+3.0%)
5. **Android performance sprint** (+2.6%)
6. **Optimize notification channel** (+variable)

### Strategic Recommendations

**Short-term (0-2 weeks)**:
- Emergency fix for S31 -> S41 backend failures
- Add loading indicators for S21 -> S43 issue
- Audit InsureOne/ADIB integrations

**Medium-term (2-8 weeks)**:
- Implement session recovery
- Android performance sprint
- Push notification reminders for expiries
- Document pre-check API for SPs

**Long-term (2-6 months)**:
- SP dashboard with real-time success rates
- Enhanced analytics and monitoring
- Promote redirect channel over notification
- Platform-specific optimizations

---

## Conclusion

The UAE PASS Digital Documents sharing system achieves a **65.6% success rate**, which is **moderate but with clear improvement paths**. The analysis reveals that:

1. **User willingness is NOT the problem** (93% consent, 96% PIN success)
2. **Document retrieval is NOT the problem** (87% success)
3. **The real problems are**:
   - Post-consent UX confusion (7.4% abandonment)
   - Backend technical failures (4.8%)
   - Platform inconsistency (5.4% iOS/Android gap)
   - SP integration quality (35% to 89% range)

By focusing engineering effort on these 4 areas, success rate can realistically improve to **~83%**, representing a **26% increase** in successful shares.

**Key Insight**: Stop optimizing what works (consent, PIN, retrieval). Fix what's actually broken (post-consent UX, backend reliability, Android performance, SP integrations).

---

**Report Date**: 2026-01-09
**Dataset**: 500 requests, 5,068 events
**Analysis Period**: November 1-28, 2025
