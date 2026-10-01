from app.config import get_model, PRO_MODEL
from app.schemas import UserInput


def generate_workout_gemini(user: UserInput) -> str:
    """Gemini Pro: 7-day workout plan."""
    prompt = f"""You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for {user.username}
(age {user.age}, weight {user.weight} kg) whose goal is "{user.goal}" and who prefers
{user.intensity} intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
End with a one-line reminder to consult a doctor before starting.
Use plain text, no markdown symbols."""
    try:
        return get_model(PRO_MODEL).generate_content(prompt).text.strip()
    except Exception as e:
        return f"Error generating workout plan: {e}"
