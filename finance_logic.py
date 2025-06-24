import csv
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

FILENAME = "trans.csv"

if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "type", "Category", "Amount"])

def add_transaction_gui():
    def save_transaction():
        date = date_entry.get()
        typ = type_combo.get()
        cat = category_entry.get()
        amt = amount_entry.get()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            amt = float(amt)
            with open(FILENAME, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date, typ.upper(), cat, amt])
            messagebox.showinfo("Success", "Transaction added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    win = tk.Toplevel()
    win.title("Add Transaction")

    tk.Label(win, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
    date_entry = tk.Entry(win)
    date_entry.grid(row=0, column=1)

    tk.Label(win, text="Type:").grid(row=1, column=0)
    type_combo = ttk.Combobox(win, values=["INCOME", "EXPENSE"])
    type_combo.grid(row=1, column=1)

    tk.Label(win, text="Category:").grid(row=2, column=0)
    category_entry = tk.Entry(win)
    category_entry.grid(row=2, column=1)

    tk.Label(win, text="Amount:").grid(row=3, column=0)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=3, column=1)

    tk.Button(win, text="Add", command=save_transaction).grid(row=4, column=0, columnspan=2, pady=5)
def delete_transaction_gui():
    def delete_by_values():
        date = date_entry.get()
        typ = type_combo.get().upper()
        amt = amount_entry.get()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            amt = float(amt)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        with open(FILENAME, "r") as f:
            rows = list(csv.reader(f))

        header = rows[0]
        data = rows[1:]
        match_index = None

        for i, row in enumerate(data):
            if row[0] == date and row[1].upper() == typ and float(row[3]) == amt:
                match_index = i + 1  # +1 to include header in final list
                break

        if match_index:
            del rows[match_index]
            with open(FILENAME, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            messagebox.showinfo("Deleted", "Transaction deleted successfully.")
            win.destroy()
        else:
            messagebox.showwarning("Not Found", "No matching transaction found.")

    win = tk.Toplevel()
    win.title("Delete Transaction by Value")
    win.configure(bg='#f0f8ff')

    tk.Label(win, text="Date (YYYY-MM-DD):", bg='#f0f8ff').grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(win)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Type (INCOME/EXPENSE):", bg='#f0f8ff').grid(row=1, column=0, padx=5, pady=5)
    type_combo = ttk.Combobox(win, values=["INCOME", "EXPENSE"])
    type_combo.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Amount:", bg='#f0f8ff').grid(row=2, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(win, text="Delete", command=delete_by_values, bg="#d9534f", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

def show_summary():
    inc, exp = 0, 0
    with open(FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amt = float(row['Amount'])
            if row['type'].upper() == "INCOME":
                inc += amt
            else:
                exp += amt
    msg = f"Total Income: ₹{inc}\nTotal Expense: ₹{exp}\nBalance: ₹{inc - exp}"
    messagebox.showinfo("Summary", msg)

def show_cat_summary():
    income, expense = defaultdict(float), defaultdict(float)
    with open(FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amt = float(row['Amount'])
            cat = row['Category']
            typ = row['type'].upper()
            if typ == 'INCOME':
                income[cat] += amt
            else:
                expense[cat] += amt
    all_cats = sorted(set(income) | set(expense))
    inc_vals = [income[cat] for cat in all_cats]
    exp_vals = [expense[cat] for cat in all_cats]
    x = np.arange(len(all_cats))

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - 0.2, inc_vals, 0.4, label='Income', color='green')
    bars2 = ax.bar(x + 0.2, exp_vals, 0.4, label='Expense', color='red')
    for bar in bars1 + bars2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.0f}', ha='center', va='bottom')
    ax.set_xticks(x)
    ax.set_xticklabels(all_cats, rotation=45)
    ax.set_title("Category-wise Summary")
    ax.legend()
    plt.tight_layout()
    plt.show()

def show_monthly_summary():
    win = tk.Tk()
    win.withdraw()
    month = simpledialog.askstring("Month", "Enter YYYY-MM:", parent=win)
    if not month:
        return

    income, expense = defaultdict(float), defaultdict(float)
    inc_total, exp_total = 0, 0
    with open(FILENAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['date'].startswith(month):
                amt = float(row['Amount'])
                cat = row['Category']
                typ = row['type'].upper()
                if typ == 'INCOME':
                    income[cat] += amt
                    inc_total += amt
                else:
                    expense[cat] += amt
                    exp_total += amt
    all_cats = sorted(set(income) | set(expense))
    inc_vals = [income[cat] for cat in all_cats]
    exp_vals = [expense[cat] for cat in all_cats]
    x = np.arange(len(all_cats))

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - 0.2, inc_vals, 0.4, label='Income', color='green')
    bars2 = ax.bar(x + 0.2, exp_vals, 0.4, label='Expense', color='red')
    for bar in bars1 + bars2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.0f}', ha='center', va='bottom')
    ax.set_xticks(x)
    ax.set_xticklabels(all_cats, rotation=45)
    ax.set_title(f"Monthly Summary: {month}\nIncome ₹{inc_total}, Expense ₹{exp_total}")
    ax.legend()
    plt.tight_layout()
    plt.show()

def clear_data():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all data?")
    if confirm:
        with open(FILENAME, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "type", "Category", "Amount"])
        messagebox.showinfo("Cleared", "All data deleted successfully.")
