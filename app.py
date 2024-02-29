from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)
app.secret_key = 'many random bytes'  

def get_db():
    """Ensure the database connection is unique per request and reused if already opened."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def db_query(query, args=(), one=False):
    """Execute a database query and return the results."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()  
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def index():
    """Show all users."""
    users = db_query("SELECT * FROM users")
    return render_template("index.html", users=users)

@app.route("/insert", methods=["POST"])
def insert():
    name = request.form['name']
    user_id = request.form['id']  
    points = request.form['points']
    insert_query = "INSERT INTO users (name, id, points) VALUES (?, ?, ?)"
    try:
        db = get_db()
        db.execute(insert_query, (name, user_id, points))
        db.commit()  
        flash("User successfully inserted.")  
    except sqlite3.IntegrityError as e:  
        flash("Error inserting user: " + str(e))  
    except Exception as e:  # 
        flash("An error occurred: " + str(e))  
    finally:
        pass
    
    return redirect(url_for("index"))  

@app.route("/search", methods=["GET"])
def search():
    """Search for users by name."""
    search_term = request.args.get('search', '')
    users = db_query("SELECT * FROM users WHERE name LIKE ?", ('%' + search_term + '%',))
    return render_template("index.html", users=users)

@app.route("/delete", methods=["POST"])
def delete():
    """Delete a user by ID."""
    id_data = request.form['id']  
    db_query("DELETE FROM users WHERE id=?", (id_data,))
    flash("Record has been successfully deleted")
    return redirect(url_for("index"))

@app.route("/update", methods=["POST"])
def update():
    original_id = request.form.get('original_id')
    new_name = request.form.get('name')
    new_points = request.form.get('points')
    
    try:
        new_points = int(new_points)
    except ValueError:
        flash("Points must be a whole number.")
        return redirect(url_for('index'))
    
    try:
        db = get_db()
        db.execute("UPDATE users SET name=?, points=? WHERE id=?", (new_name, new_points, original_id))
        db.commit()
        flash("User updated successfully.")
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
