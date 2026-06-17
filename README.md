# Tmpest

### Find peace when you need it most.

A real-time survival assistance platform that understands what you need and gets you there — built with a natural language search layer powered by Hugging Face NLP models.

---

## Live Demo

📌 https://tmpest.streamlit.app/

![Tmpest Landing Page](front-page-placeholder.png)

---

## Overview

Tmpest helps people locate essential nearby resources — shelter, food, and washrooms — in moments of real need. Unlike traditional discovery platforms built around filters and curated listings, Tmpest is built around a single idea: people in urgent situations don't want to browse, they want to be understood and routed directly to relief.

The platform is built on a simple truth:

Sometimes people don't need options. They need relief, safety, or a place to pause — and they need to be understood in one sentence, not five filters.

---

## The Problem

Tmpest addresses three real gaps in how people access basic resources in unfamiliar or urgent situations:

**Immediate Access Gap**
In unfamiliar or crowded places, people struggle to quickly locate washrooms, safe public facilities, and basic comfort points during urgent moments.

**Affordable Shelter Gap**
Central accommodation is expensive and hard to find on short notice, while spare rooms and unused space within communities remain invisible to the people who need them.

**Immediate Food Access Gap**
People in urgent situations struggle to find affordable meals, open-now food options, and small local or home-based food providers nearby.

---

## How AI Fits In

Tmpest is intentionally not built as a recommendation engine that ranks and curates dozens of options. That model fits booking platforms and marketplaces — it does not fit a survival assistance tool, where the priority is speed and clarity over choice.

Instead, the AI layer in Tmpest exists for one purpose: understanding a messy, natural language description of a situation and routing the user directly to the right place, with relevant context already carried over.

**Example:**

> "Need a cheap place to stay near Park Street tonight"

Rather than asking the user to manually select a category, set filters, and search, Tmpest's intent layer extracts what matters from that single sentence and takes the user straight to the Shelters page — with the location already understood and carried into the next screen.

### Intent Extraction Pipeline

The natural language search box on the landing page is powered by two Hugging Face models, chosen specifically to avoid the cost and complexity of training or running a custom model:

**Category Detection — `facebook/bart-large-mnli`**
A zero-shot classification model determines whether the user's query relates to shelter, food, or washrooms, without requiring any labeled training data specific to this use case.

**Location Extraction — `dslim/bert-base-NER`**
A named entity recognition model identifies location references within the query, which are then carried forward to pre-fill the search context on the destination page.

**Budget Extraction**
A lightweight rule-based extractor identifies numeric budget constraints mentioned in the query.

### Routing Flow

```
User types a natural language query
              |
              v
   Category detected (shelter / food / washroom)
              |
              v
   Location and budget extracted, if present
              |
              v
   Low-confidence or unclear queries are caught
   and the user is asked to rephrase
              |
              v
   User is routed to the matching page
              |
              v
   Destination page reads the extracted context
   and pre-fills the search bar accordingly
```

Manual browsing remains fully intact alongside this flow. Each resource category also has its own dedicated page with a standalone search bar, so a user can choose to browse directly without going through the natural language box at all.

---

## Core Features

### Shelters

A discovery system for affordable, short-term accommodation, built around listings shared directly by community members rather than commercial inventory.

![Shelters Page](shelters-ui-placeholder.png)

### Washrooms

A fast, map-based system that helps users locate nearby washrooms during urgent moments, without requiring any backend listing data.

![Washrooms Page](washrooms-ui-placeholder.png)

### Food

A discovery system for nearby food access, built around the same shared-listing model as Shelters — affordable meals, home-cooked options, and small local providers.

![Food Page](food-ui-placeholder.png)

---

## Share, Not Rent

Tmpest is not a booking platform, a delivery service, or a marketplace. The language used throughout the product is intentionally built around sharing rather than transacting.

People with a spare room or extra food capacity can share it with someone nearby who needs it, rather than listing it for rent in the conventional sense. This distinction matters: Tmpest is not trying to replicate the commercial logic of accommodation or food delivery platforms. It exists to connect real, immediate need with real, immediate availability — between people, not through a marketplace.

---

## System Architecture

```
Tmpest/
├── Tmpest.py                    Landing page with natural language search
├── pages/
│   ├── 1_Shelters.py            Shelter listings and manual search
│   ├── 2_Washrooms.py           Map-based washroom discovery
│   └── 3_Food.py                Food listings and manual search

├── Utils/
│   ├── ai.py                    Intent extraction layer (Hugging Face models)
│   ├── Searchbox.py             Shared styled search component
│   ├── button.py                Shared styled button component
│   ├── title.py                 Shared title, header, and divider components
│   └── section.py                Section layout helpers
├── images/                      Static assets
└── requirements.txt
```

---

## Technology

**Frontend**
Streamlit, with custom CSS for styling and layout.

**AI / NLP**
Hugging Face Transformers — zero-shot classification for intent detection, named entity recognition for location extraction.

**Backend**
Supabase (PostgreSQL) for storing shared listings across Shelters and Food.

**Mapping**
Folium, for washroom discovery.

---

## Design Philosophy

Tmpest is built around a single principle: people in urgent situations should not have to translate their problem into a system's language. The system should understand the problem as stated and respond accordingly.

This shapes every architectural decision in the project — the single search box instead of multi-step filters, the routing-based flow instead of a results dashboard, and the shared-listing model instead of a commercial marketplace structure.

---

## Current Stage

Core natural language routing flow is implemented and functional. Backend integration for shared listings is in progress.

---

## License

This project is open source and available under the MIT License.
