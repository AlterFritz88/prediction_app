import json
import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.toast import toast


class PredictionApp(MDApp):

    def build(self):
        return Builder.load_file('ui_main.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request_android_permissions()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.host = ""
        self.status = "Disconnected"


    @staticmethod
    def is_android():
        return platform == 'android'

    def _request_android_permissions(self):
        """Запрос разрешения доступа к камере, если приложение работает на android"""
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)

    def try_connetion(self):
        self.host = self.root.ids.ip.text
        data = {"check": "check"}
        data_json = json.dumps(data)
        try:
            r = requests.get(url=self.host + "/api/check", data=data_json, timeout=1)
            answer = json.loads(r.content)['answer']
            if answer == "ok":
                toast("Подключение установлено")
                self.status = "Connected"
                self.root.ids.ip.predict_button.disabled = False
                self.root.ids.ip.predict_button.md_bg_color: (0, 0.5, 0, 0.5)
            else:
                toast("Ошибка подкючения, попробуйте другой ip")
        except requests.exceptions.ConnectionError:
            toast("Ошибка подкючения, попробуйте другой ip")
            return 0

    def predict(self):
        self.root.ids.camera.export_to_png("test.png")
        files = {'file': ('test.png', open('test.png', 'rb'))}
        r = requests.post(self.host + "/api/predict_photo", files=files)
        answer = json.loads(r.content)['answer']


if __name__ == '__main__':
    Window.softinput_mode = "below_target"
    PredictionApp().run()