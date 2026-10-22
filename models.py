
import json
import os
import uuid
from datetime import datetime
from typing import List


# --------------------------------------------------
# Expense model
# --------------------------------------------------
class Expense:
    def __init__(
        self,
        title: str,
        amount: float,
        category: str,
        date_str: str = None,
        id: str = None,
    ):
        self.id = id or uuid.uuid4().hex
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.date = date_str or datetime.now().strftime("%Y-%m-%d")

    # Convert an expense into a dictionary for JSON storage
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }

    # Create an expense from a dictionary
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            amount=data.get("amount", 0),
            category=data.get("category", "Other"),
            date_str=data.get("date"),
        )


# --------------------------------------------------
# Expense storage
# --------------------------------------------------
class ExpenseStore:
    def __init__(self, filepath="data/expenses.json"):
        self.filepath = filepath

        # Create the data folder if it does not exist
        folder = os.path.dirname(self.filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)

    # Load all saved expenses
    def load_all(self) -> List[Expense]:
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                return []

            data = json.loads(content)

            return [
                Expense.from_dict(item)
                for item in data
            ]

        except (json.JSONDecodeError, OSError, TypeError, ValueError) as error:
            print(f"Could not load expenses: {error}")
            return []

    # Save all expenses to the JSON file
    def save_all(self, expenses: List[Expense]):
        folder = os.path.dirname(self.filepath)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in expenses],
                file,
                indent=4,
            )

    # Add a new expense
    def add(self, expense: Expense):
        expenses = self.load_all()
        expenses.append(expense)
        self.save_all(expenses)

    # Delete an expense using its ID
    def delete(self, expense_id: str):
        expenses = self.load_all()

        expenses = [
            expense
            for expense in expenses
            if expense.id != expense_id
        ]

        self.save_all(expenses)
