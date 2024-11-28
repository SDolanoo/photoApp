from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
   MDDialogButtonContainer,
   MDDialogSupportingText,
    )

import os
from functools import partial

from app_layout.just_screen import JustScreen
from database_layer import database_brain as dbrain



AS2 = """
<AcceptanceScreen2>:
    name: "screen2"
    pp: acceptance_layout_2.ids.image
    AcceptanceLayout2:
        id: acceptance_layout_2
        
    MDCircularProgressIndicator:
        id: progress
        determinate: True
        active: False
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .5, 'center_y': .5}
"""


class AcceptanceScreen2(JustScreen):
    pp = ObjectProperty(None)

    def __init__(self, controller, path, **args):
        Builder.load_string(AS2)
        super().__init__()
        self.pp.source = f"{path}"
        self.controller = controller

    def on_pre_enter(self, *args):
        self.pp.source = self.controller.image_path
        self.stop_waiting_animation()

    def start_waiting_animation(self):
        self.ids.progress.active = True

    def stop_waiting_animation(self):
        self.ids.progress.active = False



AL2 = """
<AcceptanceLayout2>:
    Image:
        id: image
        size: self.width, self.height
        allow_stretch: True
        keep_ratio:False
    ButtonsLayout2:
        id: buttons
        
    # MDButton:
    #     id: xxx
    #     text: "start"
    #     on_release: root.xxx()
    #     pos_hint: {"center_x": .2, "center_y": .5}
    # MDButton:
    #     id: ddd
    #     text: "stop"
    #     on_release: root.ddd()
    #     pos_hint: {"center_x": .8, "center_y": .5}
"""


class AcceptanceLayout2(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(AL2)
        super().__init__()

BL2 = """
<ButtonsLayout2>:
    MDButton:
        id: retry
        style: "text"
        
        theme_bg_color: "Custom"
        md_bg_color: [0, 0, 0, 0.3]
        radius: [dp(0), dp(0), dp(0), dp(0)]
        
        on_release: root.retry()
        pos_hint: {'center_x':.25,'center_y':.1}
        theme_width: "Custom"
        theme_height: "Custom"
        size_hint_y: .2
        size_hint_x: .5
        MDButtonText:
            text: "Retry"
            theme_text_color: "Custom"
            text_color: "white"
            pos_hint: {"center_x": .5, "center_y": .5}
            
        
    MDButton:
        id:other
        style: "text"
        
        theme_bg_color: "Custom"
        md_bg_color: [0, 0, 0, 0.3]
        radius: [dp(0), dp(0), dp(0), dp(0)]
        
        on_release: root.ok()
        pos_hint: {'center_x':.75,'center_y':.1}
        # parent width = 800
        theme_width: "Custom"
        theme_height: "Custom"
        size_hint_y: .2
        size_hint_x: .5
        MDButtonText:
            text: "Ok"
            theme_text_color: "Custom"
            text_color: "white"
            pos_hint: {"center_x": .5, "center_y": .5}
"""


class ButtonsLayout2(RelativeLayout):
    dialog = None

    def __init__(self, **args):
        Builder.load_string(BL2)
        super().__init__(**args)

    def ok(self):
        self.get_prompt()

    def get_prompt(self):
        self.parent.parent.start_waiting_animation()
        data_for_dialog = self.parent.parent.controller.get_prompt()
        Clock.schedule_once(partial(self.dialog_popup, data_for_dialog), 0.1)

    def dialog_popup(self, data_for_dialog: list, dt):
        if not self.dialog:
            self.dialog = MDDialog(
                # -----------------------Headline text-------------------------
                MDDialogHeadlineText(
                    text="Confirm data?",
                    halign="left"
                ),
                # -----------------------Supporting text-----------------------
                MDDialogSupportingText(
                    text=f"{data_for_dialog[0]}",
                    halign="left"
                ),
                # ---------------------Button container------------------------
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.close_dialog_and_back_to_photo
                    ),
                    MDButton(
                        MDButtonText(text="Accept"),
                        style="text",
                        on_release=partial(self.add_recipe, data_for_dialog)
                    ),
                    spacing="8dp",
                )
            )
            self.dialog.open()
        else:
            self.dialog.open()

    def add_recipe(self, data: list, dt) -> None:
        # current list is [return_text, date, produkty, suma_pln]
        dbrain.add_recipe(receipt_name=f'{data[ 1 ]}',
                          receipt_description=f"{data[ 2 ]}",
                          receipt_amount=f"{data[ 3 ]}")
        self.dialog.dismiss()
        self.parent.parent.parent.current = "screen0"
        self.parent.parent.parent.remove_widget(self.parent.parent)

    def close_dialog_and_back_to_photo(self, dt):
        self.dialog.dismiss()
        self.dialog = None
        self.parent.parent.controller.back_from_acceptancescreen2()

    def retry(self):
        image_path = self.parent.ids.image.source
        if os.path.isfile(f'{image_path}'):
            os.remove(f"{image_path}")

        self.parent.parent.controller.back_from_acceptancescreen2()
