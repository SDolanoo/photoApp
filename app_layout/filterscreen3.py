from kivy.properties import DictProperty
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDockedDatePicker
from kivy.uix.checkbox import CheckBox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, \
    MDListItemTrailingSupportingText

from app_layout.just_screen import JustScreen
from app_layout_extended_functions import filterscreen3_extenders as fs3e
from database_layer import database_brain as dbrain

import datetime


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
        size_hint: 1, .1
        pos_hint: {"center_x": .5, "center_y": 0.95}
        
        MDTopAppBarLeadingButtonContainer:
    
            MDActionTopAppBarButton:
                icon: "keyboard-backspace"
                on_release: app.swap_filtersscreen3()
    
        MDTopAppBarTitle:
            text: "Filters"
            
    # MDRecycleView:
    #     padding: [80, 0, 80, 0]
    #     size_hint_y: None
    #     height: self.parent.height - dp(138)
    #     pos_hint: {"center_x": .5, "center_y": 0.525}
    ScrollView:
        padding: [80, 0, 80, 0]
        size_hint: 1, .8
        # height: self.parent.height - dp(138)
        pos_hint: {"center_x": .5, "center_y": 0.5}
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
                    on_release: root.change_filter("paragon")
                    
                    MDSegmentButtonLabel:
                        text: "Paragon"
                        active: True
                
                MDSegmentedButtonItem:
                    id: faktura
                    on_release: root.change_filter("faktura")
            
                    MDSegmentButtonLabel:
                        text: "Faktura"
        
            DateFilter3:
                id: date
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
                
            PriceFilter3:
                id: price
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#2f47c2"
                adaptive_height: True
                height: "300dp"
                
            OdbiorcyFilter3:
                id: odbiorcy
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
                
            SprzedawcyFilter3:
                id: sprzedawcy
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#2f47c2"
                adaptive_height: True
                height: "300dp"
                
            SklepyFilter3:
                id: sklepy
                radius: [25, 0, 25, 0]
                theme_bg_color: "Custom"
                md_bg_color: "#4267B2"
                adaptive_height: True
                height: "300dp"
        
    ButtonLayout3:
        size_hint: 1, .1
        theme_bg_color: "Custom"
        md_bg_color: "#2367B2"
    # BotAppBar:
    #     id: bottom_appbar
