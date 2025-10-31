
class Config:

    def validate(self, config):
        if not isinstance(config, dict):
            return False
        required_keys = {"name", "version", "settings"}
        if not required_keys.issubset(config.keys()):
            return False
        if not isinstance(config["name"], str) or not config["name"]:
            return False
        if not isinstance(config["version"], str) or not config["version"]:
            return False
        if not isinstance(config["settings"], dict):
            return False
        return True

    def get_template_from_config(self, config):
        if not self.validate(config):
            return None
        template = {
            "template_name": config["name"] + "_template",
            "template_version": config["version"],
            "template_settings": config["settings"].copy()
        }
        return template
