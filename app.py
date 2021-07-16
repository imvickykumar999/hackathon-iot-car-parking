
from datetime import datetime
from bson.json_util import dumps
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError

from vicks.db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages

# from flask_sqlalchemy import SQLAlchemy
import requests, os
# import pyperclip
from bs4 import BeautifulSoup as bs
from werkzeug.utils import secure_filename

from vicks.encrypt import encryptpdf as enc, imgtopdf as imf
from flask import Flask, flash, jsonify, url_for, session, request, redirect, render_template, send_from_directory
# from vicks import terminal

from flask_qrcode import QRcode
from PIL import Image
import ast, json, urllib.request as ur

UPLOAD_FOLDER = 'uploads'
try:
    os.mkdir('uploads')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/videos')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/audio')
except Exception as e:
    print(e)
    pass

try:
    os.mkdir('uploads/news')
except Exception as e:
    print(e)
    pass

app = Flask(__name__)
app.secret_key = "secret key"

socketio = SocketIO(app)
login_manager = LoginManager()

login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ====================================================================================


@app.route("/covid19")
def covid19():
    return render_template('covid19.html',
                           l=[
                              {'1key1':'1value1', '1key2':'1value2'},
                              {'2key1':'2value1', '2key2':'2value2'}
                             ],
                           )

@app.route('/converted_covid19', methods=['POST', 'GET'])
def converted_covid19():

    import urllib.request
    import json
    from datetime import datetime

    dnow = datetime.now()
    s = str(dnow).split()[0].split('-')

    # --------------------------------
    y = int(s[0])
    m = int(s[1])
    d = int(s[2])

    date = f'{d}-{m}-{y}'
    pin = request.form['pin']

    if pin == '':
        pin = '302020'

    vaccine = ['COVISHIELD', 'COVAXIN', ][0]
    min_age_limit = request.form['age']

    if min_age_limit == '':
        min_age_limit = 18
    else:
        min_age_limit = int(min_age_limit)

    toaddr = request.form['email']
    if toaddr == '':
        toaddr = "hellovickykumar123@gmail.com"

    filename = f"{toaddr.split('@')[0]}.xlsx"
    # ----------------------------------
    # print('.....step 1')

    try:
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}'

        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

        url_request=urllib.request.Request(url, None, headers) #The assembled request
        response = urllib.request.urlopen(url_request)
        f = response.read() # The data u need
        data = json.loads(f.decode('utf-8'))['sessions']
        print(data)

        # with urllib.request.urlopen(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}') as f:
        #     data = json.loads(f.read().decode('utf-8'))['sessions']

    except urllib.error.URLError as e:
        print(e.reason)
        # data = [{'1key1': '1value1', '1key2': '1value2'}, {'2key1': '2value1', '2key2': '2value2'}]

    # print('.....step 2')

    l=[]
    for i, j in enumerate(data):
        # if j['available_capacity_dose2']:
            if j['available_capacity_dose1']:
                if j['vaccine'] == vaccine:
                    if j['min_age_limit'] == min_age_limit:
                        l.append(j)

    # print(l)
    if l:
        from vicks import covidmail as cov
        ifsent = cov.covail(l=l,
                  toaddr = toaddr,
                  filename = filename,
                  )
    else:
        ifsent = 0
        print(l, '...............Email not sent................')

    return render_template('covid19.html', l=l, ifsent = ifsent)

# =====================================================

@app.route("/report")
def report():
    return render_template('form.html')

