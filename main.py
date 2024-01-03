from kivy.app import App

from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
# == == == == == == == == == == == == == == ==
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex
'''-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-'''
from pygments.lexers import RustLexer
from pygments.lexers import CppLexer
from pygments.lexers import PythonLexer
from pygments.lexers import CLexer
from pygments.lexers import BashLexer

from functools import partial
import time
import subprocess
import os
'''
    File manager - свой файловый менеджер, другого я не нашёл( Или они были не совсем то что мне надо
'''
#-=-=-=-=-=-=-=-=-=-#
language = CLexer()
text_x = 0
file = None
untitled = "untitled.c"
terminal = None
code = 1
#-=-=-=-=-=-=-=-=-=-#
class File_Manager(BoxLayout):
    def open_file(self, x):
        global untitled
        global code
        self.i = x
        untitled = self.i.text
        with open(self.i.text,  "r", encoding='utf-8') as f:
            code = f.read()
    orientation = 'vertical'
    def list(self):
        image_n = ['jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'ico', 'jpg', 'ttf']
        nam = os.getcwd()
        list = os.listdir()
        file_manager_screen = ModalView(auto_dismiss=True, size_hint=(0.5, 0.5), )
        box_file = BoxLayout(orientation='vertical')
        for i in list:
            x = i.split('.')
            if x[1] in image_n:
                pass
            else:
                self.i = Button(text=f'{i}', background_color=(25/255, 25/255, 25/255))
                self.i.bind(on_press=partial(File_Manager.open_file, self.i))
                box_file.add_widget(self.i)
        file_manager_screen.add_widget(box_file)
        file_manager_screen.open()

''' Main class for Xrom code editor '''

class Xrom(App):
    def build(self):
        #Window.borderless = True
        # Window.window_icon = 'icon_test.jpg' --- Не по ня тно
        self.title = 'Xrom'
        self.icon = 'xrom.ico'
        #Window.border_color = get_color_from_hex('#000000')
        return Builder.load_file('style.kv')
    def on_start(self):
        global language
        global text_x
        global code
        self.code = CodeInput(text=str(code), lexer=language, font_size=20, size_hint=(1, 0.95),
                         background_color=(13/255, 19/255, 31/255),
                         foreground_color=(182 / 255, 189 / 255, 204 / 255))
        if text_x == 0 and code == 1:
            self.code.text = ('#include <stdio.h> \nint main(){ \n  printf("hello bro");\n  return 0; \n}')
        else:
            self.root.ids.main.remove_widget(self.code)
        self.root.ids.main.add_widget(self.code)
    def language_or(self):
        def user_lang(x):
            global language
            global text_x
            if x == 'Python':
                language = PythonLexer()
                text_x = 1
                Xrom.on_start(self)
            elif x == 'C':
                language = CLexer()
                text_x = 2
                Xrom.on_start(self)
            elif x == 'C++':
                language = CppLexer()
                text_x = 3
                Xrom.on_start(self)
            elif x == 'Rust':
                language = RustLexer()
                text_x = 4
                Xrom.on_start(self)
            else:
                pass
        win = ModalView(auto_dismiss=True, size_hint=(0.34, 0.4), pos_hint={'x': 0.33, 'y': .6})
        pyth = Button(text='Python', background_color=(25/255, 25/255, 25/255))
        c = Button(text='C', background_color=(25/255, 25/255, 25/255))
        cpp = Button(text='C++', background_color=(25/255, 25/255, 25/255))
        rust = Button(text='Rust', background_color=(25/255, 25/255, 25/255))
        box_lang = BoxLayout(orientation='vertical')
        win.add_widget(box_lang)
        box_lang.add_widget(pyth)
        box_lang.add_widget(c)
        box_lang.add_widget(cpp)
        box_lang.add_widget(rust)
        pyth.bind(on_press=lambda x: user_lang(pyth.text))
        c.bind(on_press=lambda x: user_lang(c.text))
        cpp.bind(on_press=lambda x: user_lang(cpp.text))
        rust.bind(on_press=lambda x: user_lang(rust.text))
        win.open()
    def new_file(self):
        global code
        code = ''
        self.code.text = ''
        self.on_start()
    def file_open_setting(self):
        box = BoxLayout(orientation='vertical')
        back = Button(text='Exit', background_color=(25/255, 25/255, 25/255))
        open_f = Button(text='Open file', background_color=(25/255, 25/255, 25/255))
        new_f = Button(text='New file', background_color=(25/255, 25/255, 25/255))
        view = ModalView(auto_dismiss=True, size_hint=(0.34, 0.4), pos_hint={'x': 0.0, 'y': .6})
        view.add_widget(box)
        box.add_widget(new_f)
        box.add_widget(open_f)
        box.add_widget(back)
        view.open()
        def exit_t(self):
            Xrom().stop()

        back.bind(on_press=exit_t)
        new_f.bind(on_press=lambda x: self.new_file())
        open_f.bind(on_press=File_Manager.list)
    def save_file(self):
        global untitled
        def save_fail_full():
            name_file = self.name_f.text
            code_file = self.code.text
            with open(name_file, 'w') as f:
                f.write(code_file)
        if text_x == 1 and untitled == "untitled":
            untitled = "untitled.py"
        elif text_x == 2 and untitled == "untitled":
            untitled = "untitled.c"
        elif text_x == 3 and untitled == "untitled":
            untitled = "untitled.cpp"
        elif text_x == 4 and untitled == "untitled":
            untitled = "untitled.rs"
        else:
            pass
        win_t = ModalView(auto_dismiss=True, size_hint=(0.34, 0.2), background_color=(25/255, 25/255, 25/255))
        box = BoxLayout(orientation='vertical')
        self.name_f = TextInput(text=str(untitled), background_color=(25/255, 25/255, 25/255), font_size=30, foreground_color=(1, 1, 1, 1), multiline=False)
        but = Button(text="Save", background_color=(25/255, 25/255, 25/255), font_size=24)
        box.add_widget(self.name_f)
        box.add_widget(but)
        win_t.add_widget(box)
        win_t.open()
        but.bind(on_press=lambda x: save_fail_full())

    def terminal_open(self):
        def terminal_clear():
            self.terminal_input.text = ''
        def terminal_function():
            command = self.terminal_input.text
            output_command = subprocess.run(command, shell=True, capture_output=True, text=True)
            if output_command.returncode == 0:
                output_command = output_command.stdout
                self.terminal_input.text = str(output_command)
            else:
                terminal_clear()
        '''
            Start function
        '''
        global untitled
        global terminal
        terminal_win = ModalView(auto_dismiss=True, size_hint=(1, 0.3), pos_hint={'x': .0, 'y': .0})
        box_term = BoxLayout(orientation='vertical')
        self.terminal_input = CodeInput(lexer=BashLexer(), background_color=(25/255, 25/255, 25/255), font_size=(20),foreground_color=(1, 1, 1, 1), multiline=False)
        box_term.add_widget(self.terminal_input)
        terminal_win.add_widget(box_term)
        terminal_win.open()
        self.terminal_input.bind(on_text_validate=lambda x: terminal_function())
    def start_build(self):
        global text_x
        self.terminal_open()
        try:
            name_o = self.name_f.text.split('.')
            name_o = name_o[0]
            if text_x == 1:
                self.terminal_input.text = f"python {self.name_f.text}"
            elif text_x == 2 or text_x == 0:
                self.terminal_input.text = f"gcc -o {name_o} {self.name_f.text} && {name_o}"
            elif text_x == 3:
                self.terminal_input.text = f"gpp -o {name_o} {self.name_f.text} && {name_o}"
            elif text_x == 4:
                self.terminal_input.text = f"rustc {self.name_f.text} && {name_o}"
            else:
                error = Popup(title='Error compilation or interpreter', content=Label(text='No, please reboot compilation||interpreter'),
                              auto_dismiss=True, size_hint=(0.3, 0.4))
                error.open()
        except:
            error = Popup(title='Save fail, please <3',
                          content=Label(text='Save fail'),
                          auto_dismiss=True, size_hint=(0.3, 0.4))
            error.open()
    def save_fail_window(self):
        def clear_code():
            global code
            code = ' '
            self.on_start()
        box_save = BoxLayout(orientation='vertical')
        save = Button(text='Save', background_color=(25/255, 25/255, 25/255))
        save_as = Button(text='Save AS', background_color=(25/255, 25/255, 25/255))
        build = Button(text='Build', background_color=(25/255, 25/255, 25/255))
        custom_build = Button(text='Custom build', background_color=(25 / 255, 25 / 255, 25 / 255))
        terminal_but = Button(text='Terminal', background_color=(25 / 255, 25 / 255, 25 / 255))
        clear_but = Button(text='Clear', background_color=(25 / 255, 25 / 255, 25 / 255))
        win_save = ModalView(auto_dismiss=True, size_hint=(0.34, 0.4), pos_hint={'x': 0.66, 'y': .6})
        win_save.add_widget(box_save)
        box_save.add_widget(save)
        box_save.add_widget(save_as)
        box_save.add_widget(build)
        box_save.add_widget(custom_build)
        box_save.add_widget(terminal_but)
        box_save.add_widget(clear_but)
        win_save.open()
        clear_but.bind(on_press=lambda x: clear_code())
        terminal_but.bind(on_press=lambda x: self.terminal_open())
        save.bind(on_press=lambda x: Xrom.save_file(self))
        build.bind(on_press=lambda x: self.start_build())
if __name__ == '__main__':
    Xrom().run()
