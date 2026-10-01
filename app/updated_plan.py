from app.config import get_model, PRO_MODEL


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """Revise a plan with AI, preserving it if the AI service is unavailable."""
    prompt = f"""You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan.
Keep the format and the rest of the plan unchanged if not needed. Use plain text."""
    try:
        return get_model(PRO_MODEL).generate_content(prompt).text.strip()
    except Exception:
        return (
            f"{original_plan}\n\n"
            "Update unavailable: the AI service could not process your feedback. "
            "The original plan is unchanged. Feedback to apply when the service is available: "
            f"{user_feedback}"
        )
