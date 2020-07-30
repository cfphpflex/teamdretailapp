from flask import current_app, render_template, Flask, redirect, request, url_for
# import firestore
import storage

#from google.cloud import error_reporting

app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif']),
)

app.debug = False
app.testing = False

@app.route("/")
def list_items():
    # start_after = request.args.get('start_after', None)
    # items, last_item_id = firestore.next_page(start_after=start_after)
    # return render_template("item_list.html", items=items, last_item_id=last_item_id)

    return "Hello new world, Yeeehaaa!!!! ;>"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
