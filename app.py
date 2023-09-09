from flask import jsonify
from application.app import create_app

app = create_app()

@app.route('/api/')
def index():
    data = {
        'data': [
            {
                "name": "walesl04"
            }
        ]
    }

    return jsonify(data), 200

if __name__ == '__main__':
    app.run()

