from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition

from app_layout.homescreen0  import HomeScreen0
from app_layout.photoscreen1 import PhotoScreen1


class MyApp(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        self.sm = MDScreenManager()
        self.screens = [HomeScreen0(name='screen0'), PhotoScreen1(name='screen1')]

        for s in self.screens:
            self.sm.add_widget(s)

        return self.sm

    def on_start(self):
        print(self.sm.current)

    def swap_to_photoscreen1(self):
        # transition settings
        self.sm.transition = MDSharedAxisTransition()
        self.sm.transition.transition_axis = "y"
        self.sm.transition.duration = 0.2
        self.sm.current = str(f'screen1')

    def back_to_homescreen0(self):
        self.sm.current = 'screen0'

MyApp().run()