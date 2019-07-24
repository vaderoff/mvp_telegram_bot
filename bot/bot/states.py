import re
from enum import IntEnum, auto

from telebot import types

from .state_machine import machine
from .utils import send, is_int
from .api import send_sms_code, accept_sms_code, Dialogue


class StatesEnum(IntEnum):
    AGE_CONFIRMATION = auto()
    ENTER_PHONE = auto()
    ENTER_SMS_CODE = auto()
    DIALOGUE_STATE = auto()
    WAIT_STATE = auto()


class BaseState:
    state_id = None
    pattern = None
    next_state = None

    @staticmethod
    def ask(bot, event, user):
        pass

    @staticmethod
    def handle(bot, event, user):
        '''
        handle event
        and return next state
        '''
        return None


@machine.reg_state
class AgeConfirmation(BaseState):
    state_id = StatesEnum.AGE_CONFIRMATION
    pattern = '/start'

    @staticmethod
    def ask(bot, event, user):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                'Да, подтверждаю', callback_data='confirm')
        )
        send(bot, user.telegram_id,
             'Добрый день, пожалуйста, подтвердите, что вам исполнилось 18 лет и вы являетесь потребителем табака',
             reply_markup=markup)

    @staticmethod
    def handle(bot, event, user):
        if isinstance(event, types.CallbackQuery) and event.data == 'confirm':
            user.age_confirmed = True
            return EnterPhone


@machine.reg_state
class EnterPhone(BaseState):
    state_id = StatesEnum.ENTER_PHONE

    @staticmethod
    def ask(bot, event, user):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton(
                'Поделиться номером телефона', request_contact=True)
        )
        send(bot, user.telegram_id,
             'Пожалуйста, укажите ваш номер телефона который, вы указали при регистрации в программе лояльности:\n<code>+7 xxx xxx xx xx</code>',
             reply_markup=markup
             )

    @staticmethod
    def handle(bot, event, user):
        if event.contact:
            phone = event.contact.phone_number
        else:
            if re.match(r'^((\+7|7|8)+([0-9]){10})$', event.text):
                phone = event.text
            else:
                send(bot, user.telegram_id,
                     'Пожалуйста введите номер в формате: <code>+7 XXX XXX XX XX</code>')
                return
        user.phone = phone
        send(bot, user.telegram_id, 'Номер сохранен',
             reply_markup=types.ReplyKeyboardRemove())
        return EnterSmsCode


@machine.reg_state
class EnterSmsCode(BaseState):
    state_id = StatesEnum.ENTER_SMS_CODE

    @staticmethod
    def ask(bot, event, user):
        # send code to user
        send_sms_code(user.telegram_id)

        send(bot, user.telegram_id,
             'Пожалуйста, введите код, отправленный вам в SMS на номер: <b>{}</b>'.format(user.phone))

    @staticmethod
    def handle(bot, event, user):
        if is_int(event.text):
            if accept_sms_code(user.id, event.text):
                user.phone_confirmed = True
                send(bot, user.telegram_id, 'Ваш номер был подтвержден, спасибо!')
                return WaitState
            else:
                send(bot, user.telegram_id, 'Неверный код, попробуйте еще раз')


@machine.reg_state
class DialogueState(BaseState):
    state_id = StatesEnum.DIALOGUE_STATE

    @staticmethod
    def ask(bot, event, user):
        send(bot, user.telegram_id, 'Привет, давай пообщаемся')

    @staticmethod
    def handle(bot, event, user):
        dialogue = Dialogue.find(user.telegram_id)
        if not dialogue:
            dialogue = Dialogue.create(user.telegram_id)
        dialogue.new_message(event.text)


@machine.reg_state
class WaitState(BaseState):
    state_id = StatesEnum.WAIT_STATE
    next_state = DialogueState

    @staticmethod
    def ask(bot, event, user):
        send(bot, user.telegram_id,
             'Ожидайте пока менеджер проверит вас на участие в программе лояльности')

    @staticmethod
    def handle(bot, event, user):
        pass
