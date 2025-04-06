import pytest
from server import app
import uuid

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def validate_uuid(val):
    try:
        uuid.UUID(val)
        return True
    except:
        return False

def test_full_todo_flow(client):
    print("\nTest startet")

    # Neue Liste erstellen
    list_data = {'name': 'Testliste'}
    response = client.post('/todo-list', json=list_data)
    assert response.status_code == 200, f"Fehler beim Erstellen: {response.data}"
    list_result = response.get_json()
    print(f"Liste erstellt: {list_result}")
    assert 'id' in list_result and validate_uuid(list_result['id']), "Ungültige Listen-ID"
    assert list_result['name'] == list_data['name']
    list_id = list_result['id']

    # Liste abrufen
    response = client.get(f'/todo-list/{list_id}')
    assert response.status_code == 200, f"Fehler beim Abrufen: {response.data}"
    print(f"Liste abgerufen: {response.get_json()}")

    # Eintrag hinzufügen
    entry_data = {'name': 'Testeintrag', 'description': 'Beschreibung'}
    response = client.post(f'/todo-list/{list_id}/entry', json=entry_data)
    assert response.status_code == 200, f"Fehler beim Hinzufügen des Eintrags: {response.data}"
    entry_result = response.get_json()
    print(f"Eintrag erstellt: {entry_result}")
    assert 'id' in entry_result and validate_uuid(entry_result['id']), "Ungültige Eintrags-ID"
    entry_id = entry_result['id']

    # Einträge der Liste abrufen
    response = client.get(f'/todo-list/{list_id}/entries')
    assert response.status_code == 200, f"Fehler beim Abrufen der Einträge: {response.data}"
    entries = response.get_json()
    print(f"Liste: {entries}")
    assert any(e['id'] == entry_id for e in entries), "Erstellter Eintrag nicht gefunden"

    # Eintrag bearbeiten
    update_data = {'name': 'Bearbeitet', 'description': 'Neu'}
    response = client.put(f'/todo-list/{list_id}/entry/{entry_id}', json=update_data)
    assert response.status_code == 200, f"Fehler beim Bearbeiten des Eintrags: {response.data}"
    updated = response.get_json()
    print(f"Bearbeitet: {updated}")
    assert updated['name'] == update_data['name']

    # Eintrag löschen
    response = client.delete(f'/todo-list/{list_id}/entry/{entry_id}')
    assert response.status_code == 200, f"Fehler beim Löschen des Eintrags: {response.data}"
    print(f"Eintrag Gelöscht: {response.get_json()}")

    # Liste löschen
    response = client.delete(f'/todo-list/{list_id}')
    assert response.status_code == 200, f"Fehler beim Löschen der Liste: {response.data}"
    print(f"Liste Gelöscht: {response.get_json()}")

    print("erfolgreich abgeschlossen.")
