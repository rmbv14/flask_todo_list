from flask import Flask, render_template, request, redirect, url_for

todo_list = Flask(__name__)

# Each task is a dict with name, status, and due_date
tasks = [
    {'name': 'Eat', 'status': 'Pending', 'due_date': None},
    {'name': 'Sleep', 'status': 'Done', 'due_date': None},
    {'name': 'Repeat', 'status': 'Pending', 'due_date': None}
]

@todo_list.route('/')
def base():
    return render_template('base.html', tasks=tasks)

@todo_list.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.form.get('newTask')
    if new_task:
        tasks.append({'name': new_task, 'status': 'Pending', 'due_date': None})
    return redirect(url_for('base'))

@todo_list.route('/task_status', methods=['POST'])
def task_status():
    task_id = int(request.form.get('task_id'))
    new_status = request.form.get('status')
    if 0 <= task_id < len(tasks) and new_status:
        tasks[task_id]['status'] = new_status
    return redirect(url_for('base'))

@todo_list.route('/update_due_date', methods=['POST'])
def update_due_date():
    task_id = int(request.form.get('task_id'))
    due_date = request.form.get('due_date')
    if 0 <= task_id < len(tasks):
        tasks[task_id]['due_date'] = due_date
    return redirect(url_for('base'))

if __name__ == '__main__':
    todo_list.run(debug=True)