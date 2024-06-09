<h2>Items Below Minimum Quantity</h2>
{% for item in items_below_minimum %}
    <p>{{ item.message }} - {{ item.quantity }} {{ item.unit }} (Minimum: {{ item.minimum_quantity }})
        <form action="/add_to_shopping" method="post" style="display:inline;">
            <input type="hidden" name="item" value="{{ item.message }}">
            <input type="hidden" name="quantity" value="{{ item.minimum_quantity - item.quantity }}">
            <input type="hidden" name="unit" value="{{ item.unit }}">
            <input type="hidden" name="purchase_date" value="{{ item.purchase_date }}">
            <input type="hidden" name="expiry_date" value="{{ item.expiry_date }}">
            <button type="submit">Add to Shopping List</button>
        </form>
    </p>
{% endfor %}