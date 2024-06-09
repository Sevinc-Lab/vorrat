import sqlite3

conn = sqlite3.connect('chat.db')
c = conn.cursor()

# Tabelle für Nachrichten (Lagerliste)
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit TEXT NOT NULL,
        location TEXT NOT NULL,
        purchase_date DATE,
        expiry_date DATE,
        category TEXT
    )
''')

# Tabelle für die Einkaufsliste
c.execute('''
    CREATE TABLE IF NOT EXISTS shopping_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit TEXT NOT NULL,
        purchase_date DATE,
        expiry_date DATE,
        category TEXT
    )
''')

# Tabelle für Artikeltypen, Einheiten, Kategorien und Haltbarkeitsdauer
c.execute('''
    CREATE TABLE IF NOT EXISTS item_units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL UNIQUE,
        unit TEXT NOT NULL,
        category TEXT NOT NULL,
        default_location TEXT NOT NULL,
        shelf_life_vorratsschrank INTEGER,
        shelf_life_kuehlschrank INTEGER,
        shelf_life_null_grad_zone INTEGER,
        shelf_life_gefrierschrank INTEGER
    )
''')

# Beispiel für Standardwerte
c.execute('''
    INSERT OR IGNORE INTO item_units (item, unit, category, default_location, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank) VALUES
    ('Milch', 'Liter', 'Milchprodukte & Eier', 'Kühlschrank', NULL, 7, NULL, NULL),
    ('Butter', 'Packungen', 'Milchprodukte & Eier', 'Kühlschrank', NULL, 30, NULL, 180),
    ('Eis', 'Stück', 'Tiefkühl', 'Gefrierschrank', NULL, NULL, NULL, 365)
''')

conn.commit()
conn.close()
