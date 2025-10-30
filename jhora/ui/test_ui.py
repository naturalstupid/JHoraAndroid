# Add parent directory to sys.path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
import config
from jhora import const, utils

class DropdownSelector(BoxLayout):
    selected_value = StringProperty()

    def __init__(self, label_text, values, initial_value, on_select_callback, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, **kwargs)
        self.values = values
        self.selected_value = initial_value
        self.on_select_callback = on_select_callback

        self.label = Button(text=label_text, size_hint_x=0.5)
        self.dropdown_button = Button(text=self.selected_value, size_hint_x=0.5)
        self.dropdown_button.bind(on_release=self.open_dropdown)

        self.add_widget(self.label)
        self.add_widget(self.dropdown_button)

    def open_dropdown(self, instance):
        dropdown = DropDown()
        for value in self.values:
            btn = Button(text=value, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_value(btn.text, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def select_value(self, value, dropdown):
        self.selected_value = value
        self.dropdown_button.text = value
        dropdown.dismiss()
        if self.on_select_callback:
            self.on_select_callback(value)


# Assume these are defined elsewhere
# from your_module import const, _SPINNER_HEIGHT, _SETTINGS_TAB_COLOR, GetButtonWidget, LeftAlignedSpinner

class SettingsTab(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        Window.softinput_mode = "pan"
        self.app = app
        self.res = self.app.res
        self.original_config = self.app.config.copy()  # Save original config

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.size_hint_y = 1

        # Language setting
        _available_languages = list(const.available_languages.keys())
        self.lang_selector = DropdownSelector(
            label_text="Change Language",
            values=_available_languages,
            initial_value=self.app.config["language"],
            on_select_callback=self.on_language_change
        )
        layout.add_widget(self.lang_selector)

        # Chart type setting
        _available_chart_types = ['south', 'east', 'north']
        self.chart_type_selector = DropdownSelector(
            label_text="Change chart_type",
            values=_available_chart_types,
            initial_value=self.app.config["chart_type"],
            on_select_callback=self.on_chart_type_change
        )
        layout.add_widget(self.chart_type_selector)

        # Ayanamsa setting
        _ayanamsa_modes = list(const.available_ayanamsa_modes.keys())[:-1]
        self.ayanamsa_selector = DropdownSelector(
            label_text="Ayanamsa Option",
            values=_ayanamsa_modes,
            initial_value=self.app.config["ayanamsa_mode"],
            on_select_callback=self.on_ayanamsa_change
        )
        layout.add_widget(self.ayanamsa_selector)

        # Chart spinner
        self.chart_names = [cht.replace("_str", "") for cht in const._chart_names[:-2]]
        self.chart_selector = DropdownSelector(
            label_text="Divisional Chart",
            values=self.chart_names,
            initial_value=self.chart_names[0],
            on_select_callback=self.on_chart_selected
        )
        layout.add_widget(self.chart_selector)

        # Method spinner
        methods, default_index = self.get_varga_methods(0)
        default_method = methods[default_index - 1] if default_index > 0 else "Select Method"
        self.method_selector = DropdownSelector(
            label_text="Calculation Method",
            values=methods,
            initial_value=default_method,
            on_select_callback=self.on_method_selected
        )
        layout.add_widget(self.method_selector)

        # Splash toggle
        self.splash_toggle = ToggleButton(
            text="Show Splash Screen" if self.app.config["show_splash"] else "Skip Splash Screen",
            state="down" if self.app.config["show_splash"] else "normal"
        )
        self.splash_toggle.bind(on_press=self.on_splash_toggle)
        layout.add_widget(Label(text="Splash Screen at Startup", color=_SETTINGS_TAB_COLOR))
        layout.add_widget(self.splash_toggle)

        self.add_widget(layout)

        # Save and Cancel buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        save_button = GetButtonWidget(text="Save", on_press_callback=self.on_save)
        cancel_button = GetButtonWidget(text="Cancel", on_press_callback=self.on_cancel)
        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)
        self.add_widget(button_layout)
        