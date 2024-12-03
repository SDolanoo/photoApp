import datetime

from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.uix.appbar import MDBottomAppBar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarText

from app_layout.just_screen import JustScreen
from kivy.lang import Builder
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, \
    MDListItemTrailingSupportingText

FS3 = """

<FilterScreen3>:
    name: "screen3"
    padding: 0.1, 0.1
    
    MDTopAppBar:
        id: "topappbar"
        type: "small"
        theme_bg_color: "Custom"
        md_bg_color: "#4267B2"
        id: top_appbar
        pos_hint: {"center_x": .5, "center_y": 0.96}
        
        MDTopAppBarLeadingButtonContainer:
    
            MDActionTopAppBarButton:
                icon: "keyboard-backspace"
                on_release: app.swap_filtersscreen3()
    
        MDTopAppBarTitle:
            text: "Filters"
            
    MDRecycleView:
        padding: [80, 0, 80, 0]
        size_hint_y: None
        height: self.parent.height - dp(138)
        pos_hint: {"center_x": .5, "center_y": 0.525}
        
        MDGridLayout:
            id: box
            cols: 1
            adaptive_height: True
            
            MDSegmentedButton:
                id: seg_button
                pos_hint: {'center_x': .5}
                type: "large"
                multiselect: False
                
                MDSegmentedButtonItem:
                    id: paragon
                    on_active: root.change_filter("paragon")
                    
                    MDSegmentButtonLabel:
                        text: "Paragon"
                        active: True
                
                MDSegmentedButtonItem:
                    id: faktura
                    on_active: root.change_filter("faktura")
            
                    MDSegmentButtonLabel:
                        text: "Faktura"
        
            DateFilter3:
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
                
            PriceFilter3:
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#2f47c2"
                adaptive_height: True
                height: "300dp"
                
            OdbiorcyFilter3:
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
                
            SprzedawcyFilter3:
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#2f47c2"
                adaptive_height: True
                height: "300dp"
                
            SklepyFilter3:
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
                
    BotAppBar:
        id: bottom_appbar
"""


class FilterScreen3(JustScreen):

    def __init__(self, controller, **args):
        Builder.load_string(FS3)
        super().__init__()
        self.controller = controller
        # self.add_to_grid()
        self.current_filter = "paragony"

    def add_to_grid(self):
        for i in range(20):
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{i}"),
                MDListItemSupportingText(text=f"{i}"),
                MDListItemTrailingSupportingText(text=f"{i}")
            )
            self.ids.box.add_widget(list_item)

    def change_filter(self, a):
        if self.current_filter == a:
            return "no action"

        self.current_filter = a
        # TODO show_new_filter()

    def show_new_filter(self):
        pass

    # TODO dokończyć ui, Odbiorcy, Sprzedawca, Sklep


DF3 = """
<DateFilter3>:
    MDLabel:
        text: "Data zakupu"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.1, "y": 0.8}
    
    MDCheckbox:
        group: "dates"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.65}
    
    MDLabel:
        text: "Option 1"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.65}

    # Checkbox 2 with label
    MDCheckbox:
        group: "dates"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.45}

    MDLabel:
        text: "Option 2"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.45}

    # Checkbox 3 with label
    MDCheckbox:
        group: "dates"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.25}
    
    MDLabel:
        text: "Option 3"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.25}

    # DatePicker
    MDTextField:
        id: field
        mode: "outlined"
        pos_hint: {'center_x': .25, 'center_y': .15}
        size_hint: .4, .1
        on_focus: root.show_docked_date_picker(self.focus)
        # validator: "date"
        # date_format: "dd/mm/yyyy"

        MDTextFieldHintText:
            text: "Od"

        MDTextFieldTrailingIcon:
            icon: "calendar"
   
    MDTextField:
        id: field
        mode: "outlined"
        pos_hint: {'center_x': .75, 'center_y': .15}
        size_hint: .4, .1
        on_focus: root.show_docked_date_picker(self.focus)
        # validator: "date"
        # date_format: "dd/mm/yyyy"

        MDTextFieldHintText:
            text: "Do"

        MDTextFieldTrailingIcon:
            icon: "calendar"
"""


class DateFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(DF3)
        super().__init__()
        self.size_hint = (1, .5)

    def on_ok(self, instance_date_picker):
        date = instance_date_picker.get_date()
        MDSnackbar(
            MDSnackbarText(
                text="Selected dates is:",
            ),
            MDSnackbarSupportingText(
                text="\n".join(str(date) for date in instance_date_picker.get_date()),
                padding=[ 0, 0, 0, dp(12) ],
            ),
            y=dp(124),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            padding=[ 0, 0, "8dp", "8dp" ],
        ).open()
        self.ids.field.text = str(date[ 0 ].strftime("%d/%m/%Y"))
        instance_date_picker.dismiss()

    def show_docked_date_picker(self, focus):
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()


