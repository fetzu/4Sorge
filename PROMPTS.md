# Prompts to Claude 3.7 Sonnet used to make this app

## Prompt 1
I need you to write a Python app following the following requirements:
* The app should be a single python file, additional files (for example an HTML template) are OK.
* The app should have a GUI (either a web interface or a TUI).
* The app should use a simple human readable (for example TOML or JSON) to store its data, the file should be located in the same folder as where the script is ran.
* The app should not create files elsewhere on the system.
* The app is a pension fund simulator/calculator called "4Sorge". It should do the following:
   * With data provided by the user (date of birth, age of retirement, current salary, maximum salary, estimated time to maximum salary, expected pension annual yield, and monthly pension information) it should allow to generate both a tabular and graphic projection of the total sum for pension).
   * The pension information should be configurable with the following:
      * The user should be able to set their "own" contributions (in percentage of salary) and their employers contribution.
      * The contributions should be configurable over time through ranges with changing contributions (for example, the employer contribution could be 6% between the ages of 18 to 25, 9% between 25 and 35, 14% between 35 and 45, and so on...).
      * There should be an option to set 3 different "own" contribution values in order to compare the impact on the total sum (the user could for example have their own contribution be either 6%, 7% or 9%).
      * There should be a way to setup multiple pension plans (duplicating an existing one or creating it from scratch) and compare them.
      * There should be a way for the user to enter the current total value of their pension fund (at a certain date) and simulate the data from there on.
   * The goal of the app is to provide the user with a way to
      1. Simulate their current pension fund value until their retirement. That means give the total expected value of the fund at the age or retirement and a graphical representation of its total value over time.
      2. Simulate the impact of choosing one of the 3 "own contribution" alternatives over total value and time.
      3. Compare multiple pension plans.

Give me the code using best state-of-the-art programming practices and commenting where necessary. Also provide a README.md file with features, and installation and usage instructions.

## Prompt 2
This is great.

Now I want you to add the following features to the app:
* The tabular "Detailed Projection" should be toggleable between yearly (as now) and monthly.
* There should be a flag for a 13th salary (in which case the yearly salary is divided into equal 13 months instead of 12) and a yearly bonus (settable as either a percentage of the yearly salary or just a user provided value).
* In addition to english, the app should also be available in German (Switzerland), French (Switzerland) and Italian (Switzerland). The language should be changeable through the web interface and saved in the config file.
* There should be a way to "export" the results as a PDF. Using the web browser's print option is acceptable, but the output should have a nice(r) format.

Implement those changes and return the code.

## Prompt 3
I am getting the following error when using the app (appears both in the console and the app's main web page): (paste of error message)

## Prompt 4
It is now working properly, thank you.

I need you to add the following features:
* The "own contributions" should also be configurable over time through ranges with changing contributions (for example, the employer contribution could be 6% between the ages of 18 to 25, 9% between 25 and 35, 14% between 35 and 45, and so on...). The difference with the employer contribution is that each range should have 3 different user settable percentages.
* In addition to the age, the graphics should also show the year when hovering.

## Prompt 5 (New chat, py and README provided)
I need you to introduce the following feature to this app:
* The app should take into acount a yearly "coordination fee" which is deducted from the yearly salary. It means that the amount for the own and employer contributions correspond to: "yearly salary + bonus - coordination fee".
   * This coordination fee should be user configurable, and can change over time. Introduce another setting in which the user can set the coordination fee "from" year. The user should be able to set multiple "from year coordination fee values" (for example, the coordination fee could be 20000 from 2000, and change to 22000 starting in 2010) and the simulation should take them into account properly. The coordination value is called "Koordinationsbetrag" in German, "montant de coordination" in French and "trattenuta di coordinamento" in Italian.
* The user should be able to set their degree of occupation. This is in percent, the salary always being equal to that of 100% occupation. It should be possible to have the degree of occupation change overtime (with a yearly granularity). Implement those changes and return the code for the app as well as an updated README. The README should not speak of these changes as changes but rather describe the app in its current state.
* The user should be able to input a precise date (month and year) and get the total value of their pension at that point in time according to the simulation.
* The print/export to PDF option is not currently working. Nothing happens when the user presses the button. Fix this.

Return the whole modified code as well as the README.md.I need you to introduce the following feature to this app:
* The app should take into acount a yearly "coordination fee" which is deducted from the yearly salary. It means that the amount for the own and employer contributions correspond to: "yearly salary + bonus - coordination fee".
   * This coordination fee should be user configurable, and can change over time. Introduce another setting in which the user can set the coordination fee "from" year. The user should be able to set multiple "from year coordination fee values" (for example, the coordination fee could be 20000 from 2000, and change to 22000 starting in 2010) and the simulation should take them into account properly. The coordination value is called "Koordinationsbetrag" in German, "montant de coordination" in French and "trattenuta di coordinamento" in Italian.
* The user should be able to set their degree of occupation. This is in percent, the salary always being equal to that of 100% occupation. It should be possible to have the degree of occupation change overtime (with a yearly granularity). Implement those changes and return the code for the app as well as an updated README. The README should not speak of these changes as changes but rather describe the app in its current state.
* The user should be able to input a precise date (month and year) and get the total value of their pension at that point in time according to the simulation.
* The print/export to PDF option is not currently working. Nothing happens when the user presses the button. Fix this.

Return the whole modified code as well as the README.md.

## Prompt 6
Thank you, it is working now.

The "Print/Export to PDF" does not seem to be working. Pressing it created another button beneath it, but it does not do anything. Could you make it so that using the browser's print function OR the streamlit print function returns a nicely formatted printout? Currently the printout has huge empty headers.

## Prompt 7
It looks better.
* But the button "Print/Export to PDF" is still shown on the web interface and returns an error, what do I have to remove to make it disappear? Are there any other changes I should make?
* Is there a way to make the tables look better on the printout? Currently the tables are randomly split across pages. Is there a way to make sure they fit on a single page, or to repeat the headers if they are to span across multiple pages?

## Prompt 8
The app is still showing titles for things which are not "usable" and should not be part of the PDF such as:
"Pension Calculator
Personal Information
Salary Information
Bonus Settings
Simulation Results
Check Fund Value at Specific Date"

Can you make sure the print only starts at the Final Pension Values at Retirement section? Can you also make it so that the print returns the three options (instead of just the currently selected one) on the output?

## Prompt 9 (New chat)
Here is a Python app. It has the following issues:
1. When viewing on the web, all "options" are displayed consecutively at the end of the page. This should not happen, only the currently selected option should be shown. When printing, all options should be printed.
2. The print has unnecessary elements such as "Pension Calculator
Personal Information
Salary Information
Bonus Settings
Simulation Results"
Make sure that only Final Pension Values at Retirement, Pension Fund Growth Comparison, and Detailed Projection for all options are printed.

## Prompt 10
If I deploy the app to streamlit (online), where would the data be stored?

## Prompt 11
Yes, modify the app with the option you suggested. Make sure no data is ever stored outside of the user's machine.

## Prompt 12
I have the following python app.

The "import" of data does not seem to work properly: the app goes into an infinite refresh loop.

I need you to help me troubleshoot the issue. Before making any code changes, what can I do to provide you with better logs/information?

## Prompt 13 (new chat; also ran through Gemini 2.5 Pro)
Can you analyse the following python app and make sure that indeed no data will leave the user's device EVEN IF it was deployed through the Streamlit Community Cloud?
