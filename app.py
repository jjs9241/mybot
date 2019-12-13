#일반적으로 Flask에서는 app.py를 메인으로 사용한다.

from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = f'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')

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

#@app.route('/telegram',method=['POST'])
#def telegram():
    #return 'ok'

if __name__ == '__main__':
    app.run(debug=True)