"""


class FilterScreen3(JustScreen):

    def __init__(self, controller, **args):
        Builder.load_string(FS3)
        super().__init__()
        self.controller = controller
        # self.add_to_grid()
        self.current_filter = "paragon"

    def on_enter(self, *args):
        self.clear_all_values()

    def get_all_values(self):
        # print(self.ids.date.get_values())
        # print(self.ids.price.get_values())
        # print(self.ids.odbiorcy.get_values())
        # print(self.ids.sprzedawcy.get_values())
        # print(self.ids.sklepy.get_values())

        doc_type = self.current_filter
        date_from, date_to = self.ids.date.get_values()
        price_from, price_to = self.ids.price.get_values()
        odbiorcy = self.ids.odbiorcy.get_values()
        sprzedawcy = self.ids.sprzedawcy.get_values()
        sklepy = self.ids.sklepy.get_values()
        if doc_type == 'paragon':
            receipts = dbrain.list_filtered_receipts(doc_type, date_from, date_to, price_from, price_to,
                                                        uzytkownik_id=1, sklepy=None)
            self.controller.homescreen0_apply_filters(doc_type, receipts)
        else:
            invoices = dbrain.list_filtered_invoice(doc_type, date_from, date_to, price_from, price_to,
                                                        uzytkownik_id=1, odbiorcy=None, sprzedawcy=None)
            self.controller.homescreen0_apply_filters(doc_type, invoices)

    def clear_all_values(self):
        self.ids.date.clear_values()
        self.ids.price.clear_values()
        self.ids.odbiorcy.clear_values()
        self.ids.sprzedawcy.clear_values()
        self.ids.sklepy.clear_values()

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
            print("no action")
            return "no action"

        self.current_filter = a
        # TODO show_new_filter()

    def show_new_filter(self):
        pass


DF3 = """
<DateFilter3>:
    MDLabel:
        text: "Data zakupu"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.1, "center_y": 0.9}
    
    MDLabel:
        text: "Ostatni tydzien"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.2, "center_y": 0.75}
    
    CheckBox:
        id: date_box
        group: 'dates'
        size_hint: None, None
        size: "40dp", "40dp"
        on_active: root.on_checkbox_active(*args)
        pos_hint: {"center_x": 0.1, "center_y": 0.75}
    
    MDLabel:
        text: "Ostatni miesiac"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.2, "center_y": 0.55}
        
    CheckBox:
        group: 'dates'
        size_hint: None, None
        size: "40dp", "40dp"
        on_active: root.on_checkbox_active(*args)
        pos_hint: {"center_x": 0.1, "center_y": 0.55}

    
    MDLabel:
        text: "Ostatni rok"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.2, "center_y": 0.35}

    CheckBox:
        group: 'dates'
        size_hint: None, None
        size: "40dp", "40dp"
        on_active: root.on_checkbox_active(*args)
        pos_hint: {"center_x": 0.1, "center_y": 0.35}

    # DatePicker
    MDTextField:
        id: field_from
        mode: "outlined"
        pos_hint: {'center_x': .25, 'center_y': .15}
        size_hint: .4, .1
        on_focus: root.show_docked_date_picker(self.focus, "from")
        # validator: "date"
        # date_format: "dd/mm/yyyy"

        MDTextFieldHintText:
            text: "Od"

        MDTextFieldTrailingIcon:
            icon: "calendar"
   
    MDTextField:
        id: field_to
        mode: "outlined"
        pos_hint: {'center_x': .75, 'center_y': .15}
        size_hint: .4, .1
        on_focus: root.show_docked_date_picker(self.focus, "to")
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
        self.values = None

    def get_values(self) -> list:
        # .strftime("%d/%m/%Y")
        date_to = datetime.date.today()
        date_from = datetime.date.today()
        for child in self.children:
            if isinstance(child, CheckBox):
                if child.state == 'down':
                    if child.pos_hint[ 'center_y' ] >= 0.7:  # jeżeli to ostatni tydzień
                        date_from = date_to - datetime.timedelta(days=7)
                    if 0.45 < child.pos_hint[ 'center_y' ] < 0.7:  # jeżeli początek miesiąca
                        date_from = date_to.replace(day=1)
                    if child.pos_hint[ 'center_y' ] < 0.44:
                        date_from = date_to.replace(month=1, day=1)
            if isinstance(child, MDTextField):
                if self.ids.field_from.text != "" and self.ids.field_to.text != "":
                    # jeżeli pola nie są puste
                    date_from = datetime.datetime.strptime(self.ids.field_from.text, "%d/%m/%Y")
                    date_to = datetime.datetime.strptime(self.ids.field_to.text, "%d/%m/%Y")
        if date_from == date_to:
            return [None, None]
        else:
            return [date_from, date_to]

    # def save_values(self):
    # POTENTIALLY TODO TO SAVE SPACE AND READABILITY
    def clear_values(self):
        self.disable_checkboxes()
        self.clear_date_textfields()

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.clear_date_textfields()
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')

    def disable_checkboxes(self) -> None:
        xd = self.ids.date_box.get_widgets('dates')
        for czek in xd:
            czek.active = False

    def clear_date_textfields(self) -> None:
        if self.ids.field_from.text:
            self.ids.field_from.text = ""
        if self.ids.field_to.text:
            self.ids.field_to.text = ""

    def on_ok_from(self, instance_date_picker) -> None:
        date = instance_date_picker.get_date()
        self.ids.field_from.text = str(date[0].strftime("%d/%m/%Y"))
        instance_date_picker.dismiss()

    def on_ok_to(self, instance_date_picker) -> None:
        date = instance_date_picker.get_date()
        self.ids.field_to.text = str(date[0].strftime("%d/%m/%Y"))
        instance_date_picker.dismiss()

    def show_docked_date_picker(self, focus, from_or_to):
        if not focus:
            return
        self.disable_checkboxes()
        date_dialog = MDDockedDatePicker()
        # You have to control the position of the date picker dialog yourself.
        if from_or_to == "from":
            date_dialog.bind(on_ok=self.on_ok_from)
        else:
            date_dialog.bind(on_ok=self.on_ok_to)
        date_dialog.open()


