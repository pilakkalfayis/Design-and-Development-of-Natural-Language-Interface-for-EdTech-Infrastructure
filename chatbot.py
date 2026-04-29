"""Rule-based core for the EdTech chatbot.

Each handler returns a Markdown string so the same logic powers both the
CLI (`python chatbot.py`) and the Streamlit UI (`streamlit run app.py`)."""

STUDENT = {
    "name": "Fayis",
    "roll_no": "CS2023045",
    "semester": 4,
    "program": "Computer Science and Engineering",
}

COURSES = [
    ("CS401", "Data Structures & Algorithms", 4),
    ("CS402", "Database Management Systems", 4),
    ("CS403", "Operating Systems", 3),
    ("CS404", "Computer Networks", 3),
    ("CS405", "Software Engineering", 3),
]

GRADES = [
    ("CS401", "Data Structures & Algorithms", "A"),
    ("CS402", "Database Management Systems", "A-"),
    ("CS403", "Operating Systems", "B+"),
    ("CS404", "Computer Networks", "A"),
    ("CS405", "Software Engineering", "B"),
]

ATTENDANCE = [
    ("CS401", 42, 45),
    ("CS402", 40, 45),
    ("CS403", 38, 45),
    ("CS404", 44, 45),
    ("CS405", 35, 45),
]

FEES = {
    "total": 85000,
    "paid": 70000,
    "due": 15000,
    "due_date": "2026-05-15",
}

ASSIGNMENTS = [
    ("CS401", "Implement AVL Tree", "2026-04-28", "Pending"),
    ("CS402", "Normalize given schema to 3NF", "2026-04-30", "Submitted"),
    ("CS403", "Process scheduling simulation", "2026-05-02", "Pending"),
    ("CS404", "TCP vs UDP comparison report", "2026-05-05", "Pending"),
]


def handle_help():
    return (
        "**Here is what I can do for you:**\n\n"
        "| Command | Description |\n"
        "|---------|-------------|\n"
        "| `courses` | List your enrolled courses |\n"
        "| `grades` | View your latest grades |\n"
        "| `attendance` | Check your attendance |\n"
        "| `fees` | View fee status |\n"
        "| `assignments` | See pending assignments |\n"
        "| `status` | Quick dashboard overview |\n"
        "| `help` | Show this menu |\n"
        "| `exit` | Close the chatbot |\n\n"
        "_You can also ask me anything in plain English — "
        "I'll try my best to answer!_"
    )


def handle_courses():
    lines = [f"**Enrolled courses — Semester {STUDENT['semester']}**\n",
             "| Code | Title | Credits |",
             "|------|-------|---------|"]
    for code, title, credits in COURSES:
        lines.append(f"| `{code}` | {title} | {credits} |")
    total = sum(c for _, _, c in COURSES)
    lines.append(f"| | **Total credits** | **{total}** |")
    return "\n".join(lines)


def handle_grades():
    lines = ["**Your latest grades**\n",
             "| Code | Title | Grade |",
             "|------|-------|-------|"]
    for code, title, grade in GRADES:
        lines.append(f"| `{code}` | {title} | **{grade}** |")
    return "\n".join(lines)


def handle_attendance():
    lines = ["**Attendance summary**\n",
             "| Code | Attended | Total | Percent |",
             "|------|----------|-------|---------|"]
    low = []
    for code, attended, total in ATTENDANCE:
        pct = (attended / total) * 100
        flag = " :warning:" if pct < 80 else ""
        lines.append(f"| `{code}` | {attended} | {total} | {pct:.1f}%{flag} |")
        if pct < 80:
            low.append(code)
    if low:
        lines.append(
            f"\n> :warning: Attendance below **80%** in: "
            f"{', '.join(f'`{c}`' for c in low)}. "
            f"Please attend regularly to stay above the threshold."
        )
    return "\n".join(lines)


def handle_fees():
    lines = ["**Fee status**\n",
             f"- Total fees : **Rs. {FEES['total']:,}**",
             f"- Paid       : Rs. {FEES['paid']:,}",
             f"- Balance due: **Rs. {FEES['due']:,}**",
             f"- Due date   : `{FEES['due_date']}`"]
    if FEES["due"] > 0:
        lines.append(
            f"\n> :bell: Reminder — please clear the pending balance of "
            f"**Rs. {FEES['due']:,}** before `{FEES['due_date']}`."
        )
    return "\n".join(lines)


