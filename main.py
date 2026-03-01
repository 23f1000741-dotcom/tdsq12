from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

# ✅ Create app FIRST
app = FastAPI()

# ✅ Enable CORS (REQUIRED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://exam.sanand.workers.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):

    q_lower = q.lower()

    # 1️⃣ Ticket Status
    ticket_match = re.search(r"ticket (\d+)", q_lower)
    if ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.search(
        r"on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in ([\w\s]+)",
        q_lower
    )
    if meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3).strip()
            })
        }

    # 3️⃣ Expense Balance
    if "expense" in q_lower:
        emp_match = re.search(r"employee (\d+)", q_lower)
        if emp_match:
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({
                    "employee_id": int(emp_match.group(1))
                })
            }

    # 4️⃣ Performance Bonus
    bonus_match = re.search(r"employee (\d+) for (\d{4})", q_lower)
    if "bonus" in q_lower and bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # 5️⃣ Office Issue
    issue_match = re.search(
        r"issue (\d+) for the ([\w\s]+) department",
        q_lower
    )
    if issue_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": issue_match.group(2).strip().title()
            })
        }

    # ✅ Always return valid structure (prevents JSON.parse error)
    return {
        "name": "unknown_function",
        "arguments": json.dumps({})
    }