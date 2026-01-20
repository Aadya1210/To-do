from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
FILE_NAME = "data.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    tasks = load_tasks()
    tasks.append({
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "done": False
    })

    save_tasks(tasks)
    return redirect("/")


@app.route("/done/<int:index>")
def mark_done(index):
    tasks = load_tasks()
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks(tasks)
    return redirect("/")


@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
