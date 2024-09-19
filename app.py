from flask import Flask, render_template

from flow.backend.postgresql.connect import get_db_connection

app = Flask(__name__, template_folder='/app/flow/frontend/templates/')  # prepend /app/ for Docker


@app.route('/')
def home():
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('index.html', title="My Budget App", db_version=db_version)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