PF3 = """
<PriceFilter3>:

    MDLabel:
        text: "Kwota"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.1, "center_y": 0.9}
    
    CheckBox:
        id: price_box
        group: 'price'
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"center_x": 0.1, "center_y": 0.75}
        on_active: root.on_checkbox_active(*args)
    
    MDLabel:
        text: "do 100,00"
        size_hint: None, None
        size: "100dp", "30dp"
        pos_hint: {"center_x": 0.2, "center_y": 0.75}

    # Checkbox 2 with label
    CheckBox:
        group: 'price'
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"center_x": 0.1, "center_y": 0.55}
        on_active: root.on_checkbox_active(*args)

    MDLabel:
        text: "od 100,00 do 1000,00"
        size_hint: None, None
        size: "300dp", "30dp"
        pos_hint: {"center_x": 0.3, "center_y": 0.55}

    # Checkbox 3 with label
    CheckBox:
        group: 'price'
        size_hint: None, None
        size: "40dp", "40dp"
        pos_hint: {"center_x": 0.1, "center_y": 0.35}
        on_active: root.on_checkbox_active(*args)
    
    MDLabel:
        text: "powyżej 1000,00"
        size_hint: None, None
        size: "200dp", "30dp"
        pos_hint: {"center_x": 0.2, "center_y": 0.35}

    # price picker
    MDTextField:
        id: price_field_from
        mode: "outlined"
        pos_hint: {'center_x': .25, 'center_y': .15}
        size_hint: .4, .1
        text: ""
        on_focus: root.is_text_ok(*args)

        MDTextFieldHintText:
            text: "Od"

        MDTextFieldTrailingIcon:
            icon: "numeric"
    
    MDTextField:
        id: price_field_to
        mode: "outlined"
        pos_hint: {'center_x': .75, 'center_y': .15}
        size_hint: .4, .1
        text: ""
        on_focus: root.is_text_ok(*args)

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

    def get_values(self) -> list:
        # .strftime("%d/%m/%Y")
        price_high = 0
        price_low = 0
        for child in self.children:
            if isinstance(child, CheckBox):
                if child.state == 'down':
                    if child.pos_hint['center_y'] >= 0.7:  # jeżeli to do 100,00
                        price_high = 100.00
                    if 0.45 < child.pos_hint['center_y'] < 0.7:  # jeżeli od 100 do 1000
                        price_high = 1000.00
                        price_low = 100.00
                    if child.pos_hint['center_y'] < 0.44:  # jeżeli powyżej 1000
                        price_high = 999999999.00
                        price_low = 1000.00
            if isinstance(child, MDTextField):
                if self.ids.price_field_from.text != "" and self.ids.price_field_to.text != "":
                    # jeżeli pola nie są puste
                    price_low = self.ids.price_field_from.text
                    price_high = self.ids.price_field_to.text
        if price_high == price_low:
            return [None, None]
        else:
            return [price_low, price_high]

    # def save_values(self):
    # POTENTIALLY TODO TO SAVE SPACE AND READABILITY

    def clear_values(self):
        self.disable_checkboxes()
        self.clear_price_textfields()

    def on_checkbox_active(self, checkbox, value):
        # xd = checkbox.get_widgets(groupname='dates')
        # print(xd)
        # print(type(xd))
        if value:
            self.clear_price_textfields()
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')

    def disable_checkboxes(self) -> None:
        xd = self.ids.price_box.get_widgets('price')
        for czek in xd:
            czek.active = False

    def clear_price_textfields(self) -> None:
        if self.ids.price_field_from.text:
            self.ids.price_field_from.text = ""
        if self.ids.price_field_to.text:
            self.ids.price_field_to.text = ""

    def is_text_ok(self, instance, focus):
        """
        focus is if text field is being used, if it is being used focus = true,
        but when user stops using it will be False, then we will fire validator for integers
        and show an error if there will be one
        """
        if focus:
            instance.text = ""
            self.disable_checkboxes()
        if not focus:
            if not self.textfield_validator():
                instance.text = "Tylko cyfry np. 100.00"
                instance.error = True

    def textfield_validator(self) -> bool:
        fields = [ self.ids.price_field_from, self.ids.price_field_to ]
        for field in fields:
            try:
                new_text = "%.2f" % float(field.text)
            except ValueError:
                return False
            else:
                field.text = new_text
                return True


# Tylko faktura
OF3 = """
<NewDeleteButton>:
    style: "standard"
    icon: "alpha-x-circle-outline"
    pos_hint: root.pos_hint
    on_release: self.parent.delete_DropDownItem(self)

