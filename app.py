from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# 📚 In-memory database
students = [
    {"id": 1, "name": "Michaella Pedotim", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Doe", "grade": 9, "section": "Gabriel"},
]

# 🏠 Home Page
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Student Dashboard | Flask API</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #43cea2, #185a9d);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .card {
                background-color: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 20px;
                padding: 40px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 25px rgba(0,0,0,0.3);
                text-align: center;
            }
            .btn-custom {
                border-radius: 12px;
                padding: 10px 25px;
                transition: all 0.3s ease;
                background: #fff;
                color: #185a9d;
                border: none;
                font-weight: 600;
            }
            .btn-custom:hover {
                transform: scale(1.05);
                background: #e3f2fd;
            }
            footer {
                position: fixed;
                bottom: 10px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="card col-md-6 mx-auto">
            <h1>🎓 Student Management System</h1>
            <p class="lead mb-4">Sharpening Minds, Shaping Futures</p>
            <a href="/students" class="btn btn-custom me-2">📋 View Students</a>
            <a href="/docs" class="btn btn-outline-light">📚 API Docs</a>
        </div>
        <footer>Powered by Flask & Python 3.12 🚀</footer>
    </body>
    </html>
    """
    return render_template_string(html)


# 🧑‍🎓 STUDENTS DASHBOARD (View + Add)
@app.route('/students')
def student_dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Students List</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(120deg, #00c6ff, #0072ff);
                font-family: 'Poppins', sans-serif;
                color: #fff;
                min-height: 100vh;
                padding: 50px;
            }
            .table {
                background-color: rgba(255,255,255,0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            .table th {
                background: rgba(0,0,0,0.2);
            }
            .form-control, .btn {
                border-radius: 10px;
            }
            .btn-add {
                background-color: #4CAF50;
                color: white;
            }
            .btn-add:hover {
                background-color: #45a049;
            }
            .card {
                background-color: rgba(0,0,0,0.2);
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
            a.back {
                color: #fff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <h2 class="mb-4 text-center">📋 Student Records</h2>
            <div class="card mb-4">
                <form method="POST" action="/students/add">
                    <div class="row g-2">
                        <div class="col-md-4">
                            <input type="text" name="name" class="form-control" placeholder="Name" required>
                        </div>
                        <div class="col-md-3">
                            <input type="number" name="grade" class="form-control" placeholder="Grade" required>
                        </div>
                        <div class="col-md-3">
                            <input type="text" name="section" class="form-control" placeholder="Section" required>
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-add w-100">Add</button>
                        </div>
                    </div>
                </form>
            </div>

            <table class="table table-hover text-white">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in students %}
                    <tr>
                        <td>{{ s.id }}</td>
                        <td>{{ s.name }}</td>
                        <td>{{ s.grade }}</td>
                        <td>{{ s.section }}</td>
                        <td>
                            <a href="/students/delete/{{ s.id }}" class="btn btn-sm btn-danger">Delete</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="text-center mt-4">
                <a href="/" class="back">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)


# 🟢 API ROUTE: Get all students (JSON)
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)


# 🟢 GET ONE
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


# 🟡 ADD STUDENT (via web form)
@app.route('/students/add', methods=['POST'])
def add_student_web():
    name = request.form['name']
    grade = int(request.form['grade'])
    section = request.form['section']
    new_id = max([s["id"] for s in students]) + 1 if students else 1
    students.append({"id": new_id, "name": name, "grade": grade, "section": section})
    return redirect(url_for('student_dashboard'))


# 🟡 CREATE via API
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Invalid input"}), 400
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, **data}
    students.append(new_student)
    return jsonify({"message": "Student added successfully", "student": new_student}), 201


# 🟠 UPDATE (API)
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student.update({
        "name": data.get("name", student["name"]),
        "grade": data.get("grade", student["grade"]),
        "section": data.get("section", student["section"]),
    })
    return jsonify({"message": "Student updated successfully", "student": student})


# 🔴 DELETE (via Web Button)
@app.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student_web(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return redirect(url_for('student_dashboard'))


# 🔴 DELETE (via API)
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted successfully"})


# 📄 API Docs Page
@app.route('/docs')
def docs():
    html = """
    <html>
    <head>
        <title>Student API Documentation</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: #101820;
                color: #fff;
                font-family: 'Poppins', sans-serif;
                padding: 3rem;
            }
            .endpoint {
                background: #1a1a1a;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 10px rgba(255,255,255,0.05);
            }
            code { color: #00e5ff; }
            a { color: #00e5ff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1 class="mb-4">📚 Student API Documentation</h1>
        <div class="endpoint"><b>GET</b> <code>/api/students</code> → Get all students</div>
        <div class="endpoint"><b>GET</b> <code>/api/students/&lt;id&gt;</code> → Get one student</div>
        <div class="endpoint"><b>POST</b> <code>/api/students</code> → Add new student<br>Example JSON: <code>{"name": "Ella", "grade": 11, "section": "Faith"}</code></div>
        <div class="endpoint"><b>PUT</b> <code>/api/students/&lt;id&gt;</code> → Update student info<br>Example JSON: <code>{"grade": 12}</code></div>
        <div class="endpoint"><b>DELETE</b> <code>/api/students/&lt;id&gt;</code> → Delete student</div>
        <br>
        <a href="/">← Back to Dashboard</a>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)
