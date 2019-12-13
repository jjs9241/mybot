from decouple import config

#웹훅설정을 위한 경로
token = config('TELEGRAM_BOT_TOKEN')
#ngrok_url = 'https://4cf338a5.ngrok.io/telegram'
ngrok_url = 'https://jjs9341.pythonanywhere.com/telegram'

#내가 연결하려는 주소
url = f'https://api.telegram.org/bot{token}/setWebhook'

#실행 주소
setwebhook_url = f'{url}?url={ngrok_url}'

print(setwebhook_url)