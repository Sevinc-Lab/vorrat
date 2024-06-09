import time
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_expiry_date(purchase_date, shelf_life):
    if shelf_life is None:
        return None
    purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    return (purchase_date + timedelta(days=int(shelf_life))).strftime('%Y-%m-%d')

@app.route('/')
def index():
    conn = get_db_connection()
    storage_rows = conn.execute('SELECT * FROM messages').fetchall()
    shopping_rows = conn.execute('SELECT * FROM shopping_list').fetchall()
    conn.close()
    
    storage_messages = {
        "Gefrierschrank": [dict(row) for row in storage_rows if row["location"] == "Gefrierschrank"],
        "Kühlschrank": [dict(row) for row in storage_rows if row["location"] == "Kühlschrank"],
        "Null-Grad-Zone": [dict(row) for row in storage_rows if row["location"] == "Null-Grad-Zone"],
        "Vorratsschrank": [dict(row) for row in storage_rows if row["location"] == "Vorratsschrank"],
    }
    
    shopping_messages = [dict(row) for row in shopping_rows]
    
    return render_template('index.html', storage_messages=storage_messages, shopping_messages=shopping_messages)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    quantity = request.form['quantity']
    unit = request.form['unit']
    location = request.form['location']
    purchase_date = request.form['purchase_date']
    expiry_date = request.form['expiry_date'] if request.form['expiry_date'] else None
    
    conn = get_db_connection()
    row = conn.execute('SELECT category, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank FROM item_units WHERE item = ?', (message,)).fetchone()
    
    if row:
        category = row['category']
        # Berechne das Ablaufdatum basierend auf dem Lagerort
        if location == 'Vorratsschrank':
            shelf_life = row['shelf_life_vorratsschrank']
        elif location == 'Kühlschrank':
            shelf_life = row['shelf_life_kuehlschrank']
        elif location == 'Null-Grad-Zone':
            shelf_life = row['shelf_life_null_grad_zone']
        elif location == 'Gefrierschrank':
            shelf_life = row['shelf_life_gefrierschrank']
        else:
            shelf_life = None
    else:
        category = request.form.get('category', 'Undefined')
        shelf_life = {
            'Vorratsschrank': request.form.get('shelf_life_vorratsschrank', None),
            'Kühlschrank': request.form.get('shelf_life_kuehlschrank', None),
            'Null-Grad-Zone': request.form.get('shelf_life_null_grad_zone', None),
            'Gefrierschrank': request.form.get('shelf_life_gefrierschrank', None)
        }.get(location, None)

        # Füge den neuen Artikel zur item_units Tabelle hinzu
        conn.execute('''
            INSERT INTO item_units (item, unit, category, default_location, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (message, unit, category, location, request.form.get('shelf_life_vorratsschrank', None), request.form.get('shelf_life_kuehlschrank', None), request.form.get('shelf_life_null_grad_zone', None), request.form.get('shelf_life_gefrierschrank', None)))

    if not expiry_date:
        expiry_date = calculate_expiry_date(purchase_date, shelf_life) if shelf_life else None

    conn.execute('INSERT INTO messages (message, quantity, unit, location, purchase_date, expiry_date, category) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (message, quantity, unit, location, purchase_date, expiry_date, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/add_to_shopping', methods=['POST'])
def add_to_shopping():
    item = request.form['item']
    quantity = request.form['quantity']
    unit = request.form['unit']
    purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d')
    expiry_date_input = request.form['expiry_date']

    conn = get_db_connection()
    row = conn.execute('SELECT category, default_location, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank FROM item_units WHERE item = ?', (item,)).fetchone()
    
    if row:
        category = row['category']
        default_location = row['default_location']
        # Berechne das Ablaufdatum basierend auf dem Standardlagerort
        if default_location == 'Vorratsschrank':
            shelf_life = row['shelf_life_vorratsschrank']
        elif default_location == 'Kühlschrank':
            shelf_life = row['shelf_life_kuehlschrank']
        elif default_location == 'Null-Grad-Zone':
            shelf_life = row['shelf_life_null_grad_zone']
        elif default_location == 'Gefrierschrank':
            shelf_life = row['shelf_life_gefrierschrank']
        else:
            shelf_life = None
    else:
        category = 'Undefined'
        default_location = 'Kühlschrank'
        shelf_life = None

    if expiry_date_input:
        expiry_date = expiry_date_input
    else:
        expiry_date = calculate_expiry_date(purchase_date.strftime('%Y-%m-%d'), shelf_life) if shelf_life else None

    conn.execute('INSERT INTO shopping_list (item, quantity, unit, purchase_date, expiry_date, category) VALUES (?, ?, ?, ?, ?, ?)',
                 (item, quantity, unit, purchase_date.strftime('%Y-%m-%d'), expiry_date, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete_directly/<int:id>', methods=['POST'])
def delete_directly(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM shopping_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete_shopping/<int:id>', methods=['POST'])
def delete_shopping(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM shopping_list WHERE id = ?', (id,)).fetchone()
    item = row['item']
    quantity = row['quantity']
    unit = row['unit']
    purchase_date = row['purchase_date']
    expiry_date = row['expiry_date']
    category = row['category'] if row['category'] else 'Undefined'
    
    item_unit_row = conn.execute('SELECT default_location FROM item_units WHERE item = ?', (item,)).fetchone()
    default_location = item_unit_row['default_location'] if item_unit_row else 'Kühlschrank'
    
    conn.execute('INSERT INTO messages (message, quantity, unit, location, purchase_date, expiry_date, category) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (item, quantity, unit, default_location, purchase_date, expiry_date, category))
    conn.execute('DELETE FROM shopping_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    used_quantity = float(request.form['used_quantity'])
    conn = get_db_connection()
    current_quantity = conn.execute('SELECT quantity FROM messages WHERE id = ?', (id,)).fetchone()['quantity']
    new_quantity = current_quantity - used_quantity
    if new_quantity > 0:
        conn.execute('UPDATE messages SET quantity = ? WHERE id = ?', (new_quantity, id))

    else:
        conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/move/<int:id>', methods=['POST'])
def move(id):
    new_location = request.form['new_location']
    move_quantity = float(request.form['move_quantity'])
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM messages WHERE id = ?', (id,)).fetchone()
    
    if row:
        message = row['message']
        quantity = row['quantity']
        unit = row['unit']
        purchase_date = row['purchase_date']
        category = row['category']
        existing_expiry_date = row['expiry_date']
        
        if move_quantity >= quantity:
            conn.execute('DELETE FROM messages WHERE id = ?', (id,))
        else:
            conn.execute('UPDATE messages SET quantity = quantity - ? WHERE id = ?', (move_quantity, id))
        
        item_unit_row = conn.execute('SELECT * FROM item_units WHERE item = ?', (message,)).fetchone()
        if item_unit_row:
            shelf_life_column = f'shelf_life_{new_location.lower().replace("-", "_")}'
            shelf_life = item_unit_row[shelf_life_column] if shelf_life_column in item_unit_row.keys() else None
            
            # Überprüfen, ob der neue Lagerort der Standardlagerort ist
            if new_location == item_unit_row['default_location']:
                shelf_life = item_unit_row['shelf_life_kuehlschrank']  # oder der spezifische shelf_life-Wert für den Standardlagerort
            
        else:
            shelf_life = None
        
        # Berechne das neue Ablaufdatum basierend auf dem neuen Lagerort und dem Kaufdatum
        new_expiry_date = calculate_expiry_date(purchase_date, shelf_life) if shelf_life else existing_expiry_date
        
        conn.execute('INSERT INTO messages (message, quantity, unit, location, purchase_date, expiry_date, category) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (message, move_quantity, unit, new_location, purchase_date, new_expiry_date, category))
    
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/move_to_shopping/<int:id>', methods=['POST'])
def move_to_shopping(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM messages WHERE id = ?', (id,)).fetchone()
    item = row['message']
    quantity = row['quantity']
    unit = row['unit']
    purchase_date = row['purchase_date']
    expiry_date = row['expiry_date']
    category = row['category']
    conn.execute('INSERT INTO shopping_list (item, quantity, unit, purchase_date, expiry_date, category) VALUES (?, ?, ?, ?, ?, ?)', 
                 (item, quantity, unit, purchase_date, expiry_date, category))
    conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_unit/<int:id>', methods=['POST'])
def update_unit(id):
    new_unit = request.form['new_unit']
    conn = get_db_connection()
    conn.execute('UPDATE messages SET unit = ? WHERE id = ?', (new_unit, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_quantity/<int:id>', methods=['POST'])
def update_quantity(id):
    quantity = request.form['quantity']
    conn = get_db_connection()
    conn.execute('UPDATE messages SET quantity = ? WHERE id = ?', (quantity, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_quantity_shopping/<int:id>', methods=['POST'])
def update_quantity_shopping(id):
    quantity = request.form['quantity']
    conn = get_db_connection()
    conn.execute('UPDATE shopping_list SET quantity = ? WHERE id = ?', (quantity, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_unit_shopping/<int:id>', methods=['POST'])
def update_unit_shopping(id):
    unit = request.form['unit']
    conn = get_db_connection()
    conn.execute('UPDATE shopping_list SET unit = ? WHERE id = ?', (unit, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_dates/<int:id>', methods=['POST'])
def update_dates(id):
    purchase_date = request.form['purchase_date']
    expiry_date = request.form.get('expiry_date', None)
    conn = get_db_connection()
    if expiry_date:
        conn.execute('UPDATE messages SET purchase_date = ?, expiry_date = ? WHERE id = ?', (purchase_date, expiry_date, id))
    else:
        conn.execute('UPDATE messages SET purchase_date = ?, expiry_date = NULL WHERE id = ?', (purchase_date, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_dates_shopping/<int:id>', methods=['POST'])
def update_dates_shopping(id):
    purchase_date = request.form['purchase_date']
    expiry_date = request.form.get('expiry_date', None)
    conn = get_db_connection()
    if expiry_date:
        conn.execute('UPDATE shopping_list SET purchase_date = ?, expiry_date = ? WHERE id = ?', (purchase_date, expiry_date, id))
    else:
        conn.execute('UPDATE shopping_list SET purchase_date = ?, expiry_date = NULL WHERE id = ?', (purchase_date, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update_item', methods=['POST'])
def update_item():
    message = request.form['message']
    unit = request.form['unit']
    category = request.form['category']
    default_location = request.form['default_location']
    shelf_life_vorratsschrank = request.form['shelf_life_vorratsschrank']
    shelf_life_kuehlschrank = request.form['shelf_life_kuehlschrank']
    shelf_life_null_grad_zone = request.form['shelf_life_null_grad_zone']
    shelf_life_gefrierschrank = request.form['shelf_life_gefrierschrank']

    conn = get_db_connection()
    conn.execute('''
        UPDATE item_units
        SET unit = ?, category = ?, default_location = ?, shelf_life_vorratsschrank = ?, shelf_life_kuehlschrank = ?, shelf_life_null_grad_zone = ?, shelf_life_gefrierschrank = ?
        WHERE item = ?
    ''', (unit, category, default_location, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank, message))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/get_unit', methods=['GET'])
def get_unit():
    item = request.args.get('item')
    conn = get_db_connection()
    row = conn.execute('SELECT unit, category, default_location, shelf_life_vorratsschrank, shelf_life_kuehlschrank, shelf_life_null_grad_zone, shelf_life_gefrierschrank FROM item_units WHERE item = ?', (item,)).fetchone()
    conn.close()
    if row:
        return {
            'unit': row['unit'],
            'category': row['category'],
            'default_location': row['default_location'],
            'shelf_life_vorratsschrank': row['shelf_life_vorratsschrank'],
            'shelf_life_kuehlschrank': row['shelf_life_kuehlschrank'],
            'shelf_life_null_grad_zone': row['shelf_life_null_grad_zone'],
            'shelf_life_gefrierschrank': row['shelf_life_gefrierschrank']
        }
    else:
        return {
            'unit': '',
            'category': '',
            'default_location': '',
            'shelf_life_vorratsschrank': '',
            'shelf_life_kuehlschrank': '',
            'shelf_life_null_grad_zone': '',
            'shelf_life_gefrierschrank': ''
        }

if __name__ == '__main__':
    app.run(debug=True)
