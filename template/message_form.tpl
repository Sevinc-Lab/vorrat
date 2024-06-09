<form id="message-form" action="/send" method="post" oninput="fetchUnit('message', 'unit')">
    <input type="text" name="message" placeholder="Enter your message" required>
    <input type="number" name="quantity" value="1" placeholder="Enter quantity" required>
    <select name="unit" id="unit" required>
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
    <select name="location" id="location" required>
        <option value="Gefrierschrank">Gefrierschrank</option>
        <option value="Kühlschrank">Kühlschrank</option>
        <option value="Null-Grad-Zone">Null-Grad-Zone</option>
        <option value="Vorratsschrank">Vorratsschrank</option>
        <!-- Weitere Lagerorte können hier hinzugefügt werden -->
    </select>
    <input type="date" name="purchase_date" placeholder="Purchase Date">
    <input type="date" name="expiry_date" placeholder="Expiry Date">
    <button type="submit">Add to Storage</button>
    <input type="text" id="category" name="category" placeholder="Category (if new item)">
    <input type="text" id="default_location" name="default_location" placeholder="Default Location (if new item)">
    <input type="number" id="shelf_life_vorratsschrank" name="shelf_life_vorratsschrank" placeholder="Shelf Life Vorratsschrank (if new item)">
    <input type="number" id="shelf_life_kuehlschrank" name="shelf_life_kuehlschrank" placeholder="Shelf Life Kühlschrank (if new item)">
    <input type="number" id="shelf_life_null_grad_zone" name="shelf_life_null_grad_zone" placeholder="Shelf Life Null-Grad-Zone (if new item)">
    <input type="number" id="shelf_life_gefrierschrank" name="shelf_life_gefrierschrank" placeholder="Shelf Life Gefrierschrank (if new item)">
</form>

<h2>Update Existing Item</h2>
<form id="update-form" action="/update_item" method="post">
    <input type="text" id="update_message" name="message" placeholder="Enter your message" required>
    <select name="unit" id="update_unit" required>
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
    <select name="default_location" id="update_default_location" required>
        <option value="Gefrierschrank">Gefrierschrank</option>
        <option value="Kühlschrank">Kühlschrank</option>
        <option value="Null-Grad-Zone">Null-Grad-Zone</option>
        <option value="Vorratsschrank">Vorratsschrank</option>
        <!-- Weitere Lagerorte können hier hinzugefügt werden -->
    </select>
    <input type="text" id="update_category" name="category" placeholder="Category">
    <input type="number" id="update_shelf_life_vorratsschrank" name="shelf_life_vorratsschrank" placeholder="Shelf Life Vorratsschrank">
    <input type="number" id="update_shelf_life_kuehlschrank" name="shelf_life_kuehlschrank" placeholder="Shelf Life Kühlschrank">
    <input type="number" id="update_shelf_life_null_grad_zone" name="shelf_life_null_grad_zone" placeholder="Shelf Life Null-Grad-Zone">
    <input type="number" id="update_shelf_life_gefrierschrank" name="shelf_life_gefrierschrank" placeholder="Shelf Life Gefrierschrank">
    <button type="submit">Update Item</button>
</form>
