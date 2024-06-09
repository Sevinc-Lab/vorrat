<h1>Shopping List</h1>
<div id="shopping-box">
    {% for item in shopping_messages %}
        <p>{{ item.item }} - {{ item.quantity }} {{ item.unit }} (Purchase: {{ item.purchase_date }}, Expiry: {{ item.expiry_date if item.expiry_date else 'None' }}, Category: {{ item.category }})
            <form action="/delete_shopping/{{ item.id }}" method="post" style="display:inline;">
                <button type="submit">Auslagern</button>
            </form>
            <form action="/delete_directly/{{ item.id }}" method="post" style="display:inline;">
                <button type="submit">Remove</button>
            </form>
            <form action="/update_dates_shopping/{{ item.id }}" method="post" style="display:inline;">
                <input type="date" name="purchase_date" value="{{ item.purchase_date }}" required>
                <input type="date" name="expiry_date" value="{{ item.expiry_date }}">
                <button type="submit">Update Dates</button>
            </form>
            <form action="/update_quantity_shopping/{{ item.id }}" method="post" style="display:inline;">
                <input type="number" name="quantity" value="{{ item.quantity }}" required>
                <button type="submit">Update Quantity</button>
            </form>
            <form action="/update_unit_shopping/{{ item.id }}" method="post" style="display:inline;">
                <select name="unit" required>
                    <option value="Liter" {% if item.unit == 'Liter' %}selected{% endif %}>Liter</option>
                    <option value="Stück" {% if item.unit == 'Stück' %}selected{% endif %}>Stück</option>
                    <option value="Milliliter" {% if item.unit == 'Milliliter' %}selected{% endif %}>Milliliter</option>
                    <option value="Gramm" {% if item.unit == 'Gramm' %}selected{% endif %}>Gramm</option>
                    <option value="Kilogramm" {% if item.unit == 'Kilogramm' %}selected{% endif %}>Kilogramm</option>
                    <option value="Packungen" {% if item.unit == 'Packungen' %}selected{% endif %}>Packungen</option>
                    <option value="Flaschen" {% if item.unit == 'Flaschen' %}selected{% endif %}>Flaschen</option>
                    <option value="Kästen" {% if item.unit == 'Kästen' %}selected{% endif %}>Kästen</option>
                    <option value="Boxen" {% if item.unit == 'Boxen' %}selected{% endif %}>Boxen</option>
                    <option value="Gläser" {% if item.unit == 'Gläser' %}selected{% endif %}>Gläser</option>
                    <option value="Dosen" {% if item.unit == 'Dosen' %}selected{% endif %}>Dosen</option>
                    <option value="Tuben" {% if item.unit == 'Tuben' %}selected{% endif %}>Tuben</option>
                </select>
                <button type="submit">Update Unit</button>
            </form>
        </p>
    {% endfor %}
</div>
<form id="shopping-form" action="/add_to_shopping" method="post" oninput="fetchUnit('item', 'unit_shopping')">
    <input type="text" name="item" placeholder="Enter item" required>
    <input type="number" name="quantity" value="1" placeholder="Enter quantity" required>
    <select name="unit" id="unit_shopping" required>
        <option value="Liter">Liter</option>
        <option value="Stück">Stück</option>
        <option value="Milliliter">Milliliter</option>
        <option value="Gramm">Gramm</option>
        <option value="Kilogramm">Kilogramm</option>
        <option value="Packungen">Packungen</option>
        <option value="Flaschen">Flaschen</option>
        <option value="Kästen">Kästen</option>
        <option value="Boxen">Boxen</option>
        <option value="Gläser">Gläser</option>
        <option value="Dosen">Dosen</option>
        <option value="Tuben">Tuben</option>
    </select>
    <input type="date" name="purchase_date" placeholder="Purchase Date">
    <input type="date" name="expiry_date" placeholder="Expiry Date">
    <button type="submit">Add to Shopping List</button>
</form>
