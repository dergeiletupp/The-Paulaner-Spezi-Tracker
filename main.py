from kivy.lang import Builder
Builder.load_file("tracker.kv")
import kivy
from kivy.app import App
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import json
import os
from datetime import datetime, date

DATA_FILE = "data.json"

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_logs(logs):
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f)

class Tracker(BoxLayout):
    logs = ListProperty([])
    today_count = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_data()

    def add_spezi(self):
        now = datetime.now().isoformat()
        self.logs.append(now)
        save_logs(self.logs)
        self.update_today_count()
        self.update_log_display()

    def load_data(self):
        self.logs = load_logs()
        self.update_today_count()
        self.update_log_display()

    def update_today_count(self):
        today = date.today().isoformat()
        self.today_count = sum(log.startswith(today) for log in self.logs)

    def update_log_display(self):
        grid = self.ids.get("log_grid")
        if grid is not None:
            grid.clear_widgets()
            for log in reversed(self.logs):
                label = Label(
                    text=log.replace("T", " ")[:19],
                    font_size=16,
                    color=(.30, .22, .14, 1),
                    size_hint_y=None,
                    height=25,
                    halign="left",
                    valign="middle",
                )
                label.text_size = (grid.width - 10, None)
                grid.add_widget(label)

class SpeziApp(App):
    def build(self):
        return Tracker()

if __name__ == "__main__":
    SpeziApp().run()
