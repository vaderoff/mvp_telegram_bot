from telebot import types

from .api import User
from .bot import bot


class StateMachine:
    def __init__(self, bot):
        self._bot = bot
        self.states = {}
        self.patterns = {}
        self._bot.message_handler(
            content_types=['text', 'contact'])(self.handler)
        self._bot.callback_query_handler(func=lambda call: True)(self.handler)

    def reg_state(self, _class):
        '''
        use this function as decorator
        using for adding state classes to self.states
        '''
        self.states.update({_class.state_id: _class})
        if _class.pattern:
            self.patterns.update({_class.pattern: _class})
        return _class

    def handler(self, event):
        '''
        main method in this class :)
        handle events by state from telebot handlers
        '''
        tg_id = event.from_user.id

        user = User.find(tg_id)
        if not user:
            user = User.create(tg_id, event.from_user.first_name)

        pattern_triggered = False
        if isinstance(event, types.Message):
            # handle text patterns
            for pattern, state in self.patterns.items():
                if pattern[-1] == '.':
                    if event.text.startswith(pattern[:-1]):
                        pattern_triggered = True
                        new_state = state
                else:
                    if event.text == pattern:
                        pattern_triggered = True
                        new_state = state

        if not pattern_triggered:
            if self.states.get(user.state):
                # handle event by previous state and get next state
                new_state = self.states[user.state].handle(
                    self._bot, event, user)
            else:
                # get first state
                new_state = self.states[1]

        if new_state:
            # run and save new state
            user.state = new_state.state_id
            new_state.ask(self._bot, event, user)

    def run_next_state(self, user):
        '''
        function to run next state without handle event
        using in router.py
        '''
        current_state = self.states.get(user.state)
        if current_state and current_state.next_state:
            new_state = current_state.next_state
            user.state = new_state.state_id
            new_state.ask(self._bot, None, user)


machine = StateMachine(bot)
