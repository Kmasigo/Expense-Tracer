
import flet as ft
from models import Expense, ExpenseStore


def main(page: ft.Page):
    # Page settings
    page.title = "Expense Tracker Capstone"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)
    page.padding = 20
    page.window_width = 400
    page.window_height = 750

    # Expense storage
    store = ExpenseStore()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    def build_header():
        return ft.Column(
            [
                ft.Text(
                    "My Expenses",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Track spending, stay in control",
                    size=14,
                    color=ft.Colors.GREY_600,
                ),
            ],
            spacing=2,
        )

    # --------------------------------------------------
    # Refresh the expense list and total
    # --------------------------------------------------
    def refresh_views():
        expenses = store.load_all()
        total = sum(expense.amount for expense in expenses)

        if not expenses:
            home_list.controls = [
                ft.Text(
                    "No expenses yet. Tap + to add one.",
                    color=ft.Colors.GREY_600,
                )
            ]
        else:
            home_list.controls = []

            for expense in reversed(expenses):
                home_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ATTACH_MONEY),
                        title=ft.Text(expense.title),
                        subtitle=ft.Text(
                            f"{expense.category} | {expense.date}"
                        ),
                        trailing=ft.Row(
                            [
                                ft.Text(
                                    f"R {expense.amount:.2f}",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Delete expense",
                                    on_click=lambda e, eid=expense.id:
                                        delete_expense(eid),
                                ),
                            ],
                            tight=True,
                            spacing=4,
                        ),
                    )
                )

        total_text.value = f"Total: R {total:.2f}"
        page.update()

    # --------------------------------------------------
    # Delete an expense
    # --------------------------------------------------
    def delete_expense(expense_id):
        store.delete(expense_id)
        refresh_views()

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Expense deleted successfully.")
        )
        page.snack_bar.open = True
        page.update()

    # --------------------------------------------------
    # Input fields
    # --------------------------------------------------
    title_field = ft.TextField(
        label="Title",
        hint_text="e.g. Groceries",
        prefix_icon=ft.Icons.TITLE,
    )

    amount_field = ft.TextField(
        label="Amount",
        hint_text="e.g. 250",
        prefix_icon=ft.Icons.PAYMENTS,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    category_field = ft.Dropdown(
        label="Category",
        value="Food",
        options=[
            ft.dropdown.Option(category)
            for category in [
                "Food",
                "Transport",
                "Bills",
                "Shopping",
                "Other",
            ]
        ],
    )

    # --------------------------------------------------
    # Add a new expense
    # --------------------------------------------------
    def add_expense_click(e):
        title = (title_field.value or "").strip()
        amount_input = (amount_field.value or "").strip()
        category = category_field.value or "Other"

        if not title or not amount_input:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter a title and amount.")
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            amount = float(amount_input)

            if amount <= 0:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Amount must be greater than zero.")
                )
                page.snack_bar.open = True
                page.update()
                return

        except ValueError:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Amount must be a valid number.")
            )
            page.snack_bar.open = True
            page.update()
            return

        new_expense = Expense(
            title=title,
            amount=amount,
            category=category,
        )

        store.add(new_expense)

        # Clear the input fields
        title_field.value = ""
        amount_field.value = ""
        category_field.value = "Food"

        # Return to the home screen
        page.navigate("/")

    # --------------------------------------------------
    # Home screen
    # --------------------------------------------------
    total_text = ft.Text(
        "Total: R 0.00",
        size=20,
        weight=ft.FontWeight.W_600,
    )

    home_list = ft.ListView(
        expand=True,
        spacing=5,
        auto_scroll=False,
    )

    home_view = ft.Column(
        [
            build_header(),
            ft.Divider(),
            total_text,
            ft.Container(
                content=home_list,
                expand=True,
            ),
            ft.FilledButton(
                "Add Expense",
                icon=ft.Icons.ADD,
                on_click=lambda e: page.navigate("/add"),
                style=ft.ButtonStyle(padding=20),
            ),
        ],
        expand=True,
        spacing=15,
    )

    # --------------------------------------------------
    # Add-expense screen
    # --------------------------------------------------
    add_view = ft.Column(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="Go back",
                on_click=lambda e: page.navigate("/"),
            ),
            ft.Text(
                "Add Expense",
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
            title_field,
            amount_field,
            category_field,
            ft.FilledButton(
                "Save Expense",
                icon=ft.Icons.SAVE,
                on_click=add_expense_click,
                width=400,
            ),
            ft.Text(
                "Peer tested: Button labels clarified based on user feedback",
                size=11,
                color=ft.Colors.GREY_500,
                italic=True,
            ),
        ],
        spacing=15,
        expand=True,
    )

    # --------------------------------------------------
    # Navigation between screens
    # --------------------------------------------------
    def route_change(e):
        page.views.clear()

        if page.route == "/add":
            page.views.append(
                ft.View(
                    route="/add",
                    controls=[add_view],
                )
            )
        else:
            page.views.append(
                ft.View(
                    route="/",
                    controls=[home_view],
                )
            )

        page.update()

        if page.route == "/":
            refresh_views()

    page.on_route_change = route_change

    # Open the home screen
    route_change(None)


if __name__ == "__main__":
    ft.run(main)
