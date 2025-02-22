from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    return sqlite3.connect("bus_tickets.db")

# Home route - Displays seats
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seats")
    seats = cursor.fetchall()
    conn.close()
    return render_template("index.html", seats=seats)

# Booking route
@app.route('/book/<int:seat_id>', methods=['GET', 'POST'])
def book(seat_id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        conn = connect_db()
        cursor = conn.cursor()

        # Check if seat is already booked
        cursor.execute("SELECT status FROM seats WHERE id=?", (seat_id,))
        status = cursor.fetchone()[0]

        if status == 'Booked':
            conn.close()
            return "Seat is already booked!", 400

        # Update seat status
        cursor.execute("UPDATE seats SET status='Booked', name=?, phone=? WHERE id=?", (name, phone, seat_id))
        conn.commit()
        conn.close()

        return redirect(url_for('success', seat_id=seat_id))
    
    return render_template("booking.html", seat_id=seat_id)

# Success route
@app.route('/success/<int:seat_id>')
def success(seat_id):
    return render_template("success.html", seat_id=seat_id)

if __name__ == '__main__':
    app.run(debug=True)
