"""
IF PROBLEMS WITH CAMERA LOOK TO
".VENV/LIB/CAMERA4KIVY/BASED_ON_KIVY_CORE/CAMERA/CAMERA_OPENCV":
LINE 21:
DELETE 0 AND UNCOMMENT COMMENT
"""
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition

from app_layout.homescreen0 import HomeScreen0
from app_layout.photoscreen1 import PhotoScreen1
from app_layout.acceptancescreen2 import AcceptanceScreen2

import os
from gen_ai.ai import Ai


class MyApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        self.path = 'paragon_1.jpg'

        self.sm = MDScreenManager()
        self.screens = [HomeScreen0(name='screen0', controller=self),
                        PhotoScreen1(name='screen1', controller=self),
                        AcceptanceScreen2(name='screen2', controller=self, path=self.path)] #HomeScreen0(name='screen0'), PhotoScreen1(name='screen1'),

        for s in self.screens:
            self.sm.add_widget(s)

        return self.sm

    def show_acceptancescreen2(self, path):
        self.path = path
        self.sm.current = 'screen2'

    def back_from_acceptancescreen2(self):
        self.sm.current = str(f'screen1')

    def swap_to_photoscreen1(self):
        # transition settings
        self.sm.transition = MDSharedAxisTransition()
        self.sm.transition.transition_axis = "y"
        self.sm.transition.duration = 0.2
        self.sm.current = str(f'screen1')

    def back_to_homescreen0(self):
        self.sm.current = 'screen0'

    def delete_files(self):
        files = [f for f in os.listdir('Photos')]
        for f in files:
            if os.path.isfile(f'Photos/{f}'):
                os.remove(f"Photos/{f}")


MyApp().run()