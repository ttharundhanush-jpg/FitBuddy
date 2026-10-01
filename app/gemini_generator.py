from app.config import get_model, PRO_MODEL
from app.schemas import UserInput


def _offline_workout_plan(user: UserInput) -> str:
    rounds = {"low": 2, "medium": 3, "high": 3}.get(user.intensity, 2)
    walk_minutes = {"low": 20, "medium": 30, "high": 35}.get(user.intensity, 20)
    return f"""Starter plan (AI service unavailable)
Goal: {user.goal} | Intensity: {user.intensity}

Day 1: Full body
Warm-up: 5 minutes of easy marching and shoulder circles.
Main workout: {rounds} rounds of 8-10 sit-to-stands, 6-10 wall or counter push-ups, 10 glute bridges, and 6 bird dogs per side. Rest as needed.
Cooldown: 5 minutes of gentle leg and chest stretches.

Day 2: Active recovery
Warm-up: 5 minutes of easy walking.
Main workout: Walk at a comfortable pace for {walk_minutes} minutes.
Cooldown: Gentle calf and hip stretches.

Day 3: Lower body
Warm-up: 5 minutes of easy marching.
Main workout: {rounds} rounds of 8 sit-to-stands, 10 glute bridges, and 10 calf raises. Hold a chair for balance if needed.
Cooldown: 5 minutes of gentle lower-body stretches.

Day 4: Recovery
Warm-up: 3 minutes of easy movement.
Main workout: 10-15 minutes of comfortable mobility or an easy walk.
Cooldown: Relaxed breathing and gentle stretching.

Day 5: Upper body and core
Warm-up: 5 minutes of shoulder circles and easy marching.
Main workout: {rounds} rounds of 6-10 wall or counter push-ups, 8 backpack rows, and 6 dead bugs per side.
Cooldown: 5 minutes of gentle chest and back stretches.

Day 6: Easy activity
Warm-up: 5 minutes at an easy pace.
Main workout: Choose a comfortable walk, cycling, or other enjoyable movement for 15-25 minutes.
Cooldown: Gentle stretching.

Day 7: Rest
Take a rest day or do a few minutes of gentle mobility.

Stop if you feel pain or unwell, and consult a healthcare professional before starting a new exercise routine."""


def generate_workout_gemini(user: UserInput) -> str:
    """Generate a 7-day plan, with an offline starter plan if AI is unavailable."""
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
    except Exception:
        return _offline_workout_plan(user)
