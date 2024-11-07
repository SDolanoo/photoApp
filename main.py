from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.appbar import MDActionBottomAppBarButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingSupportingText
from kivy.properties import StringProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition
from database_layer import database_brain as dbrain

KV = '''
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton
MDScreenManager:
    transition: app.transition
    
    MDScreen:
        name: "screen1"
        md_bg_color: self.theme_cls.backgroundColor
    
        MDTopAppBar:
            type: "small"
            theme_bg_color: "Custom"
            md_bg_color: "#4267B2"
            id: top_appbar
            pos_hint: {"center_x": .5, "center_y": 0.96}
    
            MDTopAppBarLeadingButtonContainer:
    
                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: nav_drawer.set_state("toggle")
    
    
            MDTopAppBarTitle:
                text: "PhotoApp"
    
            MDTopAppBarTrailingButtonContainer:
    
                MDActionTopAppBarButton:
                    id: app_bar_button
                    icon: "dots-vertical"
                    on_release: app.settings_menu_open()
    
    
        MDScrollView:
            padding: [64, 0, 80, 0]
            size_hint_y: None
            height: self.parent.height - dp(138)
            pos_hint: {"center_x": .5, "center_y": 0.525}
            MDGridLayout:
                id: box
                cols: 1
                pos_hint: {"center_x": .5}
                adaptive_height: True
    
    
        MDBottomAppBar:
            id: bottom_appbar
            action_items:
                [
                MDActionBottomAppBarButton(icon="gmail"),
                MDActionBottomAppBarButton(icon="bookmark"),
                ]
    
            MDFabBottomAppBarButton:
                id: bottom_fab_app_bar
                icon: "camera-plus-outline"
                # on_release: app.bottom_menu_open()
                on_release: root.current = "screen2"
    
        MDNavigationLayout:
    
            MDNavigationDrawer:
                id: nav_drawer
                radius: 0, dp(16), dp(16), 0
    
                MDNavigationDrawerMenu:
    
                    MDNavigationDrawerLabel:
                        text: "Menu"
    
                    MDNavigationDrawerItem:
                        on_release: app.show_paragony()
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "receipt-text-outline"
    
                        MDNavigationDrawerItemText:
                            text: "Paragony"
    
                        MDNavigationDrawerItemTrailingText:
                            id: receipt_count_label
                            text: str(app.receipt_count)
    
                    MDNavigationDrawerItem:
                        on_release: app.show_faktury()
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "invoice-outline"
    
                        MDNavigationDrawerItemText:
                            text: "Faktury"
    
                        MDNavigationDrawerItemTrailingText:
                            id: invoice_count_label
                            text: str(app.invoice_count)
    
                    MDNavigationDrawerDivider:
    
    MDScreen:
        name: "screen2"
        MDFloatLayout:
            MDIconButton:
                icon: "window-close"
                style: "standard"
                pos_hint: {"center_x": 0.05, "center_y": 0.95}
                
            MDIconButton:
                icon: "flash"
                style: "standard"
                pos_hint: {"center_x": 0.95, "center_y": 0.95}
                
            MDIconButton:
                icon: "flash-off"
                style: "standard"
                pos_hint: {"center_x": 0.9, "center_y": 0.95}
                
            MDIconButton:
                icon: "circle-outline"
                pos_hint: {"center_x": 0.5, "center_y": 0.08}
                theme_font_size: "Custom"
                font_size: "84sp"
                radius: [self.height / 2, ]
                size_hint: None, None
                size: "84dp", "84dp"
    '''

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
