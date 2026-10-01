from app.config import get_model, FLASH_MODEL
from app.nutrition import fallback_tip


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Gemini Flash: one short nutrition/recovery tip."""
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand. Max 2 sentences."
    )
    try:
        return get_model(FLASH_MODEL).generate_content(prompt).text.strip()
    except Exception:
        return fallback_tip(goal)
