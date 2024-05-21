# Programmierübung_2_K_M_M
## interaktiver Plot
### Clonen des Github-Repository auf den PC:

Öffne Git Bash, navigieren zu dem gewünschten Ordner: cd "<gewünschter Ordner>"
Repository in Ordner klonen: git clone
Öffnen Ordner in VS Code

### Virtuellen Bereich erstellen:

Öffnen eines neues Terminals --> windows Powershell
Folgender Befehl erstellt einen Virtuellen Bereich: python -m venv .venv
Folgender Befehl ein aktiviert Virtuellen Bereich: ..venv\Scripts\Activate
Falls dieser nicht funktioniert: Zugriff erlauben: Set-ExecutionPolicy RemoteSigned Scope CurrentUser
Der Virtuelle Bereich ist nun erstellt und aktiviert

### Nötigen Pakete installieren:

Nötige Pakete sind in der Text-Datei requirements.txt angeführt
alle Pakete gleichzeitig installieren: pip install -r requirements.txt (in Komandozeile von Windows Powershell)

### Verwenden des Codes

Navigieren in den richtigen Ordner cd "3_interaktiver_plot"
Befehl: streamlit run "test_e.py" startet die App
In der App links oben Eingabefenster für die maximale Herzfrequenz und der Button "Analyse starten" zum Starten 
Die App zeigt dann: 
* Tabellen Zeit in HF-Zonen, durchscnittliche Leistung in den HF-Zonen                     
* durchschnittliche Leistung gesamt und die maximale Leistung
* Diagram Leistung über die Zeit
