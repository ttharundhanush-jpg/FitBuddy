"""Optional nutrition helpers (kept separate from the AI calls)."""

FALLBACK_TIPS = {
    "weight loss": "Prioritise protein and vegetables at each meal to stay full.",
    "muscle gain": "Include protein in your post-workout meal.",
}


def fallback_tip(goal: str) -> str:
    return FALLBACK_TIPS.get(goal.lower(), "Stay hydrated and get 7-8 hours of sleep.")
