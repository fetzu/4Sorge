"""
4Sorge - Pension Fund Simulator
A comprehensive pension fund calculator that helps users simulate and compare different pension scenarios.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import numpy as np
from io import BytesIO, StringIO
import base64

# Constants
DEFAULT_PENSION_DATA = {
    "current_pension_value": 0,
    "current_value_date": date.today().isoformat(),
    "birth_date": "2000-01-01",
    "retirement_age": 65,
    "current_salary": 100000,
    "maximum_salary": 130434,
    "years_to_max_salary": 15,
    "expected_yield": 1.25,
    "personal_contribution_ranges": [
        {
            "age_from": 22, 
            "age_to": 34, 
            "options": [5.0, 5.85, 6.0]
        },
        {
            "age_from": 35, 
            "age_to": 44, 
            "options": [7.0, 7.25, 7.5]
        },
        {
            "age_from": 45, 
            "age_to": 54, 
            "options": [9.0, 9.4, 10.0]
        },
        {
            "age_from": 55, 
            "age_to": 65, 
            "options": [11.0, 12.5, 14.0]
        },
        {
            "age_from": 66, 
            "age_to": 70, 
            "options": [5.5, 5.85, 6.0]
        }
    ],
    "employer_contributions": [
        {"age_from": 22, "age_to": 34, "percentage": 6.9},
        {"age_from": 35, "age_to": 44, "percentage": 9.0},
        {"age_from": 45, "age_to": 54, "percentage": 16.6},
        {"age_from": 55, "age_to": 65, "percentage": 21.75},
        {"age_from": 66, "age_to": 70, "percentage": 5.85}
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
        "insurable_salary": "Insurable Salary",
        "download_data": "Download Data",
        "upload_data": "Upload Data",
        "data_management": "Data Management",
        "export_data": "Export data as JSON file to save all your settings and plans",
        "import_data": "Import data from a previously exported JSON file",
        "data_uploaded": "Data successfully uploaded!",
        "invalid_data": "The uploaded file contains invalid data. Please ensure it's a valid 4Sorge JSON file.",
        "data_privacy": "Data Privacy",
        "data_privacy_message": "Your data is processed on the application server only while you are actively using this app. It is not permanently stored or shared.",
        "print_report": "Print Report",
        "download_report": "Download Printable Report",
        "print_instructions_1": "1. Click the link above to download the report",
        "print_instructions_2": "2. Open the HTML file in your browser",
        "print_instructions_3": "3. Use your browser's print function (Ctrl+P or Cmd+P) to print the document"
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
        "insurable_salary": "Versichertes Gehalt",
        "download_data": "Daten herunterladen",
        "upload_data": "Daten hochladen",
        "data_management": "Datenverwaltung",
        "export_data": "Daten als JSON-Datei exportieren, um alle Einstellungen und Pläne zu speichern",
        "import_data": "Daten aus einer zuvor exportierten JSON-Datei importieren",
        "data_uploaded": "Daten erfolgreich hochgeladen!",
        "invalid_data": "Die hochgeladene Datei enthält ungültige Daten. Bitte stellen Sie sicher, dass es sich um eine gültige 4Sorge-JSON-Datei handelt.",
        "data_privacy": "Datenschutz",
        "data_privacy_message": "Ihre Daten werden nur während der aktiven Nutzung dieser App auf dem Anwendungsserver verarbeitet. Sie werden nicht dauerhaft gespeichert oder geteilt.",
        "print_report": "Bericht drucken",
        "download_report": "Druckbaren Bericht herunterladen",
        "print_instructions_1": "1. Klicken Sie auf den obigen Link, um den Bericht herunterzuladen",
        "print_instructions_2": "2. Öffnen Sie die HTML-Datei in Ihrem Browser",
        "print_instructions_3": "3. Verwenden Sie die Druckfunktion Ihres Browsers (Strg+P oder Cmd+P), um das Dokument zu drucken"
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
        "insurable_salary": "Salaire assuré",
        "download_data": "Télécharger les données",
        "upload_data": "Charger les données",
        "data_management": "Gestion des données",
        "export_data": "Exporter les données en fichier JSON pour sauvegarder tous vos paramètres et plans",
        "import_data": "Importer les données d'un fichier JSON exporté précédemment",
        "data_uploaded": "Données téléchargées avec succès !",
        "invalid_data": "Le fichier téléchargé contient des données invalides. Veuillez vous assurer qu'il s'agit d'un fichier JSON 4Sorge valide.",
        "data_privacy": "Confidentialité des données",
        "data_privacy_message": "Vos données sont traitées sur le serveur d'application uniquement pendant que vous utilisez activement cette application. Elles ne sont pas stockées de manière permanente ni partagées.",
        "print_report": "Imprimer le rapport",
        "download_report": "Télécharger le rapport imprimable",
        "print_instructions_1": "1. Cliquez sur le lien ci-dessus pour télécharger le rapport",
        "print_instructions_2": "2. Ouvrez le fichier HTML dans votre navigateur",
        "print_instructions_3": "3. Utilisez la fonction d'impression de votre navigateur (Ctrl+P ou Cmd+P) pour imprimer le document"
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
        "insurable_salary": "Salario assicurato",
        "download_data": "Scarica dati",
        "upload_data": "Carica dati",
        "data_management": "Gestione dati",
        "export_data": "Esporta i dati come file JSON per salvare tutte le impostazioni e i piani",
        "import_data": "Importa i dati da un file JSON esportato in precedenza",
        "data_uploaded": "Dati caricati con successo!",
        "invalid_data": "Il file caricato contiene dati non validi. Assicurati che sia un file JSON 4Sorge valido.",
        "data_privacy": "Privacy dei dati",
        "data_privacy_message": "I Suoi dati vengono elaborati sul server dell'applicazione solo durante l'utilizzo attivo di questa app. Non vengono memorizzati in modo permanente né condivisi.",
        "print_report": "Stampa rapporto",
        "download_report": "Scarica rapporto stampabile",
        "print_instructions_1": "1. Clicca sul link sopra per scaricare il rapporto",
        "print_instructions_2": "2. Apri il file HTML nel tuo browser",
        "print_instructions_3": "3. Utilizza la funzione di stampa del tuo browser (Ctrl+P o Cmd+P) per stampare il documento"
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

# Initialize session state with default data if not present
if 'pension_data' not in st.session_state:
    st.session_state.pension_data = DEFAULT_PENSION_DATA.copy()

# Initialize language in session state if not present
if 'language' not in st.session_state:
    st.session_state.language = st.session_state.pension_data.get('language', 'en')

# Data management functions
def export_data():
    """Create a downloadable JSON file of current data."""
    data_json = json.dumps(st.session_state.pension_data, indent=4, default=str)
    b64 = base64.b64encode(data_json.encode()).decode()
    return f"data:application/json;base64,{b64}"

def import_data(uploaded_file):
    """Import data from uploaded JSON file."""
    try:
        ## Add debug output
        #st.sidebar.write("Debug: Reading file...")
        
        content = uploaded_file.read()
        data = json.loads(content)
        
        # Validate the data structure
        required_keys = ["birth_date", "retirement_age", "current_salary", "personal_contribution_ranges", "employer_contributions"]
        
        ## More debug info
        #st.sidebar.write(f"Debug: Keys found: {list(data.keys())}")
        
        if all(key in data for key in required_keys):
            ## Debug before updating state
            #st.sidebar.write("Debug: Data valid, updating session state...")
            
            st.session_state.pension_data = data
            
            # Set processed flag to avoid refresh loop
            st.session_state.file_processed = True
            
            return True
        else:
            missing_keys = [key for key in required_keys if key not in data]
            #st.sidebar.write(f"Debug: Missing required keys: {missing_keys}")
            return False
    except json.JSONDecodeError as e:
        #st.sidebar.write(f"Debug: JSON decode error: {str(e)}")
        return False
    except Exception as e:
        #st.sidebar.write(f"Debug: Unexpected error: {str(e)}")
        return False

# Pension calculation functions remain the same
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
        # Add a flag to identify 13th month
        is_13th_month = []
        
        current_fund_value = current_pension_value
        current_date = start_date
        
        while current_date <= retirement_date:
            # Regular month processing
            dates.append(pd.Timestamp(current_date))
            year = current_date.year
            years.append(year)
            age = relativedelta(current_date, birth_date).years
            ages.append(age)
            is_13th_month.append(False)  # Regular month
            
            # Calculate base salary for this month
            years_elapsed = relativedelta(current_date, date.today()).years
            base_salary = calculate_salary(current_salary, max_salary, years_to_max, max(0, years_elapsed))
            
            # Get occupation level for this year
            occupation_level = get_occupation_level(year, occupation_levels)
            adjusted_base_salary = base_salary * occupation_level
            
            # Monthly salary (1/12 of annual)
            monthly_base = adjusted_base_salary / 12
            monthly_salary = monthly_base
            
            # Add any bonus amount to the monthly salary
            if bonus_type == "percentage" and bonus_percentage > 0:
                monthly_salary += (adjusted_base_salary * bonus_percentage / 100) / 12
            elif bonus_type == "fixed" and bonus_fixed > 0:
                monthly_salary += bonus_fixed / 12
            
            salaries.append(monthly_salary)
            
            # Get coordination fee for this year
            coordination_fee = get_coordination_fee(year, coordination_fees)
            monthly_coord_fee = coordination_fee / 12
            
            # Calculate insurable salary
            monthly_insurable_salary = max(0, monthly_salary - monthly_coord_fee)
            insurable_salaries.append(monthly_insurable_salary)
            
            # Calculate contributions
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
            
            # Add 13th month if December and has_13th_salary
            if has_13th_salary and current_date.month == 12:
                # Add 13th month right after December
                # Use same date as December but mark it as 13th month
                dates.append(pd.Timestamp(current_date))
                years.append(year)
                ages.append(age)
                is_13th_month.append(True)  # Mark as 13th month
                
                # 13th month has the base monthly salary
                salaries.append(monthly_base)
                
                # Calculate insurable salary for 13th month
                thirteenth_insurable = max(0, monthly_base - monthly_coord_fee)
                insurable_salaries.append(thirteenth_insurable)
                
                # Calculate contributions for 13th month
                thirteenth_personal = thirteenth_insurable * (personal_contribution_rate / 100)
                thirteenth_employer = thirteenth_insurable * (get_employer_contribution(age, employer_contributions) / 100)
                
                personal_contribs.append(thirteenth_personal)
                employer_contribs.append(thirteenth_employer)
                
                thirteenth_contribution = thirteenth_personal + thirteenth_employer
                monthly_contributions.append(thirteenth_contribution)
                
                # Calculate fund value after 13th month
                current_fund_value = current_fund_value * (1 + monthly_yield) + thirteenth_contribution
                fund_values.append(current_fund_value)
            
            # Move to next month
            current_date += relativedelta(months=1)
        
        # Create DataFrame with all the columns including the 13th month flag
        df = pd.DataFrame({
            "Date": dates,
            "Year": years,
            "Age": ages,
            "Salary": salaries,
            "Insurable Salary": insurable_salaries,
            "Personal Contribution": personal_contribs,
            "Employer Contribution": employer_contribs,
            "Total Contribution": monthly_contributions,
            "Fund Value": fund_values,
            "Is13thMonth": is_13th_month
        })
        
        return df
    else:
        # Original yearly projection code remains unchanged
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
    """Return minimal CSS styling for the app"""
    return """
        <style>
        /* Basic styling for the app */
        .dataframe {
            width: 100%;
            max-width: 100%;
        }
        </style>
    """

def generate_printable_html(simulations, is_monthly=False):
    """
    Generate a standalone HTML document for printing
    
    Parameters:
    - simulations: List of DataFrames with simulation results
    - is_monthly: Whether the view is monthly or yearly
    
    Returns:
    - HTML string of the printable document
    """
    if not simulations:
        return None
    
    # Prepare data for each section
    final_values_data = []
    for sim in simulations:
        final_value = sim["Fund Value"].iloc[-1]
        option_name = sim["Option"].iloc[0]
        final_values_data.append({"Option": option_name, "Final Value": final_value})
    
    # Convert to HTML tables
    final_values_df = pd.DataFrame(final_values_data)
    final_values_html = final_values_df.style.format({"Final Value": "CHF {:,.0f}"}).to_html()
    
    # Create detailed tables for each option
    detailed_tables = []
    for sim in simulations:
        option_name = sim["Option"].iloc[0]
        
        # Format the table
        if is_monthly:
            detailed_df = sim.copy()
            
            # Format month display with special handling for 13th month
            def format_month(row):
                if row.get("Is13thMonth", False):
                    # Format based on language
                    year = row["Year"]
                    if st.session_state.language == "de":
                        return f"13er {year}"
                    elif st.session_state.language == "fr":
                        return f"13e {year}"
                    elif st.session_state.language == "it":
                        return f"13a {year}"
                    else:  # default/english
                        return f"13th {year}"
                else:
                    return row["Date"].strftime("%b %Y")
            
            detailed_df["Month"] = detailed_df.apply(format_month, axis=1)
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
        
        table_html = formatted_df.to_html()
        detailed_tables.append((option_name, table_html))
    
    # Generate charts for comparison and each option
    import io
    import base64
    import plotly.io as pio
    
    # Comparison chart
    combined_df = pd.concat(simulations)
    fig_comparison = px.line(combined_df, x="Age", y="Fund Value", color="Option",
                title=t("fund_growth_comparison"),
                labels={"Fund Value": t("total_fund_value"), "Age": t("age")})
    
    fig_comparison.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    comparison_chart_img = pio.to_image(fig_comparison, format="png", width=800, height=400)
    comparison_chart_base64 = base64.b64encode(comparison_chart_img).decode('utf-8')
    
    # Contribution charts
    contribution_charts = []
    for sim in simulations:
        option_name = sim["Option"].iloc[0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sim["Age"],
            y=sim["Personal Contribution"],
            name=t("personal_contribution"),
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            x=sim["Age"],
            y=sim["Employer Contribution"],
            name=t("employer_contribution"),
            marker_color='#72b7ec'
        ))
        fig.update_layout(
            barmode="stack",
            title=f"{t('annual_contributions')} - {option_name}",
            xaxis_title=t("age"),
            yaxis_title=t("total_contribution"),
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        chart_img = pio.to_image(fig, format="png", width=800, height=400)
        chart_base64 = base64.b64encode(chart_img).decode('utf-8')
        contribution_charts.append((option_name, chart_base64))
    
    # Build the complete HTML document with proper page breaks
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pension Fund Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .page {{
                page-break-after: always;
                padding: 20px 30px;
            }}
            .last-page {{
                padding: 20px 30px;
            }}
            h1 {{
                font-size: 24px;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            h2 {{
                font-size: 20px;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            table {{
                width: calc(100% - 40px);
                margin: 20px auto;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            img {{
                max-width: calc(100% - 40px);
                height: auto;
                margin: 20px auto;
                display: block;
            }}
            @media print {{
                table thead {{
                    display: table-header-group;
                }}
                table tfoot {{
                    display: table-footer-group;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- Page 1: Final Values and Comparison Chart -->
        <div class="page">
            <h1>{t("final_values")}</h1>
            {final_values_html}
            
            <h1>{t("fund_growth_comparison")}</h1>
            <img src="data:image/png;base64,{comparison_chart_base64}" alt="Comparison Chart">
        </div>
    """
    
    # Add pages for each option (2, 3, 4)
    for i, ((option_name, table_html), (_, chart_base64)) in enumerate(zip(detailed_tables, contribution_charts)):
        page_class = "page" if i < len(detailed_tables) - 1 else "last-page"
        html += f"""
        <div class="{page_class}">
            <h1>{t("detailed_projection")} {option_name}</h1>
            {table_html}
            
            <h1>{t("annual_contributions")} - {option_name}</h1>
            <img src="data:image/png;base64,{chart_base64}" alt="Contributions Chart for {option_name}">
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html

def create_download_link(html, filename="pension_report.html"):
    """Create a download link for the HTML file"""
    import base64
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" target="_blank">{t("download_report")}</a>'
    return href

# Modify the chart creation functions to improve stability
def create_stable_plotly_chart(fig, container_id=None, use_container_width=True, static_plot=False):
    """
    Create a Plotly chart with improved stability to prevent duplication issues
    
    Parameters:
    - fig: The Plotly figure object
    - container_id: Optional ID for the container div
    - use_container_width: Whether to use container width
    - static_plot: Whether to render as static plot (for print)
    
    Returns:
    - The chart object
    """
    # Set stable dimensions to prevent auto-resizing issues
    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
    )
    
    # Create container div if ID provided
    if container_id:
        st.markdown(f'<div id="{container_id}" class="stable-chart-container">', unsafe_allow_html=True)
    
    # Configure chart options
    config = {
        'responsive': False,  # Disable responsive resizing
        'staticPlot': static_plot,  # Static for print, interactive for web
        'displayModeBar': not static_plot,  # Hide modebar in static plots
    }
    
    # Create the chart
    chart = st.plotly_chart(fig, use_container_width=use_container_width, config=config)
    
    # Close container if ID provided
    if container_id:
        st.markdown('</div>', unsafe_allow_html=True)
    
    return chart

def create_comparison_chart(simulations, container_id="main-comparison-chart"):
    """Create a stable comparison chart for all options"""
    # Combine all simulations
    combined_df = pd.concat(simulations)
    
    # Plot comparison with fixed dimensions
    fig = px.line(combined_df, x="Age", y="Fund Value", color="Option",
                title=t("fund_growth_comparison"),
                labels={"Fund Value": t("total_fund_value"), "Age": t("age")})
    
    # Update hover template to include year
    fig.update_traces(
        hovertemplate=f'{t("age")}: %{{x}}<br>{t("year")}: %{{customdata}}<br>{t("fund_value")}: CHF %{{y:,.0f}}'
    )
    fig.update_layout(
        hovermode="x unified",
        # Fixed dimensions to prevent resizing issues
        autosize=False,
        width=800,
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    fig.update_traces(customdata=combined_df["Year"])
    
    # Create container for the chart
    st.markdown(f'<div id="{container_id}" class="chart-container">', unsafe_allow_html=True)
    
    # Use stable config to prevent resizing
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        config={
            'responsive': False,  # Disable responsive behavior
            'staticPlot': False,   # Allow interactivity in web view
            'displayModeBar': True
        }
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_contribution_chart(sim_data, option_name, container_id=None, static_plot=False):
    """Create a stable contribution breakdown chart"""
    # Create unique ID if not provided
    if not container_id:
        container_id = f"contrib-chart-{option_name.replace(' ', '-')}"
    
    # Create container div
    st.markdown(f'<div id="{container_id}" class="chart-container">', unsafe_allow_html=True)
    
    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sim_data["Age"],
        y=sim_data["Personal Contribution"],
        name=t("personal_contribution"),
        marker_color='#1f77b4'  # Consistent blue color
    ))
    fig.add_trace(go.Bar(
        x=sim_data["Age"],
        y=sim_data["Employer Contribution"],
        name=t("employer_contribution"),
        marker_color='#72b7ec'  # Consistent light blue color
    ))
    fig.update_layout(
        barmode="stack",
        title=f"{t('annual_contributions')} - {option_name}",
        xaxis_title=t("age"),
        yaxis_title=t("total_contribution"),
        hovermode="x unified",
        # Fixed dimensions to prevent resizing issues
        autosize=False,
        width=800,
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Use stable config
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        config={
            'responsive': False,
            'staticPlot': static_plot,
            'displayModeBar': not static_plot
        }
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Initialize session state
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    
    if 'pension_data' not in st.session_state:
        st.session_state.pension_data = DEFAULT_PENSION_DATA.copy()
    
    if 'language' not in st.session_state:
        st.session_state.language = st.session_state.pension_data.get('language', 'en')
    
    # Add basic CSS
    st.markdown(get_print_css(), unsafe_allow_html=True)

    # Language selection in sidebar
    selected_language = st.sidebar.selectbox(
        "Language / Sprache / Langue / Lingua",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.session_state.pension_data["language"] = selected_language
        st.rerun()

    # Sidebar for navigation
    menu_options = [t("pension_calculator"), t("plan_management"), t("comparison")]
    
    selected_menu = st.sidebar.selectbox(
        t("navigation"), 
        menu_options
    )
    
    # Render the appropriate page to get simulations
    if selected_menu == t("pension_calculator"):
        simulations = pension_calculator_page()
    elif selected_menu == t("plan_management"):
        simulations = []  # No simulations on this page
        plan_management_page()
    elif selected_menu == t("comparison"):
        simulations = []  # No simulations on this page
        comparison_page()
    
    # Print Report section in sidebar (before data management)
    if simulations:
        st.sidebar.markdown("---")
        st.sidebar.header(t("print_report"))
        printable_html = generate_printable_html(simulations, is_monthly=(selected_menu == t("pension_calculator") and "is_monthly" in st.session_state and st.session_state.is_monthly))
        download_link = create_download_link(printable_html)
        st.sidebar.markdown(download_link, unsafe_allow_html=True)
        st.sidebar.markdown(t("print_instructions_1"))
        st.sidebar.markdown(t("print_instructions_2"))
        st.sidebar.markdown(t("print_instructions_3"))
    
    # Data management section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.header(t("data_management"))
    
    # Add data privacy message
    st.sidebar.info(t("data_privacy_message"))

    # Export data button
    st.sidebar.markdown(f"### {t('export_data')}")
    download_link = export_data()
    st.sidebar.markdown(
        f'<a href="{download_link}" download="4sorge_data.json" class="stButton">{t("download_data")}</a>',
        unsafe_allow_html=True
    )
    
    # Import data button
    st.sidebar.markdown(f"### {t('import_data')}")
    uploaded_file = st.sidebar.file_uploader(t("upload_data"), type=['json'])

    # Use the file_processed flag to prevent infinite loops
    if uploaded_file is not None and not st.session_state.file_processed:
        # Process the file
        if import_data(uploaded_file):
            st.sidebar.success(t("data_uploaded"))
        else:
            st.sidebar.error(t("invalid_data"))
            # Reset the flag so user can try again
            st.session_state.file_processed = False

def pension_calculator_page():
    """
    Pension calculator page with standalone printable report
    """
    # Access data from session state
    data = st.session_state.pension_data
    
    st.header(t("pension_calculator"))
    
    # Configuration inputs (columns, personal info, etc.)
    col1, col2 = st.columns(2)
    
    with col1:
        # Personal information section
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
        
        # Salary information section
        st.subheader(t("salary_information"))
        current_salary = st.number_input(
            t("current_salary"),
            min_value=0,
            value=data["current_salary"],
            step=1000
        )
        data["current_salary"] = current_salary
        
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
        
        # Bonus settings section
        st.subheader(t("bonus_settings"))
        
        has_13th_salary = st.checkbox(
            t("13th_salary"),
            value=data.get("has_13th_salary", False)
        )
        data["has_13th_salary"] = has_13th_salary
        
        bonus_options = [
            ("no_bonus", t("no_bonus")),
            ("percentage_bonus", t("percentage_bonus")),
            ("fixed_amount", t("fixed_amount"))
        ]
        
        default_bonus_type = data.get("bonus_type", "percentage")
        default_idx = 0
        for i, (val, _) in enumerate(bonus_options):
            if val == "percentage" and default_bonus_type == "percentage":
                default_idx = i
                break
            elif val == "fixed_amount" and default_bonus_type == "fixed":
                default_idx = i
                break
        
        bonus_type = st.radio(
            t("bonus_settings"),
            [label for _, label in bonus_options],
            index=default_idx,
            horizontal=True
        )
        
        if bonus_type == t("percentage_bonus"):
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
        elif bonus_type == t("fixed_amount"):
            data["bonus_type"] = "fixed"
            bonus_fixed = st.number_input(
                t("bonus_amount"),
                min_value=0,
                value=data.get("bonus_fixed", 0),
                step=1000
            )
            data["bonus_fixed"] = bonus_fixed
            data["bonus_percentage"] = 0.0
        else:  # No bonus
            data["bonus_type"] = "no_bonus"
            data["bonus_percentage"] = 0.0
            data["bonus_fixed"] = 0.0
            
        # Toggle for yearly/monthly view
        st.subheader(t("toggle_view"))
        view_toggle = st.radio(
            "View Type",  # A simple label that will be hidden
            [t("yearly"), t("monthly")],
            horizontal=True,
            label_visibility="collapsed"  # Hide the label since we have the subheader
        )
        is_monthly = view_toggle == t("monthly")
        # Store is_monthly in session state for use in the sidebar
        st.session_state.is_monthly = is_monthly
    
    with col2:
        # Pension fund info section
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
        
        # Contribution options section
        st.subheader(t("contribution_options"))
        contribution_tab, employer_tab, coordination_tab, occupation_tab = st.tabs([
            t("personal_contributions"), 
            t("employer_contributions"), 
            t("coordination_fee"),
            t("occupation_level")
        ])
        
        with contribution_tab:
            st.write(t("set_contribution_options"))
            
            num_personal_ranges = st.number_input(
                t("number_of_ranges"),
                min_value=1,
                max_value=10,
                value=len(data.get("personal_contribution_ranges", DEFAULT_PENSION_DATA["personal_contribution_ranges"]))
            )
            
            personal_contribution_ranges = []
            for i in range(num_personal_ranges):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(5)
                
                if "personal_contribution_ranges" in data and i < len(data["personal_contribution_ranges"]):
                    default_range = data["personal_contribution_ranges"][i]
                else:
                    default_range = {
                        "age_from": 22 + i * 10,
                        "age_to": 34 + i * 10,
                        "options": [5.95 + i, 6.95 + i, 8.0 + i]
                    }
                
                with cols[0]:
                    age_from = st.number_input(
                        t("from_age"),
                        min_value=18,
                        max_value=70,
                        value=default_range["age_from"],
                        key=f"personal_age_from_{i}"
                    )
                
                with cols[1]:
                    age_to = st.number_input(
                        t("to_age"),
                        min_value=age_from + 1,
                        max_value=70,
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
            
            num_employer_ranges = st.number_input(
                t("number_of_ranges"),
                min_value=1,
                max_value=10,
                value=len(data.get("employer_contributions", DEFAULT_PENSION_DATA["employer_contributions"])),
                key="num_employer_ranges"
            )
            
            employer_contributions = []
            for i in range(num_employer_ranges):
                st.write(f"{t('range')} {i+1}")
                cols = st.columns(3)
                
                if "employer_contributions" in data and i < len(data["employer_contributions"]):
                    default_range = data["employer_contributions"][i]
                else:
                    default_range = {
                        "age_from": 22 + i * 10,
                        "age_to": 34 + i * 10,
                        "percentage": 6.8 + i * 2
                    }
                
                with cols[0]:
                    age_from = st.number_input(
                        t("from_age"),
                        min_value=18,
                        max_value=70,
                        value=default_range["age_from"],
                        key=f"employer_age_from_{i}"
                    )
                
                with cols[1]:
                    age_to = st.number_input(
                        t("to_age"),
                        min_value=age_from + 1,
                        max_value=70,
                        value=default_range["age_to"],
                        key=f"employer_age_to_{i}"
                    )
                
                with cols[2]:
                    percentage = st.number_input(
                        t("contribution_percentage"),
                        min_value=0.0,
                        max_value=50.0,
                        value=default_range["percentage"],
                        step=0.5,
                        key=f"employer_contribution_{i}"
                    )
                
                employer_contributions.append({
                    "age_from": age_from,
                    "age_to": age_to,
                    "percentage": percentage
                })
            
            data["employer_contributions"] = employer_contributions
            
        with coordination_tab:
            st.write(t("coordination_fee_info"))
            
            num_coordination_entries = st.number_input(
                t("number_of_entries"),
                min_value=1,
                max_value=10,
                value=len(data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"])),
                key="num_coordination_entries"
            )
            
            coordination_fees = []
            for i in range(num_coordination_entries):
                st.write(f"{t('entry')} {i+1}")
                cols = st.columns(2)
                
                if "coordination_fees" in data and i < len(data["coordination_fees"]):
                    default_entry = data["coordination_fees"][i]
                else:
                    default_entry = {
                        "from_year": 2000 + i * 5,
                        "amount": 24120 + i * 1000
                    }
                
                with cols[0]:
                    from_year = st.number_input(
                        t("from_year"),
                        min_value=1900,
                        max_value=2100,
                        value=default_entry["from_year"],
                        key=f"coordination_from_year_{i}"
                    )
                
                with cols[1]:
                    amount = st.number_input(
                        t("amount"),
                        min_value=0,
                        max_value=100000,
                        value=default_entry["amount"],
                        step=100,
                        key=f"coordination_amount_{i}"
                    )
                
                coordination_fees.append({
                    "from_year": from_year,
                    "amount": amount
                })
            
            data["coordination_fees"] = coordination_fees
            
        with occupation_tab:
            st.write(t("occupation_info"))
            
            num_occupation_entries = st.number_input(
                t("number_of_entries"),
                min_value=1,
                max_value=10,
                value=len(data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])),
                key="num_occupation_entries"
            )
            
            occupation_levels = []
            for i in range(num_occupation_entries):
                st.write(f"{t('entry')} {i+1}")
                cols = st.columns(2)
                
                if "occupation_levels" in data and i < len(data["occupation_levels"]):
                    default_entry = data["occupation_levels"][i]
                else:
                    default_entry = {
                        "from_year": 2000 + i * 5,
                        "percentage": 100.0
                    }
                
                with cols[0]:
                    from_year = st.number_input(
                        t("from_year"),
                        min_value=1900,
                        max_value=2100,
                        value=default_entry["from_year"],
                        key=f"occupation_from_year_{i}"
                    )
                
                with cols[1]:
                    percentage = st.number_input(
                        t("percentage"),
                        min_value=0.0,
                        max_value=100.0,
                        value=default_entry["percentage"],
                        step=5.0,
                        key=f"occupation_percentage_{i}"
                    )
                
                occupation_levels.append({
                    "from_year": from_year,
                    "percentage": percentage
                })
            
            data["occupation_levels"] = occupation_levels
    
    # Update session state
    st.session_state.pension_data = data
    
    # Simulate and display results
    st.header(t("simulation_results"))
    
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
            is_monthly,  # Use the existing is_monthly value
            data.get("coordination_fees", DEFAULT_PENSION_DATA["coordination_fees"]),
            data.get("occupation_levels", DEFAULT_PENSION_DATA["occupation_levels"])
        )
        if not sim.empty:
            sim["Option"] = f"{t('option')} {i+1}"
            simulations.append(sim)
    
    # Check Fund Value at Specific Date
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
                idx,
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
    
    if simulations:
        # Combined dataframe
        combined_df = pd.concat(simulations)
        
        # Final Values
        st.subheader(t("final_values"))
        final_values = []
        for sim in simulations:
            final_value = sim["Fund Value"].iloc[-1]
            option_name = sim["Option"].iloc[0]
            final_values.append({"Option": option_name, "Final Value": final_value})
        
        final_values_df = pd.DataFrame(final_values)
        st.dataframe(final_values_df.style.format({"Final Value": "CHF {:,.0f}"}))
        
        # Comparison Chart
        st.subheader(t("fund_growth_comparison"))
        
        fig = px.line(combined_df, x="Age", y="Fund Value", color="Option",
                    title=t("fund_growth_comparison"),
                    labels={"Fund Value": t("total_fund_value"), "Age": t("age")})
        
        fig.update_traces(
            hovertemplate=f'{t("age")}: %{{x}}<br>{t("year")}: %{{customdata}}<br>{t("fund_value")}: CHF %{{y:,.0f}}'
        )
        fig.update_layout(
            hovermode="x unified",
            height=500
        )
        fig.update_traces(customdata=combined_df["Year"])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display all three options
        for i, sim in enumerate(simulations):
            option_name = sim["Option"].iloc[0]
            
            st.subheader(f"{t('detailed_projection')} {option_name}")
            
            # Format the table
            if is_monthly:
                detailed_df = sim.copy()
                
                # Format month display with special handling for 13th month
                def format_month(row):
                    if row.get("Is13thMonth", False):
                        # Format based on language
                        year = row["Year"]
                        if st.session_state.language == "de":
                            return f"13er {year}"
                        elif st.session_state.language == "fr":
                            return f"13e {year}"
                        elif st.session_state.language == "it":
                            return f"13a {year}"
                        else:  # default/english
                            return f"13th {year}"
                    else:
                        return row["Date"].strftime("%b %Y")
                
                detailed_df["Month"] = detailed_df.apply(format_month, axis=1)
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
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sim["Age"],
                y=sim["Personal Contribution"],
                name=t("personal_contribution"),
                marker_color='#1f77b4',
                hovertemplate='CHF %{y:,.0f}<extra></extra>'  # Format hover text as CHF integers
            ))
            fig.add_trace(go.Bar(
                x=sim["Age"],
                y=sim["Employer Contribution"],
                name=t("employer_contribution"),
                marker_color='#72b7ec',
                hovertemplate='CHF %{y:,.0f}<extra></extra>'  # Format hover text as CHF integers
            ))
            fig.update_layout(
                barmode="stack",
                title=f"{t('annual_contributions')} - {option_name}",
                xaxis_title=t("age"),
                yaxis_title=t("total_contribution"),
                hovermode="x unified",
                height=400,
                yaxis=dict(
                    tickformat="CHF,.0f",  # Format y-axis ticks as CHF integers
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(t("no_data_available"))
    
    # Return simulations for use in the sidebar
    return simulations

def plan_management_page():
    # Access data from session state
    data = st.session_state.pension_data
    
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
                    st.success(t("plan_deleted").format(selected_plan))
                    st.rerun()
            
            with col2:
                if st.button(t("duplicate_plan")):
                    new_name = f"{selected_plan} (copy)"
                    data["pension_plans"][new_name] = plan_data.copy()
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
            st.success(t("plan_created").format(plan_name))
        elif not plan_name:
            st.error(t("enter_plan_name"))
        else:
            st.error(t("plan_exists"))


def comparison_page():
    # Access data from session state
    data = st.session_state.pension_data
    
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