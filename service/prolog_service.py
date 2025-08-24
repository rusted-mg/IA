"""
Service d'interaction avec SWI-Prolog
"""
import subprocess
import os
from datetime import datetime

class PrologService:
    """Service responsable de l'interaction avec SWI-Prolog"""
    
    def __init__(self, core_file_path="../core.pl"):
        self.core_file_path = core_file_path
        self.history_dir = "history"
    
    def create_enquete_file(self, facts):
        """Crée un fichier d'enquête avec les faits fournis"""
        
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        
        dt = datetime.now().strftime("%Y%m%d_%H%M%S")
        enquete_file = f"{self.history_dir}/enquete_with_facts_{dt}.pl"
        
        with open(enquete_file, "w", encoding="utf-8") as f:
            f.write("% Core file importation\n")
            f.write(f":- consult('{self.core_file_path}').\n\n")
            f.write("% Facts\n")
            for fact in facts:
                f.write(fact + "\n")
        
        return enquete_file
    
    def check_guilt(self, enquete_file, suspect, crime):
        """Vérifie la culpabilité d'un suspect pour un crime donné"""
        query = f"(is_guilty({suspect}, {crime}) -> writeln(guilty) ; writeln(not_guilty))."
        
        try:
            result = subprocess.run(
                ["swipl", "-q", "-s", enquete_file, "-g", query, "-t", "halt"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                raise Exception(f"Prolog execution failed: {error_msg}")
            
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise Exception("Prolog execution timed out")
        except FileNotFoundError:
            raise Exception("SWI-Prolog not found. Please ensure it's installed and in PATH")
        except Exception as e:
            raise Exception(f"Error executing Prolog query: {str(e)}")
    
    def verify_core_file(self):
        """Vérifie que le fichier core.pl existe"""
        return os.path.exists(self.core_file_path)
    
    def list_enquete_files(self):
        """Liste tous les fichiers d'enquête dans le dossier history"""
        if not os.path.exists(self.history_dir):
            return []
        
        files = []
        for filename in os.listdir(self.history_dir):
            if filename.startswith("enquete_with_facts_") and filename.endswith(".pl"):
                files.append(os.path.join(self.history_dir, filename))
        
        return sorted(files, reverse=True)
    
    def delete_enquete_file(self, file_path):
        """Supprime un fichier d'enquête file_path (str): Chemin vers le fichier à supprimer"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise Exception(f"Error deleting file: {str(e)}")