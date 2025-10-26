from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory “database”
students = [
    {"id": 1, "name": "Michaella Pedotim", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Doe", "grade": 9, "section": "Gabriel"},
]

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Dashboard | Flask API</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #38ef7d, #11998e);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .card {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 30px rgba(0,0,0,0.2);
            }
            h1 {
                font-weight: 700;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            a.btn {
                border-radius: 12px;
                padding: 10px 25px;
                transition: all 0.3s ease;
            }
            a.btn:hover {
                transform: scale(1.05);
            }
            footer {
                position: fixed;
                bottom: 15px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="card w-75 mx-auto">
            <h1>🎓 Student API Dashboard</h1>
            <p class="lead mb-4">Sharpening Minds, Shaping Futures</p>
            <div class="d-flex justify-content-center gap-3">
                <a href="/students" class="btn btn-light">📋 View All Students</a>
                <a href="/docs" class="btn btn-outline-light">📚 API Docs</a>
            </div>
        </div>
        <footer>Powered by Flask & Python 3.12 🚀</footer>
    </body>
    </html>
    """
    return render_template_string(html)


# ✅ READ: Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


# ✅ READ: Single student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


# ✅ CREATE: Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Invalid input"}), 400
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, **data}
    students.append(new_student)
    return jsonify({"message": "Student added successfully", "student": new_student}), 201


# ✅ UPDATE: Edit student info
@app.route('/students/<int:student_id>', methods=['PUT'])
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


# ✅ DELETE: Remove student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted successfully"})


# 🧾 API Documentation Page
@app.route('/docs')
def docs():
    html = """
    <html>
    <head>
        <title>API Documentation</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: #121212;
                color: #fff;
                padding: 3rem;
                font-family: 'Poppins', sans-serif;
            }
            .endpoint {
                background: #1e1e1e;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }
            code { color: #0dcaf0; }
            a { color: #0dcaf0; }
        </style>
    </head>
    <body>
        <h1 class="mb-4">📚 Student API Documentation</h1>
        <div class="endpoint"><b>GET</b> <code>/students</code> → Get all students</div>
        <div class="endpoint"><b>GET</b> <code>/students/&lt;id&gt;</code> → Get one student</div>
        <div class="endpoint"><b>POST</b> <code>/students</code> → Add new student<br>Example JSON: <code>{"name": "Ella", "grade": 11, "section": "Faith"}</code></div>
        <div class="endpoint"><b>PUT</b> <code>/students/&lt;id&gt;</code> → Update student info<br>Example JSON: <code>{"grade": 12}</code></div>
        <div class="endpoint"><b>DELETE</b> <code>/students/&lt;id&gt;</code> → Delete a student</div>
        <a href="/">← Back to Dashboard</a>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)