@app.route('/converted_report', methods=['POST', 'GET'])
def converted_report():

    ld_itemqty = request.form['ld_itemqty']
    ld_itemunit = request.form['ld_itemunit']
    ld_itemprice = request.form['ld_itemprice']
    ld_item = request.form['ld_item']
    ld_purchasedate = request.form['ld_purchasedate']
    ld_paymentmode = request.form['ld_paymentmode']
    ld_paymentdate = request.form['ld_paymentdate']
    ld_date1 = request.form['ld_date1']
    ld_amountpaid = request.form['ld_amountpaid']
    ld_itemqtydelivered = request.form['ld_itemqtydelivered']
    ld_legalnoticedate = request.form['ld_legalnoticedate']
    ld_legalnoticedelivereddate = request.form['ld_legalnoticedelivereddate']
    ld_suitvaluation = request.form['ld_suitvaluation']
    ld_courtfees = request.form['ld_courtfees']
    ld_returnamount = request.form['ld_returnamount']


    text = f'''
                                                In the court of HC
                                            overpaid Case Number 123
                                        Suit for recovery of money OverPaid


    (1) That the plaintiff purchased {ld_item} @ Rs. {ld_itemprice} per {ld_item} from the
    defendant on date {ld_purchasedate}

    (2) That sum of Rs {ld_amountpaid} was paid to the defendant
    through {ld_paymentmode} on {ld_paymentdate}

    (3) That on receipt of {ld_item} on {ld_date1} without verifying the
    quantity of goods plaintiff paid the whole amount of
    Rs. {ld_amountpaid} to the defendant.

    (4) That on verifying the quantity of goods , it was found that
    only {ld_itemqtydelivered} were sent by the defendant whereas
    he has to deliver {ld_itemqty} Ignorant of short supply plaintiff
    paid the whole amount.

    (5) That the plaintiff repeatedly requested the defendant to
    return Rs. {ld_returnamount} which was
    wrongly overpaid but no satisfactory reply given till date.

    (6) That the plaintiff sent a legal notice dated {ld_legalnoticedate}
    through his counsel to the defendant for paying Rs. {ld_returnamount}
    and the same was delivered to him on {ld_legalnoticedelivereddate}

    (7) That it is very surprising that the defendant neither paid
    the amount demanded nor replied to the legal notice sent by
    the plaintiff.

    (8) That in the aforesaid facts and circumstances, the plaintiff
    has no option expect approaching to this court for resolving
    his genuine grievance.

    (9) That the cause of action arose on the date when plaintiff
    requested the defendant to return the þÿoverpaid money,
    but defendant didn t returned the money overpaid.

    (10) That the valuation of the suit for the purpose of
    jurisdiction is Rs. {ld_courtfees}

    (11) That this court has territorial and pecuniary jurisdiction
    to hear and decide this case

    (12) That the suit is within limitation

    (13) That it is humbly prayed that the court shall a pass a decree
    in favour of plaintiff for the sum of Rs. {ld_returnamount}
    along with interest & cost and any other relief in the favour
    of plaintiff which this court deems fit in the facts and
    circumstances of the case

    Date : 26/04/2021

    Verification

    1. That I (above named petitioner) do solemnly affirmed and verify
    the aforesaid contents stated in above para are correct and
    true to the best of my knowledge and belief.

    2. That as per my knowledge and belief nothing has been concealed.

    Date : 26/04/2021

    '''

    with open("myfile.txt", "w") as f:
        f.write(text)

    from vicks import text2pdf as pdf
    pdf.convert()

    return render_template('form.html',

    ld_itemqty = ld_itemqty,
    ld_itemunit = ld_itemunit,
    ld_item = ld_item,
    ld_itemprice = ld_itemprice,
    ld_purchasedate = ld_purchasedate,
    ld_paymentmode = ld_paymentmode,
    ld_paymentdate = ld_paymentdate,
    ld_date1 = ld_date1,
    ld_amountpaid = ld_amountpaid,
    ld_itemqtydelivered = ld_itemqtydelivered,
    ld_legalnoticedate = ld_legalnoticedate,
    ld_legalnoticedelivereddate = ld_legalnoticedelivereddate,
    ld_suitvaluation = ld_suitvaluation,
    ld_courtfees = ld_courtfees,
    ld_returnamount = ld_returnamount
                           )

@app.route("/vickstube", methods=['GET'])
def vickstube():

    vid = 'Cpc_rHf1U6g'
    tm=945
    prefill = request.args.get('list')

    if prefill == None:
        prefill = request.args.get('vix')
        if prefill == None:
            prefill = ''

    print('-------------> ', prefill)
    if len(prefill) == 11:
        vid = prefill
        tm = request.args.get('t')
        if tm==None:
            tm=0
        print(tm)
        # https://youtu.be/KgbAStrUBNY?t=25

    from vicks import ytc
    dict = ytc.comments(vid)
    info = ytc.tvl(vid)

    return render_template("ytc.html",
                            dict=dict,
                            tm=tm,
                            ap=0,
                            prefill = prefill,
                            len = len(prefill),
                            title='None',
                            video_type="0",
                            vidlist = [],
                            vid=vid,
                            info=info,
                            scroll='vickscroll',
                            )

@app.route('/uploads/videos/<filename>')
def send_videos(filename):
    return send_from_directory("uploads/videos", filename)

