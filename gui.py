import tkinter as tk
from finance_logic import (
    add_transaction_gui, delete_transaction_gui,
    show_summary, show_cat_summary, show_monthly_summary,
    clear_data
)

def run_app():
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    root.geometry("420x420")
    root.configure(bg='#f4f8fb')

    title = tk.Label(root, text="💰 Personal Finance Tracker", font=("Helvetica", 16, "bold"), bg='#f4f8fb', fg="#2a2a2a")
    title.pack(pady=20)

    btn_style = {
        "width": 30,
        "height": 2,
        "font": ("Helvetica", 10, "bold"),
        "bg": "#007acc",
        "fg": "white",
        "activebackground": "#005a99",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(root, text="➕ Add Transaction", command=add_transaction_gui, **btn_style).pack(pady=6)
    tk.Button(root, text="🗑 Delete Transaction", command=delete_transaction_gui, **btn_style).pack(pady=6)
    tk.Button(root, text="📊 Show Summary", command=show_summary, **btn_style).pack(pady=6)
    tk.Button(root, text="📂 Category Summary", command=show_cat_summary, **btn_style).pack(pady=6)
    tk.Button(root, text="📅 Monthly Summary", command=show_monthly_summary, **btn_style).pack(pady=6)
    tk.Button(root, text="🧹 Clear All Data", command=clear_data, bg="#d9534f", activebackground="#c9302c", **btn_style).pack(pady=6)

    footer = tk.Label(root, text="Made with ❤️", font=("Helvetica", 9), bg='#f4f8fb', fg="#666")
    footer.pack(pady=10)

    root.mainloop()
