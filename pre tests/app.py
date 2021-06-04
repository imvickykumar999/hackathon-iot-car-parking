
# https://stackoverflow.com/a/57864823/11493297

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def app_home():
    return render_template("passarg.html",
                            variable_here = ['1','2','3','4','5'],
                            range5 = range(5),
                            )

@app.route("/getData", methods=['GET'])
def getData():

    entry1Value = request.args.get('entry1_id')
    print(entry1Value)

    import pyttsx3
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(f"Hello, I am speaking title {entry1Value}")
    engine.runAndWait()

    return jsonify({ 'var1': str(entry1Value) })

if __name__ == '__main__':
   app.run(debug=True)