def handle_assignments():
    lines = ["**Your assignments**\n",
             "| Code | Title | Due Date | Status |",
             "|------|-------|----------|--------|"]
    for code, title, due, status in ASSIGNMENTS:
        badge = "🟢 Submitted" if status == "Submitted" else "🟠 Pending"
        lines.append(f"| `{code}` | {title} | `{due}` | {badge} |")
    pending = sum(1 for _, _, _, s in ASSIGNMENTS if s == "Pending")
    lines.append(
        f"\nYou have **{pending} pending** assignment(s). "
        f"Make sure to submit them on time!"
    )
    return "\n".join(lines)


def handle_status():
    total_attended = sum(a for _, a, _ in ATTENDANCE)
    total_classes = sum(t for _, _, t in ATTENDANCE)
    overall_attendance = (total_attended / total_classes) * 100
    pending = sum(1 for _, _, _, s in ASSIGNMENTS if s == "Pending")
    return (
        "**Quick Status Dashboard**\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| Student | **{STUDENT['name']}** |\n"
        f"| Roll No | `{STUDENT['roll_no']}` |\n"
        f"| Program | {STUDENT['program']} |\n"
        f"| Semester | {STUDENT['semester']} |\n"
        f"| Courses Enrolled | {len(COURSES)} |\n"
        f"| Overall Attendance | **{overall_attendance:.1f}%** |\n"
        f"| Pending Assignments | {pending} |\n"
        f"| Fees Due | Rs. {FEES['due']:,} |"
    )


HANDLERS = {
    "help": handle_help,
    "courses": handle_courses,
    "grades": handle_grades,
    "attendance": handle_attendance,
    "fees": handle_fees,
    "assignments": handle_assignments,
    "status": handle_status,
}


def match_intent(user_input):
    text = user_input.lower().strip()
    if not text:
        return "empty"
    if any(k in text for k in ["exit", "quit", "bye", "goodbye"]):
        return "exit"
    if any(k in text for k in ["help", "menu", "what can you do", "commands"]):
        return "help"
    if any(k in text for k in ["courses", "subjects", "enrolled",
                                "class list", "what am i taking"]):
        return "courses"
    if any(k in text for k in ["grade", "marks", "result", "gpa", "score"]):
        return "grades"
    if any(k in text for k in ["attendance", "present", "absent"]):
        return "attendance"
    if any(k in text for k in ["fee", "payment", "balance"]):
        return "fees"
    if any(k in text for k in ["assignment", "homework", "task", "submission"]):
        return "assignments"
    if any(k in text for k in ["status", "dashboard", "overview", "summary"]):
        return "status"
    if any(k in text for k in ["hi ", "hello", "hey", "namaste"]) or text in ("hi",):
        return "greet"
    if "thank" in text:
        return "thanks"
    return "unknown"


def get_response(user_input):
    """Return (intent, text). For 'unknown', text is None so the UI can
    forward the query to the LLM."""
    intent = match_intent(user_input)
    if intent == "exit":
        return intent, "Goodbye! Have a productive day. :wave:"
    if intent == "empty":
        return intent, "Please type something. Try `help` to see what I can do."
    if intent == "greet":
        first = STUDENT["name"].split()[0]
        return intent, f"Hello **{first}**! How can I help you today? :sparkles:"
    if intent == "thanks":
        return intent, "You're welcome! :blush:"
    if intent == "unknown":
        return intent, None
    return intent, HANDLERS[intent]()


def _print_welcome():
    print("=" * 60)
    print("  EdTech Chatbot - Your Academic Assistant")
    print("=" * 60)
    print(f"  Hello, {STUDENT['name']} ({STUDENT['roll_no']})!")
    print("  Type 'help' to see what I can do, or 'exit' to quit.")
    print("=" * 60)


def run_cli():
    _print_welcome()
    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Session ended. Goodbye!")
            break
        intent, response = get_response(user_input)
        if intent == "exit":
            print(f"Bot: {response}")
            break
        if response is None:
            print("Bot: Sorry, I didn't understand. Type 'help' to see what I can do.")
            continue
        print(f"Bot: {response}")


if __name__ == "__main__":
    run_cli()
