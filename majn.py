from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from app_layout.homescreen0  import HomeScreen0

class MyApp(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        self.sm = MDScreenManager()
        self.screens = [HomeScreen0(name="0")]

        for s in self.screens:
            self.sm.add_widget(s)

        return self.sm



MyApp().run()