from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Flask API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #7bdcb5, #00aaff);
                color: white;
                text-align: center;
                padding-top: 15%;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.2em;
            }
            a {
                color: #fff;
                background-color: #007acc;
                padding: 10px 20px;
                border-radius: 10px;
                text-decoration: none;
                transition: 0.3s;
            }
            a:hover {
                background-color: #005f99;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to My Flask API 🚀</h1>
        <p>Explore student data below.</p>
        <a href="/student">View Student JSON</a>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Michaella Pedotim",
        "grade": 10,
        "section": "Zechariah"
    })

if __name__ == '__main__':
    app.run(debug=True)
