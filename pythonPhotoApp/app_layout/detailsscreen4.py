from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivy.lang import Builder

from pythonPhotoApp.app_layout.just_screen import JustScreen

DS4 = """
<NewLabel>:
    text: root.text
    size_hint: None, None
    size: "300dp", "50dp"

<DetailsScreen4>:
    name: "screen4"
    padding: 0.1, 0.1

    MDTopAppBar:
        id: "topappbar"
        type: "small"
        theme_bg_color: "Custom"
        md_bg_color: "#4267B2"
        id: top_appbar
        size_hint: 1, .1
        pos_hint: {"center_x": .5, "center_y": 0.95}

        MDTopAppBarLeadingButtonContainer:

            MDActionTopAppBarButton:
                icon: "keyboard-backspace"
                on_release: app.swap_detailsscreen4()

        MDTopAppBarTitle:
            text: "Filters"


    ScrollView:
        padding: [80, 0, 80, 0]
        size_hint: 1, .9
        pos_hint: {"center_x": .5, "center_y": 0.45}
        
        MDGridLayout:
            id: box
            cols: 2
            adaptive_height: True
"""
class NewLabel(MDLabel):
    text = StringProperty()

class DetailsScreen4(JustScreen):

    def __init__(self, controller, **args):
        Builder.load_string(DS4)
        super().__init__()
        self.controller = controller
        self.details = None

    def on_enter(self, *args):
        self.show_details()

    def show_details(self):
        d = self.details[0]
        # print(d)
        # data = d["data_zakupu"]
        self.ids.box.add_widget(NewLabel(text="data_zakupu:   "))
        self.ids.box.add_widget(NewLabel(text=f'{d["data_zakupu"].strftime("%d/%m/%Y")}'))
        self.ids.box.add_widget(NewLabel(text="nazwa_sklepu:   "))
        self.ids.box.add_widget(NewLabel(text=f'{d["nazwa_sklepu"]}'))
        self.ids.box.add_widget(NewLabel(text="kwota_calkowita:   "))
        self.ids.box.add_widget(NewLabel(text=f'{d["kwota_calkowita"]}'))
        self.ids.box.add_widget(NewLabel(text="produkty: "))
        self.ids.box.add_widget(NewLabel(text="   "))
        for product in d['produkty']:
            self.ids.box.add_widget(NewLabel(text=f'{product["nazwa_produktu"]}'))
            self.ids.box.add_widget(NewLabel(text=f'{product["ilosc"]} x {product["cena_suma"]}'))
