import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
from datetime import datetime

facts = []

def add_fact():
    fact_type = fact_type_var.get()
    param1 = param1_entry.get().strip().lower()
    param2 = param2_entry.get().strip().lower()
    if not fact_type or not param1 or (fact_type != "suspect" and not param2):
        messagebox.showwarning("Error", "Please fill all fields")
        return
    if fact_type == "suspect":
        facts.append(f"suspect({param1}).")
    else:
        facts.append(f"{fact_type}({param1}, {param2}).")
    facts_listbox.insert(tk.END, facts[-1])
    param1_entry.delete(0, tk.END)
    param2_entry.delete(0, tk.END)

def finish_facts():
    # Create history folder if it doesn't exist
    if not os.path.exists("history"):
        os.makedirs("history")
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = f"history/facts_{dt}.pl"
    enquete_file = f"history/enquete_with_facts_{dt}.pl"
    # Write facts to a temp file and append to core.pl
    with open(temp_file, "w") as f:
        for fact in facts:
            f.write(fact + "\n")
    with open("core.pl", "r") as orig, open(enquete_file, "w") as out:
        out.write(orig.read())
        out.write("\n% User facts\n")
        for fact in facts:
            out.write(fact + "\n")
    fact_window.destroy()
    show_guilt_checker(enquete_file)

def show_guilt_checker(enquete_file):
    global entry_suspect, entry_crime, current_enquete_file
    current_enquete_file = enquete_file
    guilt_window = tk.Tk()
    guilt_window.title("Police Investigation")
    guilt_window.geometry("400x200")

    tk.Label(guilt_window, text="Suspect's name:").pack(pady=5)
    entry_suspect = tk.Entry(guilt_window, width=30)
    entry_suspect.pack()

    tk.Label(guilt_window, text="Type of crime:").pack(pady=5)
    entry_crime = tk.Entry(guilt_window, width=30)
    entry_crime.pack()

    btn = tk.Button(guilt_window, text="Check guilt", command=check_crime)
    btn.pack(pady=15)

    guilt_window.mainloop()

def check_crime():
    suspect = entry_suspect.get().lower()
    crime = entry_crime.get().lower()
    if not suspect or not crime:
        messagebox.showwarning("Error", "Please enter a suspect and a crime")
        return
    query = f"(is_guilty({suspect}, {crime}) -> writeln(guilty) ; writeln(not_guilty))."
    try:
        result = subprocess.run(
            ["swipl", "-q", "-s", current_enquete_file, "-g", query, "-t", "halt"],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        messagebox.showinfo("Result", f"{suspect} is {output} for {crime}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Fact Entry Interface ---
fact_window = tk.Tk()
fact_window.title("Add Facts")
fact_window.geometry("500x500")

fact_type_var = tk.StringVar()
fact_types = [
    "suspect",
    "has_motive",
    "was_near_crime_scene",
    "has_fingerprint_on_weapon",
    "has_bank_transaction",
    "owns_fake_identity",
    "eyewitness_identification"
]
ttk.Label(fact_window, text="Fact type:").pack(pady=5)
fact_type_menu = ttk.Combobox(fact_window, textvariable=fact_type_var, values=fact_types, state="readonly")
fact_type_menu.pack()

ttk.Label(fact_window, text="Parameter 1:").pack(pady=5)
param1_entry = ttk.Entry(fact_window, width=30)
param1_entry.pack()

ttk.Label(fact_window, text="Parameter 2 (if needed):").pack(pady=5)
param2_entry = ttk.Entry(fact_window, width=30)
param2_entry.pack()

add_btn = ttk.Button(fact_window, text="Add Fact", command=add_fact)
add_btn.pack(pady=10)

facts_listbox = tk.Listbox(fact_window, width=60)
facts_listbox.pack(pady=5)

finish_btn = ttk.Button(fact_window, text="Finish", command=finish_facts)
finish_btn.pack(pady=15)

fact_window.mainloop()
