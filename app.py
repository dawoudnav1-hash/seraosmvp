from flask import Flask, render_template, jsonify, request
from canvas_integration import CanvasService
from octavia import OctaviaAgent

app = Flask(__name__)
canvas = CanvasService()
octavia = OctaviaAgent(canvas)

@app.route('/')
def dashboard():
    stats = canvas.get_dashboard_stats()
    courses = canvas.get_courses()
    assignments = canvas.get_assignments()
    return render_template('dashboard.html', stats=stats, courses=courses, assignments=assignments)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    assignment = canvas.get_assignment_by_id(task_id)
    if not assignment:
        return "Task not found", 404
    return render_template('task_detail.html', assignment=assignment)

@app.route('/subject/<int:course_id>')
def subject_detail(course_id):
    course = canvas.get_course_by_id(course_id)
    if not course:
        return "Course not found", 404
    # Filter assignments for this course
    # Filter assignments for this course
    assignments = [a for a in canvas.get_assignments() if a['course_id'] == course_id]
    custom_sections = canvas.get_custom_sections(course_id)
    lecture_summaries = canvas.get_lecture_summaries(course_id)
    quizzes = canvas.get_quizzes(course_id)
    workflow = canvas.get_workflow(course_id)
    return render_template('subject.html', course=course, assignments=assignments, custom_sections=custom_sections, lecture_summaries=lecture_summaries, quizzes=quizzes, workflow=workflow)

@app.route('/subject/<int:course_id>/workflow')
def subject_workflow(course_id):
    course = canvas.get_course_by_id(course_id)
    if not course: return "Course not found", 404
    workflow = canvas.get_full_workflow(course_id)
    return render_template('workflow_detail.html', course=course, workflow=workflow)

@app.route('/integrations')
def integrations():
    services = canvas.get_connected_services()
    return render_template('integrations.html', services=services)

@app.route('/api/integrations/connect', methods=['POST'])
def connect_integration():
    data = request.json
    service = data.get('service')
    success = canvas.connect_service(service)
    return jsonify({'success': success, 'status': 'connected'})

@app.route('/api/integrations/disconnect', methods=['POST'])
def disconnect_integration():
    data = request.json
    service = data.get('service')
    success = canvas.disconnect_service(service)
    return jsonify({'success': success, 'status': 'disconnected'})

@app.route('/tasks')
def tasks():
    assignments = canvas.get_assignments()
    courses = canvas.get_courses()
    return render_template('tasks.html', assignments=assignments, courses=courses)

@app.route('/schedule')
def schedule():
    assignments = canvas.get_assignments()
    return render_template('schedule.html', assignments=assignments)

@app.route('/subjects')
def subjects_list():
    courses = canvas.get_courses()
    return render_template('subjects_list.html', courses=courses)

@app.route('/octavia')
def octavia_page():
    return render_template('octavia.html')

@app.route('/database')
def database():
    files = canvas.get_files()
    return render_template('database.html', files=files)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Mock upload process
    new_file = canvas.add_file(file.filename)
    return jsonify(new_file)

@app.route('/api/octavia', methods=['POST'])
def chat_octavia():
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', None) # Expecting {type: 'task', data: {...}}
    response = octavia.process_message(user_message, context)
    return jsonify(response)

@app.route('/api/task/<int:task_id>/breakdown', methods=['POST'])
def task_breakdown(task_id):
    # Simulated breakdown
    steps = [
        {"id": 1, "text": "Research key concepts", "completed": False},
        {"id": 2, "text": "Draft outline", "completed": False},
        {"id": 3, "text": "Write introduction", "completed": False},
        {"id": 4, "text": "Compile references", "completed": False}
    ]
    return jsonify({"steps": steps})

@app.route('/api/task/<int:task_id>/research', methods=['POST'])
def task_research(task_id):
    # Simulated research resources
    resources = [
        {"title": "Academic Paper: Advanced Concepts", "url": "#", "type": "pdf"},
        {"title": "Video Lecture: Topic Overview", "url": "#", "type": "video"},
        {"title": "Course Notes: Week 3", "url": "#", "type": "doc"}
    ]
    resources = [
        {"title": "Academic Paper: Advanced Concepts", "url": "#", "type": "pdf"},
        {"title": "Video Lecture: Topic Overview", "url": "#", "type": "video"},
        {"title": "Course Notes: Week 3", "url": "#", "type": "doc"}
    ]
    return jsonify({"resources": resources})

# --- Subject Customization APIs ---
@app.route('/api/subject/<int:course_id>/section', methods=['POST'])
def add_section(course_id):
    data = request.json
    section = canvas.add_custom_section(course_id, data.get('title'))
    return jsonify(section)

@app.route('/api/subject/<int:course_id>/note', methods=['POST'])
def add_note(course_id):
    data = request.json
    section = canvas.add_note_to_section(course_id, data.get('section_id'), data.get('content'))
    return jsonify(section)

@app.route('/api/subject/<int:course_id>/lecture', methods=['POST'])
def save_lecture(course_id):
    data = request.json
    summary = canvas.add_lecture_summary(course_id, data.get('transcript'))
    return jsonify(summary)

# --- Project Dev Routes ---
@app.route('/project-dev')
def project_dev():
    projects = canvas.get_projects()
    return render_template('project_dev.html', projects=projects)

@app.route('/project-dev/<int:project_id>')
def project_detail(project_id):
    project = canvas.get_project_by_id(project_id)
    if not project:
        return "Project not found", 404
    return render_template('project_detail.html', project=project)

@app.route('/api/projects/create', methods=['POST'])
def create_project():
    data = request.json
    project = canvas.create_project(data.get('title'), data.get('description'), data.get('category'))
    return jsonify(project)

@app.route('/api/projects/<int:project_id>/note', methods=['POST'])
def add_project_note(project_id):
    data = request.json
    note = canvas.add_project_note(project_id, data.get('content'))
    return jsonify(note)

@app.route('/api/projects/<int:project_id>/note/<int:note_id>', methods=['DELETE'])
def delete_project_note(project_id, note_id):
    success = canvas.delete_project_note(project_id, note_id)
    return jsonify({'success': success})

@app.route('/api/projects/<int:project_id>/workflow', methods=['POST'])
def add_project_workflow(project_id):
    data = request.json
    step = canvas.add_project_workflow_step(project_id, data.get('step'))
    return jsonify(step)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
