# UAE PASS Digital Vault — "Ask Your Documents" AI Feature BRD

**Document Version**: 1.0
**Date**: 2026-02-17
**Feature Code**: DV-RAG-2026
**Document Owner**: Product Management, Digital Vault
**Stakeholders**: TDRA (Policy/Approval), DDA (Design Approval), ICP (Issuer), Engineering (FE/BE/ML), Legal/Compliance

---

## 1. Executive Summary

### Business Objective
Introduce an AI-powered conversational assistant ("Ask Your Documents") that enables UAE PASS users to query their entire Digital Vault using natural language, instantly retrieving information across all stored documents without manual searching through individual files.

### Value Proposition
- **For Users**: Instant access to critical information (e.g., "When does my visa expire?", "What's my total monthly rent?") without navigating multiple documents
- **For UAE PASS**: First-to-market AI feature in GCC digital identity space, increasing user engagement and reinforcing leadership in digital government services
- **For Service Providers**: Reduced friction in document discovery, enabling more efficient sharing workflows
- **For TDRA**: Demonstrates UAE's commitment to AI-driven government services aligned with national AI strategy

### Key Metrics Target
- **User Adoption**: 25% of active users try feature within 3 months of GA
- **Engagement**: Average 5 queries per user per month
- **Accuracy**: 95%+ factual accuracy on issued documents (eSeal-backed), 85%+ on uploaded documents
- **Performance**: <3s response time for 90th percentile queries
- **Satisfaction**: 4.2+ star rating in in-app feedback

### High-Level Scope
**In Scope**: Natural language queries against user's own documents (issued + uploaded), bilingual EN/AR support, mobile-first UX, privacy-preserving architecture
**Out of Scope**: Cross-user queries, predictive analytics, external data sources, document generation/editing

---

## 2. Use Cases by Document Type

### Emirates ID
| Use Case | Example Query (EN) | Example Query (AR) |
|----------|-------------------|-------------------|
| Expiry check | "When does my Emirates ID expire?" | «متى تنتهي صلاحية هويتي الإماراتية؟» |
| ID number lookup | "What is my Emirates ID number?" | «ما هو رقم هويتي الإماراتية؟» |
| Sponsor info | "Who is my sponsor?" | «من هو كفيلي؟» |
| Nationality | "What nationality is on my EID?" | «ما الجنسية المسجلة في هويتي؟» |
| Date of birth | "What's my date of birth on the EID?" | «ما تاريخ ميلادي في الهوية؟» |

### Passport
| Use Case | Example Query |
|----------|--------------|
| Number lookup | "What is my passport number?" |
| Expiry | "When does my passport expire?" |
| Issuing country | "Which country issued my passport?" |
| Validity | "Is my passport valid for travel?" |

### Residency/Visa
| Use Case | Example Query |
|----------|--------------|
| Visa type | "What type of visa do I have?" |
| Validity period | "When does my residency visa expire?" |
| Sponsor details | "Who sponsors my visa?" |
| Entry permits | "Do I have any entry permit records?" |

### Tenancy Contract (Ejari)
| Use Case | Example Query |
|----------|--------------|
| Rent amount | "What is my current rent?" |
| Contract period | "When does my tenancy contract end?" |
| Landlord details | "Who is my landlord?" |
| DEWA premises | "What is my DEWA premises number?" |
| Payment terms | "How many cheques is my rent split into?" |

### Employment Contract
| Use Case | Example Query |
|----------|--------------|
| Salary | "What is my monthly salary?" |
| Benefits | "What benefits does my contract include?" |
| Notice period | "What's my notice period?" |
| Employer | "Who is my employer?" |
| Start date | "When did my employment start?" |

### Cross-Document Queries (High Value)
| Use Case | Example Query |
|----------|--------------|
| Expiry dashboard | "What documents expire in the next 6 months?" |
| Identity summary | "What's my complete identity summary?" |
| Financial overview | "What are all my monthly financial commitments?" |
| Document inventory | "How many documents do I have and what types?" |
| Renewal planning | "What do I need to renew this quarter?" |

---

## 3. Technical Approaches Comparison

### Option A: On-Device Processing + Cloud LLM (RECOMMENDED)

**Architecture**: OCR + Embeddings + Vector Search on device; only query + top 5 chunks (max 2KB) sent to cloud LLM

| Aspect | Details |
|--------|---------|
| **Privacy** | Documents never leave device |
| **Data Residency** | Only minimal query context to UAE-region cloud |
| **Performance** | 2-3s response time on modern devices |
| **Cost** | ~$100K/year for 1M users |
| **Arabic Support** | GPT-4o-mini has strong Arabic; on-device OCR supports AR |
| **Offline** | Vector search works offline; LLM needs connectivity |

**Stack**: Apple Vision/ML Kit (OCR) + Core ML/TFLite (embeddings) + FAISS (vector search) + Azure OpenAI UAE North (LLM)

### Option B: Hybrid (On-Device Embedding + Cloud Retrieval)

| Aspect | Details |
|--------|---------|
| **Privacy** | Embeddings in cloud (semantic meaning preserved) |
| **Performance** | Faster retrieval, consistent across devices |
| **Cost** | ~$186K/year |
| **Trade-off** | Better performance, weaker privacy |

### Option C: Fully Cloud-Based

| Aspect | Details |
|--------|---------|
| **Privacy** | Full document content in cloud |
| **Performance** | Most consistent, no device variance |
| **Cost** | ~$450K/year |
| **Trade-off** | Simplest client but highest privacy risk |

**Recommendation**: Option A — aligns with UAE PASS's trust-sensitive positioning, 60-78% lower cost, "Your documents stay on your device" messaging.

---

## 4. Phased Rollout

| Phase | Sprints | Scope | Rollout |
|-------|---------|-------|---------|
| **Phase 0**: Pre-Development | 71-72 | PoC, stakeholder approval, user research | Internal |
| **Phase 1**: MVP (Official Docs) | 73-76 | Emirates ID, Passport, Visa queries | 10% users, iOS first |
| **Phase 2**: Expansion | 77-80 | Uploaded docs, voice input | 50% users |
| **Phase 3**: Advanced | 81-84 | Summaries, multilingual, export | 100% GA |
| **Phase 4**: Optimization | 85+ | Fine-tuning, caching, on-device LLM | Ongoing |

---

## 5. Key Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| LLM Hallucination | Critical | Grounding enforcement, citation requirement, confidence scoring |
| TDRA/DDA Approval Delays | High | Early engagement, parallel workstreams |
| Privacy/Data Breach | Critical | On-device processing, TLS+pinning, zero retention |
| Arabic Quality Gaps | Medium | UAE terminology glossary, human eval, Jais model evaluation |
| OCR Quality (Uploaded) | Medium | Quality detection, re-upload prompts, disclaimers |

---

## 6. Success Metrics

**North Star**: AI-Assisted Document Access Rate — 25% by end of Year 1

| Phase | Adoption | Engagement | Accuracy |
|-------|----------|------------|----------|
| Phase 1 | 15% try feature | 3 queries/user/month | <5% inaccuracy reports |
| Phase 2 | 25% active | 5 queries/user/month | <10% (uploaded docs) |
| Phase 3 | 30% monthly users | 15+ for power users | <5% overall |
