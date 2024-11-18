from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
   MDDialogButtonContainer,
   MDDialogSupportingText,
    )
from kivy.uix.widget import Widget

from gen_ai.ai import Ai
import threading
import os
import json
from functools import partial

from app_layout.just_screen import JustScreen
from database_layer import database_brain as dbrain



AS2 = """
<AcceptanceScreen2>:
    name: "screen2"
    pp: acceptance_layout_2.ids.image
    AcceptanceLayout2:
        id: acceptance_layout_2
"""


class AcceptanceScreen2(JustScreen):
    pp = ObjectProperty(None)

    def __init__(self, controller, path, **args):
        Builder.load_string(AS2)
        super().__init__()
        self.pp.source = f"{path}"
        self.controller = controller

    def on_pre_enter(self, *args):
        self.pp.source = self.controller.path



AL2 = """
<AcceptanceLayout2>:
    Image:
        id: image
        size: self.width, self.height
        allow_stretch: True
        keep_ratio:False
    ButtonsLayout2:
        id: buttons
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
    # MDButton:
    #     id: hidden
    #     on_release: app.print()
    #     theme_bg_color: "Custom"
    #     md_bg_color: [0, 0, 0, 0]
"""


class ButtonsLayout2(RelativeLayout):
    dialog = None

    def __init__(self, **args):
        Builder.load_string(BL2)
        super().__init__(**args)

    def ok(self):
        self.get_prompt()

    def get_prompt(self):
        def format_prompt(text) -> list:
            jo = json.loads(text)
            date = jo['data_zakupu']
            produkty = [produkt for produkt in jo['produkty']]
            suma_pln = jo['suma_pln']
            return_text = f"Data zakupu: {jo['data_zakupu']}\n"
            for p in produkty:
                t = f"Nazwa produkty: {p['nazwa']}, cena: {p['cena']}\n"
                return_text = return_text + t
            return_text = return_text + f"Suma ptu: {jo['suma_ptu']}\n"
            return_text = return_text + f"Suma pln: {jo['suma_pln']}"
            return [return_text, date, produkty, suma_pln]



        # ai = Ai(path=self.parent.ids.image.source)
        ai = Ai(path="paragon_2.jpg")
        text = ai.ai_first_prompt()
        data_for_dialog = format_prompt(text)
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
                        on_release=self.close_dialog
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

    def add_recipe(self, data: list, dt) -> None:
        # current list is [return_text, date, produkty, suma_pln]
        dbrain.add_recipe(receipt_name=f'{data[ 1 ]}',
                          receipt_description=f"{data[ 2 ]}",
                          receipt_amount=f"{data[ 3 ]}")
        self.dialog.dismiss()
        self.parent.parent.parent.current = "screen0"
        self.parent.parent.parent.remove_widget(self.parent.parent)

    def close_dialog(self, dt):
        self.dialog.dismiss()
        self.dialog = None

    def retry(self):
        image_path = self.parent.ids.image.source
        if os.path.isfile(f'{image_path}'):
            os.remove(f"{image_path}")

        self.parent.parent.controller.back_from_acceptancescreen2()
