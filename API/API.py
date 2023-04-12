import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = []

FILENAME = "todos.json"

def load_todos():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_todos():
    with open(FILENAME, "w") as f:
        json.dump(todos, f)

todos = load_todos()

class TodoResource(Resource):
    def get(self, todo_id):
        if 0 <= todo_id < len(todos):
            return {todo_id: todos[todo_id]}
        return {"error": "Todo not found"}, 404

    def put(self, todo_id):
        data = request.get_json()
        todo_item = {"task": data["task"], "event": data["event"]}
        if 0 <= todo_id < len(todos):
            todos[todo_id] = todo_item
            save_todos()
            return {todo_id: todos[todo_id]}
        return {"error": "Todo not found"}, 404

    def delete(self, todo_id):
        if 0 <= todo_id < len(todos):
            del todos[todo_id]
            save_todos()
            return {"result": "Todo deleted"}
        return {"error": "Todo not found"}, 404

class TodoListResource(Resource):
    def get(self):
        return todos

    def post(self):
        data = request.get_json()
        todo_item = {"task": data["task"], "event": data["event"]}
        todos.append(todo_item)
        save_todos()
        return {len(todos) - 1: todo_item}, 201

api.add_resource(TodoResource, '/todos/<int:todo_id>')
api.add_resource(TodoListResource, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
