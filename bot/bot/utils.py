def send(bot, chat_id, text, reply_markup=None):
    return bot.send_message(chat_id, text, parse_mode='Html',
                            reply_markup=reply_markup)


def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
