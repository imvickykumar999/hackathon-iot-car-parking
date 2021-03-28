
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():

    from firebase import firebase
    firebase1 = firebase.FirebaseApplication('https://led-blink-wifi-default-rtdb.firebaseio.com/', None)
    result = firebase1.get('/led1', None)
    list_result = list(result.values())[-11:-1]
    is_occupied = sum(list_result)/10
    return "{}".format(is_occupied)

if __name__ == '__main__':
    app.run(debug=True)
