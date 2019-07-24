import telebot
from flask import Flask, json, request, abort

from .api import User
from .states import machine
from .utils import send

app = Flask(__name__)


@app.route('/bot/telegram', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        machine._bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@app.route('/bot/sendMessage', methods=['POST'])
def send_message():
    if request.headers.get('content-type') == 'application/json':
        data = request.json
        if data.get('telegram_id') and data.get('text'):
            resp = {'ok': True}
            send(machine._bot, data['telegram_id'],
                 data['text'], reply_markup=data.get('markup'))
            if data.get('next_state') and data['next_state']:
                user = User.find(data['telegram_id'])
                user._allow_update = False
                machine.run_next_state(user)
                resp['data'] = user.data
            return app.response_class(
                response=json.dumps(
                    resp),
                status=200,
                mimetype='application/json'
            )
        return app.response_class(
            response=json.dumps(
                {'ok': False, 'messasge': 'missing parameters'}),
            status=400,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response=json.dumps(
                {'ok': False, 'messasge': 'Invalid Content-Type'}),
            status=403,
            mimetype='application/json'
        )
