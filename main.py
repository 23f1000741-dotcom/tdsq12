from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

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
    match = re.search(r"ticket\s+(\d+)", q_lower)
    if match and "status" in q_lower:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)",
        q_lower
    )
    if match and "schedule" in q_lower:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": match.group(1),
                "time": match.group(2),
                "meeting_room": match.group(3).strip()
            })
        }

    # 3️⃣ Expense Balance
    match = re.search(r"employee\s+(\d+)", q_lower)
    if match and "expense" in q_lower:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(match.group(1))
            })
        }

    # 4️⃣ Performance Bonus
    match = re.search(r"employee\s+(\d+)\s+for\s+(\d{4})", q_lower)
    if match and "bonus" in q_lower:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(match.group(1)),
                "current_year": int(match.group(2))
            })
        }

    # 5️⃣ Office Issue
    match = re.search(r"issue\s+(\d+).*department", q_lower)
    if match:
        dept_match = re.search(r"for\s+the\s+(.+)\s+department", q_lower)
        department = dept_match.group(1).strip() if dept_match else ""
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": department.title()
            })
        }

    # If nothing matches, return valid dummy but unlikely case
    return {
        "name": "get_ticket_status",
        "arguments": json.dumps({
            "ticket_id": 1
        })
    }