from app_layout.just_screen import JustScreen
from kivy.lang import Builder
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingSupportingText

from database_layer import database_brain as dbrain


HS0 = """
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton
<HomeScreen0>:
    name: "screen0"
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
            on_release: app.swap_to_photoscreen1()

    MDNavigationLayout:

        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0

            MDNavigationDrawerMenu:

                MDNavigationDrawerLabel:
                    text: "Menu"

                MDNavigationDrawerItem:
                    on_release: root.show_paragony()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "receipt-text-outline"

                    MDNavigationDrawerItemText:
                        text: "Paragony"

                    MDNavigationDrawerItemTrailingText:
                        id: receipt_count_label
                        text: str(root.receipt_count)

                MDNavigationDrawerItem:
                    on_release: root.show_faktury()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "invoice-outline"

                    MDNavigationDrawerItemText:
                        text: "Faktury"

                    MDNavigationDrawerItemTrailingText:
                        id: invoice_count_label
                        text: str(root.invoice_count)

                MDNavigationDrawerDivider:
"""



class HomeScreen0(JustScreen):
    receipt_count = len(dbrain.list_all_receipts())
    invoice_count = len(dbrain.list_all_invoices())

    def __init__(self, **args):
        Builder.load_string(HS0)
        super().__init__()
        self.fill_the_grid()


    def fill_the_grid(self):
        all_receipts = dbrain.list_all_receipts()
        for receipt in all_receipts:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{receipt[ 1 ]}"),
                MDListItemSupportingText(text=f"desc // {receipt[ 2 ]} // desc"),
                MDListItemTrailingSupportingText(text=f"{receipt[ 3 ]}")
            )
            self.ids.box.add_widget(list_item)

    def show_paragony(self):
        self.clear_grid_layout()

        all_receipts = dbrain.list_all_receipts()

        for receipt in all_receipts:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{receipt[ 1 ]}"),
                MDListItemSupportingText(text=f"desc // {receipt[ 2 ]} // desc"),
                MDListItemTrailingSupportingText(text=f"{receipt[ 3 ]}")
            )
            self.ids.box.add_widget(list_item)

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
            self.ids.box.add_widget(list_item)

        # set invoice count to change label on Navigaion Drawer
        self.set_navigation_drawer_count()

    def clear_grid_layout(self):
        self.ids.box.clear_widgets()

    def set_navigation_drawer_count(self):
        all_receipts = dbrain.list_all_receipts()
        self.receipt_count = len(all_receipts)
        self.ids.receipt_count_label.text = str(self.receipt_count)

        all_invoices = dbrain.list_all_invoices()
        self.invoice_count = len(all_invoices)
        self.ids.invoice_count_label.text = str(self.invoice_count)