from app.config import get_model, FLASH_MODEL


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Gemini Flash: one short nutrition/recovery tip."""
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand. Max 2 sentences."
    )
    try:
        return get_model(FLASH_MODEL).generate_content(prompt).text.strip()
    except Exception as e:
        return f"Error generating tip: {e}"
