from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import sqlite3
import datetime

Window.clearcolor = (0, 0, 0, 1)

DB_NAME = "mbele_life_ultimate.db"
DEFAULT_PIN = "2540"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, product_name TEXT, amount REAL, date TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS targets (id INTEGER PRIMARY KEY, target_amount REAL)''')
    if c.execute("SELECT COUNT(*) FROM targets").fetchone()[0] == 0:
        c.execute("INSERT INTO targets (target_amount) VALUES (1000.0)")
    conn.commit()
    conn.close()

class PinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        layout.add_widget(Label(text='🇰🇪 MBELE LIFE', font_size=32))
        layout.add_widget(Label(text='Enter Access PIN', font_size=22))
        self.pin_input = TextInput(password=True, multiline=False, font_size=28)
        layout.add_widget(self.pin_input)
        btn = Button(text='UNLOCK', font_size=20, background_color=(0.6,0,0,1))
        btn.bind(on_press=self.check_pin)
        layout.add_widget(btn)
        self.add_widget(layout)

    def check_pin(self, instance):
        if self.pin_input.text == DEFAULT_PIN:
            self.manager.current = 'main'
        else:
            self.pin_input.text = ''
            self.pin_input.hint_text = 'Wrong PIN! Try 2540'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text='🇰🇪 MBELE LIFE', font_size=26))
        for text in ["UUZA - Sell Products", "REPORTS", "HISTORIA", "STOCK - Add Product"]:
            btn = Button(text=text, font_size=18, background_color=(0.6,0,0,1))
            layout.add_widget(btn)
        self.add_widget(layout)

class MbeleLife(App):
    def build(self):
        init_db()
        sm = ScreenManager()
        sm.add_widget(PinScreen(name='pin'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    MbeleLife().run()
