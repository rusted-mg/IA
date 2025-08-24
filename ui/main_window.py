"""
Interface principale pour la saisie des faits
"""
import tkinter as tk
from tkinter import messagebox, ttk
from service.fact_service import FactService
from service.prolog_service import PrologService
from ui.guilt_checker_window import GuiltCheckerWindow

class FactEntryWindow:
    """Fenêtre de saisie des faits d'enquête"""
    
    def __init__(self):
        self.fact_service = FactService()
        self.prolog_service = PrologService()
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.root = tk.Tk()
        self.root.title("Add Facts")
        self.root.geometry("500x500")
        
        self.fact_type_var = tk.StringVar()
        self.fact_types = [
            "suspect",
            "has_motive",
            "was_near_crime_scene",
            "has_fingerprint_on_weapon",
            "has_bank_transaction",
            "owns_fake_identity",
            "eyewitness_identification"
        ]
        
        # Création des composants UI
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée tous les widgets de l'interface"""
        ttk.Label(self.root, text="Fact type:").pack(pady=5)
        self.fact_type_menu = ttk.Combobox(
            self.root, 
            textvariable=self.fact_type_var, 
            values=self.fact_types, 
            state="readonly", 
            width=30
        )
        self.fact_type_menu.pack()

        ttk.Label(self.root, text="Suspect Name:").pack(pady=5)
        self.entry_suspect = ttk.Entry(self.root, width=34)
        self.entry_suspect.pack()

        ttk.Label(self.root, text="Crime type (not needed if 'suspect' fact):").pack(pady=5)
        self.entry_crime_var = tk.StringVar()
        self.entry_crime_menu = ttk.Combobox(
            self.root, 
            textvariable=self.entry_crime_var, 
            values=["", "assassinat", "vol", "escroquerie"],
            state="readonly", 
            width=30
        )
        self.entry_crime_menu.pack()

        add_btn = ttk.Button(self.root, text="Add Fact", command=self.add_fact)
        add_btn.pack(pady=10)

        self.facts_listbox = tk.Listbox(self.root, width=60)
        self.facts_listbox.pack(pady=5)

        finish_btn = ttk.Button(self.root, text="Finish", command=self.finish_facts)
        finish_btn.pack(pady=15)
    
    def add_fact(self):
        """Ajoute un nouveau fait à la liste"""
        fact_type = self.fact_type_var.get()
        param1 = self.entry_suspect.get().strip().lower()
        param2 = self.entry_crime_var.get().strip().lower()
        
        if not fact_type or not param1 or (fact_type != "suspect" and not param2):
            messagebox.showwarning("Error", "Please fill all fields")
            return
        
        fact = self.fact_service.create_fact(fact_type, param1, param2)
        self.facts_listbox.insert(tk.END, fact)
        
        self.entry_suspect.delete(0, tk.END)
    
    def finish_facts(self):
        """Termine la saisie des faits et lance la vérification de culpabilité"""
        facts = self.fact_service.get_all_facts()
        
        if not facts:
            messagebox.showwarning("Warning", "No facts entered!")
            return
        
        enquete_file = self.prolog_service.create_enquete_file(facts)
        
        self.root.destroy()
        
        guilt_checker = GuiltCheckerWindow(enquete_file, self.prolog_service)
        guilt_checker.run()
    
    def run(self):
        """Lance la boucle principale de l'interface"""
        self.root.mainloop()