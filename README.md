# 4Sorge - Pension Fund Simulator

[English](#english) | [Deutsch](#deutsch) | [Français](#français) | [Italiano](#italiano)

[Online version on Streamlit](https://4sorge.streamlit.app)

🇬🇧 TL;DR: play with your pension fund's outcome without any risk!  
🇨🇭🇩🇪 TL;DR: Spiel mit dem Ergebnis deines Pensionsfonds ohne Risiko!  
🇨🇭🇫🇷 TL;DR : joue avec les résultats de ton fonds de pension sans aucun risque!  
🇨🇭🇮🇹 TL;DR: gioca con il risultato del tuo fondo pensione senza alcun rischio!  

## <a name="english"></a>English

4Sorge is a comprehensive pension fund calculator that helps users simulate and compare different pension scenarios. The app provides a user-friendly web interface to visualize pension growth over time and compare different contribution strategies with Swiss market features.

[Try it online on Streamlit](https://4sorge.streamlit.app)

### Features

- **1st Pillar (AHV/AVS) & 2nd Pillar (Pension Fund)**: Calculate projections for both pillars of the Swiss pension system
- **Multiple Contribution Options**: Compare up to 3 different personal contribution scenarios
- **Customizable Parameters**:
  - Personal information (birth date, retirement age)
  - Salary progression (current salary, maximum salary, years to reach maximum)
  - Expected investment yield
  - Configurable employer contribution rates by age range
  - 13th salary option
  - Annual bonus (percentage or fixed amount)
  - Coordination fee deduction with time-based changes
  - Degree of occupation with time-based changes
- **Plan Management**: Save, duplicate, and compare multiple pension plan scenarios
- **Detailed Projections**: Toggle between yearly and monthly views
- **Fund Value Checker**: Check pension fund value at any specific date
- **Multi-language Support**: Available in English, German, French, and Italian
- **Print/Export**: Export results for offline use

### Offline / Local use

#### Installation

1. Make sure you have Python 3.7+ installed on your system.

2. Install the required dependencies:
```bash
pip install streamlit pandas plotly python-dateutil numpy
```

3. Download the `4Sorge.py` file to your desired directory.

#### Usage

1. Navigate to the directory containing the script:
```bash
cd /path/to/directory
```

2. Run the Streamlit app:
```bash
streamlit run 4Sorge.py
```

3. The app will open in your default web browser.

### Data Privacy

4Sorge is designed to respect your privacy. All data is processed locally in your browser when using the app, and nothing is permanently stored on servers. The app includes an export/import feature that allows you to save your data as a JSON file locally.

When using the hosted version on Streamlit, your data is processed on Streamlit's servers only while you are actively using the app. However, for complete privacy assurance, you may prefer to run the app locally as described in the "Offline / Local use" section.

---

## <a name="deutsch"></a>Deutsch (Schweiz)

4Sorge ist ein umfassender Pensionskassenrechner, der dir hilft, verschiedene Pensionsszenarien zu simulieren und zu vergleichen. Die App bietet eine benutzerfreundliche Weboberfläche, um das Pensionswachstum im Laufe der Zeit zu visualisieren und verschiedene Beitragsstrategien mit Schweizer Marktmerkmalen zu vergleichen.

[Online-Version auf Streamlit ausprobieren](https://4sorge.streamlit.app)

### Funktionen

- **1. Säule (AHV) & 2. Säule (Pensionskasse)**: Berechnung von Projektionen für beide Säulen des Schweizer Pensionssystems
- **Mehrere Beitragsoptionen**: Vergleiche bis zu 3 verschiedene persönliche Beitragsszenarien
- **Anpassbare Parameter**:
  - Persönliche Informationen (Geburtsdatum, Pensionsalter)
  - Gehaltsentwicklung (aktuelles Gehalt, maximales Gehalt, Jahre bis zum Erreichen des Maximums)
  - Erwartete Anlagerendite
  - Konfigurierbare Arbeitgeberbeitragssätze nach Altersgruppe
  - 13. Monatsgehalt Option
  - Jährlicher Bonus (Prozentsatz oder fester Betrag)
  - Koordinationsabzug mit zeitbasierten Änderungen
  - Beschäftigungsgrad mit zeitbasierten Änderungen
- **Planverwaltung**: Speichere, dupliziere und vergleiche mehrere Pensionspläne
- **Detaillierte Projektionen**: Wechsle zwischen Jahres- und Monatsansichten
- **Fondswertprüfung**: Prüfe den Pensionskassenwert zu einem bestimmten Datum
- **Mehrsprachige Unterstützung**: Verfügbar in Englisch, Deutsch, Französisch und Italienisch
- **Druck/Export**: Exportiere Ergebnisse zur Offline-Nutzung

### Offline / Lokale Nutzung

#### Installation

1. Stelle sicher, dass Python 3.7+ auf deinem System installiert ist.

2. Installiere die erforderlichen Abhängigkeiten:
```bash
pip install streamlit pandas plotly python-dateutil numpy
```

3. Lade die Datei `4Sorge.py` in dein gewünschtes Verzeichnis herunter.

#### Verwendung

1. Navigiere zum Verzeichnis, das das Skript enthält:
```bash
cd /pfad/zum/verzeichnis
```

2. Führe die Streamlit-App aus:
```bash
streamlit run 4Sorge.py
```

3. Die App wird in deinem Standardbrowser geöffnet.

### Datenschutz

4Sorge ist darauf ausgelegt, deine Privatsphäre zu respektieren. Alle Daten werden bei der Nutzung der App lokal in deinem Browser verarbeitet, und nichts wird dauerhaft auf Servern gespeichert. Die App enthält eine Export/Import-Funktion, mit der du deine Daten als JSON-Datei lokal speichern kannst.

Bei Verwendung der gehosteten Version auf Streamlit werden deine Daten nur während der aktiven Nutzung der App auf Streamlit-Servern verarbeitet. Für eine vollständige Gewährleistung der Privatsphäre kannst du die App jedoch lokal ausführen, wie im Abschnitt "Offline / Lokale Nutzung" beschrieben.

---

## <a name="français"></a>Français (Suisse)

4Sorge est un calculateur complet de caisse de pension qui t'aide à simuler et à comparer différents scénarios de retraite. L'application offre une interface web conviviale pour visualiser la croissance de ta pension au fil du temps et comparer différentes stratégies de cotisation avec les caractéristiques du marché suisse.

[Essaie la version en ligne sur Streamlit](https://4sorge.streamlit.app)

### Fonctionnalités

- **1er Pilier (AVS) & 2ème Pilier (Caisse de Pension)**: Calcule des projections pour les deux piliers du système de pension suisse
- **Options de cotisation multiples**: Compare jusqu'à 3 scénarios de cotisation personnelle différents
- **Paramètres personnalisables**:
  - Informations personnelles (date de naissance, âge de la retraite)
  - Progression salariale (salaire actuel, salaire maximum, années pour atteindre le maximum)
  - Rendement d'investissement attendu
  - Taux de cotisation de l'employeur configurables par tranche d'âge
  - Option 13ème salaire
  - Bonus annuel (pourcentage ou montant fixe)
  - Déduction de coordination avec changements basés sur le temps
  - Degré d'occupation avec changements basés sur le temps
- **Gestion des plans**: Sauvegarde, duplique et compare plusieurs scénarios de plan de pension
- **Projections détaillées**: Bascule entre les vues annuelles et mensuelles
- **Vérificateur de valeur du fonds**: Vérifie la valeur de ta caisse de pension à une date spécifique
- **Support multilingue**: Disponible en anglais, allemand, français et italien
- **Impression/Exportation**: Exporte les résultats pour une utilisation hors ligne

### Utilisation hors ligne / locale

#### Installation

1. Assure-toi d'avoir Python 3.7+ installé sur ton système.

2. Installe les dépendances requises:
```bash
pip install streamlit pandas plotly python-dateutil numpy
```

3. Télécharge le fichier `4Sorge.py` dans le répertoire de ton choix.

#### Utilisation

1. Navigue vers le répertoire contenant le script:
```bash
cd /chemin/vers/repertoire
```

2. Exécute l'application Streamlit:
```bash
streamlit run 4Sorge.py
```

3. L'application s'ouvrira dans ton navigateur par défaut.

### Confidentialité des données

4Sorge est conçu pour respecter ta vie privée. Toutes les données sont traitées localement dans ton navigateur lors de l'utilisation de l'application, et rien n'est stocké de façon permanente sur les serveurs. L'application comprend une fonctionnalité d'exportation/importation qui te permet de sauvegarder tes données sous forme de fichier JSON localement.

Lorsque tu utilises la version hébergée sur Streamlit, tes données sont traitées sur les serveurs de Streamlit uniquement pendant que tu utilises activement l'application. Cependant, pour une garantie complète de confidentialité, tu pourrais préférer exécuter l'application localement comme décrit dans la section "Utilisation hors ligne / locale".

---

## <a name="italiano"></a>Italiano (Svizzera)

4Sorge è un calcolatore completo di fondi pensione che ti aiuta a simulare e confrontare diversi scenari pensionistici. L'app offre un'interfaccia web facile da usare per visualizzare la crescita della pensione nel tempo e confrontare diverse strategie di contribuzione con le caratteristiche del mercato svizzero.

[Prova la versione online su Streamlit](https://4sorge.streamlit.app)

### Funzionalità

- **1° Pilastro (AVS) e 2° Pilastro (Cassa Pensioni)**: Calcola proiezioni per entrambi i pilastri del sistema pensionistico svizzero
- **Opzioni di contribuzione multiple**: Confronta fino a 3 diversi scenari di contribuzione personale
- **Parametri personalizzabili**:
  - Informazioni personali (data di nascita, età pensionabile)
  - Progressione salariale (stipendio attuale, stipendio massimo, anni per raggiungere il massimo)
  - Rendimento d'investimento previsto
  - Tassi di contribuzione del datore di lavoro configurabili per fascia d'età
  - Opzione 13a mensilità
  - Bonus annuale (percentuale o importo fisso)
  - Deduzione di coordinamento con modifiche basate sul tempo
  - Grado di occupazione con modifiche basate sul tempo
- **Gestione dei piani**: Salva, duplica e confronta più scenari di piani pensionistici
- **Proiezioni dettagliate**: Alterna tra visualizzazioni annuali e mensili
- **Verifica del valore del fondo**: Controlla il valore del tuo fondo pensione in una data specifica
- **Supporto multilingue**: Disponibile in inglese, tedesco, francese e italiano
- **Stampa/Esportazione**: Esporta i risultati per uso offline

### Uso offline / locale

#### Installazione

1. Assicurati di avere Python 3.7+ installato sul tuo sistema.

2. Installa le dipendenze richieste:
```bash
pip install streamlit pandas plotly python-dateutil numpy
```

3. Scarica il file `4Sorge.py` nella directory desiderata.

#### Utilizzo

1. Naviga alla directory contenente lo script:
```bash
cd /percorso/alla/directory
```

2. Esegui l'app Streamlit:
```bash
streamlit run 4Sorge.py
```

3. L'app si aprirà nel tuo browser predefinito.

### Privacy dei dati

4Sorge è progettato per rispettare la tua privacy. Tutti i dati vengono elaborati localmente nel tuo browser quando usi l'app, e nulla viene memorizzato permanentemente sui server. L'app include una funzionalità di esportazione/importazione che ti permette di salvare i tuoi dati come file JSON localmente.

Quando utilizzi la versione ospitata su Streamlit, i tuoi dati vengono elaborati sui server di Streamlit solo mentre stai utilizzando attivamente l'app. Tuttavia, per una completa garanzia di privacy, potresti preferire eseguire l'app localmente come descritto nella sezione "Uso offline / locale".
