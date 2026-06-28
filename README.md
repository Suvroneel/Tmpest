# Tmpest

### Minimum Friction, Maximum Action.

Crisis mode brain can't handle friction. Survi asks minimum, acts maximum. One or two questions max, then gets you there.

---

## Live Demo

📌 https://tmpest.streamlit.app/

---

## Overview

Tmpest helps people locate essential nearby resources — shelter, food, and washrooms — in moments of real need.

Most discovery platforms are built around filters and curated listings. Tmpest is built around a different idea: people in urgent situations don't want to browse. They want to be understood.

The core of Tmpest is **Survi**, a conversational AI companion that replaces the traditional search box entirely. Instead of typing keywords into filters, a user describes their situation in plain language. Survi figures out the rest.

> *"I'm stuck in Jadavpur, I need somewhere to sleep and eat."*

Survi extracts the intent, confirms it, and surfaces shelter and food listings near Jadavpur — together, without separate searches.

---

## The Problem

**Immediate Access Gap**
In unfamiliar or urgent situations, people struggle to find washrooms, safe facilities, and basic comfort points quickly.

**Affordable Shelter Gap**
Short-notice accommodation is expensive and hard to find centrally, while spare rooms in communities remain invisible to people who need them.

**Immediate Food Access Gap**
People in urgent situations struggle to find affordable meals, open-now options, and small local food providers nearby.

---

## How Survi Works

Survi is Tmpest's conversational AI layer. She replaces the search box on the homepage with a full chat interface — activated the moment a user types and hits enter.

### Conversation Flow

```
User types anything → page transforms into chat
         ↓
Survi reads the message
         ↓
Intent extraction runs (category + location + budget)
         ↓
If location missing → Survi asks
If need unclear    → Survi asks
         ↓
Survi confirms: "Got it — you need shelter near Jadavpur. Correct?"
         ↓
User confirms → Survi says "Finding results now."
         ↓
Contextual intro message + mixed listings render below chat
         ↓
Follow-up input stays live
```

### What Makes It Different

Traditional flow:
```
User → Category filter → Location filter → Search → Results
```

Tmpest flow:
```
User describes situation → Survi understands → Results
```

No filters. No navigation. No translating your problem into a system's language.

---

## AI Architecture

### Survi — Conversational Layer (`Utils/tmpest_chat.py`)

- **Model:** Llama 3.1 8B Instruct via Hugging Face Inference API
- **State machine:** `initial → awaiting_confirm → confirmed`
- **Fallback handling:** travel/emergency keywords trigger helpline responses (Kolkata Police: 100, WB Tourism: 1800-345-5555, Kolkata Metro: 033-2229-0000)
- **Stateless by design:** no conversation stored — privacy-first for users in distress

### Intent Extraction Layer (`Utils/ai.py`)

Two Hugging Face models, no training required:

**Category Detection — `facebook/bart-large-mnli`**
Zero-shot classification across shelter / food / washroom. Keyword matching runs first for speed; model handles ambiguous queries.

**Location Extraction — `dslim/bert-base-NER`**
Named entity recognition pulls location references from natural language. Subword artifacts cleaned in post-processing.

**Budget Extraction**
Lightweight regex extracts numeric budget constraints from the query.

### Mixed Results Layer (`Utils/tmpest_results.py`)

After confirmation, Survi surfaces listings across multiple categories for the same location — shelter and food side by side, not on separate pages. Primary category shown first, secondary categories below. Budget filtering applied to primary category.

---

## System Architecture

```
Tmpest/
├── Tmpest.py                    Landing page — header + Survi trigger
├── pages/
│   ├── 1_Shelters.py            Shelter listings with manual search
│   ├── 2_Washrooms.py           Washroom discovery
│   ├── 3_Food.py                Food listings with manual search
│   └── 4_Seller_Section.py      Seller dashboard — create and manage listings

├── Utils/
│   ├── tmpest_chat.py           Survi — full conversational AI layer
│   ├── tmpest_results.py        Mixed multi-category listing renderer
│   ├── ai.py                    Intent extraction (bart-large-mnli + bert-base-NER)
│   ├── listings.py              Listing fetch layer with fuzzy location matching
│   ├── seller_profile.py        Seller profile + listing creation UI
│   ├── auth.py                  Seller signup and login
│   ├── storage.py               Supabase storage — listing images + identity docs
│   ├── supabase_client.py       Shared Supabase client
│   ├── Searchbox.py             Styled search component
│   ├── button.py                Styled button component
│   ├── title.py                 Title, header, and divider components
│   └── section.py              Section layout helpers

├── images/
└── requirements.txt
```

---

## Page Flow

### Landing Page — Survi Chat

User opens Tmpest → types their situation → page transforms into Survi chat interface. Shelter, washroom, and food sections below are hidden during chat (`st.stop()`). User can return to browse mode via "← New Search".

### Shelters / Washrooms / Food

Manual browsing remains fully intact. Each page has its own styled search bar, location filtering, and listing grid — accessible directly without going through Survi.

### Seller Section

Sellers log in or sign up (with identity document upload) and access a dashboard to post listings across Shelter, Food, and Washroom categories. Each listing type has its own tab with relevant fields. Images upload to Supabase Storage.

---

## Seller Model

Tmpest is not a marketplace. Sellers are community members sharing spare rooms, home-cooked meals, or washroom access — not commercial operators. The language throughout is intentionally built around sharing rather than transacting.

---

## Technology

| Layer | Stack |
|---|---|
| Frontend | Streamlit + custom CSS |
| Conversational AI | Llama 3.1 8B Instruct (Hugging Face Inference API) |
| Intent Classification | facebook/bart-large-mnli |
| Location Extraction | dslim/bert-base-NER |
| Backend / Database | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Auth | Supabase Auth |
| Mapping | Folium (future) |

---

## Design Philosophy

People in urgent situations should not have to translate their problem into a system's language. The system should understand the problem as stated and respond accordingly.

This is why Tmpest has no multi-step filters, no category landing pages required, and no results dashboard to browse before finding relief. Survi handles the translation. The user just talks.

---

## Current Stage

Core Survi conversational flow is implemented and functional. Seller listing system is live with Supabase backend. Manual browsing across all three categories is fully operational.

---

## License

MIT License.
