"""
4Sorge - Pension Fund Simulator
A comprehensive pension fund calculator that helps users simulate and compare different pension scenarios.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np
from io import BytesIO
import base64

# Constants
DATA_FILE = "pension_data.json"
DEFAULT_PENSION_DATA = {
    "current_pension_value": 0,
    "current_value_date": date.today().isoformat(),
    "birth_date": "1990-01-01",
    "retirement_age": 65,
    "current_salary": 60000,
    "maximum_salary": 120000,
    "years_to_max_salary": 15,
    "expected_yield": 5.0,
    "personal_contribution_ranges": [
        {
            "age_from": 18, 
            "age_to": 25, 
            "options": [4.0, 6.0, 8.0]
        },
        {
            "age_from": 25, 
            "age_to": 35, 
            "options": [6.0, 7.0, 9.0]
        },
        {
            "age_from": 35, 
            "age_to": 50, 
            "options": [7.0, 9.0, 11.0]
        },
        {
            "age_from": 50, 
            "age_to": 65, 
            "options": [8.0, 10.0, 12.0]
        }
    ],
    "employer_contributions": [
        {"age_from": 18, "age_to": 25, "percentage": 6.0},
        {"age_from": 25, "age_to": 35, "percentage": 9.0},
        {"age_from": 35, "age_to": 45, "percentage": 14.0},
        {"age_from": 45, "age_to": 55, "percentage": 18.0},
        {"age_from": 55, "age_to": 65, "percentage": 20.0}
    ],
    "pension_plans": {},
    "language": "en",
    "has_13th_salary": False,
    "bonus_type": "percentage",  # "percentage" or "fixed"
    "bonus_percentage": 0.0,
    "bonus_fixed": 0.0,
    "coordination_fees": [
        {"from_year": 2000, "amount": 25725}
    ],
    "occupation_levels": [
        {"from_year": 2000, "percentage": 100.0}
    ]
}

# Translations
TRANSLATIONS = {
    "en": {
        "app_title": "4Sorge - Pension Fund Simulator",
        "app_subtitle": "Simulate and compare your pension scenarios",
        "navigation": "Navigation",
        "pension_calculator": "Pension Calculator",
        "plan_management": "Plan Management",
        "comparison": "Comparison",
        "personal_information": "Personal Information",
        "date_of_birth": "Date of birth",
        "retirement_age": "Retirement age",
        "salary_information": "Salary Information",
        "current_salary": "Current annual salary",
        "maximum_salary": "Expected maximum salary",
        "years_to_max": "Years to reach maximum salary",
        "pension_fund_info": "Pension Fund Information",
        "current_pension_value": "Current pension fund value",
        "as_of_date": "As of date",
        "expected_yield": "Expected annual yield (%)",
        "contribution_options": "Contribution Options",
        "personal_contributions": "Personal Contributions",
        "employer_contributions": "Employer Contributions",
        "simulation_results": "Simulation Results",
        "final_values": "Final Pension Values at Retirement",
        "option": "Option",
        "final_value": "Final Value",
        "fund_growth_comparison": "Pension Fund Growth Comparison",
        "total_fund_value": "Total Fund Value ($)",
        "age": "Age (years)",
        "select_option": "Select an option to view details",
        "detailed_projection": "Detailed Projection for",
        "salary": "Salary",
        "personal_contribution": "Personal Contribution",
        "employer_contribution": "Employer Contribution",
        "total_contribution": "Total Contribution",
        "fund_value": "Fund Value",
        "annual_contributions": "Annual Contributions",
        "existing_plans": "Existing Plans",
        "no_saved_plans": "No saved pension plans yet. Create one below.",
        "select_plan": "Select a plan to view/edit",
        "delete_plan": "Delete Plan",
        "duplicate_plan": "Duplicate Plan",
        "create_new_plan": "Create New Plan",
        "plan_name": "Plan name",
        "create_from_current": "Create from current settings",
        "compare_pension_plans": "Compare Pension Plans",
        "no_plans_for_comparison": "No saved pension plans available for comparison. Please create some plans first.",
        "select_plans_to_compare": "Select plans to compare",
        "include_current_settings": "Include current settings in comparison",
        "final_value_comparison": "Final Value Comparison",
        "key_metrics_comparison": "Key Metrics Comparison",
        "plan": "Plan",
        "starting_value": "Starting Value",
        "total_growth": "Total Growth",
        "avg_annual_contribution": "Average Annual Contribution",
        "years_to_retirement": "Years to Retirement",
        "language": "Language",
        "13th_salary": "13th Salary",
        "bonus_settings": "Bonus Settings",
        "no_bonus": "No Bonus",
        "percentage_bonus": "Percentage of Salary",
        "fixed_amount": "Fixed Amount",
        "bonus_percentage": "Bonus Percentage (%)",
        "bonus_amount": "Bonus Amount",
        "monthly": "Monthly",
        "yearly": "Yearly",
        "toggle_view": "Toggle View",
        "date": "Date",
        "month": "Month",
        "year": "Year",
        "from_age": "From age",
        "to_age": "To age",
        "contribution_percentage": "Contribution (%)",
        "number_of_ranges": "Number of age ranges",
        "range": "Range",
        "configure_employer_contributions": "Configure employer contribution rates by age range:",
        "set_contribution_options": "Set 3 personal contribution options to compare:",
        "current_settings": "Current Settings",
        "no_data_available": "No data available for the specified parameters. Please check your inputs.",
        "plan_deleted": "Plan '{0}' deleted.",
        "plan_duplicated": "Plan duplicated as '{0}'",
        "plan_created": "Plan '{0}' created successfully!",
        "enter_plan_name": "Please enter a plan name.",
        "plan_exists": "A plan with this name already exists.",
        "select_one_plan": "Please select at least one plan to compare.",
        "no_data_for_comparison": "No data available for comparison.",
        "coordination_fee": "Coordination Fee",
        "from_year": "From Year",
        "amount": "Amount",
        "number_of_entries": "Number of entries",
        "coordination_fee_info": "Configure coordination fees that will be deducted from salary before calculating contributions.",
        "occupation_level": "Degree of Occupation",
        "percentage": "Percentage",
        "occupation_info": "Configure your degree of occupation over time (100% = full-time)",
        "check_fund_value": "Check Fund Value at Specific Date",
        "select_month_year": "Select month and year to check fund value",
        "show_value": "Show Value",
        "fund_value_at_date": "Fund value at {0}",
        "insurable_salary": "Insurable Salary"
    },
    "de": {
        "app_title": "4Sorge - Pensionskassen-Simulator",
        "app_subtitle": "Simulieren und vergleichen Sie Ihre Pensionsszenarien",
        "navigation": "Navigation",
        "pension_calculator": "Pensionsrechner",
        "plan_management": "Planverwaltung",
        "comparison": "Vergleich",
        "personal_information": "Persönliche Informationen",
        "date_of_birth": "Geburtsdatum",
        "retirement_age": "Pensionsalter",
        "salary_information": "Gehaltsinformationen",
        "current_salary": "Aktuelles Jahresgehalt",
        "maximum_salary": "Erwartetes maximales Gehalt",
        "years_to_max": "Jahre bis zum Maximalgehalt",
        "pension_fund_info": "Pensionskasseninformationen",
        "current_pension_value": "Aktueller Pensionskassenwert",
        "as_of_date": "Stand",
        "expected_yield": "Erwartete jährliche Rendite (%)",
        "contribution_options": "Beitragsoptionen",
        "personal_contributions": "Persönliche Beiträge",
        "employer_contributions": "Arbeitgeberbeiträge",
        "simulation_results": "Simulationsergebnisse",
        "final_values": "Endwerte der Pensionskasse bei Pensionierung",
        "option": "Option",
        "final_value": "Endwert",
        "fund_growth_comparison": "Vergleich des Pensionskassenwachstums",
        "total_fund_value": "Gesamtwert der Pensionskasse (CHF)",
        "age": "Alter (Jahre)",
        "select_option": "Wählen Sie eine Option für Details",
        "detailed_projection": "Detaillierte Projektion für",
        "salary": "Gehalt",
        "personal_contribution": "Persönlicher Beitrag",
        "employer_contribution": "Arbeitgeberbeitrag",
        "total_contribution": "Gesamtbeitrag",
        "fund_value": "Kassenwert",
        "annual_contributions": "Jährliche Beiträge",
        "existing_plans": "Bestehende Pläne",
        "no_saved_plans": "Noch keine gespeicherten Pensionspläne. Erstellen Sie unten einen.",
        "select_plan": "Wählen Sie einen Plan zum Anzeigen/Bearbeiten",
        "delete_plan": "Plan löschen",
        "duplicate_plan": "Plan duplizieren",
        "create_new_plan": "Neuen Plan erstellen",
        "plan_name": "Planname",
        "create_from_current": "Aus aktuellen Einstellungen erstellen",
        "compare_pension_plans": "Pensionspläne vergleichen",
        "no_plans_for_comparison": "Keine gespeicherten Pensionspläne zum Vergleich verfügbar. Bitte erstellen Sie zuerst einige Pläne.",
        "select_plans_to_compare": "Wählen Sie Pläne zum Vergleichen",
        "include_current_settings": "Aktuelle Einstellungen im Vergleich einbeziehen",
        "final_value_comparison": "Endwertvergleich",
        "key_metrics_comparison": "Vergleich der Kennzahlen",
        "plan": "Plan",
        "starting_value": "Startwert",
        "total_growth": "Gesamtwachstum",
        "avg_annual_contribution": "Durchschnittlicher Jahresbeitrag",
        "years_to_retirement": "Jahre bis zur Pensionierung",
        "language": "Sprache",
        "13th_salary": "13. Monatsgehalt",
        "bonus_settings": "Bonuseinstellungen",
        "no_bonus": "Kein Bonus",
        "percentage_bonus": "Prozentsatz des Gehalts",
        "fixed_amount": "Fixer Betrag",
        "bonus_percentage": "Bonusprozentsatz (%)",
        "bonus_amount": "Bonusbetrag",
        "monthly": "Monatlich",
        "yearly": "Jährlich",
        "toggle_view": "Ansicht wechseln",
        "date": "Datum",
        "month": "Monat",
        "year": "Jahr",
        "from_age": "Ab Alter",
        "to_age": "Bis Alter",
        "contribution_percentage": "Beitrag (%)",
        "number_of_ranges": "Anzahl Altersgruppen",
        "range": "Bereich",
        "configure_employer_contributions": "Konfigurieren Sie die Arbeitgeberbeiträge nach Altersgruppen:",
        "set_contribution_options": "Legen Sie 3 persönliche Beitragsoptionen zum Vergleich fest:",
        "current_settings": "Aktuelle Einstellungen",
        "no_data_available": "Keine Daten für die angegebenen Parameter verfügbar. Bitte überprüfen Sie Ihre Eingaben.",
        "plan_deleted": "Plan '{0}' gelöscht.",
        "plan_duplicated": "Plan als '{0}' dupliziert",
        "plan_created": "Plan '{0}' erfolgreich erstellt!",
        "enter_plan_name": "Bitte geben Sie einen Plannamen ein.",
        "plan_exists": "Ein Plan mit diesem Namen existiert bereits.",
        "select_one_plan": "Bitte wählen Sie mindestens einen Plan zum Vergleich aus.",
        "no_data_for_comparison": "Keine Daten für den Vergleich verfügbar.",
        "coordination_fee": "Koordinationsbetrag",
        "from_year": "Ab Jahr",
        "amount": "Betrag",
        "number_of_entries": "Anzahl Einträge",
        "coordination_fee_info": "Konfigurieren Sie Koordinationsbeträge, die vom Gehalt abgezogen werden, bevor die Beiträge berechnet werden.",
        "occupation_level": "Beschäftigungsgrad",
        "percentage": "Prozentsatz",
        "occupation_info": "Konfigurieren Sie Ihren Beschäftigungsgrad über die Zeit (100% = Vollzeit)",
        "check_fund_value": "Kassenwert zu bestimmtem Datum prüfen",
        "select_month_year": "Monat und Jahr auswählen, um den Kassenwert zu prüfen",
        "show_value": "Wert anzeigen",
        "fund_value_at_date": "Kassenwert am {0}",
        "insurable_salary": "Versichertes Gehalt"
    },
    "fr": {
        "app_title": "4Sorge - Simulateur de caisse de pension",
        "app_subtitle": "Simulez et comparez vos scénarios de retraite",
        "navigation": "Navigation",
        "pension_calculator": "Calculateur de pension",
        "plan_management": "Gestion des plans",
        "comparison": "Comparaison",
        "personal_information": "Informations personnelles",
        "date_of_birth": "Date de naissance",
        "retirement_age": "Âge de la retraite",
        "salary_information": "Informations salariales",
        "current_salary": "Salaire annuel actuel",
        "maximum_salary": "Salaire maximum attendu",
        "years_to_max": "Années pour atteindre le salaire maximum",
        "pension_fund_info": "Informations sur la caisse de pension",
        "current_pension_value": "Valeur actuelle de la caisse de pension",
        "as_of_date": "Au",
        "expected_yield": "Rendement annuel attendu (%)",
        "contribution_options": "Options de contribution",
        "personal_contributions": "Contributions personnelles",
        "employer_contributions": "Contributions de l'employeur",
        "simulation_results": "Résultats de la simulation",
        "final_values": "Valeurs finales de la pension à la retraite",
        "option": "Option",
        "final_value": "Valeur finale",
        "fund_growth_comparison": "Comparaison de la croissance de la caisse de pension",
        "total_fund_value": "Valeur totale de la caisse (CHF)",
        "age": "Âge (années)",
        "select_option": "Sélectionnez une option pour voir les détails",
        "detailed_projection": "Projection détaillée pour",
        "salary": "Salaire",
        "personal_contribution": "Contribution personnelle",
        "employer_contribution": "Contribution de l'employeur",
        "total_contribution": "Contribution totale",
        "fund_value": "Valeur de la caisse",
        "annual_contributions": "Contributions annuelles",
        "existing_plans": "Plans existants",
        "no_saved_plans": "Aucun plan de pension sauvegardé. Créez-en un ci-dessous.",
        "select_plan": "Sélectionnez un plan à afficher/modifier",
        "delete_plan": "Supprimer le plan",
        "duplicate_plan": "Dupliquer le plan",
        "create_new_plan": "Créer un nouveau plan",
        "plan_name": "Nom du plan",
        "create_from_current": "Créer à partir des paramètres actuels",
        "compare_pension_plans": "Comparer les plans de pension",
        "no_plans_for_comparison": "Aucun plan de pension sauvegardé disponible pour la comparaison. Veuillez d'abord créer des plans.",
        "select_plans_to_compare": "Sélectionnez les plans à comparer",
        "include_current_settings": "Inclure les paramètres actuels dans la comparaison",
        "final_value_comparison": "Comparaison des valeurs finales",
        "key_metrics_comparison": "Comparaison des indicateurs clés",
        "plan": "Plan",
        "starting_value": "Valeur initiale",
        "total_growth": "Croissance totale",
        "avg_annual_contribution": "Contribution annuelle moyenne",
        "years_to_retirement": "Années jusqu'à la retraite",
        "language": "Langue",
        "13th_salary": "13ème salaire",
        "bonus_settings": "Paramètres de bonus",
        "no_bonus": "Pas de bonus",
        "percentage_bonus": "Pourcentage du salaire",
        "fixed_amount": "Montant fixe",
        "bonus_percentage": "Pourcentage de bonus (%)",
        "bonus_amount": "Montant du bonus",
        "monthly": "Mensuel",
        "yearly": "Annuel",
        "toggle_view": "Changer de vue",
        "date": "Date",
        "month": "Mois",
        "year": "Année",
        "from_age": "Dès l'âge",
        "to_age": "Jusqu'à l'âge",
        "contribution_percentage": "Contribution (%)",
        "number_of_ranges": "Nombre de tranches d'âge",
        "range": "Tranche",
        "configure_employer_contributions": "Configurez les taux de contribution de l'employeur par tranche d'âge :",
        "set_contribution_options": "Définissez 3 options de contribution personnelle à comparer :",
        "current_settings": "Paramètres actuels",
        "no_data_available": "Aucune donnée disponible pour les paramètres spécifiés. Veuillez vérifier vos entrées.",
        "plan_deleted": "Plan '{0}' supprimé.",
        "plan_duplicated": "Plan dupliqué sous '{0}'",
        "plan_created": "Plan '{0}' créé avec succès !",
        "enter_plan_name": "Veuillez entrer un nom de plan.",
        "plan_exists": "Un plan avec ce nom existe déjà.",
        "select_one_plan": "Veuillez sélectionner au moins un plan à comparer.",
        "no_data_for_comparison": "Aucune donnée disponible pour la comparaison.",
        "coordination_fee": "Montant de coordination",
        "from_year": "À partir de l'année",
        "amount": "Montant",
        "number_of_entries": "Nombre d'entrées",
        "coordination_fee_info": "Configurez les montants de coordination qui seront déduits du salaire avant le calcul des contributions.",
        "occupation_level": "Taux d'occupation",
        "percentage": "Pourcentage",
        "occupation_info": "Configurez votre taux d'occupation dans le temps (100% = temps plein)",
        "check_fund_value": "Vérifier la valeur de la caisse à une date spécifique",
        "select_month_year": "Sélectionnez le mois et l'année pour vérifier la valeur de la caisse",
        "show_value": "Afficher la valeur",
        "fund_value_at_date": "Valeur de la caisse au {0}",
        "insurable_salary": "Salaire assuré"
    },
    "it": {
        "app_title": "4Sorge - Simulatore di fondi pensione",
        "app_subtitle": "Simula e confronta i tuoi scenari pensionistici",
        "navigation": "Navigazione",
        "pension_calculator": "Calcolatore pensione",
        "plan_management": "Gestione piani",
        "comparison": "Confronto",
        "personal_information": "Informazioni personali",
        "date_of_birth": "Data di nascita",
        "retirement_age": "Età pensionabile",
        "salary_information": "Informazioni salariali",
        "current_salary": "Stipendio annuale attuale",
        "maximum_salary": "Stipendio massimo previsto",
        "years_to_max": "Anni per raggiungere lo stipendio massimo",
        "pension_fund_info": "Informazioni sul fondo pensione",
        "current_pension_value": "Valore attuale del fondo pensione",
        "as_of_date": "Al",
        "expected_yield": "Rendimento annuo previsto (%)",
        "contribution_options": "Opzioni di contribuzione",
        "personal_contributions": "Contributi personali",
        "employer_contributions": "Contributi del datore di lavoro",
        "simulation_results": "Risultati della simulazione",
        "final_values": "Valori finali della pensione al pensionamento",
        "option": "Opzione",
        "final_value": "Valore finale",
        "fund_growth_comparison": "Confronto della crescita del fondo pensione",
        "total_fund_value": "Valore totale del fondo (CHF)",
        "age": "Età (anni)",
        "select_option": "Seleziona un'opzione per vedere i dettagli",
        "detailed_projection": "Proiezione dettagliata per",
        "salary": "Stipendio",
        "personal_contribution": "Contributo personale",
        "employer_contribution": "Contributo del datore di lavoro",
        "total_contribution": "Contributo totale",
        "fund_value": "Valore del fondo",
        "annual_contributions": "Contributi annuali",
        "existing_plans": "Piani esistenti",
        "no_saved_plans": "Nessun piano pensionistico salvato. Creane uno qui sotto.",
        "select_plan": "Seleziona un piano da visualizzare/modificare",
        "delete_plan": "Elimina piano",
        "duplicate_plan": "Duplica piano",
        "create_new_plan": "Crea nuovo piano",
        "plan_name": "Nome del piano",
        "create_from_current": "Crea dalle impostazioni attuali",
        "compare_pension_plans": "Confronta piani pensionistici",
        "no_plans_for_comparison": "Nessun piano pensionistico salvato disponibile per il confronto. Si prega di creare prima alcuni piani.",
        "select_plans_to_compare": "Seleziona i piani da confrontare",
        "include_current_settings": "Includi le impostazioni attuali nel confronto",
        "final_value_comparison": "Confronto dei valori finali",
        "key_metrics_comparison": "Confronto delle metriche chiave",
        "plan": "Piano",
        "starting_value": "Valore iniziale",
        "total_growth": "Crescita totale",
        "avg_annual_contribution": "Contributo annuale medio",
        "years_to_retirement": "Anni al pensionamento",
        "language": "Lingua",
        "13th_salary": "13ª mensilità",
        "bonus_settings": "Impostazioni bonus",
        "no_bonus": "Nessun bonus",
        "percentage_bonus": "Percentuale dello stipendio",
        "fixed_amount": "Importo fisso",
        "bonus_percentage": "Percentuale bonus (%)",
        "bonus_amount": "Importo bonus",
        "monthly": "Mensile",
        "yearly": "Annuale",
        "toggle_view": "Cambia vista",
        "date": "Data",
        "month": "Mese",
        "year": "Anno",
        "from_age": "Dall'età",
        "to_age": "Fino all'età",
        "contribution_percentage": "Contributo (%)",
        "number_of_ranges": "Numero di fasce d'età",
        "range": "Fascia",
        "configure_employer_contributions": "Configura i tassi di contribuzione del datore di lavoro per fascia d'età:",
        "set_contribution_options": "Imposta 3 opzioni di contribuzione personale da confrontare:",
        "current_settings": "Impostazioni attuali",
        "no_data_available": "Nessun dato disponibile per i parametri specificati. Si prega di verificare gli input.",
        "plan_deleted": "Piano '{0}' eliminato.",
        "plan_duplicated": "Piano duplicato come '{0}'",
        "plan_created": "Piano '{0}' creato con successo!",
        "enter_plan_name": "Si prega di inserire un nome per il piano.",
        "plan_exists": "Esiste già un piano con questo nome.",
        "select_one_plan": "Si prega di selezionare almeno un piano da confrontare.",
        "no_data_for_comparison": "Nessun dato disponibile per il confronto.",
        "coordination_fee": "Trattenuta di coordinamento",
        "from_year": "Dall'anno",
        "amount": "Importo",
        "number_of_entries": "Numero di voci",
        "coordination_fee_info": "Configura le trattenute di coordinamento che verranno detratte dallo stipendio prima del calcolo dei contributi.",
        "occupation_level": "Grado di occupazione",
        "percentage": "Percentuale",
        "occupation_info": "Configura il tuo grado di occupazione nel tempo (100% = tempo pieno)",
        "check_fund_value": "Verifica il valore del fondo in una data specifica",
        "select_month_year": "Seleziona mese e anno per verificare il valore del fondo",
        "show_value": "Mostra valore",
        "fund_value_at_date": "Valore del fondo al {0}",
        "insurable_salary": "Salario assicurato"
    }
}

LANGUAGES = {
    "en": "English",
    "de": "Deutsch (Schweiz)",
    "fr": "Français (Suisse)",
    "it": "Italiano (Svizzera)"
}

# Get current language translations
def t(key):
    """Get translation for the current language"""
    return TRANSLATIONS.get(st.session_state.get('language', 'en'), {}).get(key, key)

# Data management functions
def load_data():
    """Load pension data from JSON file or create default if not exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Convert date strings back to date objects for non-pension plan data
            data["current_value_date"] = data.get("current_value_date", date.today().isoformat())
            
            # Migrate old format to new format if necessary
            if "personal_contribution_options" in data and isinstance(data["personal_contribution_options"], list):
                # Convert old simple list to new ranges format
                if isinstance(data["personal_contribution_options"][0], (int, float)):
                    default_ranges = DEFAULT_PENSION_DATA["personal_contribution_ranges"]
                    for i, default_range in enumerate(default_ranges):
                        if i < len(data["personal_contribution_options"]):
                            default_range["options"][1] = data["personal_contribution_options"][i]
                    data["personal_contribution_ranges"] = default_ranges
                    del data["personal_contribution_options"]
                    
            # Ensure coordination fees and occupation levels exist
            if "coordination_fees" not in data:
                data["coordination_fees"] = DEFAULT_PENSION_DATA["coordination_fees"]
            if "occupation_levels" not in data:
                data["occupation_levels"] = DEFAULT_PENSION_DATA["occupation_levels"]
    else:
        data = DEFAULT_PENSION_DATA.copy()
    
    # Initialize language in session state if not present
    if 'language' not in st.session_state:
        st.session_state.language = data.get('language', 'en')
    
    return data


