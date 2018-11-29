import os
import imp
import sys


class GeneralHelpers(object):
    """
    General object helper
    """

    @staticmethod
    def get_dir_contents(path):
        """
        Returns the contents of a directory recursively
        Args:
            path: string
        Returns: list
        """
        path_list = []
        full_path = os.path.abspath(path)
        for root, dirs, files in os.walk(full_path):
            if root and len(dirs) == 0 and len(files) != 0:
                for file_name in files:
                    path_list.append({
                        'path': root,
                        'file': file_name
                    })
        return path_list

    @staticmethod
    def get_dir_structure(path):
        """
        Returns the structure of the directory
        Args:
            path:
        Returns: list
        """
        app_path = os.path.abspath(path)
        path_list = []
        full_path = os.path.abspath(path)
        for root, dirs, files in os.walk(full_path):
            if root and len(dirs) == 0:
                path_list.append({
                    'path': root,
                    'url': root.replace(app_path, '')
                })
        return path_list

    @staticmethod
    def get_dir_structure_with_files(path):
        """
        Returns the directory structure with file array
        Args:
            path: string
        Returns: list
        """
        path_list = []
        full_path = os.path.abspath(path)
        for root, dirs, files in os.walk(full_path):
            if "__pycache__" not in root:
                # condition which assures skipping the modules/__init__.py file
                if len(files) is not 1:
                    if '\\' in root:
                        dir_contents = root.split('\\')
                    else:
                        dir_contents = root.split('/')
                    dir_contents_len = len(dir_contents) - 1
                    module_name = dir_contents[dir_contents_len]
                    path_list.append({
                        'route': root,
                        'files': files,
                        'module_name': module_name
                    })
        return path_list

    @staticmethod
    def get_app_routes():
        """
        Returns the app routes located inside module directory in routes.py files
        Returns: list
        """
        divider = '\\' if 'win' in sys.platform and 'darwin' not in sys.platform else '/'
        route_files = GeneralHelpers.get_dir_structure_with_files('modules') + \
                      GeneralHelpers.get_dir_structure_with_files('core{}sys_modules'.format(divider))
        app_routes = []
        for route_file in route_files:
            if 'routes.py' in route_file['files']:
                module = imp.load_source('routes.routes', route_file['route'] + '/routes.py')
                app_routes = app_routes + module.routes
        return app_routes

    @staticmethod
    def get_models():
        """
        Returns the list of models
        :return:
        """
        divider = '\\' if 'win' in sys.platform and 'darwin' not in sys.platform else '/'
        module_files = GeneralHelpers.get_dir_structure_with_files('core{}sys_modules'.format(divider)) + \
                       GeneralHelpers.get_dir_structure_with_files('modules')
        model_files = []
        for model_file in module_files:
            for file in model_file['files']:
                if '_model.py' in file:
                    module_name = file.replace('_model.py', '') \
                        if 'authentication' in model_file['module_name'] \
                        else model_file['module_name']
                    module = imp.load_source(
                        module_name + 'Model',
                        model_file['route'] + divider + module_name + '_model.py'
                    )
                    item = getattr(module, module_name + 'Model')
                    model_files.append(item)
        return model_files
