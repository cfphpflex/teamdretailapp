from flask import current_app, render_template, Flask, redirect, request, url_for
import firestore
import storage
import email_helper
from google.cloud import error_reporting


app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif']),
)

app.debug = False
app.testing = False

# ***MICROSERVICE #1: "ADD ITEMS"  ***

@app.route("/items/add", methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        data["price"] = float(data.get("price", 100000))
        data["quantity"] = int(data.get("quantity", 0))
        # If an image was uploaded, update the data to point to the
        image_urls = storage.upload_image_files(request.files.getlist('images'))
        if image_urls:
            data['images'] = image_urls
        item = firestore.create(data)
        return redirect(url_for('.item_detail', item_id=item['id']))

    return render_template("item_entry_form.html", action='Add', item={})


# ***MICROSERVICE #2: "CONFIRM ITEM ID"  ***

@app.route("/confirm/<item_id>", methods=['GET', 'POST'])
def confirm_item(item_id):
    item = firestore.read(item_id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        email = data.get("email")
        if email is None:
            return render_template("confirm.html", error_message="Please enter a valid email")
        if email_helper.send_order_confirmation(email, item):
            firestore.update_inventory(item_id)
        user_data = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
        }
         
        user = firestore.create_user(user_data)
        order_data = {
            "item_id": item.get("id"),
            "user_id": user.get("id"),
            "units": int(data.get("units")),
        }
        firestore.create_order(order_data)
        return redirect(url_for('.list_items'))
    return render_template("confirm.html", item=item)


# ***MICROSERVICE #3: "ITEM DETAIL"  ***

@app.route("/item/detail/<item_id>")
def item_detail(item_id):
    item = firestore.read(item_id)
    return render_template('item_details.html', item=item)


# ***MICROSERVICE #4: "ORDERS"  ***

@app.route("/orders")
def list_orders():
    orders = firestore.list_collection(u'Order')
    return render_template("order_list.html", orders=orders)


# ***MICROSERVICE #5: "List of USERS"  ***

@app.route("/users")
def list_users():
    users = firestore.list_collection(u'User')
    return render_template("user_list.html", users=users)


# ***MICROSERVICE #6: "List of Items"  ***

@app.route("/")
def list_items():
    start_after = request.args.get('start_after', None)
    items, last_item_id = firestore.next_page(start_after=start_after)
    return render_template("item_list.html", items=items, last_item_id=last_item_id)

# Add an error handler that reports exceptions to Stackdriver Error
# Reporting. Note that this error handler is only used when debug
# is False


# ***MICROSERVICE #7: "ERROR HANDLDER"  ***

@app.errorhandler(500)
def server_error(e):
    client = error_reporting.Client()
    client.report_exception(
        http_context=error_reporting.build_flask_context(request))
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