<NewDropDownOdbiorcy>:
    size_hint: .7, .1
    pos_hint: root.pos_hint
    on_release: self.parent.open_menu(self)
    
    MDDropDownItemText:
        id: odbiorcy_drop
        text: "Wszyscy"
    
<OdbiorcyFilter3>:
    
    MDLabel:
        text: "Odbiorcy"
        size_hint: 0.4, 0.1
        pos_hint: {"center_x": 0.2, "center_y": 0.9}
        
    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        on_release: root.open_menu(self)
        MDDropDownItemText:
            text: "Wszyscy"
           
    MDButton:
        id: odbiorcy_add
        style: "text"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        on_release: root.add_new_field(self)
        
        MDButtonIcon:
            icon: "plus"
        
        MDButtonText: 
            text: "Dodaj odbiorce"
            
"""


class NewDropDownOdbiorcy(MDDropDownItem):
    pos_hint = DictProperty()


class NewDeleteButton(MDIconButton):
    pos_hint = DictProperty()


# Tylko faktura
class OdbiorcyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(OF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def get_values(self):
        fs3e.get_values_for_OF3_SP3_SkF3(self)

    def clear_values(self):
        fs3e.clear_values_for_OF3_SP3_SkF3(self)

    def delete_DropDownItem(self, btn):
        fs3e.delete_DropDownItem_for_OF3_SP3_SkF3(instance=self, btn=btn)

    def add_new_field(self, button):
        button_position_x = button.pos_hint[ 'center_x' ]
        button_position_y = button.pos_hint[ 'center_y' ]
        if button_position_y <= .1:
            button.pos_hint = {'center_x': button_position_x + 1, 'center_y': button_position_y - 0.15}
        else:
            button.pos_hint = {'center_x': button_position_x, 'center_y': button_position_y - 0.15}
        new_delete_button = NewDeleteButton(
            pos_hint={'center_x': button_position_x - 0.3, 'center_y': button_position_y})
        new_drop_down = NewDropDownOdbiorcy(
            pos_hint={'center_x': button_position_x + 0.1, 'center_y': button_position_y})
        self.add_widget(new_delete_button)
        self.add_widget(new_drop_down)

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        odbiorcy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                     "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{odbiorca}",
                "on_release": lambda x=f"{odbiorca}": self.menu_callback(x, item),
            } for odbiorca in odbiorcy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item, item):
        child = item._drop_down_text
        child.text = text_item
        self.menu.dismiss()


# Tylko faktura
SF3 = """
<NewDropDownSprzedawcy>:
    size_hint: .7, .1
    pos_hint: root.pos_hint
    on_release: self.parent.open_menu(self)
    
    MDDropDownItemText:
        id: odbiorcy_drop
        text: "Wszyscy"
        
<SprzedawcyFilter3>:
    MDLabel:
        text: "Sprzedawcy - tylko faktury!"
        size_hint: 0.4, 0.1
        pos_hint: {"center_x": 0.2, "center_y": 0.9}

    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        on_release: root.open_menu(self)
        MDDropDownItemText:
            text: "Wszyscy"

    MDButton:
        style: "text"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        on_release: root.add_new_field(self)
        
        MDButtonIcon:
            icon: "plus"
        
        MDButtonText: 
            text: "Dodaj sprzedawce"

"""


class NewDropDownSprzedawcy(MDDropDownItem):
    pos_hint = DictProperty()


# Tylko faktura
class SprzedawcyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(SF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def get_values(self):
        fs3e.get_values_for_OF3_SP3_SkF3(self)

    def clear_values(self):
        fs3e.clear_values_for_OF3_SP3_SkF3(self)

    def delete_DropDownItem(self, btn):
        fs3e.delete_DropDownItem_for_OF3_SP3_SkF3(instance=self, btn=btn)

    def add_new_field(self, button):
        button_position_x = button.pos_hint[ 'center_x' ]
        button_position_y = button.pos_hint[ 'center_y' ]
        if button_position_y <= .1:
            button.pos_hint = {'center_x': button_position_x + 1, 'center_y': button_position_y - 0.15}
        else:
            button.pos_hint = {'center_x': button_position_x, 'center_y': button_position_y - 0.15}
        new_delete_button = NewDeleteButton(
            pos_hint={'center_x': button_position_x - 0.3, 'center_y': button_position_y})
        new_drop_down = NewDropDownSprzedawcy(
            pos_hint={'center_x': button_position_x + 0.1, 'center_y': button_position_y})
        self.add_widget(new_delete_button)
        self.add_widget(new_drop_down)

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        sprzedawcy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                       "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{sprzedawca}",
                "on_release": lambda x=f"{sprzedawca}": self.menu_callback(x, item),
            } for sprzedawca in sprzedawcy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item, item):
        child = item._drop_down_text
        child.text = text_item
        self.menu.dismiss()


# Tylko faktura
SkF3 = """
<NewDropDownSklepy>:
    size_hint: .8, .1
    pos_hint: root.pos_hint
    on_release: self.parent.open_menu(self)
    
    MDDropDownItemText:
        id: odbiorcy_drop
        text: "Wszyscy"
        
