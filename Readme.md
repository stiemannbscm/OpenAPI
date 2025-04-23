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
```

Testen der API:
```bash
pytest -s test_server.py
```

Edit:
[simple Frontend](https://stiemannbscm.github.io/OpenAPI/client.html)
Nach Hinzufügen einer Liste dauert es ein wenig bis die Liste erstellt wird, da Render das Projekt pausiert wenn es zu lange inaktiv ist. Es gibt keine User, deswegen werden alle die den Link haben alle listen sehen können.
