<head>
    <title>Storage and Shopping List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        #chat-box, #shopping-box, .location-box {
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #fff;
            max-height: 300px;
            overflow-y: scroll;
            margin-bottom: 20px;
        }
        #message-form, #shopping-form, .move-form {
            margin-top: 10px;
        }
        button {
            margin: 2px;  /* Sicherstellen, dass die Buttons Abstand haben */
        }
    </style>
    <script>
        function fetchUnit(inputName, selectId) {
            var item = document.getElementsByName(inputName)[0].value;
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/get_unit?item=' + item, true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.unit) {
                        document.getElementById(selectId).value = response.unit;
                        document.getElementById('update_unit').value = response.unit;
                    }
                    if (response.category) {
                        document.getElementById('update_category').value = response.category;
                        document.getElementById('category').value = response.category;
                    }
                    if (response.default_location) {
                        document.getElementById('update_default_location').value = response.default_location;
                        document.getElementById('default_location').value = response.default_location;
                        document.getElementsByName('location')[0].value = response.default_location;
                    }
                    if (response.shelf_life_vorratsschrank) {
                        document.getElementById('update_shelf_life_vorratsschrank').value = response.shelf_life_vorratsschrank;
                        document.getElementById('shelf_life_vorratsschrank').value = response.shelf_life_vorratsschrank;
                    }
                    if (response.shelf_life_kuehlschrank) {
                        document.getElementById('update_shelf_life_kuehlschrank').value = response.shelf_life_kuehlschrank;
                        document.getElementById('shelf_life_kuehlschrank').value = response.shelf_life_kuehlschrank;
                    }
                    if (response.shelf_life_null_grad_zone) {
                        document.getElementById('update_shelf_life_null_grad_zone').value = response.shelf_life_null_grad_zone;
                        document.getElementById('shelf_life_null_grad_zone').value = response.shelf_life_null_grad_zone;
                    }
                    if (response.shelf_life_gefrierschrank) {
                        document.getElementById('update_shelf_life_gefrierschrank').value = response.shelf_life_gefrierschrank;
                        document.getElementById('shelf_life_gefrierschrank').value = response.shelf_life_gefrierschrank;
                    }

                    // Update the input fields in the update form
                    document.querySelector('#update-form input[name="message"]').value = item;
                }
            };
            xhr.send();
        }

        function setDefaultDate(formId) {
            var today = new Date().toISOString().split('T')[0];
            document.querySelector(`#${formId} input[name="purchase_date"]`).value = today;
        }

        window.onload = function() {
            setDefaultDate('shopping-form');
            setDefaultDate('message-form');
        };
    </script>
</head>
