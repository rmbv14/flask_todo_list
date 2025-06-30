from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

todo_list = Flask(__name__)

DATA_FILE = 'data.json'

# Load and save functions
def load_pages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "Academics": [{'name': 'Study for exam', 'status': 'Pending', 'due_date': None, 'note': ''}],
        "Work": [{'name': 'Finish report', 'status': 'Done', 'due_date': None, 'note': ''}],
        "Extracurriculars": [{'name': 'Basketball practice', 'status': 'Pending', 'due_date': None, 'note': ''}]
    }

def save_pages():
    with open(DATA_FILE, 'w') as f:
        json.dump(pages, f)

# Load pages from file
pages = load_pages()

@todo_list.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y'):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except Exception:
        return value

@todo_list.route('/')
def home():
    first_page = next(iter(pages))
    return redirect(url_for('show_page', page_name=first_page))

@todo_list.route('/page/<page_name>')
def show_page(page_name):
    status_filter = request.args.get('status_filter')
    today = datetime.today().date()
    tasks = pages.get(page_name, [])
    filtered_tasks = tasks
    if status_filter:
        filtered_tasks = [task for task in tasks if task['status'] == status_filter]
    for task in filtered_tasks:
        due_str = task.get('due_date')
        if due_str:
            try:
                due_date = datetime.strptime(due_str, '%Y-%m-%d').date()
                task['days_left'] = (due_date - today).days
            except Exception:
                task['days_left'] = None
        else:
            task['days_left'] = None
    return render_template('base.html', tasks=filtered_tasks, page_name=page_name, pages=pages.keys())

@todo_list.route('/add_page', methods=['POST'])
def add_page():
    new_page = request.form.get('new_page')
    if new_page and new_page not in pages:
        pages[new_page] = []
        save_pages()
    return redirect(url_for('show_page', page_name=new_page))

@todo_list.route('/page/<page_name>/add_task', methods=['POST'])
def add_task(page_name):
    new_task = request.form.get('newTask')
    if new_task:
        pages[page_name].append({'name': new_task, 'status': 'Pending', 'due_date': None, 'note': ''})
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/page/<page_name>/task_status', methods=['POST'])
def task_status(page_name):
    task_id = int(request.form.get('task_id'))
    new_status = request.form.get('status')
    if 0 <= task_id < len(pages[page_name]) and new_status:
        pages[page_name][task_id]['status'] = new_status
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/page/<page_name>/update_due_date', methods=['POST'])
def update_due_date(page_name):
    task_id = int(request.form.get('task_id'))
    due_date = request.form.get('due_date')
    if 0 <= task_id < len(pages[page_name]):
        pages[page_name][task_id]['due_date'] = due_date
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/page/<page_name>/update_task_name', methods=['POST'])
def update_task_name(page_name):
    task_id = int(request.form.get('task_id'))
    new_name = request.form.get('task_name')
    if 0 <= task_id < len(pages[page_name]) and new_name:
        pages[page_name][task_id]['name'] = new_name
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/page/<page_name>/update_note', methods=['POST'])
def update_note(page_name):
    task_id = int(request.form.get('task_id'))
    note = request.form.get('note')
    if 0 <= task_id < len(pages[page_name]):
        pages[page_name][task_id]['note'] = note
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/page/<page_name>/delete_task', methods=['POST'])
def delete_task(page_name):
    task_id = int(request.form.get('task_id'))
    if 0 <= task_id < len(pages[page_name]):
        pages[page_name].pop(task_id)
        save_pages()
    return redirect(url_for('show_page', page_name=page_name))

@todo_list.route('/rename_page', methods=['POST'])
def rename_page():
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    if old_name and new_name and old_name in pages and new_name not in pages:
        pages[new_name] = pages.pop(old_name)
        save_pages()
    return redirect(url_for('show_page', page_name=new_name if new_name else old_name))

@todo_list.route('/delete_page', methods=['POST'])
def delete_page():
    page_name = request.form.get('page_name')
    if page_name in pages and len(pages) > 1:
        pages.pop(page_name)
        save_pages()
        first_page = next(iter(pages))
        return redirect(url_for('show_page', page_name=first_page))
    return redirect(url_for('show_page', page_name=page_name))

if __name__ == '__main__':
    todo_list.run(debug=True)