def save_data(data):
    """Save pension data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_personal_contribution(age, personal_contribution_ranges, option_index):
    """Get personal contribution percentage for a specific age and option."""
    for range_data in personal_contribution_ranges:
        if range_data["age_from"] <= age < range_data["age_to"]:
            if option_index < len(range_data["options"]):
                return range_data["options"][option_index]
    return 0.0

def get_employer_contribution(age, employer_contributions):
    """Get employer contribution percentage for a specific age."""
    for contrib in employer_contributions:
        if contrib["age_from"] <= age < contrib["age_to"]:
            return contrib["percentage"]
    return 0.0


def get_coordination_fee(year, coordination_fees):
    """Get coordination fee for a specific year."""
    applicable_fee = 0
    for fee_entry in sorted(coordination_fees, key=lambda x: x["from_year"]):
        if year >= fee_entry["from_year"]:
            applicable_fee = fee_entry["amount"]
    return applicable_fee


def get_occupation_level(year, occupation_levels):
    """Get occupation level for a specific year."""
    applicable_level = 100.0
    for level_entry in sorted(occupation_levels, key=lambda x: x["from_year"]):
        if year >= level_entry["from_year"]:
            applicable_level = level_entry["percentage"]
    return applicable_level / 100.0  # Return as decimal (e.g., 0.8 for 80%)


def calculate_salary(current_salary, max_salary, years_to_max, years_from_now):
    """Calculate salary at a specific future year based on growth projection."""
    if years_from_now >= years_to_max:
        return max_salary
    if years_to_max == 0:
        return current_salary
    growth_rate = (max_salary / current_salary) ** (1 / years_to_max) - 1
    return current_salary * (1 + growth_rate) ** years_from_now


def calculate_yearly_salary_with_bonus(base_salary, has_13th_salary, bonus_type, bonus_percentage, bonus_fixed):
    """Calculate total yearly salary including 13th salary and bonus."""
    yearly_salary = base_salary
    
    if has_13th_salary:
        # If 13th salary is active, add an extra month
        yearly_salary = base_salary * (13/12)
    
    # Add bonus
    if bonus_type == "percentage" and bonus_percentage > 0:
        yearly_salary += base_salary * (bonus_percentage / 100)
    elif bonus_type == "fixed" and bonus_fixed > 0:
        yearly_salary += bonus_fixed
    
    return yearly_salary


def simulate_pension(birth_date, retirement_age, current_salary, max_salary, years_to_max,
                    yield_rate, personal_contribution_option_index, 
                    personal_contribution_ranges, employer_contributions,
                    current_pension_value=0, current_value_date=None,
                    has_13th_salary=False, bonus_type="percentage", 
                    bonus_percentage=0.0, bonus_fixed=0.0, monthly=False,
                    coordination_fees=None, occupation_levels=None):
    """Simulate pension fund growth over time."""
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    
    if current_value_date:
        if isinstance(current_value_date, str):
            current_value_date = datetime.strptime(current_value_date, "%Y-%m-%d").date()
        start_date = current_value_date
    else:
        start_date = birth_date + relativedelta(years=18)
    
    retirement_date = birth_date + relativedelta(years=retirement_age)
    
    if start_date >= retirement_date:
        return pd.DataFrame()
    
    # Create monthly projection if requested
    if monthly:
        dates = []
        ages = []
        years = []
        salaries = []
        insurable_salaries = []
        personal_contribs = []
        employer_contribs = []
        monthly_contributions = []
        fund_values = []
        
        current_fund_value = current_pension_value
        current_date = start_date
        
        while current_date <= retirement_date:
            dates.append(pd.Timestamp(current_date))
            year = current_date.year
            years.append(year)
            age = relativedelta(current_date, birth_date).years
            ages.append(age)
            
            # Calculate base salary for this month
            years_elapsed = relativedelta(current_date, date.today()).years
            base_salary = calculate_salary(current_salary, max_salary, years_to_max, max(0, years_elapsed))
            
            # Get occupation level for this year
            occupation_level = get_occupation_level(year, occupation_levels)
            adjusted_base_salary = base_salary * occupation_level
            
            # Calculate total yearly salary including 13th and bonus
            yearly_salary = calculate_yearly_salary_with_bonus(
                adjusted_base_salary, has_13th_salary, bonus_type, bonus_percentage, bonus_fixed
            )
            
            # Get coordination fee for this year
            coordination_fee = get_coordination_fee(year, coordination_fees)
            
            # Calculate insurable salary (yearly salary - coordination fee)
            insurable_yearly_salary = max(0, yearly_salary - coordination_fee)
            
            # Monthly salary is the yearly salary divided by 12 (even with 13th salary)
            monthly_salary = yearly_salary / 12
            monthly_insurable_salary = insurable_yearly_salary / 12
            
            salaries.append(monthly_salary)
            insurable_salaries.append(monthly_insurable_salary)
            
            # Calculate monthly contributions based on insurable salary
            personal_contribution_rate = get_personal_contribution(age, personal_contribution_ranges, personal_contribution_option_index)
            personal_contrib = monthly_insurable_salary * (personal_contribution_rate / 100)
            employer_contrib = monthly_insurable_salary * (get_employer_contribution(age, employer_contributions) / 100)
            
            personal_contribs.append(personal_contrib)
            employer_contribs.append(employer_contrib)
            
            monthly_contribution = personal_contrib + employer_contrib
            monthly_contributions.append(monthly_contribution)
            
            # Calculate fund value including yield (monthly compounding)
            monthly_yield = (1 + yield_rate / 100) ** (1/12) - 1
            current_fund_value = current_fund_value * (1 + monthly_yield) + monthly_contribution
            fund_values.append(current_fund_value)
            
            current_date += relativedelta(months=1)
        
        df = pd.DataFrame({
            "Date": dates,
            "Year": years,
            "Age": ages,
            "Salary": salaries,
            "Insurable Salary": insurable_salaries,
            "Personal Contribution": personal_contribs,
            "Employer Contribution": employer_contribs,
            "Total Contribution": monthly_contributions,
            "Fund Value": fund_values
        })
        df["Date"] = pd.to_datetime(df["Date"])  # Ensure datetime type
        return df
    else:
        # Original yearly projection
        dates = []
        ages = []
        years = []
        salaries = []
        insurable_salaries = []
        personal_contribs = []
        employer_contribs = []
        yearly_contributions = []
        fund_values = []
        
        current_fund_value = current_pension_value
        current_date = start_date
        
        while current_date <= retirement_date:
            dates.append(pd.Timestamp(current_date))
            year = current_date.year
            years.append(year)
            age = relativedelta(current_date, birth_date).years
            ages.append(age)
            
            # Calculate base salary for this year
            years_elapsed = relativedelta(current_date, date.today()).years
            base_salary = calculate_salary(current_salary, max_salary, years_to_max, max(0, years_elapsed))
            
            # Get occupation level for this year
            occupation_level = get_occupation_level(year, occupation_levels)
            adjusted_base_salary = base_salary * occupation_level
            
            # Calculate total yearly salary including 13th and bonus
            yearly_salary = calculate_yearly_salary_with_bonus(
                adjusted_base_salary, has_13th_salary, bonus_type, bonus_percentage, bonus_fixed
            )
            
            # Get coordination fee for this year
            coordination_fee = get_coordination_fee(year, coordination_fees)
            
            # Calculate insurable salary (yearly salary - coordination fee)
            insurable_salary = max(0, yearly_salary - coordination_fee)
            
            salaries.append(yearly_salary)
            insurable_salaries.append(insurable_salary)
            
            # Calculate contributions based on insurable salary
            personal_contribution_rate = get_personal_contribution(age, personal_contribution_ranges, personal_contribution_option_index)
            personal_contrib = insurable_salary * (personal_contribution_rate / 100)
            employer_contrib = insurable_salary * (get_employer_contribution(age, employer_contributions) / 100)
            
            personal_contribs.append(personal_contrib)
            employer_contribs.append(employer_contrib)
            
            yearly_contribution = personal_contrib + employer_contrib
            yearly_contributions.append(yearly_contribution)
            
            # Calculate fund value including yield
            current_fund_value = current_fund_value * (1 + yield_rate / 100) + yearly_contribution
            fund_values.append(current_fund_value)
            
            current_date += relativedelta(years=1)
        
        df = pd.DataFrame({
            "Date": dates,
            "Year": years,
            "Age": ages,
            "Salary": salaries,
            "Insurable Salary": insurable_salaries,
            "Personal Contribution": personal_contribs,
            "Employer Contribution": employer_contribs,
            "Total Contribution": yearly_contributions,
            "Fund Value": fund_values
        })
        df["Date"] = pd.to_datetime(df["Date"])  # Ensure datetime type
        return df

def get_print_css():
    """Return CSS for print styling."""
    return """
        <style>
        @media print {
            /* Hide Streamlit UI elements */
            header, footer {
                display: none !important;
            }
            .stApp > header {
                display: none !important;
            }
            .stApp [data-testid="stSidebar"] {
                display: none !important;
            }
            .stApp [data-testid="stHeader"] {
                display: none !important;
            }
            .stApp [data-testid="stToolbar"] {
                display: none !important;
            }
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            div[data-testid="stDecoration"] {
                display: none !important;
            }
            div[data-testid="stStatusWidget"] {
                display: none !important;
            }
            iframe {
                display: none !important;
            }
            
            /* Hide all buttons */
            button {
                display: none !important;
            }
            .stButton {
                display: none !important;
            }
            .print-button {
                display: none !important;
            }
            
            /* Hide input elements */
            .stTextInput {
                display: none !important;
            }
            .stSelectbox {
                display: none !important;
            }
            .stNumberInput {
                display: none !important;
            }
            .stRadio {
                display: none !important;
            }
            .stCheckbox {
                display: none !important;
            }
            .stSlider {
                display: none !important;
            }
            .stDateInput {
                display: none !important;
            }
            
            /* Hide tabs */
            .stTabs [data-baseweb="tab-list"] {
                display: none !important;
            }
            
            /* Hide expanders */
            .streamlit-expanderHeader {
                display: none !important;
            }
            
            /* Hide all sections except the results */
            .hide-from-print {
                display: none !important;
            }
            
            /* Hide option selector in print view */
            #select-an-option-to-view-details, #select-an-option-to-view-details + div,
            [data-testid="stSelectbox"], .stSelectbox {
                display: none !important;
            }
            
            /* Show print sections */
            .print-all-options {
                display: block !important;
            }
            
            /* Hide the selected option details section in print */
            .selected-option-details {
                display: none !important;
            }
            
            /* Style the content */
            .stMarkdown {
                font-size: 12pt !important;
            }
            .stMarkdown h1 {
                font-size: 24pt !important;
                margin-top: 10pt !important;
                margin-bottom: 10pt !important;
            }
            .stMarkdown h2 {
                font-size: 18pt !important;
                margin-top: 8pt !important;
                margin-bottom: 8pt !important;
            }
            .stMarkdown h3 {
                font-size: 14pt !important;
                margin-top: 6pt !important;
                margin-bottom: 6pt !important;
            }
            
            /* Ensure dataframes and charts are visible */
            .dataframe {
                width: 100% !important;
                overflow: visible !important;
                font-size: 10pt !important;
                page-break-inside: auto !important;
            }
            .dataframe th, .dataframe td {
                padding: 5px !important;
                border: 1px solid #ddd !important;
            }
            .dataframe th {
                background-color: #f8f9fa !important;
                font-weight: bold !important;
            }
            
            /* Repeat headers when tables break across pages */
            thead {
                display: table-header-group !important;
            }
            tr {
                page-break-inside: avoid !important;
                page-break-after: auto !important;
            }
            
            canvas, .js-plotly-plot, .plotly {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                page-break-inside: avoid !important;
            }
            
            /* Remove margins */
            .element-container {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* Hide plotly modebar */
            .modebar {
                display: none !important;
            }
            
            /* Adjust page margins */
            @page {
                margin: 2cm;
                size: A4 portrait;
            }
            
            /* Ensure content is not cut off */
            body {
                overflow: visible !important;
            }
            .main .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            
            /* Show print header */
            .print-header {
                display: block !important;
                text-align: center;
                margin-bottom: 20pt;
                border-bottom: 1px solid #ccc;
                padding-bottom: 10pt;
            }
            .print-header h1 {
                margin: 0;
                padding: 0;
            }
            .print-header p {
                margin: 5pt 0 0 0;
                font-size: 10pt;
                color: #666;
            }
        }
        
        /* Hide print header in normal view */
        .print-header {
            display: none;
        }
        
        /* Style for the print button */
        .print-button {
            background-color: #007bff;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            margin: 1rem 0;
        }
        .print-button:hover {
            background-color: #0056b3;
        }
        
        /* Hide print sections in normal view */
        .print-all-options {
            display: none;
        }
        
        /* Hide these sections in print */
        @media print {
            .hide-in-print {
                display: none !important;
            }
        }
        </style>
    """

def get_fund_value_at_date(simulation_df, target_date):
    """Get the fund value at a specific date from the simulation."""
    if simulation_df.empty:
        return None
        
    # Find the row with the closest date to the target date
    simulation_df['date_diff'] = abs((simulation_df['Date'] - pd.Timestamp(target_date)).dt.total_seconds())
    closest_row = simulation_df.loc[simulation_df['date_diff'].idxmin()]
    
    return closest_row['Fund Value']


# Streamlit app
def main():
    st.set_page_config(
        page_title="4Sorge - Pension Fund Simulator",
        page_icon="📈",
        layout="wide"
    )
    
    # Load data
    data = load_data()
    
    # Language selection in sidebar
    selected_language = st.sidebar.selectbox(
        "Language / Sprache / Langue / Lingua",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(data.get("language", "en")),
        key="language_selector"
    )
    
    if selected_language != data.get("language", "en"):
        data["language"] = selected_language
        st.session_state.language = selected_language
        save_data(data)
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    
    st.title(t("app_title"))
    st.caption(t("app_subtitle"))
    
    # Print CSS
    st.markdown(get_print_css(), unsafe_allow_html=True)
    
    # Sidebar for navigation
    menu_options = [t("pension_calculator"), t("plan_management"), t("comparison")]
    selected_menu = st.sidebar.selectbox(t("navigation"), menu_options)
    
    if selected_menu == t("pension_calculator"):
        pension_calculator_page(data)
    elif selected_menu == t("plan_management"):
        plan_management_page(data)
    elif selected_menu == t("comparison"):
        comparison_page(data)


def pension_calculator_page(data):
    # Wrap header and configuration sections in hide-from-print divs
    st.markdown('<div class="hide-from-print">', unsafe_allow_html=True)
    
    st.header(t("pension_calculator"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t("personal_information"))
        birth_date = st.date_input(
            t("date_of_birth"),
            value=datetime.strptime(data["birth_date"], "%Y-%m-%d").date()
        )
        data["birth_date"] = birth_date.strftime("%Y-%m-%d")
        
        retirement_age = st.number_input(
            t("retirement_age"),
            min_value=50,
            max_value=75,
            value=data["retirement_age"]
        )
        data["retirement_age"] = retirement_age
        
        st.subheader(t("salary_information"))
        current_salary = st.number_input(
            t("current_salary"),
            min_value=0,
            value=data["current_salary"],
            step=1000
        )
        data["current_salary"] = current_salary
        
        # Fix for max_salary issue: ensure default value is always at least current_salary
        default_max_salary = max(data["maximum_salary"], current_salary)
        max_salary = st.number_input(
            t("maximum_salary"),
            min_value=current_salary,
            value=default_max_salary,
            step=1000
        )
        data["maximum_salary"] = max_salary
        
        years_to_max = st.number_input(
            t("years_to_max"),
            min_value=0,
            max_value=50,
            value=data["years_to_max_salary"]
        )
        data["years_to_max_salary"] = years_to_max
        
        # 13th salary and bonus settings
        st.subheader(t("bonus_settings"))
        has_13th_salary = st.checkbox(
            t("13th_salary"),
            value=data.get("has_13th_salary", False)
        )
        data["has_13th_salary"] = has_13th_salary
        
        bonus_type = st.radio(
            t("bonus_settings"),
            ["no_bonus", "percentage_bonus", "fixed_amount"],
            format_func=lambda x: t(x),
            horizontal=True,
            index=0 if data.get("bonus_type", "percentage") == "no_bonus" else 1 if data.get("bonus_type", "percentage") == "percentage" else 2
        )
        
        if bonus_type == "percentage_bonus":
            data["bonus_type"] = "percentage"
            bonus_percentage = st.number_input(
                t("bonus_percentage"),
                min_value=0.0,
                max_value=100.0,
                value=data.get("bonus_percentage", 0.0),
                step=0.5
            )
            data["bonus_percentage"] = bonus_percentage
            data["bonus_fixed"] = 0.0
        elif bonus_type == "fixed_amount":
            data["bonus_type"] = "fixed"
            bonus_fixed = st.number_input(
                t("bonus_amount"),
                min_value=0,
                value=data.get("bonus_fixed", 0),
                step=1000
            )
            data["bonus_fixed"] = bonus_fixed
            data["bonus_percentage"] = 0.0
        else:
            data["bonus_type"] = "no_bonus"
            data["bonus_percentage"] = 0.0
            data["bonus_fixed"] = 0.0
    
    with col2:
        st.subheader(t("pension_fund_info"))
        
        current_pension_value = st.number_input(
            t("current_pension_value"),
            min_value=0,
            value=data["current_pension_value"],
            step=1000
        )
        data["current_pension_value"] = current_pension_value
        
        current_value_date = st.date_input(
            t("as_of_date"),
            value=datetime.strptime(data["current_value_date"], "%Y-%m-%d").date()
        )
        data["current_value_date"] = current_value_date.strftime("%Y-%m-%d")
        
        expected_yield = st.number_input(
            t("expected_yield"),
            min_value=0.0,
            max_value=20.0,
            value=data["expected_yield"],
            step=0.1
        )
        data["expected_yield"] = expected_yield
        
        st.subheader(t("contribution_options"))
        contribution_tab, employer_tab, coordination_tab, occupation_tab = st.tabs([
            t("personal_contributions"), 
            t("employer_contributions"), 
            t("coordination_fee"),
            t("occupation_level")
        ])
        
        with contribution_tab:
            st.write(t("set_contribution_options"))
            
            # Number of personal contribution ranges
            num_personal_ranges = st.number_input(
                t("number_of_ranges"),
                min_value=1,
                max_value=10,
                value=len(data.get("personal_contribution_ranges", DEFAULT_PENSION_DATA["personal_contribution_ranges"])),
                key="num_personal_ranges"
            )
            
            personal_contribution_ranges = []
            for i in range(num_personal_ranges):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(5)
                
                if "personal_contribution_ranges" in data and i < len(data["personal_contribution_ranges"]):
                    default_range = data["personal_contribution_ranges"][i]
                else:
                    default_range = {
                        "age_from": 18 + i * 10,
                        "age_to": 28 + i * 10,
                        "options": [4.0 + i, 6.0 + i, 8.0 + i]
                    }
                
                with cols[0]:
                    age_from = st.number_input(
                        t("from_age"),
                        min_value=18,
                        max_value=data["retirement_age"],
                        value=default_range["age_from"],
                        key=f"personal_age_from_{i}"
                    )
                
                with cols[1]:
                    age_to = st.number_input(
                        t("to_age"),
                        min_value=age_from + 1,
                        max_value=data["retirement_age"] + 1,
                        value=default_range["age_to"],
                        key=f"personal_age_to_{i}"
                    )
                
                options = []
                for j, col in enumerate([cols[2], cols[3], cols[4]]):
                    with col:
                        option_value = st.number_input(
                            f"{t('option')} {j+1} (%)",
                            min_value=0.0,
                            max_value=50.0,
                            value=default_range["options"][j] if j < len(default_range["options"]) else 6.0 + j,
                            step=0.5,
                            key=f"personal_option_{i}_{j}"
                        )
                        options.append(option_value)
                
                personal_contribution_ranges.append({
                    "age_from": age_from,
                    "age_to": age_to,
                    "options": options
                })
            
            data["personal_contribution_ranges"] = personal_contribution_ranges
        
        with employer_tab:
            st.write(t("configure_employer_contributions"))
            num_ranges = st.number_input(
                t("number_of_ranges"),
                min_value=1,
                max_value=10,
                value=len(data["employer_contributions"]),
                key="num_employer_ranges"
            )
            
            employer_contributions = []
            for i in range(num_ranges):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(3)
                
                default_range = data["employer_contributions"][i] if i < len(data["employer_contributions"]) else {
                    "age_from": 18 + i * 10,
                    "age_to": 28 + i * 10,
                    "percentage": 6.0 + i * 2
                }
                
                with cols[0]:
                    age_from = st.number_input(
                        t("from_age"),
                        min_value=18,
                        max_value=data["retirement_age"],
                        value=default_range["age_from"],
                        key=f"age_from_{i}"
                    )
                
                with cols[1]:
                    age_to = st.number_input(
                        t("to_age"),
                        min_value=age_from + 1,
                        max_value=data["retirement_age"] + 1,
                        value=default_range["age_to"],
                        key=f"age_to_{i}"
                    )
                
                with cols[2]:
                    percentage = st.number_input(
                        t("contribution_percentage"),
                        min_value=0.0,
                        max_value=50.0,
                        value=default_range["percentage"],
                        step=0.5,
                        key=f"percentage_{i}"
                    )
                
                employer_contributions.append({
                    "age_from": age_from,
                    "age_to": age_to,
                    "percentage": percentage
                })
            
            data["employer_contributions"] = employer_contributions
        
        with coordination_tab:
            st.write(t("coordination_fee_info"))
            num_entries = st.number_input(
                t("number_of_entries"),
                min_value=1,
                max_value=10,
                value=len(data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"])),
                key="num_coordination_fees"
            )
            
            coordination_fees = []
            for i in range(num_entries):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(2)
                
                if "coordination_fees" in data and i < len(data["coordination_fees"]):
                    default_entry = data["coordination_fees"][i]
                else:
                    default_entry = {"from_year": 2000 + i * 10, "amount": 25000 + i * 1000}
                
                with cols[0]:
                    from_year = st.number_input(
                        t("from_year"),
                        min_value=1900,
                        max_value=2100,
                        value=default_entry["from_year"],
                        key=f"coord_from_year_{i}"
                    )
                
                with cols[1]:
                    amount = st.number_input(
                        t("amount"),
                        min_value=0,
                        value=default_entry["amount"],
                        step=1000,
                        key=f"coord_amount_{i}"
                    )
                
                coordination_fees.append({
                    "from_year": from_year,
                    "amount": amount
                })
            
            data["coordination_fees"] = coordination_fees
            
        with occupation_tab:
            st.write(t("occupation_info"))
            num_entries = st.number_input(
                t("number_of_entries"),
                min_value=1,
                max_value=10,
                value=len(data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])),
                key="num_occupation_levels"
            )
            
            occupation_levels = []
            for i in range(num_entries):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(2)
                
                if "occupation_levels" in data and i < len(data["occupation_levels"]):
                    default_entry = data["occupation_levels"][i]
                else:
                    default_entry = {"from_year": 2000 + i * 10, "percentage": 100.0}
                
                with cols[0]:
                    from_year = st.number_input(
                        t("from_year"),
                        min_value=1900,
                        max_value=2100,
                        value=default_entry["from_year"],
                        key=f"occ_from_year_{i}"
                    )
                
                with cols[1]:
                    percentage = st.number_input(
                        t("percentage"),
                        min_value=0.0,
                        max_value=100.0,
                        value=default_entry["percentage"],
                        step=10.0,
                        key=f"occ_percentage_{i}"
                    )
                
                occupation_levels.append({
                    "from_year": from_year,
                    "percentage": percentage
                })
            
            data["occupation_levels"] = occupation_levels
    
    # Save updated data
    save_data(data)
    
    # End hide-from-print section
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulate and display results
    st.header(t("simulation_results"))
    
    # Toggle for yearly/monthly view (wrapped in hide-from-print)
    st.markdown('<div class="hide-from-print">', unsafe_allow_html=True)
    view_toggle = st.radio(
        t("toggle_view"),
        [t("yearly"), t("monthly")],
        horizontal=True
    )
    is_monthly = view_toggle == t("monthly")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulate for each personal contribution option
    simulations = []
    for i in range(3):  # Always have 3 options
        sim = simulate_pension(
            data["birth_date"],
            data["retirement_age"],
            data["current_salary"],
            data["maximum_salary"],
            data["years_to_max_salary"],
            data["expected_yield"],
            i,  # Option index (0, 1, or 2)
            data["personal_contribution_ranges"],
            data["employer_contributions"],
            data["current_pension_value"],
            data["current_value_date"],
            data.get("has_13th_salary", False),
            data.get("bonus_type", "percentage"),
            data.get("bonus_percentage", 0.0),
            data.get("bonus_fixed", 0.0),
            is_monthly,
            data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"]),
            data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])
        )
        if not sim.empty:
            sim["Option"] = f"{t('option')} {i+1}"
            simulations.append(sim)
    
    # Check Fund Value at Specific Date (wrapped in hide-from-print)
    st.markdown('<div class="hide-from-print">', unsafe_allow_html=True)
    st.subheader(t("check_fund_value"))
    check_date = st.date_input(t("select_month_year"), value=date.today())
    
    if st.button(t("show_value")):
        for idx, sim in enumerate(simulations):
            # Make sure we simulate monthly for accurate date checking
            monthly_sim = simulate_pension(
                data["birth_date"],
                data["retirement_age"],
                data["current_salary"],
                data["maximum_salary"],
                data["years_to_max_salary"],
                data["expected_yield"],
                idx,  # Use enumeration index directly
                data["personal_contribution_ranges"],
                data["employer_contributions"],
                data["current_pension_value"],
                data["current_value_date"],
                data.get("has_13th_salary", False),
                data.get("bonus_type", "percentage"),
                data.get("bonus_percentage", 0.0),
                data.get("bonus_fixed", 0.0),
                True,  # Always monthly for this calculation
                data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"]),
                data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])
            )
            value = get_fund_value_at_date(monthly_sim, check_date)
            
            # Get option name defensively
            try:
                option_name = sim["Option"].iloc[0]
            except:
                option_name = f"{t('option')} {idx+1}"  # Fallback
            
            if value is not None:
                st.info(f"{option_name}: {t('fund_value_at_date').format(check_date.strftime('%B %Y'))} = CHF {value:,.2f}")
            else:
                st.warning(f"{option_name}: {t('no_data_available')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if simulations:
        # Combine all simulations
        combined_df = pd.concat(simulations)
        
        # Display final values for each option
        st.subheader(t("final_values"))
        final_values = []
        for sim in simulations:
            final_value = sim["Fund Value"].iloc[-1]
            option_name = sim["Option"].iloc[0]
            final_values.append({"Option": option_name, "Final Value": final_value})
        
        final_values_df = pd.DataFrame(final_values)
        
        # Add CSS for better table printing
        st.markdown("""
            <style>
            .dataframe {
                page-break-inside: avoid !important;
            }
            .dataframe thead {
                display: table-header-group !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(final_values_df.style.format({"Final Value": "CHF {:,.0f}"}))
        
        # Plot comparison
        fig = px.line(combined_df, x="Age", y="Fund Value", color="Option",
                     title=t("fund_growth_comparison"),
                     labels={"Fund Value": t("total_fund_value"), "Age": t("age")})
        
        # Update hover template to include year
        fig.update_traces(
            hovertemplate=f'{t("age")}: %{{x}}<br>{t("year")}: %{{customdata}}<br>{t("fund_value")}: CHF %{{y:,.0f}}'
        )
        fig.update_layout(hovermode="x unified")
        fig.update_traces(customdata=combined_df["Year"])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Option selector and selected option details (wrapped in hide-from-print)
        st.markdown('<div class="hide-from-print">', unsafe_allow_html=True)
        selected_option = st.selectbox(
            t("select_option"),
            [sim["Option"].iloc[0] for sim in simulations]
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show selected option detailed view in web (wrapped in selected-option-details)
        st.markdown('<div class="selected-option-details">', unsafe_allow_html=True)
        selected_sim = next(sim for sim in simulations if sim["Option"].iloc[0] == selected_option)
        
        # Detailed table
        st.subheader(f"{t('detailed_projection')} {selected_option}")
        
        # Format the table differently for monthly vs yearly view
        if is_monthly:
            detailed_df = selected_sim.copy()
            detailed_df["Month"] = detailed_df["Date"].dt.strftime("%b %Y")
            columns_to_show = ["Month", "Age", "Salary", "Insurable Salary", "Personal Contribution", "Employer Contribution", "Total Contribution", "Fund Value"]
        else:
            detailed_df = selected_sim.copy()
            detailed_df["Year"] = detailed_df["Date"].dt.year
            columns_to_show = ["Year", "Age", "Salary", "Insurable Salary", "Personal Contribution", "Employer Contribution", "Total Contribution", "Fund Value"]
        
        formatted_df = detailed_df[columns_to_show].style.format({
            "Salary": "CHF {:,.0f}",
            "Insurable Salary": "CHF {:,.0f}",
            "Personal Contribution": "CHF {:,.0f}",
            "Employer Contribution": "CHF {:,.0f}",
            "Total Contribution": "CHF {:,.0f}",
            "Fund Value": "CHF {:,.0f}"
        })
        
        st.dataframe(formatted_df)
        
        # Contribution breakdown chart
        fig_contrib = go.Figure()
        fig_contrib.add_trace(go.Bar(
            x=selected_sim["Age"],
            y=selected_sim["Personal Contribution"],
            name=t("personal_contribution")
        ))
        fig_contrib.add_trace(go.Bar(
            x=selected_sim["Age"],
            y=selected_sim["Employer Contribution"],
            name=t("employer_contribution")
        ))
        fig_contrib.update_layout(
            barmode="stack",
            title=f"{t('annual_contributions')} - {selected_option}",
            xaxis_title=t("age"),
            yaxis_title=t("total_contribution"),
            hovermode="x unified"
        )
        st.plotly_chart(fig_contrib, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Print-only section: show all options (hidden in web view)
        st.markdown('<div class="print-all-options">', unsafe_allow_html=True)
        for sim in simulations:
            option_name = sim["Option"].iloc[0]
            st.subheader(f"{t('detailed_projection')} {option_name}")
            
            # Format the table differently for monthly vs yearly view
            if is_monthly:
                detailed_df = sim.copy()
                detailed_df["Month"] = detailed_df["Date"].dt.strftime("%b %Y")
                columns_to_show = ["Month", "Age", "Salary", "Insurable Salary", "Personal Contribution", "Employer Contribution", "Total Contribution", "Fund Value"]
            else:
                detailed_df = sim.copy()
                detailed_df["Year"] = detailed_df["Date"].dt.year
                columns_to_show = ["Year", "Age", "Salary", "Insurable Salary", "Personal Contribution", "Employer Contribution", "Total Contribution", "Fund Value"]
            
            formatted_df = detailed_df[columns_to_show].style.format({
                "Salary": "CHF {:,.0f}",
                "Insurable Salary": "CHF {:,.0f}",
                "Personal Contribution": "CHF {:,.0f}",
                "Employer Contribution": "CHF {:,.0f}",
                "Total Contribution": "CHF {:,.0f}",
                "Fund Value": "CHF {:,.0f}"
            })
            
            st.dataframe(formatted_df)
            
            # Contribution breakdown chart
            fig_contrib = go.Figure()
            fig_contrib.add_trace(go.Bar(
                x=sim["Age"],
                y=sim["Personal Contribution"],
                name=t("personal_contribution")
            ))
            fig_contrib.add_trace(go.Bar(
                x=sim["Age"],
                y=sim["Employer Contribution"],
                name=t("employer_contribution")
            ))
            fig_contrib.update_layout(
                barmode="stack",
                title=f"{t('annual_contributions')} - {option_name}",
                xaxis_title=t("age"),
                yaxis_title=t("total_contribution"),
                hovermode="x unified"
            )
            st.plotly_chart(fig_contrib, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning(t("no_data_available"))

def plan_management_page(data):
    st.header(t("plan_management"))
    
    # List existing plans
    st.subheader(t("existing_plans"))
    if not data["pension_plans"]:
        st.info(t("no_saved_plans"))
    else:
        plan_names = list(data["pension_plans"].keys())
        selected_plan = st.selectbox(t("select_plan"), plan_names)
        
        if selected_plan:
            plan_data = data["pension_plans"][selected_plan]
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(t("delete_plan")):
                    del data["pension_plans"][selected_plan]
                    save_data(data)
                    st.success(t("plan_deleted").format(selected_plan))
                    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
            
            with col2:
                if st.button(t("duplicate_plan")):
                    new_name = f"{selected_plan} (copy)"
                    data["pension_plans"][new_name] = plan_data.copy()
                    save_data(data)
                    st.success(t("plan_duplicated").format(new_name))
            
            st.json(plan_data)
    
    # Create new plan
    st.subheader(t("create_new_plan"))
    plan_name = st.text_input(t("plan_name"))
    
    if st.button(t("create_from_current")):
        if plan_name and plan_name not in data["pension_plans"]:
            new_plan = {
                "birth_date": data["birth_date"],
                "retirement_age": data["retirement_age"],
                "current_salary": data["current_salary"],
                "maximum_salary": data["maximum_salary"],
                "years_to_max_salary": data["years_to_max_salary"],
                "expected_yield": data["expected_yield"],
                "personal_contribution_ranges": data["personal_contribution_ranges"],
                "employer_contributions": data["employer_contributions"],
                "current_pension_value": data["current_pension_value"],
                "current_value_date": data["current_value_date"],
                "has_13th_salary": data.get("has_13th_salary", False),
                "bonus_type": data.get("bonus_type", "percentage"),
                "bonus_percentage": data.get("bonus_percentage", 0.0),
                "bonus_fixed": data.get("bonus_fixed", 0.0),
                "coordination_fees": data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"]),
                "occupation_levels": data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])
            }
            data["pension_plans"][plan_name] = new_plan
            save_data(data)
            st.success(t("plan_created").format(plan_name))
        elif not plan_name:
            st.error(t("enter_plan_name"))
        else:
            st.error(t("plan_exists"))


def comparison_page(data):
    st.header(t("compare_pension_plans"))
    
    if not data["pension_plans"]:
        st.warning(t("no_plans_for_comparison"))
        return
    
    # Select plans to compare
    available_plans = list(data["pension_plans"].keys())
    selected_plans = st.multiselect(
        t("select_plans_to_compare"),
        available_plans,
        default=available_plans[:2] if len(available_plans) >= 2 else available_plans
    )
    
    if not selected_plans:
        st.info(t("select_one_plan"))
        return
    
    # Add current settings as a comparison option
    include_current = st.checkbox(t("include_current_settings"), value=True)
    
    if include_current:
        selected_plans.append(t("current_settings"))
    
    # Simulate and compare
    comparison_data = []
    
    for plan_name in selected_plans:
        if plan_name == t("current_settings"):
            plan_data = data
        else:
            plan_data = data["pension_plans"][plan_name]
        
        # Simulate for each personal contribution option
        for i in range(3):  # Always use 3 options
            sim = simulate_pension(
                plan_data["birth_date"],
                plan_data["retirement_age"],
                plan_data["current_salary"],
                plan_data["maximum_salary"],
                plan_data["years_to_max_salary"],
                plan_data["expected_yield"],
                i,  # Option index
                plan_data.get("personal_contribution_ranges", DEFAULT_PENSION_DATA["personal_contribution_ranges"]),
                plan_data["employer_contributions"],
                plan_data["current_pension_value"],
                plan_data["current_value_date"],
                plan_data.get("has_13th_salary", False),
                plan_data.get("bonus_type", "percentage"),
                plan_data.get("bonus_percentage", 0.0),
                plan_data.get("bonus_fixed", 0.0),
                False,
                plan_data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"]),
                plan_data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])
            )
            
            if not sim.empty:
                sim["Plan"] = plan_name
                sim["Contribution Option"] = f"{t('option')} {i+1}"
                comparison_data.append(sim)
    
    if not comparison_data:
        st.warning(t("no_data_for_comparison"))
        return
    
    # Combine all data
    comparison_df = pd.concat(comparison_data)
    
    # Create comparison visualizations
    st.subheader(t("final_value_comparison"))
    
    # Bar chart of final values
    final_values = []
    for sim in comparison_data:
        final_value = sim["Fund Value"].iloc[-1]
        plan_name = sim["Plan"].iloc[0]
        option = sim["Contribution Option"].iloc[0]
        final_values.append({
            "Plan": plan_name,
            "Option": option,
            "Final Value": final_value
        })
    
    final_values_df = pd.DataFrame(final_values)
    
    fig_bar = px.bar(
        final_values_df,
        x="Plan",
        y="Final Value",
        color="Option",
        barmode="group",
        title=t("final_value_comparison"),
        labels={"Final Value": t("final_value")}
    )
    fig_bar.update_traces(texttemplate='CHF %{y:,.0f}', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Line chart comparison over time
    fig_line = px.line(
        comparison_df,
        x="Age",
        y="Fund Value",
        color="Plan",
        line_dash="Contribution Option",
        title=t("fund_growth_comparison"),
        labels={"Fund Value": t("total_fund_value"), "Age": t("age")}
    )
    
    # Update hover template to include year
    fig_line.update_traces(
        hovertemplate=f'{t("age")}: %{{x}}<br>{t("year")}: %{{customdata}}<br>{t("fund_value")}: CHF %{{y:,.0f}}'
    )
    fig_line.update_layout(hovermode="x unified")
    fig_line.update_traces(customdata=comparison_df["Year"])
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Table comparison of key metrics
    st.subheader(t("key_metrics_comparison"))
    metrics = []
    
    for sim in comparison_data:
        plan_name = sim["Plan"].iloc[0]
        option = sim["Contribution Option"].iloc[0]
        
        metrics.append({
            t("plan"): plan_name,
            t("option"): option,
            t("starting_value"): sim["Fund Value"].iloc[0],
            t("final_value"): sim["Fund Value"].iloc[-1],
            t("total_growth"): sim["Fund Value"].iloc[-1] - sim["Fund Value"].iloc[0],
            t("avg_annual_contribution"): sim["Total Contribution"].mean(),
            t("years_to_retirement"): len(sim) - 1
        })
    
    metrics_df = pd.DataFrame(metrics)
    st.dataframe(
        metrics_df.style.format({
            t("starting_value"): "CHF {:,.0f}",
            t("final_value"): "CHF {:,.0f}",
            t("total_growth"): "CHF {:,.0f}",
            t("avg_annual_contribution"): "CHF {:,.0f}"
        })
    )


if __name__ == "__main__":
    main()