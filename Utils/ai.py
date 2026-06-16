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

CATEGORIES = ["shelter", "food", "washroom"]


# ── Cache both models so they load once per session, not on every search ─────
@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


@st.cache_resource
def load_ner():
    return pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)


def detect_category(query: str) -> str:
    """Returns one of: shelter / food / washroom"""
    classifier = load_classifier()
    result = classifier(query, candidate_labels=CATEGORIES)
    return result["labels"][0]  # highest scoring label


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
    category = detect_category(query)
    location = extract_location(query)
    budget = extract_budget(query)

    return {
        "category": category,
        "location": location,
        "budget": budget,
        "raw_query": query
    }