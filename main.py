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
from kivy.core.window import Window
from kivy.utils import platform

from android_permissions import AndroidPermissions

from app_layout.homescreen0 import HomeScreen0
from app_layout.photoscreen1 import PhotoScreen1
from app_layout.acceptancescreen2 import AcceptanceScreen2
from app_layout.filterscreen3 import FilterScreen3
from app_layout.detailsscreen4 import DetailsScreen4

from excel_packer.excel_packer import ExcelPacker

from database_layer import database_brain as dbrain

import os
import json
import threading
from gen_ai.ai import Ai
from datetime import date
import random


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse, disable_multitouch')


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
                        FilterScreen3(name='screen3', controller=self),
                        DetailsScreen4(name='screen4', controller=self)]
        for s in self.screens:
            self.sm.add_widget(s)
        self.sm.current = 'screen3'
        return self.sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None

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

    def swap_detailsscreen4(self):
        if self.sm.current_screen.name == "screen0":
            self.sm.transition = MDSharedAxisTransition()
            self.sm.transition.transition_axis = "x"
            self.sm.transition.duration = 0.2
            self.sm.current = str(f'screen4')
        elif self.sm.current_screen.name == "screen4":
            self.sm.transition = MDSharedAxisTransition()
            self.sm.transition.transition_axis = "x"
            self.sm.transition.opposite = True
            self.sm.transition.duration = 0.2
            self.sm.current = str(f'screen0')

    def show_detailsscreen4(self, details_info):
        self.screens[4].details = details_info
        self.swap_detailsscreen4()

    def homescreen0_apply_filters(self, doc_type, filters):
        self.screens[0].apply_filters(doc_type, filters)
        self.swap_filtersscreen3()

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