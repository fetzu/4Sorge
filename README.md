# 4Sorge - Pension Fund Simulator

🇬🇧 TL;DR: play with your pension fund's outcome without any risk!  
🇨🇭🇩🇪 TL;DR: Spiel mit dem Ergebnis deines Pensionsfonds ohne Risiko!  
🇨🇭🇫🇷 TL;DR : jouez avec les résultats de votre fonds de pension sans aucun risque!  
🇨🇭🇮🇹 TL;DR: gioca con il risultato del tuo fondo pensione senza alcun rischio!  

[Online version on Streamlit](https://4sorge.streamlit.app).

4Sorge is a comprehensive pension fund calculator that helps users simulate and compare different pension scenarios. The app provides a user-friendly web interface to visualize pension growth over time and compare different contribution strategies with Swiss market features.

## Features

- **Pension Simulation**: Calculate expected pension fund growth based on personal and employer contributions
- **Multiple Contribution Options**: Compare up to 3 different personal contribution scenarios
- **Customizable Parameters**:
  - Personal information (birth date, retirement age)
  - Salary progression (current salary, maximum salary, years to reach maximum)
  - Expected investment yield
  - Configurable employer contribution rates by age range
  - 13th salary option
  - Annual bonus (percentage or fixed amount)
  - Coordination fee deduction with time-based changes (Koordinationsbetrag/montant de coordination/trattenuta di coordinamento)
  - Degree of occupation with time-based changes
- **Plan Management**:
  - Save multiple pension plan scenarios
  - Duplicate existing plans
  - Delete plans
- **Plan Comparison**: Compare multiple pension plans side-by-side with interactive visualizations
- **Detailed Projections**: Toggle between yearly and monthly views for detailed contribution breakdowns
- **Fund Value Checker**: Check pension fund value at any specific date
- **Multi-language Support**: Available in English, German (Schweiz), French (Suisse), and Italian (Svizzera)
- **Print/Export**: Export results for offline use

## Advanced Features

### Coordination Fee
The coordination fee is deducted from your yearly salary before calculating contributions. This is a standard practice in Swiss pension systems to account for the portion of salary already covered by the first pillar (AHV/AVS). You can:
- Set multiple coordination fee values for different years
- The app will automatically apply the correct fee based on the simulation year

### Degree of Occupation
Your degree of occupation (part-time percentage) affects your insurable salary. You can:
- Set different occupation levels for different years
- Model career changes from part-time to full-time (or vice versa)
- Contributions are calculated based on your actual working percentage

### Insurable Salary
The insurable salary is calculated as: `Yearly Salary + Bonus - Coordination Fee`, adjusted by your degree of occupation. This is the amount on which your pension contributions are calculated.

## Installation

1. Make sure you have Python 3.7+ installed on your system.

2. Install the required dependencies:
```bash
pip install streamlit pandas plotly python-dateutil numpy
```

3. Download the `4Sorge.py` file to your desired directory.

## Usage

1. Navigate to the directory containing the script:
```bash
cd /path/to/directory
```

2. Run the Streamlit app:
```bash
streamlit run 4Sorge.py
```

3. The app will open in your default web browser.

4. Use the navigation menu in the sidebar to access different sections:
   - **Pension Calculator**: Enter your personal information and simulate pension growth
   - **Plan Management**: Create, duplicate, or delete pension plans
   - **Comparison**: Compare multiple pension plans side-by-side

## Data Storage

The app stores all data in a JSON file called `pension_data.json` in the same directory as the script. This file is human-readable and can be edited manually if needed.

## Features Breakdown

### Pension Calculator
- Enter personal information (birth date, retirement age)
- Set current and expected maximum salary
- Specify current pension fund value and date
- Configure personal contribution options (3 scenarios)
- Set employer contribution rates by age range
- Configure coordination fees that change over time
- Set degree of occupation levels for different years
- View projected pension growth with interactive charts
- Check fund value at any specific date
- Detailed yearly/monthly breakdown of contributions and fund value

### Plan Management
- Create new pension plans based on current settings
- View existing plans in JSON format
- Duplicate plans to create variations
- Delete plans you no longer need

### Comparison
- Select multiple plans to compare
- Include current settings in comparison
- Visual comparison with bar and line charts
- Key metrics comparison table showing:
  - Starting and final values
  - Total growth
  - Average annual contribution
  - Years to retirement
