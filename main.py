from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.appbar import MDActionBottomAppBarButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty

KV = '''
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton

<MD3ListItem>
    MDListItem:
        size_hint_x: self.parent.width
        
        MDListItemLeadingIcon:
            icon: "account"
    
        MDListItemHeadlineText:
            text: "Headline"
    
        MDListItemSupportingText:
            text: "Supporting text"
    
        MDListItemTertiaryText:
            text: "Tertiary text"
    
        MDListItemTrailingSupportingText:
            text: "Textttt"

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    orientation: "vertical"

    MDTopAppBar:
        type: "small"
        size_hint_x: 1
        pos_hint: {"center_x": .5, "center_y": 0.96}
        theme_bg_color: "Custom"
        md_bg_color: "#4267B2"

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
        pos_hint: {"center_x": .5, "center_y": 0.41}
        MDGridLayout:
            id: box
            cols: 1
            pos_hint: {"center_x": .5}
        
            
            

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
            on_release: app.bottom_menu_open()
       
    MDNavigationLayout:
                
        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0
        
            MDNavigationDrawerMenu:
    
                MDNavigationDrawerLabel:
                    text: "Menu"
    
                MDNavigationDrawerItem:
    
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "receipt-text-outline"
    
                    MDNavigationDrawerItemText:
                        text: "Paragony"
    
                    MDNavigationDrawerItemTrailingText:
                        text: "0"
                
                MDNavigationDrawerItem:
    
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "invoice-outline"
    
                    MDNavigationDrawerItemText:
                        text: "Faktury"
    
                    MDNavigationDrawerItemTrailingText:
                        text: "0"
    
                MDNavigationDrawerDivider:
'''


class MD3ListItem(MDListItem):
    '''Implements a material design MDListItem.'''
    pass

class Photoapp(MDApp):

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
        for i in range(20):
            self.root.ids.box.add_widget(MD3ListItem())

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

    # def open_camera(self, instance):
    #     try:
    #         camera.open_camera()  # Open the camera
    #     except Exception as e:
    #         print(f"Error opening camera: {e}")


if __name__ == '__main__':
    Photoapp().run()
