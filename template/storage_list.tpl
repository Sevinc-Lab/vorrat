<h1>Storage List</h1>
{% for location, messages in storage_messages.items() %}
<h2>{{ location }}</h2>
<div class="location-box">
    {% for message in messages %}
        <p>{{ message.message }} - {{ message.quantity }} {{ message.unit }} (Purchase: {{ message.purchase_date }}, Expiry: {{ message.expiry_date }}, Category: {{ message.category }})
            <form action="/update_quantity/{{ message.id }}" method="post" style="display:inline;">
                <input type="number" name="quantity" value="{{ message.quantity }}" required>
                <button type="submit">Update Quantity</button>
            </form>
            <form action="/update/{{ message.id }}" method="post" style="display:inline;">
                <input type="number" name="used_quantity" step="0.1" placeholder="Enter quantity used" required>
                <button type="submit">Update</button>
            </form>
            <form action="/delete/{{ message.id }}" method="post" style="display:inline;">
                <button type="submit">Remove</button>
            </form>
            <form action="/move/{{ message.id }}" method="post" style="display:inline;" class="move-form">
                <input type="number" name="move_quantity" value="1" step="0.1" placeholder="Quantity to move" required>
                <select name="new_location" required>
                    <option value="Gefrierschrank">Gefrierschrank</option>
                    <option value="Kühlschrank">Kühlschrank</option>
                    <option value="Null-Grad-Zone">Null-Grad-Zone</option>
                    <option value="Vorratsschrank">Vorratsschrank</option>
                </select>
                <button type="submit">Move</button>
            </form>
            <form action="/update_unit/{{ message.id }}" method="post" style="display:inline;">
                <select name="new_unit" required>
                    <option value="Liter" {% if message.unit == 'Liter' %}selected{% endif %}>Liter</option>
                    <option value="Stück" {% if message.unit == 'Stück' %}selected{% endif %}>Stück</option>
                    <option value="Milliliter" {% if message.unit == 'Milliliter' %}selected{% endif %}>Milliliter</option>
                    <option value="Gramm" {% if message.unit == 'Gramm' %}selected{% endif %}>Gramm</option>
                    <option value="Kilogramm" {% if message.unit == 'Kilogramm' %}selected{% endif %}>Kilogramm</option>
                    <option value="Packungen" {% if message.unit == 'Packungen' %}selected{% endif %}>Packungen</option>
                    <option value="Flaschen" {% if message.unit == 'Flaschen' %}selected{% endif %}>Flaschen</option>
                    <option value="Kästen" {% if message.unit == 'Kästen' %}selected{% endif %}>Kästen</option>
                    <option value="Boxen" {% if message.unit == 'Boxen' %}selected{% endif %}>Boxen</option>
                    <option value="Gläser" {% if message.unit == 'Gläser' %}selected{% endif %}>Gläser</option>
                    <option value="Dosen" {% if message.unit == 'Dosen' %}selected{% endif %}>Dosen</option>
                    <option value="Tuben" {% if message.unit == 'Tuben' %}selected{% endif %}>Tuben</option>
                </select>
                <button type="submit">Update Unit</button>
            </form>
            <form action="/update_dates/{{ message.id }}" method="post" style="display:inline;">
                <input type="date" name="purchase_date" value="{{ message.purchase_date }}" required>
                <input type="date" name="expiry_date" value="{{ message.expiry_date }}">
                <button type="submit">Update Dates</button>
            </form>
            <form action="/move_to_shopping/{{ message.id }}" method="post" style="display:inline;">
                <button type="submit">Move to Shopping List</button>
            </form>
        </p>
    {% endfor %}
</div>
{% endfor %}
