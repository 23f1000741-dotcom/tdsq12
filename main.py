from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# CORS for exam portal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://exam.sanand.workers.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):

    # 1️⃣ Ticket Status
    match = re.search(r"status of ticket (\d+)", q, re.IGNORECASE)
    if match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    match = re.search(
        r"schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)",
        q,
        re.IGNORECASE
    )
    if match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": match.group(1),
                "time": match.group(2),
                "meeting_room": match.group(3).strip()
            })
        }

    # 3️⃣ Expense Balance
    match = re.search(r"expense balance for employee (\d+)", q, re.IGNORECASE)
    if match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(match.group(1))
            })
        }

    # 4️⃣ Performance Bonus
    match = re.search(
        r"performance bonus for employee (\d+) for (\d{4})",
        q,
        re.IGNORECASE
    )
    if match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(match.group(1)),
                "current_year": int(match.group(2))
            })
        }

    # 5️⃣ Office Issue
    match = re.search(
        r"office issue (\d+) for the (.+) department",
        q,
        re.IGNORECASE
    )
    if match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": match.group(2).strip()
            })
        }

    # Fallback (never unknown_function)
    return {
        "name": "get_ticket_status",
        "arguments": json.dumps({
            "ticket_id": 0
        })
    }