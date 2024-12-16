# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

# Import actions
from .actions.WriteText import WriteText

class WriteTextStandalone(PluginBase): # Changed plugin class name
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        ## Register actions
        self.write_text_holder = ActionHolder(
            plugin_base = self,
            action_base = WriteText,
            action_id_suffix = "WriteTextStandalone", # Changed suffix
            action_name = self.lm.get("write-text-standalone.actions.write-text.name"), # Changed label
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.write_text_holder)

        # Register plugin
        self.register(
            plugin_name = self.lm.get("write-text-standalone.plugin.name"), # Changed plugin name
            github_repo = "https://github.com/orehren/WriteTextPlugin", # changed github location
            plugin_version = "0.1.0", # Changed plugin version
            app_version = "1.4.5-beta"
        )

