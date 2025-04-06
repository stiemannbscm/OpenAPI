from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

todo_lists = {}
todo_entries = {}

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(list(todo_lists.values())), 200

@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    list_id = str(uuid4())
    new_list = {'id': list_id, 'name': data['name']}
    todo_lists[list_id] = new_list
    todo_entries[list_id] = []
    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>', methods=['GET'])
def get_list(list_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    return jsonify(todo_lists[list_id]), 200

@app.route('/todo-list/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    del todo_lists[list_id]
    todo_entries.pop(list_id, None)
    return jsonify({'msg': 'success'}), 200

@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_entries(list_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    return jsonify(todo_entries.get(list_id, [])), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    entry_id = str(uuid4())
    entry = {
        'id': entry_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'list_id': list_id
    }
    todo_entries[list_id].append(entry)
    return jsonify(entry), 200

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    for i, entry in enumerate(todo_entries[list_id]):
        if entry['id'] == entry_id:
            updated = {
                'id': entry_id,
                'name': data['name'],
                'description': data.get('description', ''),
                'list_id': list_id
            }
            todo_entries[list_id][i] = updated
            return jsonify(updated), 200
    return jsonify({'error': 'Entry not found'}), 404

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    entries = todo_entries[list_id]
    for i, entry in enumerate(entries):
        if entry['id'] == entry_id:
            del entries[i]
            return jsonify({'msg': 'success'}), 200
    return jsonify({'error': 'Entry not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
