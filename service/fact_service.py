"""
Service de gestion des faits d'enquête
"""

class FactService:
    """Service responsable de la création et gestion des faits Prolog"""
    
    def __init__(self):
        self.facts = []
    
    def create_fact(self, fact_type, param1, param2):
        """Crée un fait Prolog basé sur le type et les paramètres"""
        if fact_type == "suspect":
            fact = f"suspect({param1})."
        else:
            fact = f"{fact_type}({param1}, {param2})."
        
        self.facts.append(fact)
        return fact
    
    def get_all_facts(self):
        """Retourne tous les faits créés"""
        return self.facts.copy()
    
    def clear_facts(self):
        """Efface tous les faits stockés"""
        self.facts.clear()
    
    def get_facts_count(self):
        """Retourne le nombre de faits stockés"""
        return len(self.facts)
    
    def remove_fact(self, index):
        """Supprime un fait à l'index donné"""
        if 0 <= index < len(self.facts):
            del self.facts[index]
    
    def validate_fact_parameters(self, fact_type, param1, param2):
        """Valide les paramètres d'un fait"""
        if not fact_type:
            return False, "Fact type is required"
        
        if not param1:
            return False, "Parameter 1 is required"
        
        if fact_type != "suspect" and not param2:
            return False, "Parameter 2 is required for this fact type"
        
        return True, ""