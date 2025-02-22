import sqlite3

conn = sqlite3.connect("bus_tickets.db")
cursor = conn.cursor()

# Create seats table
cursor.execute("""
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seat_number TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'Available',
    name TEXT,
    phone TEXT
)
""")

# Insert sample seats
seats = [(f"Seat {i+1}",) for i in range(10)]
cursor.executemany("INSERT OR IGNORE INTO seats (seat_number) VALUES (?)", seats)

conn.commit()
conn.close()
