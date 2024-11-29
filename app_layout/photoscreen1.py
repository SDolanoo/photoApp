from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from camera4kivy import Preview

from datetime import datetime
from functools import partial

from app_layout.just_screen import JustScreen
from app_layout.acceptancescreen2 import AcceptanceScreen2

PS1 = """
<PhotoScreen1>:
    name: "screen1"
    photo_preview: photo_layout.ids.preview
    PhotoLayout1:
        id: photo_layout
"""


class PhotoScreen1(JustScreen):
    photo_preview = ObjectProperty(None)

    def __init__(self, controller, **args):
        Builder.load_string(PS1)
        super().__init__()
        self.controller = controller

    def on_enter(self):
        self.photo_preview.connect_camera(mirrored=False)

    def on_pre_leave(self):
        self.photo_preview.disconnect_camera()


PL1 = """
<PhotoLayout1>:
    Preview:
        id: preview
    ButtonsLayout1:
        id: buttons
"""


class PhotoLayout1(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(PL1)
        super().__init__(**args)

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.orientation = 'vertical'
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (1, .2)
        else:
            self.orientation = 'horizontal'
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (.2, 1)


BL1 = """
<ButtonsLayout1>:
    MDIconButton:
        id:other
        icon: "window-close"
        on_release: app.back_to_homescreen0()
        style: "standard"
        pos_hint: {"center_x": 0.05, "center_y": 0.95}
    MDIconButton:
        id:flash
        icon: "flash"
        style: "standard"
        pos_hint: {"center_x": 0.95, "center_y": 0.95}
        on_release: root.flash()
    MDIconButton:
        id:photo
        on_release: root.photo()
        icon: "circle-outline"
        pos_hint: {"center_x": 0.5, "center_y": 0.08}
        theme_font_size: "Custom"
        font_size: "84sp"
        radius: [self.height / 2, ]
        size_hint: None, None
        size: "84dp", "84dp"
"""


class ButtonsLayout1(RelativeLayout):

    def __init__(self, **args):
        Builder.load_string(BL1)
        super().__init__(**args)

    def on_size(self, layout, size):
        if platform in [ 'android', 'ios' ]:
            self.ids.photo.min_state_time = 0.3
        else:
            self.ids.photo.min_state_time = 1
        if Window.width < Window.height:
            self.ids.other.pos_hint = {'center_x': .2, 'center_y': .5}
            self.ids.other.size_hint = (.2, None)
            self.ids.photo.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.photo.size_hint = (.24, None)
            self.ids.flash.pos_hint = {'center_x': .8, 'center_y': .5}
            self.ids.flash.size_hint = (.15, None)
        else:
            self.ids.other.pos_hint = {'center_x': .5, 'center_y': .8}
            self.ids.other.size_hint = (None, .2)
            self.ids.photo.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.photo.size_hint = (None, .24)
            self.ids.flash.pos_hint = {'center_x': .5, 'center_y': .2}
            self.ids.flash.size_hint = (None, .15)

    def photo(self):
        """
        https://github.com/Android-for-Python/Camera4Kivy?tab=readme-ov-file#location
        """
        now = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        self.photo2(now)

    def photo2(self, now):
        self.parent.ids.preview.capture_photo(location='private',
                                              subdir="Photos",
                                              name=f"recipe_{now}")
        Clock.schedule_once(partial(self.photo3, path=f"Photos/recipe_{now}.jpg"), 0.1)

    def photo3(self, dt, path):
        self.parent.parent.controller.show_acceptancescreen2(path="Photos/paragon_4.jpg")

    def flash(self):
        icon = self.parent.ids.preview.flash()
        if icon == 'on':
            self.ids.flash.icon = 'flash'
        elif icon == 'auto':
            self.ids.flash.icon = 'flash-auto'
        else:
            self.ids.flash.icon = 'flash-off'
