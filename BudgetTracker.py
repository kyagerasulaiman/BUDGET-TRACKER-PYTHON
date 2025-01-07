import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.categories = {}

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Budget Tracker", font=("Arial", 24)).pack(pady=10)

        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab_add = ttk.Frame(self.tab_control)
        self.tab_view = ttk.Frame(self.tab_control)
        self.tab_graph = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_add, text="Add Transactions")
        self.tab_control.add(self.tab_view, text="View Totals")
        self.tab_control.add(self.tab_graph, text="View Graph")

        self.tab_control.pack(expand=1, fill="both")

        # Add Transaction Tab
        tk.Label(self.tab_add, text="Category:").grid(row=0, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(self.tab_add)
        self.category_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.tab_add, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.tab_add)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.tab_add, text="Type:").grid(row=2, column=0, padx=10, pady=10)
        self.transaction_type = ttk.Combobox(self.tab_add, values=["Income", "Expense"])
        self.transaction_type.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.tab_add, text="Add Transaction", command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=20)

        # View Totals Tab
        self.totals_text = tk.Text(self.tab_view, width=50, height=15, state="disabled")
        self.totals_text.pack(pady=20)

        tk.Button(self.tab_view, text="Refresh Totals", command=self.show_totals).pack(pady=10)

        # Graph Tab
        tk.Button(self.tab_graph, text="Show Graph", command=self.show_graph).pack(pady=20)

    def add_transaction(self):
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        transaction_type = self.transaction_type.get()

        if not category or not amount or not transaction_type:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return

        if category not in self.categories:
            self.categories[category] = 0

        if transaction_type == "Income":
            self.categories[category] += amount
        elif transaction_type == "Expense":
            self.categories[category] -= amount

        messagebox.showinfo("Success", f"{transaction_type} of {amount} added to {category}.")
        self.clear_entries()

    def clear_entries(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.transaction_type.set("")

    def show_totals(self):
        self.totals_text.config(state="normal")
        self.totals_text.delete(1.0, tk.END)

        for category, total in self.categories.items():
            self.totals_text.insert(tk.END, f"{category}: {total:.2f}\n")

        self.totals_text.config(state="disabled")

    def show_graph(self):
        if not self.categories:
            messagebox.showinfo("No Data", "No transactions to display.")
            return

        labels = self.categories.keys()
        values = self.categories.values()

        plt.bar(labels, values, color=['green' if value >= 0 else 'red' for value in values])
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.title('Budget Tracker')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
