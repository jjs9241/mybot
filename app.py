#일반적으로 Flask에서는 app.py를 메인으로 사용한다.

from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!' #escape는 코드를 집어 넣었을 때 처리해주기 위해서 사용한다.

if __name__ == '__main__':
    app.run(debug=True)