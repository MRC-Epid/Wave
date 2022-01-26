from PyQt5.QtCore import QSettings


class SettingsManager:
    """Create a settings manager to handle all settings."""
    widget_mappers = {"QCheckBox": ("isChecked", "setChecked", bool),
                      "QRadioButton": ("isChecked", "setChecked", bool)}

    def __init__(self):
        """Use QSettings to create a repository of all the settings."""
        self.settings = QSettings("SuperChess", "settings")

    def update_widgets_from_settings(self, repository):
        """Get setting values to set widget states from them."""
        for setting_name, widget in repository.items():
            widget_name = widget.__class__.__name__
            getter, setter, data_type = self.widget_mappers.get(widget_name)
            setting_value = self.settings.value(setting_name, type=data_type)

            if setter and setting_value is not None:
                update_value = getattr(widget, setter)
                update_value(setting_value)

    def update_settings_from_widgets(self, repository):
        """Get widget states to set setting values from them."""
        for setting_name, widget in repository.items():
            widget_name = widget.__class__.__name__
            getter, setter, data_type = self.widget_mappers.get(widget_name)

            if getter:
                widget_state = getattr(widget, getter)
                setting_value = widget_state()

                if setting_value is not None:
                    self.settings.setValue(setting_name, setting_value)


settings_manager = SettingsManager()