KV = '''
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton
MDScreenManager:
    transition: app.transition
    
    MDScreen:
        name: "screen1"
        orientation: "vertical"
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
        orientation: "vertical"
        name: "screen2"

        MDFloatLayout:

            # CAMERA SETUP
            Camera:
                id: camera
                resolution: (378, 645)
                # SET PLAY TO AUTO TRUE
                play: True
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

            MDIconButton:
                icon: "window-close"
                style: "standard"
                pos_hint: {"center_x": 0.05, "center_y": 0.95}
                on_release: root.current = "screen1"

            MDIconButton:
                icon: "flash"
                style: "standard"
                pos_hint: {"center_x": 0.95, "center_y": 0.95}

            MDIconButton:
                icon: "flash-off"
                style: "standard"
                on_release: app.prpr(self.parent.width, self.parent.height)
                pos_hint: {"center_x": 0.9, "center_y": 0.95}

            MDIconButton:
                on_release: app.capture_photo()
                icon: "circle-outline"
                pos_hint: {"center_x": 0.5, "center_y": 0.08}
                theme_font_size: "Custom"
                font_size: "84sp"
                radius: [self.height / 2, ]
                size_hint: None, None
                size: "84dp", "84dp"
    '''
