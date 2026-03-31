# SP-Specific Action Items & Recommendations

**Generated**: 2026-01-09
**Purpose**: Actionable fixes for each problematic Service Provider

---

## Priority Matrix

| Priority | SP | Success Rate | Impact | Effort | ROI |
|----------|----|--------------:|--------|--------|-----|
| 🔥 **P0** | InsureOne | 36% | Very High | Medium | ★★★★★ |
| 🔥 **P0** | ADIB | 37% | High | High | ★★★★☆ |
| 🚨 **P1** | Beyon Money | 58% | Medium | Low | ★★★★☆ |
| 🚨 **P1** | NBF | 55% | Medium | Low | ★★★☆☆ |
| 🚨 **P1** | National Bonds | 54% | Medium | Low | ★★★★☆ |
| ⚠️ **P2** | Baraka | 57% | Medium | Medium | ★★★☆☆ |
| ⚠️ **P2** | Etisalat Business | 62% | Medium | Medium | ★★★☆☆ |
| ⚠️ **P2** | Arab Bank | 61% | Low | Low | ★★☆☆☆ |

---

## 🔥 PRIORITY 0 - CRITICAL (Fix This Sprint)

### InsureOne (Premier Insurance Brokers) - 36% Success

**Current State**:
- Success Rate: 36% (10/28)
- User Abort Rate: 36% (10/28) - **HIGHEST IN DATASET**
- Technical Errors: 11% (3/28)
- Volume: 28 requests (10th highest)

**Primary Issue**: S32 Post-PIN Processing Stuck State

**Symptoms**:
- Users successfully enter PIN (reach S31)
- Abandon at S32 (post-PIN validation/document packaging)
- 36% of all users get stuck here
- Average 28 days to failure (users retry multiple times)

**Root Causes**:
1. **Backend Processing Delay**: S32→S40 taking too long (timeout or actual processing)
2. **Lack of User Feedback**: No progress indicator, users see spinner indefinitely
3. **DV Backend Errors**: 3 errors suggest integration quality issues
4. **Document Packaging Issues**: Complex document requirements causing validation delays

**Recommended Fixes**:

#### Fix 1: Profile S32 Latency (Week 1)
- **Owner**: Backend Engineering
- **Actions**:
  - Add instrumentation to S32 processing
  - Measure time spent in: document retrieval, validation, packaging, eSeal verification
  - Identify bottleneck (likely issuer API call or eSeal validation)
- **Success Criteria**: Latency profile showing >5s delay = problem identified

#### Fix 2: Add Progress Indicators (Week 1)
- **Owner**: Frontend + UX
- **Actions**:
  - Replace generic spinner with step-by-step progress:
    - "Retrieving documents..." (S31→S32)
    - "Validating documents..." (S32 validation)
    - "Preparing secure package..." (S32 packaging)
    - "Almost ready..." (S32→S40)
  - Add estimated time remaining if possible
  - Add timeout escape hatch: "Taking longer than usual? [Try Again] [Cancel]"
- **Success Criteria**: Users see what's happening, abort rate drops

