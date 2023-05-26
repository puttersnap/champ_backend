from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    due_date = db.Column(db.Date)
    order = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer)


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json.get('title')
    description = request.json.get('description')
    due_date = request.json.get('due_date')
    order = request.json.get('order')
    list_id = request.json.get('list_id')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description,
                due_date=due_date, order=order, list_id=list_id)
    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    title = request.json.get('title')
    description = request.json.get('description')
    due_date = request.json.get('due_date')
    order = request.json.get('order')

    if title:
        task.title = title
    if description:
        task.description = description
    if due_date:
        task.due_date = due_date
    if order:
        task.order = order

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


@app.route('/lists', methods=['POST'])
def create_list():
    title = request.json.get('title')
    order = request.json.get('order')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    new_list = List(title=title, order=order)
    db.session.add(new_list)
    db.session.commit()

    return jsonify({'message': 'List created successfully'}), 201


@app.route('/lists/<list_id>', methods=['PUT'])
def update_list(list_id):
    list_obj = List.query.get(list_id)

    if not list_obj:
        return jsonify({'error': 'List not found'}), 404

    title = request.json.get('title')
    order = request.json.get('order')

    if title:
        list_obj.title = title
    if order:
        list_obj.order = order

    db.session.commit()

    return jsonify({'message': 'List updated successfully'}), 200


@app.route('/tasks/<task_id>/move', methods=['PUT'])
def move_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    list_id = request.json.get('list_id')

    if not list_id:
        return jsonify({'error': 'List ID is required'}), 400

    task.list_id = list_id
    db.session.commit()

    return jsonify({'message': 'Task moved to another list successfully'}), 200


@app.route('/tasks/<task_id>/reorder', methods=['PUT'])
def reorder_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    new_order = request.json.get('order')

    if not new_order:
        return jsonify({'error': 'New order is required'}), 400

    task.order = new_order
    db.session.commit()

    return jsonify({'message': 'Task reordered successfully'}), 200


@app.route('/lists/<list_id>/reorder', methods=['PUT'])
def reorder_list(list_id):
    list_obj = List.query.get(list_id)

    if not list_obj:
        return jsonify({'error': 'List not found'}), 404

    new_order = request.json.get('order')

    if not new_order:
        return jsonify({'error': 'New order is required'}), 400

    list_obj.order = new_order
    db.session.commit()

    return jsonify({'message': 'List reordered successfully'}), 200


@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    list_obj = List.query.get(list_id)

    if not list_obj:
        return jsonify({'error': 'List not found'}), 404

    # Delete all tasks associated with the list
    Task.query.filter_by(list_id=list_id).delete()

    db.session.delete(list_obj)
    db.session.commit()

    return jsonify({'message': 'List deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
