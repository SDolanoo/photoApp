from kivymd.uix.button import MDButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel


def get_values_for_OF3_SP3_SkF3(instance):
    """
        instance: class object of OF3/SP3/SkF3
    """
    values = []
    for child in instance.children:
        if isinstance(child, MDDropDownItem):
            if child._drop_down_text.text in values:
                continue
            values.append(child._drop_down_text.text)
    if len(values) > 1:
        values.remove("Wszyscy")
    return values


def clear_values_for_OF3_SP3_SkF3(instance):
    """
        instance: class object of OF3/SP3/SkF3
    """
    all_widgets = instance.children  # list of all widgets
    to_remove = []  # store the indexes of widgets in list above
    print("starting for loop....")
    for i in range(len(all_widgets)):
        print(all_widgets[i])
        if isinstance(all_widgets[i], MDLabel) and all_widgets[i].pos_hint['center_y'] > 0.85:
            # don't remove giga chad label
            continue
        if isinstance(all_widgets[i], MDDropDownItem) and 0.75 < all_widgets[i].pos_hint['center_y'] < 0.85:
            # if the widget is the first one, change option to Wszyscy and skip it then remove all widgets
            text_field = all_widgets[i]._drop_down_text
            text_field.text = "Wszyscy"
            continue
        if isinstance(all_widgets[i], MDButton) and 0.45 < all_widgets[i].pos_hint['center_x'] < 0.55:
            # if the widget is "+ dodaj ..." move it to starting position and skip
            all_widgets[i].pos_hint = {'center_x': 0.5, 'center_y': 0.65}
            continue
        to_remove.append(i)  # append if widget doesn't apply to above criteria
        print("item to remove: ", i)
        print("start removing processs......")
    for widget in to_remove[ ::-1 ]:
        # remove widgets from a BACKWARDS list,
        # because removing items from a list is not a good idea (I did experience it here)
        print("removing: ", all_widgets[widget])
        instance.remove_widget(all_widgets[widget])

def delete_DropDownItem_for_OF3_SP3_SkF3(instance, btn):
    """
        instance: class object of OF3/SP3/SkF3
        btn: button object that was clicked (the 'X' button)
    """
    for child in instance.children:
        if isinstance(child, MDDropDownItem) and child.pos_hint[ 'center_y' ] == btn.pos_hint[ 'center_y' ]:
            instance.remove_widget(btn)
            instance.remove_widget(child)
    for child in instance.children:
        print(child)
        pos_y = child.pos_hint[ 'center_y' ]
        pos_x = child.pos_hint[ 'center_x' ]
        if pos_y > btn.pos_hint[ 'center_y' ]:
            # skip we don't want to change widgets that are higher
            continue
        if isinstance(child, MDButton):
            # move hidden button from the out of screen right by moving X position to the left
            if pos_x > 1:
                pos_x -= 1
            # child.pos_hint = {'center_x': pos_x - 1, 'center_y': pos_y}
        child.pos_hint = {'center_x': pos_x, 'center_y': pos_y + 0.15}