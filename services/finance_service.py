from __future__ import annotations

from database.db_manager import get_connection


class FinanceService:
    def __init__(self, connection_factory=get_connection):
        self.connection_factory = connection_factory

    def get_wallet(self, user_id):
        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT * FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            return dict(wallet) if wallet else None

    def get_currency(self, user_id):
        with self.connection_factory() as conn:
            setting = conn.execute("SELECT currency FROM settings WHERE user_id = ?", (user_id,)).fetchone()
            return setting["currency"] if setting else "BDT"

    def set_currency(self, user_id, currency):
        with self.connection_factory() as conn:
            conn.execute(
                "INSERT INTO settings (user_id, currency, updated_at) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(user_id) DO UPDATE SET currency = excluded.currency, updated_at = datetime('now')",
                (user_id, currency),
            )
            conn.commit()

    def add_money(self, user_id, amount, note=""):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            if not wallet:
                raise ValueError("Wallet not found.")
            new_balance = float(wallet["balance"]) + amount
            conn.execute(
                "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                (new_balance, user_id),
            )
            conn.execute(
                "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Add Money', 'Self', ?, ?)",
                (user_id, amount, note or "Add money"),
            )
            conn.commit()
            return new_balance

    def withdraw_money(self, user_id, amount, note=""):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            if not wallet:
                raise ValueError("Wallet not found.")
            balance = float(wallet["balance"])
            if amount > balance:
                raise ValueError("Insufficient balance.")
            new_balance = balance - amount
            conn.execute(
                "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                (new_balance, user_id),
            )
            conn.execute(
                "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Withdraw Money', 'Self', ?, ?)",
                (user_id, amount, note or "Withdraw money"),
            )
            conn.commit()
            return new_balance

    def transfer_money(self, user_id, recipient_name, amount, note=""):
        recipient_name = (recipient_name or "").strip()
        if not recipient_name:
            raise ValueError("Recipient name is required.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            if not wallet:
                raise ValueError("Wallet not found.")
            balance = float(wallet["balance"])
            if amount > balance:
                raise ValueError("Insufficient balance.")
            new_balance = balance - amount
            conn.execute(
                "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                (new_balance, user_id),
            )
            conn.execute(
                "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Transfer', ?, ?, ?)",
                (user_id, recipient_name, amount, note or "Transfer payment"),
            )
            conn.commit()
            return new_balance

    def add_debt(self, user_id, direction, person_name, amount, due_date, note, affect_balance):
        direction = direction.strip()
        person_name = (person_name or "").strip()
        amount = float(amount)
        if not person_name:
            raise ValueError("Person name is required.")
        if amount <= 0:
            raise ValueError("Debt amount must be greater than zero.")
        if direction not in {"owe_me", "owe_others"}:
            raise ValueError("Debt direction is invalid.")

        with self.connection_factory() as conn:
            debt_id = conn.execute(
                """
                INSERT INTO debts (user_id, direction, person_name, amount, remaining_amount, due_date, note, status, affect_balance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    direction,
                    person_name,
                    amount,
                    amount,
                    due_date,
                    note or "",
                    "Active" if amount > 0 else "Paid",
                    1 if affect_balance else 0,
                ),
            ).lastrowid

            if affect_balance:
                wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
                balance = float(wallet["balance"]) if wallet else 0.0
                if direction == "owe_me":
                    new_balance = balance + amount
                else:
                    new_balance = balance - amount
                conn.execute(
                    "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                    (new_balance, user_id),
                )
                conn.execute(
                    "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, ?, ?, ?, ?)",
                    (user_id, "Debt Payment Received" if direction == "owe_me" else "Debt Payment Made", person_name, amount, note or "Debt created"),
                )

            conn.commit()
            return debt_id

    def delete_debt(self, user_id, debt_id):
        with self.connection_factory() as conn:
            conn.execute("DELETE FROM debts WHERE id = ? AND user_id = ?", (debt_id, user_id))
            conn.commit()

    def update_debt(self, user_id, debt_id, person_name, amount, due_date, note):
        person_name = (person_name or "").strip()
        if not person_name:
            raise ValueError("Person name is required.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Debt amount must be greater than zero.")
        with self.connection_factory() as conn:
            debt = conn.execute("SELECT * FROM debts WHERE id = ? AND user_id = ?", (debt_id, user_id)).fetchone()
            if not debt:
                raise ValueError("Debt not found.")
            remaining = float(debt["remaining_amount"])
            if amount < remaining:
                # keep the remaining amount aligned with the new total if no payment history is involved
                remaining = max(0.0, amount)
            conn.execute(
                "UPDATE debts SET person_name = ?, amount = ?, remaining_amount = ?, due_date = ?, note = ? WHERE id = ? AND user_id = ?",
                (person_name, amount, remaining, due_date, note or "", debt_id, user_id),
            )
            conn.commit()

    def get_debts(self, user_id):
        with self.connection_factory() as conn:
            rows = conn.execute(
                "SELECT * FROM debts WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def get_debt_payments(self, debt_id):
        with self.connection_factory() as conn:
            rows = conn.execute(
                "SELECT * FROM debt_payments WHERE debt_id = ? ORDER BY created_at DESC",
                (debt_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def record_debt_payment(self, user_id, debt_id, amount, note, affect_balance):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        with self.connection_factory() as conn:
            debt = conn.execute("SELECT * FROM debts WHERE id = ? AND user_id = ?", (debt_id, user_id)).fetchone()
            if not debt:
                raise ValueError("Debt not found.")
            remaining = float(debt["remaining_amount"])
            if amount > remaining:
                raise ValueError("Payment cannot exceed remaining debt amount.")

            new_remaining = remaining - amount
            status = "Paid" if new_remaining <= 0 else ("Partially Paid" if new_remaining < float(debt["amount"]) else "Active")
            conn.execute(
                "INSERT INTO debt_payments (debt_id, amount, note, affect_balance) VALUES (?, ?, ?, ?)",
                (debt_id, amount, note or "Debt payment", 1 if affect_balance else 0),
            )
            conn.execute(
                "UPDATE debts SET remaining_amount = ?, status = ? WHERE id = ?",
                (new_remaining, status, debt_id),
            )

            if affect_balance:
                wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
                balance = float(wallet["balance"]) if wallet else 0.0
                if debt["direction"] == "owe_me":
                    new_balance = balance + amount
                else:
                    new_balance = balance - amount
                conn.execute(
                    "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                    (new_balance, user_id),
                )
                conn.execute(
                    "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, ?, ?, ?, ?)",
                    (
                        user_id,
                        "Debt Payment Received" if debt["direction"] == "owe_me" else "Debt Payment Made",
                        debt["person_name"],
                        amount,
                        note or "Debt repayment",
                    ),
                )
            conn.commit()
            return new_remaining

    def get_dashboard_data(self, user_id):
        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            people_owe_me = conn.execute(
                "SELECT COALESCE(SUM(remaining_amount), 0) FROM debts WHERE user_id = ? AND direction = 'owe_me'",
                (user_id,),
            ).fetchone()[0]
            i_owe_others = conn.execute(
                "SELECT COALESCE(SUM(remaining_amount), 0) FROM debts WHERE user_id = ? AND direction = 'owe_others'",
                (user_id,),
            ).fetchone()[0]
            total_transactions = conn.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ?", (user_id,)).fetchone()[0]
            recent_transactions = conn.execute(
                "SELECT * FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 5",
                (user_id,),
            ).fetchall()
            upcoming_debts = conn.execute(
                "SELECT * FROM debts WHERE user_id = ? AND due_date IS NOT NULL AND due_date >= date('now') ORDER BY due_date ASC LIMIT 5",
                (user_id,),
            ).fetchall()

            return {
                "balance": float(wallet["balance"]) if wallet else 0.0,
                "people_owe_me": float(people_owe_me or 0.0),
                "i_owe_others": float(i_owe_others or 0.0),
                "total_transactions": total_transactions,
                "recent_transactions": [dict(row) for row in recent_transactions],
                "upcoming_debts": [dict(row) for row in upcoming_debts],
            }

    def get_transactions(self, user_id, type_filter=None, search=""):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [user_id]
        if type_filter and type_filter != "All":
            query += " AND type = ?"
            params.append(type_filter)
        if search:
            query += " AND (person LIKE ? OR note LIKE ? OR type LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        query += " ORDER BY id DESC"
        with self.connection_factory() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def create_goal(self, user_id, name, target_amount, goal_type):
        name = (name or "").strip()
        if not name:
            raise ValueError("Goal name is required.")
        target_amount = float(target_amount)
        if target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")
        if goal_type not in {"separate", "direct"}:
            raise ValueError("Invalid goal type.")

        with self.connection_factory() as conn:
            goal_id = conn.execute(
                "INSERT INTO goals (user_id, name, target_amount, goal_type, saved_amount, status) VALUES (?, ?, ?, ?, 0.0, 'active')",
                (user_id, name, target_amount, goal_type),
            ).lastrowid
            conn.commit()
            return goal_id

    def get_goals(self, user_id, include_completed=False):
        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            wallet_balance = float(wallet["balance"]) if wallet else 0.0
            rows = conn.execute(
                "SELECT * FROM goals WHERE user_id = ? AND status = 'active' ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
            goals = []
            for row in rows:
                goal = dict(row)
                if goal["goal_type"] == "direct":
                    goal["saved_amount"] = wallet_balance
                goals.append(goal)

            if include_completed:
                completed_rows = conn.execute(
                    "SELECT * FROM goals WHERE user_id = ? AND status = 'completed' ORDER BY completed_at DESC",
                    (user_id,),
                ).fetchall()
                for row in completed_rows:
                    goal = dict(row)
                    if goal["goal_type"] == "direct":
                        goal["saved_amount"] = wallet_balance
                    goals.append(goal)
            return goals

    def get_completed_goals(self, user_id):
        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            wallet_balance = float(wallet["balance"]) if wallet else 0.0
            rows = conn.execute(
                "SELECT * FROM goals WHERE user_id = ? AND status = 'completed' ORDER BY completed_at DESC",
                (user_id,),
            ).fetchall()
            goals = []
            for row in rows:
                goal = dict(row)
                if goal["goal_type"] == "direct":
                    goal["saved_amount"] = wallet_balance
                goals.append(goal)
            return goals

    def get_goal_summary(self, user_id):
        with self.connection_factory() as conn:
            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            wallet_balance = float(wallet["balance"]) if wallet else 0.0
            active_goals = conn.execute(
                "SELECT * FROM goals WHERE user_id = ? AND status = 'active' ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
            total_target = sum(float(goal["target_amount"]) for goal in active_goals)
            separate_saved = sum(float(goal["saved_amount"]) for goal in active_goals if goal["goal_type"] == "separate")
            direct_goals_count = sum(1 for goal in active_goals if goal["goal_type"] == "direct")
            total_saved = separate_saved + (wallet_balance if direct_goals_count > 0 else 0.0)
            return {
                "active_goals": len(active_goals),
                "total_target": total_target,
                "total_saved": total_saved,
            }

    def add_goal_savings(self, user_id, goal_id, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Savings amount must be greater than zero.")

        with self.connection_factory() as conn:
            goal = conn.execute("SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id)).fetchone()
            if not goal:
                raise ValueError("Goal not found.")
            if goal["goal_type"] != "separate":
                raise ValueError("This goal does not use separate savings.")

            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            if not wallet:
                raise ValueError("Wallet not found.")
            if float(wallet["balance"]) < amount:
                raise ValueError("Insufficient VaultPay balance to add to this goal.")

            new_saved = float(goal["saved_amount"]) + amount
            conn.execute("UPDATE goals SET saved_amount = ? WHERE id = ?", (new_saved, goal_id))
            conn.execute(
                "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                (float(wallet["balance"]) - amount, user_id),
            )
            conn.execute(
                "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Goal Savings', ?, ?, ?)",
                (user_id, goal["name"], amount, f"Added savings to goal: {goal['name']}"),
            )
            conn.commit()
            return new_saved

    def withdraw_goal_savings(self, user_id, goal_id, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        with self.connection_factory() as conn:
            goal = conn.execute("SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id)).fetchone()
            if not goal:
                raise ValueError("Goal not found.")
            if goal["goal_type"] != "separate":
                raise ValueError("This goal does not have separate savings.")
            if float(goal["saved_amount"]) < amount:
                raise ValueError("Withdrawal amount exceeds the saved amount for this goal.")

            wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            new_balance = float(wallet["balance"]) + amount if wallet else amount
            conn.execute("UPDATE goals SET saved_amount = ? WHERE id = ?", (float(goal["saved_amount"]) - amount, goal_id))
            conn.execute(
                "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                (new_balance, user_id),
            )
            conn.execute(
                "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Goal Withdrawal', ?, ?, ?)",
                (user_id, goal["name"], amount, f"Withdrew savings from goal: {goal['name']}"),
            )
            conn.commit()
            return float(goal["saved_amount"]) - amount

    def complete_goal(self, user_id, goal_id):
        with self.connection_factory() as conn:
            goal = conn.execute("SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id)).fetchone()
            if not goal:
                raise ValueError("Goal not found.")
            if goal["status"] == "completed":
                return dict(goal)
            conn.execute(
                "UPDATE goals SET status = 'completed', completed_at = datetime('now') WHERE id = ? AND user_id = ?",
                (goal_id, user_id),
            )
            conn.commit()
            updated = conn.execute("SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id)).fetchone()
            return dict(updated)

    def remove_goal(self, user_id, goal_id):
        with self.connection_factory() as conn:
            goal = conn.execute("SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id)).fetchone()
            if not goal:
                raise ValueError("Goal not found.")

            if goal["goal_type"] == "separate" and float(goal["saved_amount"]) > 0:
                wallet = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
                balance = float(wallet["balance"]) if wallet else 0.0
                conn.execute(
                    "UPDATE wallets SET balance = ?, updated_at = datetime('now') WHERE user_id = ?",
                    (balance + float(goal["saved_amount"]), user_id),
                )
                conn.execute(
                    "INSERT INTO transactions (user_id, type, person, amount, note) VALUES (?, 'Goal Removed', ?, ?, ?)",
                    (user_id, goal["name"], float(goal["saved_amount"]), f"Returned saved goal funds to wallet: {goal['name']}"),
                )

            conn.execute("DELETE FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id))
            conn.commit()
            return True
