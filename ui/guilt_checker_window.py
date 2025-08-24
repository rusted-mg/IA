"""
Interface de vérification de culpabilité
"""
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import messagebox

class GuiltCheckerWindow:
    """Fenêtre de vérification de culpabilité des suspects"""
    
    def __init__(self, enquete_file, prolog_service):
        self.enquete_file = enquete_file
        self.prolog_service = prolog_service
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.root = tk.Tk()
        self.root.title("Police Investigation")
        self.root.geometry("400x200")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée tous les widgets de l'interface"""
        tk.Label(self.root, text="Suspect's name:").pack(pady=5)
        self.entry_suspect = tk.Entry(self.root, width=30)
        self.entry_suspect.pack()

        tk.Label(self.root, text="Type of crime:").pack(pady=5)
        self.entry_crime_var = tk.StringVar()
        self.entry_crime = ttk.Combobox(
            self.root, 
            textvariable=self.entry_crime_var, 
            values=["assassinat", "vol", "escroquerie"],
            state="readonly", 
            width=30
        )
        self.entry_crime.pack()

        btn = tk.Button(self.root, text="Check guilt", command=self.check_crime)
        btn.pack(pady=15)
        
        back_btn = tk.Button(self.root, text="Add More Facts", command=self.back_to_facts)
        back_btn.pack(pady=5)
    
    def check_crime(self):
        """Vérifie la culpabilité d'un suspect pour un crime"""
        suspect = self.entry_suspect.get().strip().lower()
        crime = self.entry_crime_var.get().strip().lower()
        
        if not suspect or not crime:
            messagebox.showwarning("Error", "Please enter a suspect and a crime")
            return
        
        try:
            result = self.prolog_service.check_guilt(self.enquete_file, suspect, crime)
            messagebox.showinfo("Result", f"{suspect} is {result} for {crime}")
        except Exception as e:
            messagebox.showerror("Error", f"Error checking guilt: {str(e)}")
    
    def back_to_facts(self):
        """Retourne à la fenêtre d'ajout de faits"""
        from ui.main_window import FactEntryWindow
        
        self.root.destroy()
        app = FactEntryWindow()
        app.run()
    
    def run(self):
        """Lance la boucle principale de l'interface"""
        self.root.mainloop()