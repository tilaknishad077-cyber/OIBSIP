import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be greater than zero.")
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        cursor.execute(
            "INSERT INTO bmi_records(weight,height,bmi,category) VALUES(?,?,?,?)",
            (weight, height, bmi, category)
        )
        conn.commit()

        result.config(
            text=f"BMI = {bmi:.2f}\nCategory = {category}",
            fg=color
        )

    except:
        messagebox.showerror("Error", "Enter valid values.")


def view_history():
    win = tk.Toplevel(root)
    win.title("BMI History")
    win.geometry("600x350")

    text = tk.Text(win, font=("Consolas", 11))
    text.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM bmi_records")
    rows = cursor.fetchall()

    if rows:
        text.insert(tk.END, "ID\tWeight\tHeight\tBMI\tCategory\n")
        text.insert(tk.END, "-" * 55 + "\n")

        for row in rows:
            text.insert(
                tk.END,
                f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]:.2f}\t{row[4]}\n"
            )
    else:
        text.insert(tk.END, "No Records Found")


def show_graph():
    cursor.execute("SELECT bmi FROM bmi_records")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Info", "No records available.")
        return

    bmi_values = [x[0] for x in data]
    x = list(range(1, len(bmi_values)+1))

    plt.figure(figsize=(6,4))
    plt.plot(x, bmi_values, marker="o")
    plt.title("BMI History")
    plt.xlabel("Record Number")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.show()


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("450x450")
root.configure(bg="#EAF6F6")

title = tk.Label(
    root,
    text="Advanced BMI Calculator",
    font=("Arial",18,"bold"),
    bg="#EAF6F6",
    fg="#0077B6"
)
title.pack(pady=15)

tk.Label(root,text="Weight (kg)",bg="#EAF6F6",font=("Arial",11)).pack()

weight_entry = ttk.Entry(root,width=30)
weight_entry.pack(pady=5)

tk.Label(root,text="Height (m)",bg="#EAF6F6",font=("Arial",11)).pack()

height_entry = ttk.Entry(root,width=30)
height_entry.pack(pady=5)

ttk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi
).pack(pady=10)

ttk.Button(
    root,
    text="View History",
    command=view_history
).pack(pady=5)

ttk.Button(
    root,
    text="Show BMI Graph",
    command=show_graph
).pack(pady=5)

result = tk.Label(
    root,
    text="",
    font=("Arial",14,"bold"),
    bg="#EAF6F6"
)
result.pack(pady=20)

root.mainloop()

conn.close()