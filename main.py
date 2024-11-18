from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.appbar import MDActionBottomAppBarButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingSupportingText
from kivymd.uix.transition import MDSharedAxisTransition
from database_layer import database_brain as dbrain
import os
import google.generativeai as genai
from mainKV import KV
from kivy.core.window import Window


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

Window.size = (378, 678)

class Photoapp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.receipt_count = len(dbrain.list_all_receipts())
        self.invoice_count = len(dbrain.list_all_invoices())

        # transition settings
        self.transition = MDSharedAxisTransition()
        self.transition.transition_axis = "y"
        self.transition.duration = 0.2




    def change_actions_items(self):
        self.root.ids.bottom_appbar.action_items = [
            MDActionBottomAppBarButton(icon="magnify"),
            MDActionBottomAppBarButton(icon="trash-can-outline"),
            MDActionBottomAppBarButton(icon="download-box-outline"),
        ]

    def build(self):
        # self.theme_cls.primary_palette = "Orange"
        # self.theme_cls.secondaryColor = "Green"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        return Builder.load_string(KV)

    def on_start(self):
        all_receipts = dbrain.list_all_receipts()
        for receipt in all_receipts:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{receipt[1]}"),
                MDListItemSupportingText(text=f"desc // {receipt[2]} // desc"),
                MDListItemTrailingSupportingText(text=f"{receipt[3]}")
                )
            self.root.ids.box.add_widget(list_item)

    def prpr(self, x, y):
        print(x, "   ", y)

    def settings_menu_open(self):
        menu_items = [
            {
                "text": "Ustawienia",
                "on_release": lambda x=f"Ustawienia": self.menu_callback(x)
            },
            {
                "text": "Pomoc",
                "on_release": lambda x=f"Pomoc": self.menu_callback(x)
            }
        ]
        MDDropdownMenu(
            caller=self.root.ids.app_bar_button, items=menu_items
        ).open()

    def bottom_menu_open(self):
        menu_items = [
            {
                "text": "Wybierz akcje",
                "leading_icon": "gesture-tap-button"
            },
            {
                "text": "Dodaj Paragon",
                "on_release": lambda x="Dodaj Paragon": self.menu_callback(x)
            },
            {
                "text": "Dodaj Fakture",
                "on_release": lambda x="Dodaj Fakture": self.menu_callback(x)
            }
        ]
        MDDropdownMenu(
            caller=self.root.ids.bottom_fab_app_bar,
            items=menu_items,
            ver_growth="up", hor_growth="left"
        ).open()

    def menu_callback(self, text_item):
        print(text_item)

    def capture_photo(self):

        self.root.ids.camera.export_to_png("image.png")

        self.ai_prompt()

    def ai_prompt(self):

        def upload_to_gemini(path, mime_type=None):
            """Uploads the given file to Gemini.

            See https://ai.google.dev/gemini-api/docs/prompting_with_media
            """
            file = genai.upload_file(path, mime_type=mime_type)
            print(f"Uploaded file '{file.display_name}' as: {file.uri}")
            return file

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="przeczytaj zdjęcie paragonu i uzyskaj z niego nastepujące informacje w formacie json: data zakupu, wymień wszystkie produkty i ich ceny, suma PTU, SUMA PLN",
        )

        # TODO Make these files available on the local file system
        # You may need to update the file paths
        files = [
            upload_to_gemini("image.png", mime_type="image/png"),
        ]

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[ 0 ],
                    ],
                },
            ]
        )

        response = chat_session.send_message("INSERT_INPUT_HERE")

        print(response.text)

    def show_paragony(self):
        self.clear_grid_layout()

        all_receipts = dbrain.list_all_receipts()

        for receipt in all_receipts:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{receipt[ 1 ]}"),
                MDListItemSupportingText(text=f"desc // {receipt[ 2 ]} // desc"),
                MDListItemTrailingSupportingText(text=f"{receipt[ 3 ]}")
            )
            self.root.ids.box.add_widget(list_item)

        # set receipt count to change label on Navigaion Drawer
        self.set_navigation_drawer_count()

    def show_faktury(self):
        self.clear_grid_layout()

        all_invoices = dbrain.list_all_invoices()

        for invoice in all_invoices:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{invoice[ 1 ]}"),
                MDListItemSupportingText(text=f"desc // {invoice[ 2 ]} // desc"),
                MDListItemTrailingSupportingText(text=f"{invoice[ 3 ]}")
            )
            self.root.ids.box.add_widget(list_item)

        # set invoice count to change label on Navigaion Drawer
        self.set_navigation_drawer_count()

    def clear_grid_layout(self):
        self.root.ids.box.clear_widgets()

    def set_navigation_drawer_count(self):
        all_receipts = dbrain.list_all_receipts()
        self.receipt_count = len(all_receipts)
        self.root.ids.receipt_count_label.text = str(self.receipt_count)

        all_invoices = dbrain.list_all_invoices()
        self.invoice_count = len(all_invoices)
        self.root.ids.invoice_count_label.text = str(self.invoice_count)

if __name__ == '__main__':
    Photoapp().run()
