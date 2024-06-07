from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('Product.db')
cur = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS pro (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    details INTEGER
);
'''
cur.execute(create_table_query)
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_prod', methods=['POST'])
def add_prod():
    name = request.form['name']
    details = request.form['details']
    
    conn = sqlite3.connect('Product.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO pro (name, details) VALUES (?, ?)", (name, details))
    conn.commit()

    conn.close()

    return redirect('/home')

@app.route('/view_prod')
def view_users():
    conn = sqlite3.connect('Product.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM pro")
    rows = cur.fetchall()

    conn.close()

    return render_template('view_prod.html', rows=rows)

@app.route('/delete_prod', methods=['POST'])
def delete_prod():
    if 'id' in request.form:
        prod_id = request.form['id']
    else:
        prod_id = request.form['delete_id']

    conn = sqlite3.connect('Product.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM pro WHERE id = ?", (prod_id,))
    conn.commit()

    conn.close()

    return redirect('/view_prod')

@app.route('/update_prod', methods=['POST'])
def update_prod():
    prod_id = request.form['id']
    
    # Fetch the existing user data
    conn = sqlite3.connect('Product.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM pro WHERE id = ?", (prod_id,))
    prod_data = cur.fetchone()
    conn.close()
    
    return render_template('update_prod.html', user_data=prod_data)

if __name__ == '__main__':
    app.run(debug=True)