#### Fix 3: Optimize Backend Processing (Week 2)
- **Owner**: Backend Engineering
- **Actions**:
  - Parallelize document retrieval calls (don't fetch sequentially)
  - Cache eSeal validation results (don't re-verify same document)
  - Implement request-level timeout of 30s (fail fast if stuck)
  - Add retry logic for transient DV errors
- **Success Criteria**: S32 avg processing time <10s

#### Fix 4: Simplify Document Requirements (Week 2)
- **Owner**: Product + InsureOne Partnership Team
- **Actions**:
  - Review InsureOne's required_docs list
  - Are they requesting rare/complex documents?
  - Propose removing non-critical documents from default request
  - Test with InsureOne: does reducing scope improve success?
- **Success Criteria**: Reduced required_count → faster S32 processing

**Expected Impact**:
- Success Rate: 36% → **65%** (+29pp)
- At scale (28 req/week): +8 successful shares/week
- User satisfaction: High (no more stuck states)

**Timeline**: 2 weeks
**Stakeholders**: TDRA, DDA (UX approval), InsureOne partnership team, Engineering

---

### ADIB (Abu Dhabi Islamic Bank) - 37% Success

**Current State**:
- Success Rate: 37% (7/19)
- User Abort Rate: 26% (5/19) - **2ND HIGHEST**
- Expiry Rate: 21% (4/19) - **HIGHEST IN DATASET**
- Not Eligible Rate: 11% (2/19) - **2ND HIGHEST**
- Volume: 19 requests

**Primary Issues**:
1. **Futile Requests**: 11% of users don't have required documents (S44)
2. **Early Abandonment**: Users abort at S10 (document availability check)
3. **Slow/Confusing Journeys**: 21% expiry suggests users struggle, give up

**Symptoms**:
- Stuck at S10: Users see "checking documents" then abandon
- 26% abort even when documents are available
- Long average journey time (21 days)

**Root Causes**:
1. **No Pre-Check**: ADIB creates requests before checking document availability
2. **Poor S10 UX**: Document check screen is confusing or slow
3. **Overwhelming Document Requirements**: Consent screen scares users off
4. **Timeout Too Long**: Users abandon, request sits open, eventually expires

**Recommended Fixes**:

#### Fix 1: Implement Document Pre-Check API (Week 1-2)
- **Owner**: Backend Engineering + Product
- **Actions**:
  - Build `/v1/check-eligibility` endpoint
  - Input: user_id + required_docs list
  - Output: { eligible: true/false, missing_docs: [...] }
  - ADIB calls BEFORE creating sharing request
  - If not eligible, show "Missing documents" screen with list
  - Block request creation if user lacks documents
- **Success Criteria**: Zero S44 failures, 11% waste eliminated

#### Fix 2: Redesign S10 Screen (Week 1)
- **Owner**: DDA + Frontend
- **Actions**:
  - Replace generic "Checking documents..." with:
    - ✓ Emirates ID - Found
    - ✓ Passport - Found
    - ⊗ Bank Statement - Not available
  - Add "What happens next" explanation
  - Add "Why we need these" tooltips
  - Reduce perceived wait time with instant results (if pre-check implemented)
- **Success Criteria**: S10 abandonment <10%

#### Fix 3: Consent Screen Optimization (Week 2)
- **Owner**: DDA + UX Research
- **Actions**:
  - Simplify document requirement display:
    - Before: Long list with legal descriptions
    - After: Icons + short names + expandable details
  - Add trust signals: "Secure", "TDRA Approved", "ADIB Partner Badge"
  - Test "Why we need this" messaging variations
  - A/B test: Simplified vs Current consent screen
- **Success Criteria**: Consent conversion (S20→S21) >85%

#### Fix 4: Reduce Expiry Timeout (Week 2)
- **Owner**: Backend Engineering
- **Actions**:
  - Current timeout seems too long (21 day avg journey time)
  - Reduce to 15 minutes active session
  - Add session recovery: "Your previous request expired. [Try Again]"
  - Monitor expiry rate after change
- **Success Criteria**: Expiry rate <10%

#### Fix 5: ADIB-Specific UX Audit (Week 3)
- **Owner**: UX Research + Product
- **Actions**:
  - Schedule user testing with 10 ADIB customers
  - Screen-by-screen walkthrough
  - Identify friction points (likely S10, S20, consent screen)
  - Document pain points and confusion areas
  - Create prioritized fix list
- **Success Criteria**: Validated hypotheses, user feedback captured

**Expected Impact**:
- Success Rate: 37% → **65%** (+28pp)
- At scale (19 req/week): +5 successful shares/week
- Reduced waste: 2 futile requests/week eliminated

**Timeline**: 3 weeks
**Stakeholders**: TDRA, DDA, ADIB partnership team, Engineering, UX Research

---

## 🚨 PRIORITY 1 - HIGH (Fix This Month)

### Beyon Money - 58% Success

**Current State**:
- Success Rate: 58% (14/24)
- Expiry Rate: 21% (5/24) - **2ND HIGHEST**
- Technical Errors: 8% (2/24)
- Volume: 24 requests

**Primary Issue**: High Expiry Rate (Long/Stuck Journeys)

**Recommended Fixes**:

#### Fix 1: Profile Journey Time for Expired Requests
- **Owner**: Data Analytics + Engineering
- **Actions**:
  - Analyze all 5 expired requests (request_ids)
  - Map status progression: where did they spend time?
  - Identify stuck states (e.g., S20→S21 taking 10 minutes)
  - Check for backend delays or user inactivity
- **Success Criteria**: Bottleneck identified

#### Fix 2: Optimize Slow States
- **Owner**: Engineering
- **Actions**:
  - If S20→S21 slow: pre-load PIN screen in background
  - If S31→S32 slow: implement fixes from InsureOne (see above)
  - If user inactivity: add "Still there?" prompt after 2 min
- **Success Criteria**: Avg journey time <90 seconds

#### Fix 3: Add Progress Persistence
- **Owner**: Frontend + Backend
- **Actions**:
  - If user backgrounds app, save progress
  - When returning, resume from last state (don't restart)
  - Reduce perceived friction of multi-step process
- **Success Criteria**: Expiry rate <12%

**Expected Impact**:
- Success Rate: 58% → **72%** (+14pp)
- At scale: +3 successful shares/week

**Timeline**: 2 weeks

---

### National Bank of Fujairah (NBF) - 55% Success

**Current State**:
- Success Rate: 55% (12/22)
- User Abort Rate: 18% (4/22)
- Expiry Rate: 18% (4/22)
- Stuck at: **S06 (Pre-consent screen)**

**Primary Issue**: Users Abandon Before Seeing Consent (S06)

**Recommended Fixes**:

#### Fix 1: Audit S06 Screen Design
- **Owner**: DDA + UX
- **Actions**:
  - S06 is "Preparing consent screen" loading state
  - If taking >3 seconds, users abort
  - Optimize consent screen load time:
    - Pre-cache SP logo/branding
    - Pre-load document icons
    - Reduce API calls before S06→S20
  - Add skeleton screen (not blank spinner)
- **Success Criteria**: S06 load time <2 seconds

#### Fix 2: Improve Entry Point Messaging
- **Owner**: Product + NBF Partnership
- **Actions**:
  - Review notification copy for NBF requests
  - Does it clearly explain what will happen?
  - Test: "Share your documents with NBF" vs "NBF needs your ID"
  - Add NBF logo/branding in notification
- **Success Criteria**: S06 abandonment <10%

#### Fix 3: Test Trust Signals
- **Owner**: UX Research
- **Actions**:
  - A/B test: Add "Approved by TDRA" badge at S06
  - Test: Show progress indicator "Step 1 of 3" at S06
  - Measure impact on abandon rate
- **Success Criteria**: S06→S20 conversion >90%

**Expected Impact**:
- Success Rate: 55% → **70%** (+15pp)
- At scale: +3 successful shares/week

**Timeline**: 2 weeks

---

### National Bonds Corporation - 54% Success

**Current State**:
- Success Rate: 54% (14/26)
- User Abort Rate: 23% (6/26) - **4TH HIGHEST**
- Stuck at: **S21 (Post-consent, pre-PIN)**

**Primary Issue**: Users Consent But Don't Enter PIN

**Recommended Fixes**:

#### Fix 1: Streamline S21→S30 Transition
- **Owner**: Frontend + UX
- **Actions**:
  - Remove any intermediate screens between consent confirm and PIN prompt
  - Current flow likely: S20 → [Consent] → S21 → [?] → S30
  - New flow: S20 → [Consent + "Next: Enter PIN"] → S30 immediately
  - Add messaging at S21: "Great! Now enter your PIN to complete"
- **Success Criteria**: S21→S30 conversion >95%

#### Fix 2: Test PIN Prompt Copy
- **Owner**: UX Research
- **Actions**:
  - A/B test PIN prompt variations:
    - A: "Enter your UAE PASS PIN"
    - B: "One last step: Enter your PIN to securely share documents"
    - C: "Verify with PIN (last step!)"
  - Measure which reduces abandonment
- **Success Criteria**: S30 abandonment <10%

#### Fix 3: Pre-Load PIN Screen
- **Owner**: Frontend Engineering
- **Actions**:
  - While user is reviewing consent (S20), pre-load PIN screen in background
  - When they tap "Approve", transition instantly (no delay)
  - Reduce perceived friction
- **Success Criteria**: S21→S30 latency <1 second

**Expected Impact**:
- Success Rate: 54% → **70%** (+16pp)
- At scale: +4 successful shares/week

**Timeline**: 1 week

---

## ⚠️ PRIORITY 2 - MEDIUM (Fix This Quarter)

### Baraka - 57% Success

**Current State**:
- Success Rate: 57% (13/23)
- Multiple failure modes (no single dominant issue)

**Recommended Fixes**:
1. **Consent Screen UX Audit**: Test simplified version
2. **Error Handling Improvements**: 2 DV backend errors need investigation
3. **Platform Testing**: Ensure iOS and Android parity

**Expected Impact**: 57% → 70% (+13pp)
**Timeline**: 3 weeks

---

### Etisalat Business - 62% Success

**Current State**:
- Success Rate: 62% (8/13)
- Technical Errors: 23% (3/13) - **HIGHEST IN DATASET**
- Error Source: **2 network errors** (15% of requests!)

**Primary Issue**: Network Instability

**Recommended Fixes**:

#### Fix 1: Implement Request Retry Logic
- **Owner**: Backend Engineering
- **Actions**:
  - Wrap Etisalat Business API calls in retry decorator
  - 3 attempts with exponential backoff (1s, 2s, 4s)
  - If all fail, return actionable error to user
  - Log retry attempts for monitoring
- **Success Criteria**: Network error rate <5%

#### Fix 2: Add Connection Pooling
- **Owner**: Backend Engineering
- **Actions**:
  - Reuse TCP connections to Etisalat Business endpoints
  - Reduce connection overhead
  - Implement connection health checks
- **Success Criteria**: Request latency reduced 20%

#### Fix 3: Circuit Breaker Pattern
- **Owner**: Backend Engineering
- **Actions**:
  - If Etisalat Business API fails >50% in 5 min window, open circuit
  - Return friendly error to users: "Etisalat Business temporarily unavailable"
  - Alert ops team for investigation
  - Auto-retry after 5 min cooldown
- **Success Criteria**: Graceful degradation during outages

**Expected Impact**:
- Success Rate: 62% → **80%** (+18pp)
- Network errors: 23% → **5%** (retry logic absorbs failures)

**Timeline**: 2 weeks

---

### Arab Bank - 61% Success

**Current State**:
- Success Rate: 61% (14/23)
- Issuer Errors: 3 cases - **HIGHEST IN DATASET**
- Not Eligible Rate: 9% (2/23)

**Primary Issue**: Issuer Document Retrieval Failures

**Recommended Fixes**:

#### Fix 1: Implement Issuer Retry Logic
- **Owner**: Backend Engineering
- **Actions**:
  - When S12→S13 issuer call fails, retry 3x
  - Wait 2s between attempts (give issuer time to recover)
  - If all fail, return error to user with "Try again later" option
- **Success Criteria**: Issuer error rate <2%

#### Fix 2: Cache Successful Issuer Responses
- **Owner**: Backend Engineering
- **Actions**:
  - If issuer returns document successfully, cache for 5 min
  - If same user retries within 5 min, use cached response
  - Reduce load on issuer APIs
- **Success Criteria**: Faster S12→S13 transition, fewer issuer errors

#### Fix 3: Add Document Pre-Check
- **Owner**: Product
- **Actions**:
  - Prevent 9% S44 failures by checking doc availability upfront
  - (See ADIB Fix 1 for implementation details)
- **Success Criteria**: Zero S44 failures

**Expected Impact**:
- Success Rate: 61% → **75%** (+14pp)

**Timeline**: 2 weeks

---

## 📊 SYSTEM-WIDE IMPROVEMENTS

### 1. Document Pre-Check API (All SPs)

**Problem**: 2.4% of all requests are futile (S44 - Not Eligible)

**Solution**:
- Build `/v1/check-eligibility` endpoint
- SPs call BEFORE creating sharing request
- Returns: eligible (true/false) + missing_docs list
- Block request creation if user lacks required docs

**Impact**:
- Eliminate 12 futile requests in sample (2.4%)
- At 350K requests/week: **8,400 futile requests/week eliminated**
- Improved user experience (no "document not found" errors)
- Reduced backend processing load

**Effort**: 2 weeks (Engineering + QA)
**Priority**: 🔥 P0 (affects multiple SPs)

---

### 2. Consent Screen A/B Testing Program

**Problem**: Consent conversion varies wildly (67% InsureOne → 95% FAB)

**Solution**:
- Create 3 consent screen variants:
  - **A (Current)**: Detailed legal text + full document list
  - **B (Simplified)**: Icons + short names + "Learn more" expandable
  - **C (Progressive)**: Show only document names, hide details unless requested
- A/B test across all SPs for 2 weeks
- Measure: consent conversion (S20→S21)
- Roll out winner to all SPs

**Impact**:
- If variant B wins, apply to InsureOne → +18% consent conversion
- System-wide: +5-10% success rate

**Effort**: 3 weeks (DDA design + Frontend + QA + Analytics)
**Priority**: 🚨 P1

---

### 3. SP Health Monitoring Dashboard

**Problem**: No real-time visibility into SP-specific issues

**Solution**:
- Build Grafana/Tableau dashboard showing per-SP:
  - Success rate (last hour, day, week)
  - User abort rate
  - Technical error rate
  - Expiry rate
  - Most common stuck status
  - Avg journey time
- Alert thresholds:
  - Success <60% for 1 hour → Slack alert
  - Tech errors >10% for 30 min → PagerDuty
  - Zero successful shares for 3 hours → Critical alert

**Impact**:
- Catch SP issues in real-time (not post-mortem)
- Faster incident response
- Prevent user frustration

**Effort**: 1 week (Data Engineering + DevOps)
**Priority**: 🚨 P1

---

### 4. Journey Time Optimization

**Problem**: Slow journeys → high expiry rates (21% for ADIB/Beyon)

**Solution**:
- Profile latency at each status transition:
  - S00→S08: App launch + notification load
  - S08→S20: Consent screen load
  - S20→S21: User decision time (can't optimize)
  - S21→S30: PIN screen load
  - S30→S31: PIN validation
  - S31→S32: Document retrieval
  - S32→S40: Document packaging + eSeal
- Identify slowest transitions (target: >5s)
- Optimize:
  - Pre-load next screen in background
  - Parallelize API calls
  - Cache static assets (SP logos, icons)
  - Implement lazy loading

**Impact**:
- Reduce avg journey time from 60s → 30s
- Reduce expiry rate from 9.4% → 5%

**Effort**: 2 weeks (Frontend + Backend)
**Priority**: ⚠️ P2

---

## 🎯 Success Metrics

### Per-SP Targets

| SP | Current | 1-Month Target | 3-Month Target |
|----|--------:|---------------:|---------------:|
| InsureOne | 36% | 60% | 75% |
| ADIB | 37% | 60% | 75% |
| Beyon Money | 58% | 70% | 80% |
| NBF | 55% | 70% | 80% |
| National Bonds | 54% | 70% | 80% |
| Baraka | 57% | 70% | 80% |
| Etisalat Business | 62% | 75% | 85% |
| Arab Bank | 61% | 75% | 85% |

### System-Wide Targets

| Metric | Current | 1-Month Target | 3-Month Target |
|--------|--------:|---------------:|---------------:|
| Overall Success Rate | 65.6% | 72% | 78% |
| User Abort Rate | 17.8% | 12% | 8% |
| Tech Error Rate | 4.8% | 3% | 2% |
| Expiry Rate | 9.4% | 7% | 5% |
| Not Eligible Rate | 2.4% | 1% | 0% |
| Avg Journey Time | 60s | 45s | 30s |

---

## 📅 Implementation Timeline

### Week 1 (Immediate)
- [ ] InsureOne S32 latency profiling
- [ ] InsureOne progress indicator implementation
- [ ] ADIB document pre-check API design
- [ ] NBF S06 screen audit
- [ ] National Bonds S21→S30 streamlining

### Week 2
- [ ] InsureOne backend optimization
- [ ] ADIB pre-check API implementation
- [ ] ADIB S10 screen redesign
- [ ] Beyon Money journey time analysis
- [ ] Etisalat Business retry logic

### Week 3-4
- [ ] ADIB consent screen A/B test
- [ ] ADIB UX audit with real users
- [ ] System-wide consent screen testing
- [ ] SP health monitoring dashboard
- [ ] Arab Bank issuer retry logic

### Month 2-3
- [ ] Roll out winning consent screen variant
- [ ] Journey time optimization (all SPs)
- [ ] Document pre-check API (all SPs)
- [ ] Platform parity testing (iOS vs Android)
- [ ] Continuous monitoring + iteration

---

## 🤝 Stakeholder Engagement Plan

### TDRA (Product Owner)
- **Week 1**: Present findings, get buy-in for top 3 priorities
- **Weekly**: Status update on P0 fixes
- **Monthly**: Review metrics dashboard, adjust priorities

### DDA (Design Authority)
- **Week 1**: Request UX design approval for:
  - InsureOne progress indicators
  - ADIB S10 + consent screen redesigns
  - NBF S06 screen
- **Week 2**: Review and iterate on designs
- **Week 3**: Approve final designs for implementation

### SP Partnership Teams
- **Week 1**: Schedule calls with InsureOne, ADIB, NBF, National Bonds
- **Present findings**: "Your integration has X issue, here's the fix"
- **Get buy-in**: Some fixes require SP-side changes (e.g., pre-check API adoption)
- **Coordinate testing**: SP-specific QA before rollout

### Engineering Teams
- **Week 1**: Assign owners for each fix (see fix details above)
- **Daily standups**: Track progress on P0 items
- **Weekly**: Demo completed fixes to stakeholders

### QA Team
- **Week 2**: Test InsureOne fixes with 10 users
- **Week 3**: Test ADIB fixes with 10 users
- **Week 4**: Regression testing (ensure fixes don't break other SPs)

---

## 📈 Monitoring & Iteration

### Real-Time Monitoring (Post-Launch)
- Monitor SP health dashboard daily
- Watch for:
  - Regressions (success rate drops after fix)
  - New issues (different failure modes emerge)
  - User feedback (support tickets, app reviews)

### Weekly Review
- Review success rate trends per SP
- Identify new problem SPs (data-driven)
- Adjust priorities based on impact

### Monthly Retrospective
- Did fixes achieve target success rates?
- What worked well? What didn't?
- New insights from user research?
- Update action items for next month

---

## 🎓 Lessons Learned (Proactive)

### For Future SP Onboarding
- **Mandatory**: Document pre-check API integration
- **Mandatory**: UX testing with 10 users before production
- **Mandatory**: Platform parity testing (iOS + Android)
- **Required**: Consent screen must meet <15% abandon target in testing
- **Required**: Avg journey time <45s in testing
- **Required**: Success rate >70% in pilot (100 requests)

### Integration Quality Checklist
- [ ] SP has tested with 10 real users
- [ ] Success rate >70% in pilot
- [ ] User abort rate <15%
- [ ] Tech error rate <5%
- [ ] Avg journey time <45s
- [ ] iOS and Android performance parity (<5pp gap)
- [ ] Document pre-check API integrated
- [ ] Error handling implemented (retry logic, timeouts)
- [ ] Progress indicators on all slow operations (>2s)

---

**Document Owner**: Product Team
**Last Updated**: 2026-01-09
**Next Review**: 2026-01-16 (weekly)
