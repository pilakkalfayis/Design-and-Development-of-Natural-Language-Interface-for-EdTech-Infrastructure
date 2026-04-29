# EdTech Chatbot

An AI-powered academic assistant for college students. Modern chat UI built
with **Streamlit**. Powered by a **hybrid intent engine** — fast keyword
matching for common questions and a free **Llama 3.3 70B** LLM (via Groq)
for everything else.

## Features

- Modern chat UI: dark sidebar, profile card, gradient header, side-tab
  message bubbles, compact chip shortcuts above the input.
- Hybrid AI: rule-based handler for the eight common intents, LLM
  fallback for free-form questions.
- Context-aware AI: the student's data is sent to the LLM as system
  context so answers stay factual.
- Free to run: Groq API has a generous free tier — no credit card.
- Also runs as a CLI: `python chatbot.py`.

## Setup

```bash
pip install -r requirements.txt
```

Get a free Groq API key at <https://console.groq.com> (Google sign-in,
no credit card). Then:

```bash
copy .env.example .env       # Windows
cp .env.example .env         # macOS / Linux
```

Edit `.env` and paste your key:

```
GROQ_API_KEY=gsk_your_real_key_here
```

> The app still works without a key — it just disables the AI fallback.

## Run

```bash
streamlit run app.py
```

Browser opens at <http://localhost:8501>.

## Example Questions

### Rule-based (instant, free)
- `courses`
- `grades`
- `attendance`
- `fees`
- `pending assignments`
- `status`

### AI-powered (uses Llama 3.3 via Groq)

**About the student's data:**
- *Which subject am I weakest in?*
- *Should I worry about CS405?*
- *Summarise my academic performance in 3 bullets.*
- *Plan a 3-day study schedule for my pending assignments.*

**About computer-science topics (study help):**
- *Explain CSS Flexbox in simple terms.*
- *What is the difference between CSS `flex` and `grid`?*
- *How does CSS specificity work? Give an example.*
- *What is the box model in CSS?*
- *Difference between `position: absolute` and `position: fixed`?*
- *Explain CSS pseudo-classes vs pseudo-elements.*
- *What are CSS variables and how do I use them?*

**General CS:**
- *Explain Big O notation.*
- *What is normalisation in DBMS? When do you stop at 3NF?*
- *Difference between TCP and UDP.*

## Project Layout

```
edtech-chatbot/
├── app.py              # Streamlit UI
├── chatbot.py          # rule-based engine + CLI
├── llm.py              # Groq LLM wrapper
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml
└── docs/
    ├── 01-Proposal.md
    ├── 02-HLD.md
    ├── 03-LLD.md
    └── 04-Final-Report.md
```