@app.route('/uploads/audio/<filename>')
def send_audio(filename):
    return send_from_directory("uploads/audio", filename)

@app.route('/converted_vickstube', methods=['POST'])
def converted_vickstube():

    from vicks import ytc
    from youtube_search import YoutubeSearch

    vidlist = []
    url = request.form['ytc']
    if url == '':
        url = 'https://www.youtube.com/watch?v=Cpc_rHf1U6g'

    pid = vid = None
    try:
        pid = url.split('list=')[1].split('&')[0]
        tm = 945
    except:
        s = url.split('/')
        tm=0

        if s[0] != 'https:':
            vidict = YoutubeSearch(s[0], max_results = 10).to_dict()
            vidlist = []
            for i in vidict:
                vidlist.append(i['id'])
            vid = vidlist[0]
            # print('.....---------', vidlist)

        else:
            if s[2] == 'www.youtube.com':
                vid = s[3].split('=')[1].split('?')[0]

            elif s[2] == 'youtu.be':
                vid = s[3].split('?')[0]

            else:
                vid = 'Cpc_rHf1U6g'
                tm = 945
                print("Sorry... Code couldn't be extracted !!!")

    info = (None, None, None)
    try:
        com = ytc.comments(vid)
        info = ytc.tvl(vid)
    except:
        com = {
            "Comments": ["...are Disabled by user !", "Sorry ...or,", ],
            "Playlist" : ["...do not support Comments !",],
        }

    print(com)
    title = "None"
    video_type = request.form['customRadio'].upper()
    print('............', video_type)

    # if requests.status_code == 429: # ...shifted 404.html
    #     import shutil
    #     shutil.rmtree('uploads/videos')
    #     os.mkdir('uploads/videos')

    from vicks import ytdownload as ytd
    ts = request.form['vts']
    te = request.form['vte']

    if ts=='':
        ts=0
    if te=='':
        te=600

    if pid == None:
        if video_type == "V":
            title = ytd.yt_video(vid, int(ts), int(te))

        elif video_type == "A":
            title = ytd.yt_audio(vid, int(ts), int(te))
        else:
            video_type = "0"
    else:
        video_type = "P"

    # print(title, pid)
    print(vidlist)
    return render_template("ytc.html",
                            dict=com,
                            tm=tm,
                            ap=0,
                            title=title,
                            video_type=video_type,
                            vidlist=vidlist,
                            pid = pid,
                            range10=range(1,11),
                            info=info,
                            vid=vid,
                            )

# ========================================================


@app.route("/firechat")
def firechat():
    # https://console.firebase.google.com/u/0/project/chatting-c937e/database/chatting-c937e-default-rtdb/data
    from vicks import crud
    obj1 = crud.vicks('@Hey_Vicks')

    data = obj1.pull('Group/Chat')
    # print('=============================', data)

    if data == None:
        obj1.push()

    data = obj1.pull('Group/Chat')
    return render_template("firechat.html",
                           data = data,
                           )


@app.route('/converted_firechat', methods=['POST'])
def converted_firechat():
    from vicks import crud

    credentials = request.form['credentials']
    person = request.form['person']

    if person == '':
        obj1 = crud.vicks(credentials)
    else:
        # print(credentials)
        obj1 = crud.vicks(credentials, name = person)

    message = request.form['message']
    if message == '':
        obj1.push()
    else:
        obj1.push(message)

    data = obj1.pull('Group/Chat')
    return render_template("firechat.html",
                           data = data,
                           )

# ====================================================


@app.route('/iotcar')
def iotcar():

    from firebase import firebase
    firebase_obj = firebase.FirebaseApplication('https://iot-car-parking-da247-default-rtdb.firebaseio.com/', None)

    result1 = firebase_obj.get('/slot1', None)
    data1="{}".format(result1)

    result2 = firebase_obj.get('/slot2', None)
    data2="{}".format(result2)

    # list_result = list(result.values())[-11:-1]
    # is_occupied = sum(list_result)/10

    with open('YOLO/data1.txt', "r") as myfile:
        slot1 = myfile.read().splitlines()
    a = [len(i) for i in slot1]
    i = a.index(max(a))
    car1 = slot1[i].strip()

    with open('YOLO/data2.txt', "r") as myfile:
        slot2 = myfile.read().splitlines()
    a = [len(i) for i in slot2]
    i = a.index(max(a))
    car2 = slot2[i].strip()

    if result1 == 1:
        img1="static/screenshots/present.png"
    else:
        img1="static/screenshots/absent.png"

    if result2 == 1:
        img2="static/screenshots/present.png"
    else:
        img2="static/screenshots/absent.png"

    return render_template("iotcar.html",
                            data=[data1, data2],
                            car=[car1, car2],
                            img=[img1, img2],
                            len=2
                          )

    # return redirect(url_for('iotcar'),
    #                         # data=[data1, data2],
    #                         # img=[img1, img2],
    #                         # len=2
    #                       )

