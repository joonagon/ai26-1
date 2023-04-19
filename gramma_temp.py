import sqlite3
conn = sqlite3.connect('grammar.db')
c = conn.cursor()

# Create a table to store the sentences
c.execute('''CREATE TABLE IF NOT EXISTS sentences
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              sentence TEXT,
              corrected_sentence TEXT)''')