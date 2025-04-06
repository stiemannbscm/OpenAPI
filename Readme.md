# Todo-Listen-API (Flask + OpenAPI)

Dies ist eine einfache REST-API zur Verwaltung von Todo-Listen und deren Einträgen. Die API ist mit Python und Flask implementiert und folgt dem OpenAPI 3.0 Standard. Alle Daten werden zur Laufzeit im Arbeitsspeicher gehalten (keine persistente Speicherung).

## Funktionen

- Erstellen und Löschen von Todo-Listen
- Abrufen aller Listen oder einer einzelnen Liste
- Hinzufügen, Bearbeiten und Löschen von Einträgen in einer Liste
- Automatisierte Tests mit pytest
- Optionaler HTML/JS-Client

## Voraussetzungen

- Python 3.x
- Abhängigkeiten: `flask`, `flask-cors`, `pytest`

Installation der Pakete:
```bash
pip install flask flask-cors pytest
