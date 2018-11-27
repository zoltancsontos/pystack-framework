from modules.Settings.Settings_resource import SettingsResource

routes = [
    # Settings api routes
    {'url': '/v1/settings', 'controller': SettingsResource()},
    {'url': '/v1/settings/{uid}', 'controller': SettingsResource()}
]
