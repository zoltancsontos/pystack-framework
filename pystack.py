import sys
import os
import re
from subprocess import call

# ==================================================
# pystack framework command line interface logic
# @version: 1.0.0
# @author: Csontos_Zoltan@solarturbines.com
# ==================================================
args = sys.argv

# ==================================================
# Constants definitions
# ==================================================
TXT_RESOURCES_PATH = 'core/.core-resources/'
MODULES_PATH = 'modules/'


# ==================================================
# Private functions
# ==================================================
def camel_case_to_underscore(item):
    """
    Converts a string from CamelCase to underscore
    :param item: str item
    :return: str
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# ==================================================
# Generators
# ==================================================
def throw_error(message):
    """
    Generates an error message
    :param message: String
    :return:
    """
    print('ERROR: ' + str(message))


def __load_txt_resource__(path):
    """
    Loads a txt file template
    :param path:
    :return:
    """
    txt_file = open(path, "r")
    return txt_file


def create(creatable_type, py_name, py_model="", py_routes="", py_resource="", py_page="", py_template=""):
    """
    Creates a certain resource type
    :param creatable_type:
    :param py_name:
    :param py_model:
    :param py_routes:
    :param py_resource:
    :param py_page:
    :param py_template:
    :return:
    """
    os.mkdir(MODULES_PATH + py_name)

    # Create a blank init file
    init_file = open(MODULES_PATH + py_name + '/__init__.py', 'w')
    init_file.write('')
    init_file.close()

    # Create the model file
    model_file = open(MODULES_PATH + py_name + '/' + py_name + '_model.py', 'w')
    model_file.write(py_model)
    model_file.close()

    # Create the routes file
    routes_file = open(MODULES_PATH + py_name + '/routes.py', 'w')
    routes_file.write(py_routes)
    routes_file.close()

    if creatable_type == 'resource':
        # Create the resource files
        resource_file = open(MODULES_PATH + py_name + '/' + py_name + '_resource.py', 'w')
        resource_file.write(py_resource)
        resource_file.close()
    else:
        # Create the page files
        page_file = open(MODULES_PATH + py_name + '/' + py_name + '_page.py', 'w')
        page_file.write(py_page)
        page_file.close()

        # Create the template files
        template_file = open(MODULES_PATH + py_name + '/' + py_name + '_template.html', 'w')
        template_file.write(py_template)
        template_file.close()


def get_arg_based_on_config_param(conf_param):
    """
    Returns a s single arg based on command line option
    :param conf_param:
    :return: Dictionary
    """
    item = None
    for arg in args:
        if conf_param in arg:
            raw_conf = arg.split('=')
            item = {
                'param': raw_conf[0],
                'value': raw_conf[1]
            }
    return item


def args_contain_str(search_str):
    """
    Checks if any of the argument values is containing a certain string
    :param search_str: string
    :return:
    """
    for item in args:
        if search_str in item:
            return True
    return False


def check_if_item_exists(item_path):
    """
    Checks if the item already exists
    :param item_path: string
    :return:
    """
    return os.path.exists(item_path)


# ==================================================
# Raw resource definitions
# ==================================================
pystack_logo = __load_txt_resource__(TXT_RESOURCES_PATH + 'pystack_logo.txt').read()
blank_model = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_model.txt').read()
blank_page = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_page.txt').read()
blank_page_routes = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_page_routes.txt').read()
blank_page_template = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_page_template.txt').read()
blank_resource = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_resource.txt').read()
blank_resource_routes = __load_txt_resource__(TXT_RESOURCES_PATH + 'blank_resource_routes.txt').read()

# ==========================================================
#
# Resource creation logic
#
# ==========================================================
if 'create' in args and ('resource' in args or 'page' in args):
    item_name = args[3] if len(args) >= 4 else None
    item_type = 'resource'
    item_url = args[4] if len(args) >= 5 else item_name

    model = ''
    page = ''
    routes = ''
    template = ''
    resource = ''
    resource_routes = ''

    model = ''
    routes = ''
    resource = ''
    page = ''
    template = ''

    if 'page' in args:
        item_type = 'page'

    if item_type is 'resource':
        model = blank_model.replace('{}', item_name)
        routes = blank_resource_routes.replace('{}', item_name).replace('{url}', item_url)
        resource = blank_resource.replace('{}', item_name)
    else:
        model = blank_model.replace('{}', item_name)
        routes = blank_page_routes.replace('{}', item_name).replace('{url}', item_url)
        page = blank_page.replace('{}', item_name)
        template = blank_page_template.replace('{}', item_name)

    db_item_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item_name)
    db_table_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', db_item_name).lower()
    model = model.replace(item_name + '_Model', db_table_name)

    if not check_if_item_exists(MODULES_PATH + item_name):
        create(item_type, item_name, model, routes, resource, page, template)
    else:
        throw_error('Item with the name "' + item_name + '" already exists, ' +
                    'please choose different resource / page name')

# ==========================================================
#
# Application run logic
#
# ==========================================================
elif 'run' in args:
    port_str = '--port=8888'
    port_arg = get_arg_based_on_config_param('--port')
    if port_arg is not None:
        port_str = '--port={}'.format(port_arg['value'])
    print(pystack_logo)
    print("")
    try:
        call(["waitress-serve", port_str, "app:app"])
    except KeyboardInterrupt as ki:
        print("Shutting down PyStack...")
# ==========================================================
#
# Help logic
#
# ==========================================================
elif '--help' in args:
    print(pystack_logo)
    print("")
    print("python pystack.py run --port=port - runs the application on the specified port")
    print("python pystack.py create page PageName page-url - creates a page")
    print("python pystack.py create resource ResourceName resource-url - creates a standard rest api")
# ==========================================================
#
# Error handling
#
# ==========================================================
else:
    throw_error('pystack needs at least 3 arguments for options please see --help')
