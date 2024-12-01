from app_layout.just_screen import JustScreen
from kivy.lang import Builder
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingSupportingText

from database_layer import database_brain as dbrain


HS0 = """
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton
<HomeScreen0>:
    name: "screen0"
    padding: 0.1, 0.1
    
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
                id: delete_images
                icon: "delete"
                on_release: app.delete_files()

            MDActionTopAppBarButton:
                id: app_bar_button
                icon: "filter"
                on_release: app.swap_filtersscreen3()


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
    receipt_count = len(dbrain.list_all_receipts(uzytkownik_id=1))
    invoice_count = len(dbrain.list_all_invoices(uzytkownik_id=1))

    def __init__(self, controller, **args):
        Builder.load_string(HS0)
        super().__init__()
        self.controller = controller
        self.fill_the_grid()


    def fill_the_grid(self):
        self.show_paragony()

    def show_paragony(self):
        self.clear_grid_layout()

        all_receipts = dbrain.list_all_receipts(uzytkownik_id=1)

        for receipt in all_receipts:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{receipt['data_zakupu']}"),
                MDListItemSupportingText(text=f"{receipt['nazwa_sklepu']}"),
                MDListItemTrailingSupportingText(text=f"{receipt['kwota_calkowita']}")
            )
            self.ids.box.add_widget(list_item)

        # set receipt count to change label on Navigaion Drawer
        self.set_navigation_drawer_count()

    def show_faktury(self):
        self.clear_grid_layout()

        all_invoices = dbrain.list_all_invoices(uzytkownik_id=1)

        for invoice in all_invoices:
            list_item = MDListItem(
                MDListItemHeadlineText(text=f"{invoice['numer_faktury']}"),
                MDListItemSupportingText(text=f"{invoice['razem_stawka']}"),
                MDListItemTrailingSupportingText(text=f"{invoice['razem_brutto']}")
            )
            self.ids.box.add_widget(list_item)

        # set invoice count to change label on Navigaion Drawer
        self.set_navigation_drawer_count()

    def clear_grid_layout(self):
        self.ids.box.clear_widgets()

    def set_navigation_drawer_count(self):
        all_receipts = dbrain.list_all_receipts(uzytkownik_id=1)
        self.receipt_count = len(all_receipts)
        self.ids.receipt_count_label.text = str(self.receipt_count)

        all_invoices = dbrain.list_all_invoices(uzytkownik_id=1)
        self.invoice_count = len(all_invoices)
        self.ids.invoice_count_label.text = str(self.invoice_count)