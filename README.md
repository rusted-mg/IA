# DESCRIPTION
**Projet**: PROJET IA
**Parcours**: M1 GB
**Institut**: Ecole Nationale de Fianarantsoa
**Année scolaire**: 2024 - 2025

# MEMBRE DU GROUPE
2546 - ANDRIANJAKA Anjarasoa Princila
2580 - RALAIVAO Solotiana Nancy Christelle
2645 - ANDRIAMAOLINTSOA Tatiana
2701 - RANDIANANDRAINA Tahina Lukas André
2716 - Tsiriherivonjy Flavien
2725 - RAKOTONARIVO Dylan Mickaël
2733 - RANDIAMAMPIANDRA Tianarilanto Christian Mario Gabriel
2734 - RAENIRINA Johnny Marc Faniry

# OUTILS UTILISES
Programme **PROLOG** d'enquête judiciaire executé et à partir de **PYTHON** et **TKINKER**

# ARBORESCENCE
Projet_IA/
├── app.py # Point d'entrée principal
├── core.pl # Fichier de base des règles Prolog
├── ui/
│ ├── __init__.py # Package UI
│ ├── main_window.py # Interface de saisie des faits
│ └── guilt_checker_window.py # Interface de vérification
├── service/
│ ├── __init__.py # Package Service
│ ├── fact_service.py # Service de gestion des faits
│ └── prolog_service.py # Service d'interaction avec Prolog
└── history/ # Dossier généré automatiquement pour stocker les faits
└── enquete_with_facts*\*.pl # Fichiers d'enquête générés