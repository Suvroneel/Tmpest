"""
ai.py — Intent Extraction Layer for Tmpest
Uses two HuggingFace models (jugad style, no training, no API cost):

1. facebook/bart-large-mnli  -> zero-shot category classification
2. dslim/bert-base-NER       -> location entity extraction
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

WASHROOM_KEYWORDS = [
    "bathroom", "toilet", "restroom", "loo", "lavatory",
    "washroom", "wc", "w.c", "latrine", "potty"
]

SHELTER_KEYWORDS = [
    "shelter", "room", "stay", "sleep", "rent", "accommodation",
    "lodge", "hostel", "hotel", "pg", "guesthouse"
]

FOOD_KEYWORDS = [
    "food", "eat", "meal", "restaurant", "hunger", "hungry",
    "lunch", "dinner", "breakfast", "snack", "tiffin", "dhaba"
]


@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


@st.cache_resource
def load_ner():
    return pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")


def keyword_match(query: str) -> str | None:
    q = query.lower()
    for kw in WASHROOM_KEYWORDS:
        if kw in q:
            return "washroom"
    for kw in SHELTER_KEYWORDS:
        if kw in q:
            return "shelter"
    for kw in FOOD_KEYWORDS:
        if kw in q:
            return "food"
    return None


def detect_category(query: str) -> tuple[str, float]:
    keyword_result = keyword_match(query)
    if keyword_result:
        return keyword_result, 1.0
    classifier = load_classifier()
    result = classifier(query, candidate_labels=CATEGORIES)
    top_label = result["labels"][0]
    return LABEL_TO_CATEGORY[top_label], result["scores"][0]


def extract_location(query: str) -> str | None:
    ner = load_ner()
    entities = ner(query)
    locations = [e["word"] for e in entities if e["entity_group"] == "LOC"]
    if not locations:
        return None
    full_location = " ".join(locations)
    # Clean BERT subword tokens like ##vpur
    full_location = full_location.replace(" ##", "").replace("##", "")
    return full_location


def extract_budget(query: str) -> int | None:
    import re
    numbers = re.findall(r"\d+", query)
    return int(numbers[0]) if numbers else None


def extract_intent(query: str) -> dict:
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