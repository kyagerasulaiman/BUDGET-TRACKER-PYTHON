import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.categories = {"Income": 0, "Expenses": 0, "Savings": 0, "Debts": 0}
        self.transactions = {"Income": [], "Expenses": [], "Savings": [], "Debts": []}

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="lightcoral", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Personal Budget Tracker", font=("Arial", 24), bg="lightcoral", fg="white").pack()

        # Main Content
        content = tk.Frame(self.root)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Panel - Data Entry
        self.setup_left_panel(content)

        # Right Panel - Overview and Graphs
        self.setup_right_panel(content)

    def setup_left_panel(self, parent):
        left_panel = tk.Frame(parent, width=300, relief=tk.GROOVE, borderwidth=2)
        left_panel.pack(side="left", fill="y", padx=10)

        tk.Label(left_panel, text="Add Transaction", font=("Arial", 18)).pack(pady=10)

        tk.Label(left_panel, text="Category:").pack(anchor="w", padx=10)
        self.category_combobox = ttk.Combobox(left_panel, values=["Income", "Expenses", "Savings", "Debts"], state="readonly")
        self.category_combobox.pack(fill="x", padx=10, pady=5)

        tk.Label(left_panel, text="Description:").pack(anchor="w", padx=10)
        self.description_entry = tk.Entry(left_panel)
        self.description_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(left_panel, text="Amount:").pack(anchor="w", padx=10)
        self.amount_entry = tk.Entry(left_panel)
        self.amount_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(left_panel, text="Add", command=self.add_transaction).pack(pady=10)

    def setup_right_panel(self, parent):
        right_panel = tk.Frame(parent)
        right_panel.pack(side="right", fill="both", expand=True)

        # Overview Section
        overview_frame = tk.Frame(right_panel)
        overview_frame.pack(fill="x", pady=10)

        tk.Label(overview_frame, text="Overview", font=("Arial", 18)).pack(anchor="w")

        self.overview_text = tk.Text(overview_frame, height=8, state="disabled", wrap="word", bg="lightyellow")
        self.overview_text.pack(fill="x", pady=5)

        # Graph Section
        graph_frame = tk.Frame(right_panel)
        graph_frame.pack(fill="both", expand=True)

        tk.Label(graph_frame, text="Visual Representation", font=("Arial", 18)).pack(anchor="w", pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.update_graph()

    def add_transaction(self):
        category = self.category_combobox.get()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not category or not description or not amount:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return

        self.categories[category] += amount
        self.transactions[category].append((description, amount))

        messagebox.showinfo("Success", f"Added {amount} to {category}.")
        self.update_overview()
        self.update_graph()

        # Clear inputs
        self.category_combobox.set("")
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def update_overview(self):
        self.overview_text.config(state="normal")
        self.overview_text.delete(1.0, tk.END)

        total = sum(self.categories.values())
        for category, amount in self.categories.items():
            self.overview_text.insert(tk.END, f"{category}: {amount:.2f}\n")

        self.overview_text.insert(tk.END, f"\nTotal: {total:.2f}")
        self.overview_text.config(state="disabled")

    def update_graph(self):
        self.ax.clear()

        categories = list(self.categories.keys())
        amounts = list(self.categories.values())

        # Handle case where all amounts are zero
        if all(amount == 0 for amount in amounts):
            self.ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=14)
            self.ax.set_title("Category Distribution")
        else:
            self.ax.pie(
                amounts,
                labels=categories,
                autopct="%1.1f%%",
                startangle=90,
                colors=["green", "red", "blue", "orange"]
            )
            self.ax.set_title("Category Distribution")

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
