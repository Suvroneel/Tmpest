"""
ai.py — Intent Extraction Layer for Tmpest
Uses two HuggingFace models (jugad style, no training, no API cost):

1. facebook/bart-large-mnli  -> zero-shot category classification
   (decides if user needs: shelter / food / washroom)

2. dslim/bert-base-NER       -> location entity extraction
   (pulls out place names from the query)
"""

import streamlit as st
from transformers import pipeline

CATEGORY_LABELS = {
    "shelter": "a place to stay, sleep, rent a room, or take shelter",
    "food": "food, meals, or a place to eat",
    "washroom": "a washroom, toilet, or restroom"
}
CATEGORIES = list(CATEGORY_LABELS.values())
LABEL_TO_CATEGORY = {v: k for k, v in CATEGORY_LABELS.items()}


# ── Cache both models so they load once per session, not on every search ─────
@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


@st.cache_resource
def load_ner():
    return pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")


def detect_category(query: str) -> tuple[str, float]:
    """Returns (label, confidence_score) — highest scoring category."""
    classifier = load_classifier()
    result = classifier(query, candidate_labels=CATEGORIES)
    top_label = result["labels"][0]
    return LABEL_TO_CATEGORY[top_label], result["scores"][0]


def extract_location(query: str) -> str | None:
    """Pulls the first location entity (LOC) found in the query, if any."""
    ner = load_ner()
    entities = ner(query)

    locations = [e["word"] for e in entities if e["entity_group"] == "LOC"]
    return locations[0] if locations else None


def extract_budget(query: str) -> int | None:
    """Simple jugad budget extractor — pulls the first number from the query."""
    import re
    numbers = re.findall(r"\d+", query)
    return int(numbers[0]) if numbers else None


def extract_intent(query: str) -> dict:
    """
    Main function called from Tmpest.py
    Takes a raw natural language query and returns structured intent.
    """
    category, score = detect_category(query)
    location = extract_location(query)
    budget = extract_budget(query)

    return {
        "category": category,
        "score": score,
        "location": location,
        "budget": budget,
        "raw_query": query
    }