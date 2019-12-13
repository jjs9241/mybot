#일반적으로 Flask에서는 app.py를 메인으로 사용한다.

from flask import Flask, escape, request, render_template
from decouple import config
import requests
import html

app = Flask(__name__)

api_url = f'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')
goole_key = config('GOOGLE_KEY')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!' #escape는 코드를 집어 넣었을 때 처리해주기 위해서 사용한다.

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    user_input = request.args.get('user_input')
    get_user_api = f'{api_url}{token}/getUpdates'

    res = requests.get(get_user_api).json()
    user_id = res['result'][0]['message']['from']['id']

    method = '/sendMessage'
    appended = f'?text={user_input}&chat_id={user_id}'
    print(api_url + token + method + appended)
    res = requests.get(api_url + token + method + appended).json()
    print(res)
    return render_template('send.html')

@app.route('/telegram',methods=['POST'])
def telegram():
    req = request.get_json()
    print(req)
    user_id = req['message']['from']['id'] 
    user_input = req['message']['text']
    method = '/sendMessage'
    appended = f'?text={user_input}&chat_id={user_id}'
    
    if user_input == '로또':
        return_data = '로또를 입력하셨습니다.'
        appended = f'?text={return_data}&chat_id={user_id}'
    elif user_input[0:3] == '번역 ':
        google_api_url = 'https://translation.googleapis.com/language/translate/v2'
        before_text = user_input[3:]

        data = {
            'q': before_text,
            'source':'ko',
            'target':'en',
        }
        request_url = f'{google_api_url}?key={goole_key}'

        req = requests.post(request_url, data).json()
        print(req)
        return_data = html.unescape(req['data']['translations'][0]['translatedText'])
        print(return_data)
        appended = f'?text={return_data}&chat_id={user_id}'
    else:
        return_data = '무슨 말인지 모르겠어요. ㅠㅠ'
        appended = f'?text={return_data}&chat_id={user_id}'

    res = requests.get(api_url + token + method + appended).json()
    print(res)
    

    return 'ok', 200 # 200을 텔레그램 서버에 보내지 않으면 텔레그램 서버는 요청을 계속 보내도록 되어 있다.

if __name__ == '__main__':
    app.run(debug=True)