<SklepyFilter3>:
    MDLabel:
        text: "Sklepy - tylko paragony!"
        size_hint: 0.4, 0.1
        pos_hint: {"center_x": 0.2, "center_y": 0.9}

    MDDropDownItem:
        size_hint: .8, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        on_release: root.open_menu(self)
        MDDropDownItemText:
            text: "Wszyscy"

    MDButton:
        style: "text"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        on_release: root.add_new_field(self)
        
        MDButtonIcon:
            icon: "plus"
        
        MDButtonText: 
            text: "Dodaj sklep"

"""


class NewDropDownSklepy(MDDropDownItem):
    pos_hint = DictProperty()


# Tylko faktura
class SklepyFilter3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(SkF3)
        super().__init__()
        self.size_hint = (1, .5)
        self.menu = None

    def get_values(self):
        fs3e.get_values_for_OF3_SP3_SkF3(self)

    def clear_values(self):
        fs3e.clear_values_for_OF3_SP3_SkF3(self)

    def delete_DropDownItem(self, btn):
        fs3e.delete_DropDownItem_for_OF3_SP3_SkF3(instance=self, btn=btn)

    def add_new_field(self, button):
        button_position_x = button.pos_hint[ 'center_x' ]
        button_position_y = button.pos_hint[ 'center_y' ]
        if button_position_y <= .1:
            button.pos_hint = {'center_x': button_position_x + 1, 'center_y': button_position_y - 0.15}
        else:
            button.pos_hint = {'center_x': button_position_x, 'center_y': button_position_y - 0.15}
        new_delete_button = NewDeleteButton(
            pos_hint={'center_x': button_position_x - 0.3, 'center_y': button_position_y})
        new_drop_down = NewDropDownSklepy(
            pos_hint={'center_x': button_position_x + 0.1, 'center_y': button_position_y})
        self.add_widget(new_delete_button)
        self.add_widget(new_drop_down)

    def open_menu(self, item):
        if self.menu is not None:
            self.menu = None
        sklepy = [ "Wszyscy", "Agata Mak", "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan", "Agata Mak",
                   "Beata Poziomka", "Bartosz Ziemniak", "Dariusz Banan" ]
        menu_items = [
            {
                "text": f"{sklep}",
                "on_release": lambda x=f"{sklep}": self.menu_callback(x, item),
            } for sklep in sklepy
        ]
        self.menu = MDDropdownMenu(caller=item, items=menu_items, position="bottom", max_height=200)
        self.menu.open()

    def menu_callback(self, text_item, item):
        child = item._drop_down_text
        child.text = text_item
        self.menu.dismiss()


BL3 = """
<ButtonLayout3>:
    MDButton:
        id: clear
        style: "text"
        pos_hint: {"center_x": 0.25, "center_y": 0.5}
        size_hint: 1, 1
        on_release: root.clear()

        MDButtonText: 
            text: "WYCZYŚĆ"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 1, 1
            
    MDButton:
        id: apply
        style: "text"
        pos_hint: {"center_x": 0.75, "center_y": 0.5}
        size_hint: 1, 1
        on_release: root.ok()

        MDButtonText: 
            text: "ZASTOSUJ"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 1, 1
        
"""


class ButtonLayout3(MDFloatLayout):

    def __init__(self, **args):
        Builder.load_string(BL3)
        super().__init__()

    def ok(self):
        self.parent.get_all_values()

    def clear(self):
        self.parent.clear_all_values()
        self.parent.controller.swap_filtersscreen3()
