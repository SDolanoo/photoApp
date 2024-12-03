"""
IF PROBLEMS WITH CAMERA LOOK TO
".VENV/LIB/CAMERA4KIVY/BASED_ON_KIVY_CORE/CAMERA/CAMERA_OPENCV":
LINE 21:
DELETE 0 AND UNCOMMENT COMMENT
"""
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition
from kivy.clock import mainthread

from app_layout.homescreen0 import HomeScreen0
from app_layout.photoscreen1 import PhotoScreen1
from app_layout.acceptancescreen2 import AcceptanceScreen2
from app_layout.filterscreen3 import FilterScreen3

from excel_packer.excel_packer import ExcelPacker

from database_layer import database_brain as dbrain

import os
import json
import threading
from gen_ai.ai import Ai


class MyApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"


        self.image_path = 'paragon_3.jpg'
        self.ai = Ai()
        self.ep = ExcelPacker()

        self.sm = MDScreenManager()
        self.screens = [HomeScreen0(name='screen0', controller=self),
                        PhotoScreen1(name='screen1', controller=self),
                        AcceptanceScreen2(name='screen2', controller=self, path=self.image_path),
                        FilterScreen3(name='screen3', controller=self)]
        for s in self.screens:
            self.sm.add_widget(s)
        self.sm.current = 'screen3'
        return self.sm

    def on_start(self):
        print(self.sm.current_screen.name)

    def show_acceptancescreen2(self, path):
        self.image_path = path
        self.sm.current = 'screen2'

    def back_from_acceptancescreen2(self):
        self.sm.current = str(f'screen1')

    def swap_to_photoscreen1(self):
        # transition settings
        self.sm.transition = MDSharedAxisTransition()
        self.sm.transition.transition_axis = "y"
        self.sm.transition.duration = 0.2
        self.sm.current = str(f'screen1')

    def swap_filtersscreen3(self):
        if self.sm.current_screen.name == "screen0":
            self.sm.transition = MDSharedAxisTransition()
            self.sm.transition.transition_axis = "x"
            self.sm.transition.duration = 0.2
            self.sm.current = str(f'screen3')
        elif self.sm.current_screen.name == "screen3":
            self.sm.transition = MDSharedAxisTransition()
            self.sm.transition.transition_axis = "x"
            self.sm.transition.opposite = True
            self.sm.transition.duration = 0.2
            self.sm.current = str(f'screen0')

    def back_to_homescreen0(self):
        self.sm.current = 'screen0'

    def delete_files(self):
        files = [f for f in os.listdir('Photos')]
        for f in files:
            if os.path.isfile(f'Photos/{f}'):
                os.remove(f"Photos/{f}")


    def get_prompt(self) -> list:
        # ai = Ai(path=self.parent.ids.image.source)
        self.ai.image_path = self.image_path
        data_for_dialog = self.ai.ai_recipe_prompt()
        return data_for_dialog

    def to_excel(self, desired_list: list):
        self.ep.pack_to_excel(desired_list=desired_list)


MyApp().run()