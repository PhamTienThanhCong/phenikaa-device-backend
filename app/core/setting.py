
class SettingCore:
    def __init__(self):
        self.name = "API for Device Management"
        self.version = "1.0.0"
        self.description = "This API is for managing devices in a company"
        self.base_url = "http://127.0.0.1:8000"

    def get_setting(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "base_url": self.base_url
        }
    
def get_setting():
    setting = SettingCore()
    return setting.get_setting()