@app.route("/share")
def share():
    return render_template("share.html")

# ================================================


@app.route('/adafruit')
def adafruit():

    from vicksbase import firebase as vix
    firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)

    from Adafruit_IO import Client, Data

    aio = Client('imvickykumar999', 'aio_uOXe85j28wfog5Ix3SE8Np0nO4Ke')
    feed = 'ledswitch'

    data = aio.receive(feed).value
    if data == 'ON':
        d=1
    else:
        d=0

    firebase_obj.put('A/B/C','Switch', d)
    result1 = firebase_obj.get('A/B/C/Switch', None)
    data1="{}".format(result1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    else:
        img = 'static/logo/bulboff.jpg'

    return render_template("adafruit.html",
                            data=data1,
                            img = img
                          )

# -------------------------------------------

@app.route('/')
def iotled():

    # from vicksbase import firebase as vix
    # firebase_obj = vix.FirebaseApplication('https://home-automation-336c0-default-rtdb.firebaseio.com/', None)
    # result1 = firebase_obj.get('A/B/C/Switch', None)

    import multivicks.crud as c
    obj = c.vicks('@Hey_Vicks', 'Vicky', 'https://home-automation-336c0-default-rtdb.firebaseio.com/')
    result1 = obj.pull('A/B/C/Switch')
    if result1 == '':
        result1 = None

    data1="{}".format(result1)
    print(data1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    elif data1 == '0':
        img = 'static/logo/bulboff.jpg'
    else:
        img = 'static/logo/error.png'

    return render_template("iotled.html",
                            data=data1,
                            img = img,
                          )


@app.route('/converted_iotled', methods=['POST'])
def converted_iotled():

    import multivicks.crud as c

    credentials = request.form['credentials']
    obj = c.vicks(credentials, 'Vicky', 'https://home-automation-336c0-default-rtdb.firebaseio.com/')

    data = request.form['iotled']
    if data == '':
        data = None
    else:
        data = int(data)
    obj.push(data, 'A/B/C/Switch')

    result1 = obj.pull('A/B/C/Switch')
    data1="{}".format(result1)
    # print(data1)

    if data1 == '1':
        img = 'static/logo/bulbon.jpg'
    elif data1 == '0':
        img = 'static/logo/bulboff.jpg'
    else:
        img = 'static/logo/error.png'

    return render_template("iotled.html",
                            data=data1,
                            img = img,
                          )

# --------------------------------------------

@app.route("/playfair_cipher")
def playfair_cipher():

    data0 = "security, monarchy"
    data1 = "eiioqoyldc, instruments"
    data2 = "stalxlings, gatlmzclrqtx"

    return render_template("playfair_cipher.html",
                            data0=data0,
                            data1=data1,
                            data2=data2
                            )


@app.route('/converted_playfair_cipher', methods=['POST'])
def converted_playfair_cipher():

    from vicks import playfair_cipher as vix
    key = request.form['playfair_cipher_key']
    text = request.form['playfair_cipher_text']
    data = vix.encrypt(key, text)

    return render_template("playfair_cipher.html",
                            data0=key.upper(),
                            data1=data[0],
                            data2=data[1]
                            )

# -------------------------------------------------


@app.route("/qrcode")
def qrcode():
    data = "https://github.com/imvickykumar999/Android-Web-App/blob/main/web2app-master/app/outputs/apk/debug/app-debug.apk"
    img = "static/logo/link.jpeg"
    return render_template("qrcode.html",
                            data=data,
                            img=img)

@app.route('/converted_qrcode', methods=['POST'])
def converted_qrcode():

    data = request.form['qrcode']
    qrcode = QRcode()
    img = qrcode(data, border=10)

    return render_template("qrcode.html",
                            img=img,
                            data=data)

@app.route("/ipynb")
def ipynb():
    return render_template("ipynb.html", infolist = [["Output"]])

@app.route('/converted_ipynb', methods=['POST'])
def convert_ipynb():

    def ipynbinfo(info, file_name):
        def call(file_name):

            if 'http' == file_name[0:4]:
                print('\nPlease WAIT, content is loading from URL...\n')
                su = ur.urlopen(str(file_name)).read().decode('ascii')

            elif '{' == file_name[0]:
                su = file_name

            elif '\\' or '/' in file_name:
                su = open(file_name).read()

            try:
                y = json.loads(str(su))
            except:
                y = su
            return ast.literal_eval(str(y))

        def recdict(d):
            try:
                box.append(d[info])
            except Exception as e:
                pass

            for i in list(d.values()):
                if type(i) == list:
                    for j in i:

                        if type(j) == dict:
                            recdict(j)

                if type(i) == dict:
                    recdict(i)
            return box
        return recdict(call(file_name))

    n, box = 130, []
    file_name = request.form['ipynb']

    if file_name == '':
        file_name = 'https://raw.githubusercontent.com/imvickykumar999/vixtor/master/vixtor.ipynb'

    infolist = ipynbinfo('source', file_name)
    # for i in infolist:
    #     for j in i:
    #         print(j)
    #     print('='*n, end='\n\n')

    return render_template('ipynb.html', infolist = infolist, range = range(40))

@app.route("/morse")
def morse():
    return render_template("morse.html", text = "Output")

@app.route('/converted_morse', methods=['POST'])
def convert_morse():

    decrypted = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6',
                 '7', '8', '9', '0', ',', '?', '(', ')', '!']

    encrypted = ['/', '.-', '-...', '-.-.', '-..', '.', '..-.', '--.',
                 '....', '..', '.---', '-.-', '.-..', '--', '-.', '---',
                 '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--',
                 '-..-', '-.--', '--..', '.----', '..---', '...--', '....-',
                 '.....', '-....', '--...', '---..', '----.', '-----', '--..--',
                 '..--..', '-.--.', '-.--.-', '-.-.--']

    morse_enc = dict(zip(decrypted, encrypted))
    morse_dec = dict([(encrypted, decrypted) for decrypted,
                      encrypted in morse_enc.items()])

    test = request.form['morse']
    # test = input('Enter Morse Code or, Simple Text (or, just Press Ok/Enter for default entry) : ')
    if test == '':
        test = '- .... . / -.. ..- .-. .- - .. --- -. / --- ..-. / .- / -.. .- ... .... / .. ... / - .... .-. . . / - .. -- . ... / - .... . / -.. ..- .-. .- - .. --- -. / --- ..-. / .- / -.. --- - --..-- / . .- -.-. .... / -.. --- - / --- .-. / -.. .- ... .... / .-- .. - .... .. -. / .- / -.-. .... .- .-. .- -.-. - . .-. / .. ... / ..-. --- .-.. .-.. --- .-- . -.. / -... -.-- / .--. . .-. .. --- -.. / --- ..-. / ... .. --. -. .- .-.. / .- -... ... . -. -.-. . --..-- / -.-. .- .-.. .-.. . -.. / .- / ... .--. .- -.-. . --..-- / . --.- ..- .- .-.. / - --- / - .... . / -.. --- - / -.. ..- .-. .- - .. --- -. --..-- / - .... . / .-.. . - - . .-. ... / --- ..-. / .- / .-- --- .-. -.. / .- .-. . / ... . .--. .- .-. .- - . -.. / -... -.-- / .- / ... .--. .- -.-. . / --- ..-. / -.. ..- .-. .- - .. --- -. / . --.- ..- .- .-.. / - --- / - .... .-. . . / -.. --- - ... --..-- / .- -. -.. / - .... . / .-- --- .-. -.. ... / .- .-. . / ... . .--. .- .-. .- - . -.. / -... -.-- / .- / ... .--. .- -.-. . / . --.- ..- .- .-.. / - --- / ... . ...- . -. / -.. --- - ... /'

    test = test.replace("_", "-").upper()
    test_list = test.split(' ')

    decrypt = []
    def convert(j):
        for i in j:
            try:
              decrypt.append((morse_enc[i]))
            except:
              try:
                decrypt.append((morse_dec[i]))
              except:
                pass

    if not any(ele in encrypted for ele in test_list):
        box=[]
        for i in test_list:
            box.append(i+' ')
        test_list = box

        for j in test_list:
            convert(j)
            text = ' '.join(decrypt)
    else:
        convert(test_list)
        text = ''.join(decrypt)

#     pyperclip.copy(text)
#     flash(f'Note: Output of {test} is copied in clipboard !!!')
    return render_template('morse.html', text = text)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    loc='uploads/error.txt'
    if request.method == 'POST':

        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        password = request.form['unique']

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(loc)

                try:
                    loc = enc(loc, password)
                except:
                    try:
                        loc = enc(imf(loc), password)
                    except:
                        pass
        # return render_template('complete.html', aloc=aloc)

#         pyperclip.copy(loc)
        flash(f'Shareable link is https://imvickykumar999.herokuapp.com/{loc}')
        return redirect(f'/{loc}')

# def redirect(loc):
#     return redirect(f'/{loc}')

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)

