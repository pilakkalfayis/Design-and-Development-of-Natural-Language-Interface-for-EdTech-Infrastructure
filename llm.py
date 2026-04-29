"""LLM fallback (Groq + Llama 3.3 70B) used when the rule-based matcher
cannot classify the user's query. The student profile is injected as
system context so factual answers stay grounded in real data."""

import os
from groq import Groq

import chatbot as cb

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def _build_student_context():
    courses = "\n".join(
        f"  - {c} {t} ({cr} credits)" for c, t, cr in cb.COURSES
    )
    grades = "\n".join(
        f"  - {c} {t}: {g}" for c, t, g in cb.GRADES
    )
    attendance = "\n".join(
        f"  - {c}: {a}/{t} ({a / t * 100:.1f}%)"
        for c, a, t in cb.ATTENDANCE
    )
    assignments = "\n".join(
        f"  - {c} {t} (due {d}, {s})"
        for c, t, d, s in cb.ASSIGNMENTS
    )
    fees = (
        f"  - Total: Rs.{cb.FEES['total']}, Paid: Rs.{cb.FEES['paid']}, "
        f"Due: Rs.{cb.FEES['due']} by {cb.FEES['due_date']}"
    )
    return (
        f"STUDENT PROFILE\n"
        f"  Name: {cb.STUDENT['name']}\n"
        f"  Roll No: {cb.STUDENT['roll_no']}\n"
        f"  Program: {cb.STUDENT['program']}\n"
        f"  Semester: {cb.STUDENT['semester']}\n\n"
        f"COURSES\n{courses}\n\n"
        f"GRADES\n{grades}\n\n"
        f"ATTENDANCE\n{attendance}\n\n"
        f"FEES\n{fees}\n\n"
        f"ASSIGNMENTS\n{assignments}"
    )


SYSTEM_PROMPT = f"""You are an EdTech assistant chatbot for a Computer Science student.

You can help with two kinds of questions:

1. STUDENT-DATA QUESTIONS — about the student's courses, grades, attendance,
   fees and assignments. Always base these on the data given below; never
   invent information; if the data does not contain the answer, say so.

2. STUDY QUESTIONS — general academic / programming / computer-science
   topics (algorithms, OOP, databases, networks, web development including
   HTML/CSS/JavaScript, software engineering, etc.). Answer these like a
   helpful tutor: clear explanation first, small example second.

Style rules:
- Use Markdown (bullets, bold, fenced code blocks for code).
- Be concise — under 250 words unless the user asks for detail.
- Address the student by their first name when natural.

{_build_student_context()}
"""


def is_configured():
    return bool(os.getenv("GROQ_API_KEY"))


def ask_llm(user_message, history=None, model=DEFAULT_MODEL):
    if not is_configured():
        return (
            ":warning: **LLM is not configured.**\n\n"
            "I couldn't find a `GROQ_API_KEY` in the environment, so I can't "
            "answer free-form questions yet. You can still use the built-in "
            "commands like `courses`, `grades`, `attendance`, `fees`, "
            "`assignments`, `status` and `help`.\n\n"
            "_To enable AI replies: get a free key at "
            "[console.groq.com](https://console.groq.com) and add it to the "
            "`.env` file._"
        )

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=600,
        )
        return completion.choices[0].message.content
    except Exception as exc:
        return (
            f":warning: **LLM call failed.** `{type(exc).__name__}: {exc}`\n\n"
            "Please check your API key, internet connection or rate limits."
        )
