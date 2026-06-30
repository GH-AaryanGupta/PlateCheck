# PlateCheck

**AI-powered, accessible nutrition guidance for anyone who can't afford or conveniently access a dietitian.**

PlateCheck lets users snap a photo of a meal and get an instant nutritional breakdown, chat with a personalized AI nutrition assistant ("Ronnie AI"), and track daily macros against goals calculated from their own profile — all without manual food logging.

## Features

- **Account system** — simple username/password sign-up, no email required
- **Profile-based targets** — BMI, BMR (Mifflin-St Jeor), TDEE, and daily macro targets calculated from age, weight, height, goal, and activity level
- **Photo-based meal logging** — upload a food photo and get calories, protein, carbs, fat, fiber, and sugar estimated by a vision model
- **Ronnie AI** — a context-aware chatbot that knows your live profile, today's logged macros, and remaining calorie budget, so you don't have to repeat yourself every message
- **Dashboard** — daily macro progress, meal journal, and a logging streak
- **BMI calculator** — standalone quick-check tool, no data stored
- **Admin panel** — full visibility into users, profiles, daily logs, uploaded images, and chat history

---

## Tech Stack

| Component           | Technology                          |
|---------------------|-------------------------------------|
| Backend framework   | Django 6.0                          |
| Database            | PostgreSQL (production)             |
| AI inference        | Groq API                            |
| Vision model        | `meta-llama/llama-4-scout-17b`      |
| Chat model          | `llama-3.3-70b-versatile`           |
| Image handling      | Pillow                              |