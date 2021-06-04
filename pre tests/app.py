
# https://stackoverflow.com/a/57864823/11493297

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/SomeFunction')
def SomeFunction(parameter = '1'):
    print('In SomeFunction')

    import pyttsx3
    engine = pyttsx3.init()

    # rate = engine.getProperty('rate')   # getting details of current speaking rate
    # print (rate)                        #printing current voice rate
    # engine.setProperty('rate', 150)     # setting up new voice rate

    # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    # print (volume)                          #printing current volume level
    # engine.setProperty('volume',1.0)

    voices = engine.getProperty('voices')       #getting details of current voice
    # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)

    # content = '''
    # A video of Mika Singh has surfaced online, in which he can be seen visiting Kamaal R Khan's house and claiming that the latter sold the property out of fear. "Please don't sell all your other houses because I have no personal enmity with you," he said. "Don't be scared. I won't beat you up," Mika added.
    # '''

    engine.say(f"Hello, I am speaking title {parameter}")
    # engine.say(content)
    engine.runAndWait()

    return "Nothing"


@app.route('/', methods=['GET', 'POST'])
def app_home():
    return render_template("passarg.html",
                            variable_here = [1,2,3,4,5],
                            range5 = range(5),
                            )

@app.route("/getData", methods=['GET'])
def getData():

    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')
    #
    var1 = int(entry2Value) + int(entry1Value)
    # var1 = 29
    var2 = 10
    var3 = 15

    import pyttsx3
    engine = pyttsx3.init()

    # rate = engine.getProperty('rate')   # getting details of current speaking rate
    # print (rate)                        #printing current voice rate
    # engine.setProperty('rate', 150)     # setting up new voice rate

    # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    # print (volume)                          #printing current volume level
    # engine.setProperty('volume',1.0)

    voices = engine.getProperty('voices')       #getting details of current voice
    # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)

    # content = '''
    # A video of Mika Singh has surfaced online, in which he can be seen visiting Kamaal R Khan's house and claiming that the latter sold the property out of fear. "Please don't sell all your other houses because I have no personal enmity with you," he said. "Don't be scared. I won't beat you up," Mika added.
    # '''

    engine.say(f"Hello, I am speaking title {var1}")
    # engine.say(content)
    engine.runAndWait()
    # time.sleep(7)
    # engine.startLoop(False)
    # engine.endLoop()

    # import threading
    # engine = pyttsx3.init()
    # engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
    # engine.startLoop(False)
    # # engine.iterate() must be called inside Server_Up.start()
    # Server_Up = threading.Thread(target = Comm_Connection)
    # Server_Up.start()
    # engine.endLoop()

    return jsonify({ 'var1': var1, 'var2': var2, 'var3': var3 })


if __name__ == '__main__':
   app.run(debug=True)