PF3 = """
<PriceFilter3>:

    MDLabel:
        text: "Kwota"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.1, "y": 0.8}
    
    MDCheckbox:
        group: "price"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.65}
    
    MDLabel:
        text: "do 100,00"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.65}

    # Checkbox 2 with label
    MDCheckbox:
        group: "price"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.45}

    MDLabel:
        text: "od 100,00 do 1000,00"
        size_hint: None, None
        size: "300dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.45}

    # Checkbox 3 with label
    MDCheckbox:
        group: "price"
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"x": 0.1, "y": 0.25}
    
    MDLabel:
        text: "powyżej 1000,00"
        size_hint: None, None
        size: "200dp", "30dp"
        pos_hint: {"x": 0.2, "y": 0.25}

    # price picker
    MDTextField:
        id: price_field
        mode: "outlined"
        pos_hint: {'center_x': .25, 'center_y': .15}
        size_hint: .4, .1
        text: ""

        MDTextFieldHintText:
            text: "Od"

        MDTextFieldTrailingIcon:
            icon: "numeric"
    
    MDTextField:
        id: price_field
        mode: "outlined"
        pos_hint: {'center_x': .75, 'center_y': .15}
        size_hint: .4, .1
        text: ""

        MDTextFieldHintText:
            text: "Do"

        MDTextFieldTrailingIcon:
            icon: "numeric"
"""


class PriceFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(PF3)
        super().__init__()
        self.size_hint = (1, .5)


# Tylko faktura
OF3 = """
<OdbiorcyFilter3>:
    MDLabel:
        text: "Odbiorcy"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.1, "y": 0.8}
        
    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"x": 0.1, "y": 0.65}
        on_release: root.open_menu(self)
        
        MDDropDownItemText:
            id: odbiorcy_drop
            text: "Wszyscy"
            
    MDButton:
        style: "text"
        pos_hint: {"x": 0.1, "y": 0.4}
        MDButtonIcon:
            icon: "plus"
        
        MDButtonText: 
            text: "Dodaj odbiorce"
            
"""


# Tylko faktura
class OdbiorcyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(OF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        odbiorcy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                     "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{odbiorca}",
                "on_release": lambda x=f"{odbiorca}": self.menu_callback(x),
            } for odbiorca in odbiorcy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.odbiorcy_drop.text = text_item
        self.menu.dismiss()

    def on_drop_down_text(self, instance):
        instance.dismiss()
        print(self.ids.odbiorcy_drop.text)


# Tylko faktura
SF3 = """
<SprzedawcyFilter3>:
    MDLabel:
        text: "Sprzedawcy"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.1, "y": 0.8}

    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"x": 0.1, "y": 0.65}
        on_release: root.open_menu(self)

        MDDropDownItemText:
            id: sprzedawcy_drop
            text: "Wszyscy"

    MDButton:
        style: "text"
        pos_hint: {"x": 0.1, "y": 0.4}
        MDButtonIcon:
            icon: "plus"

        MDButtonText: 
            text: "Dodaj sprzedawce"

"""


# Tylko faktura
class SprzedawcyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(SF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        sprzedawcy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                       "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{sprzedawca}",
                "on_release": lambda x=f"{sprzedawca}": self.menu_callback(x),
            } for sprzedawca in sprzedawcy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.sprzedawcy_drop.text = text_item
        self.menu.dismiss()


# Tylko faktura
SkF3 = """
<SklepyFilter3>:
    MDLabel:
        text: "Sklepy"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"x": 0.1, "y": 0.8}

    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"x": 0.1, "y": 0.65}
        on_release: root.open_menu(self)

        MDDropDownItemText:
            id: sklepy_drop
            text: "Wszystkie"

    MDButton:
        style: "text"
        pos_hint: {"x": 0.1, "y": 0.4}
        MDButtonIcon:
            icon: "plus"

        MDButtonText: 
            text: "Dodaj sklep"

"""


# Tylko faktura
class SklepyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(SkF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        sklepy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                       "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{sklep}",
                "on_release": lambda x=f"{sklep}": self.menu_callback(x),
            } for sklep in sklepy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.sklepy_drop.text = text_item
        self.menu.dismiss()


BAB3 = """
<BotAppBar>:
    MDFabBottomAppBarButton:
        id: bottom_fab_app_bar
        icon: "camera-plus-outline"
        # on_release: app.bottom_menu_open()
        on_release: app.swap_to_photoscreen1()
"""


class BotAppBar(MDBottomAppBar):

    def __init__(self, **args):
        Builder.load_string(BAB3)
        super().__init__()
