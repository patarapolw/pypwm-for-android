from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import kivy
try:
    import androidhelper
except ImportError:
    pass

from pwm.vault import Vault
from randomsentence.sentence import SentenceTool
import re
import pickle

sentence_tool = SentenceTool()


class PasswordViewerSub(BoxLayout):
    viewerKey = ''
    viewerValue = ''

    def __init__(self, key, value):
        super().__init__()
        self.viewerKey = key
        self.viewerValue = value


class PasswordChoiceButton(Button):
    pass


class ScreenManagement(ScreenManager):
    vault = None
    password_generator = None
    current_password_dict = None
    current_name = None
    if kivy.platform == 'android':
        droid = androidhelper.Android()
    else:
        droid = None

    def do_login(self, master_password):
        if self.password_generator is None:
            with open('generate_password.pkl', 'rb') as f:
                self.password_generator = pickle.load(f)

        try:
            self.vault = Vault(master_password)
            self.current = 'passwordShowcaseScreen'
            for k, v in dict(self.vault).items():
                text = k + '\n' + v.get('note', '')
                btn = PasswordChoiceButton(text=text)
                self.ids.showcaseLayout.add_widget(btn)
        except ValueError:
            if self.droid is not None:
                self.droid.makeToast('Wrong password')

    def view_password(self, name):
        if hasattr(self.vault, 'data'):
            self.current = 'passwordScreen'
            if name not in dict(self.vault).keys():
                password, token = self.password_generator.new_common_diceware_password(hint=name)
                self.vault[name] = {
                    'password': password,
                    'note': render_tokens(token)
                }
            for k, v in self.vault[name].items():
                pvs = PasswordViewerSub(k, v)
                self.ids.passwordScreenLayout.add_widget(pvs)
            self.current_password_dict = self.vault[name]
            self.current_name = name
        else:
            self.current = 'loginScreen'

    def new_password(self, new_name):
        self.view_password(new_name)

    def update_password(self, new_k, new_v):
        if hasattr(self.vault, 'data'):
            self.current_password_dict[new_k] = new_v
            self.vault[self.current_name] = self.current_password_dict
            self.current = 'passwordShowcaseScreen'
        else:
            self.current = 'loginScreen'


class MainApp(App):
    def build(self):
        return ScreenManagement()


def main():
    MainApp().run()


def render_tokens(tagged_tokens):
    def boldify(match_obj):
        to_consider = match_obj.group(0)
        if to_consider.lower() == token.lower():
            return '[{}]'.format(to_consider)
        else:
            return to_consider

    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in sorted(tagged_tokens, key=len):
        if is_overlap:
            sentence = re.sub('(\w+)', boldify, sentence)

    return sentence


if __name__ == '__main__':
    main()
