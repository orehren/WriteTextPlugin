from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import gtk modules
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk

import evdev

from evdev import ecodes

from loguru import logger as log
import os
import pyclip

import xkbcommon.xkb as xkb  # Corrected import

from typing import List


class WriteText(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = True

    def on_ready(self):
        self.set_media(
            media_path=os.path.join(
                self.plugin_base.PATH, "assets", "keyboard.png"
            )
        )

    def get_custom_config_area(self):
        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True,
            margin_top=5,
            margin_bottom=5,
            margin_start=5,
            margin_end=5,
        )

        self.main_box.append(
            Gtk.Label(
                label=self.plugin_base.lm.get("actions.write-text.text.title"),
                xalign=0,
                css_classes=["com_core447_OSPlugin-header"],
                margin_bottom=15,
            )
        )

        self.text_view = Gtk.TextView(
            editable=True,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            hexpand=True,
            vexpand=True,
        )
        self.main_box.append(self.text_view)
        self.buffer = self.text_view.get_buffer()

        self.load_defaults_for_custom_area()

        self.buffer.connect("changed", self.on_change)

        self.main_box.append(
            Gtk.Label(
                label=self.plugin_base.lm.get(
                    "actions.write-text.missing-permission.title"
                ),
                use_markup=True,
                css_classes=["bold", "warning"],
            )
        )

        return self.main_box

    def get_config_rows(self) -> list:
        self.delay_row = Adw.SpinRow.new_with_range(min=0, max=1, step=0.01)
        self.delay_row.set_title(
            self.plugin_base.lm.get("actions.write-text.delay.title")
        )
        self.delay_row.set_subtitle(
            self.plugin_base.lm.get("actions.write-text.delay.subtitle")
        )

        self.load_defaults_for_rows()

        self.delay_row.connect("changed", self.on_delay_changed)

        return [self.delay_row]

    def on_delay_changed(self, spin_row):
        settings = self.get_settings()
        settings["delay"] = spin_row.get_value()
        self.set_settings(settings)

    def load_defaults_for_custom_area(self):
        settings = self.get_settings()
        text = settings.get("text", "")
        self.buffer.set_text(text)
        log.debug(f"Loaded text from settings: {text}")

    def load_defaults_for_rows(self):
        settings = self.get_settings()
        delay = settings.get("delay", 0.01)
        self.delay_row.set_value(delay)
        log.debug(f"Loaded delay from settings: {delay}")

    def on_change(self, buffer):
        settings = self.get_settings()
        settings["text"] = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False
        )
        self.set_settings(settings)

    def on_key_down(self) -> None:
        settings = self.get_settings()
        text = settings.get("text")
        if text is None:
            return

        if self.plugin_base.ui is None:
            self.show_error(1)
            return

        delay = settings.get("delay", 0.01)

        