@app.route('/hacker_vicky')
def hacker_vicky():
    image_names = os.listdir('./uploads')

    from pathlib import Path
    paths = sorted(Path('./uploads').iterdir(),
                        key=os.path.getmtime)

    audio_path = sorted(Path('./uploads/audio').iterdir(),
                        key=os.path.getmtime)
    news_path = sorted(Path('./uploads/news').iterdir(),
                        key=os.path.getmtime)
    video_path = sorted(Path('./uploads/videos').iterdir(),
                        key=os.path.getmtime)

    return render_template("gallery.html",
                            image_names=image_names,
                            audio_path=audio_path,
                            news_path=news_path,
                            video_path=video_path,
                            paths=paths,
                            )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/news', methods=['GET', 'POST'])
def news():
    from gtts import gTTS

    # empty = False
    # if len(os.listdir('uploads/news')) == 0:
    #     empty = True

    try:
        link = 'https://inshorts.com/en/read'
        req = requests.get(link)

        soup = bs(req.content, 'html5lib')
        box = soup.findAll('div', attrs = {'class':'news-card z-depth-1'})

        ha,ia,ba,la,ta = [],[],[],[],[]
        for i in range(10):
            h = box[i].find('span', attrs = {'itemprop':'headline'}).text

            m = box[i].find('div', attrs = {'class':'news-card-image'})
            m = m['style'].split("'")[1]

            b = box[i].find('div', attrs = {'itemprop':'articleBody'}).text
            tts = gTTS(b)

            t = ''.join([i for i in h if i.isalpha()])
            # if empty:
            tts.save(f'uploads/news/{t}.mp3')

            l='link not found'
            try:
                l = box[i].find('a', attrs = {'class':'source'})['href']
            except:
                pass

            ha.append(h)
            ia.append(m)
            ba.append(b)
            la.append(l)
            ta.append(t)

        # try:
        #     entry_id = int(request.args.get('entry_id'))
        #     print(entry_id+1)
        #
        #     import pyttsx3
        #     engine = pyttsx3.init()
        #
        #     rate = engine.getProperty('rate')
        #     engine.setProperty('rate', 150)
        #
        #     voices = engine.getProperty('voices')
        #     engine.setProperty('voice', voices[1].id)
        #
        #     engine.say(f"{ba[entry_id]}")
        #     engine.runAndWait()
        #
        # except:
        #     print('passed...')
        #     pass

        return render_template('news.html',
                                ha=ha,
                                ia=ia,
                                ba=ba,
                                la=la,
                                ta=ta,
                                range_ha = range(10),
                                )
    except Exception as e:
        print(e)
        return render_template('404.html')

@app.route('/uploads/news/<filename>')
def send_news(filename):
    return send_from_directory("uploads/news", filename)

@app.errorhandler(404)
def page_not_found(e):
    try:
        # import shutil
        # shutil.rmtree('uploads/videos')
        os.mkdir('uploads/videos')
    except:
        pass
    return render_template('404.html'), 404

@app.route('/chat')
def chat():
    rooms = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
    return render_template("chat.html", rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    message = 'Welcome to Vicks Chat Room'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('news'))


@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for('view_room', room_id=room_id))
        else:
            message = "Failed to create room"
    return render_template('create_room.html', message=message)


@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room edited successfully'
            room_members_str = ",".join(new_members)
        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)


# from app import app
# from livereload import Server
#
# if __name__ == '__main__':
#     server = Server(app.wsgi_app)
#     server.serve(debug=True)
