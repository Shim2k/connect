#!/usr/bin/python

""" Alias manager with plugins (SSH, ..) """

import getopt
import os
import shutil
import subprocess
import sys
import pickle
import errno

class SSH(object):
    def __init__(self):
        self.name = 'ssh'

class Paths(object):
    ''' Paths used by the Connect module '''

    connection_path = ''

    def __init__(self):
        self.container = sys.path[0].split('/')
        self.invoker = os.path.dirname(os.path.realpath("path"))
        self.lib = '/'.join(self.container[:-1]) + '/lib/connect/'
        self.help = self.lib + 'help.py'
        self.map = self.lib + 'map.py'

    def connection_lib(self, name):
        ''' Returns the connection folder path '''
        self.connection_path = self.lib + name
        return self.connection_path

def is_using_plugin(argument):
    ''' Check if an argument is a plugin '''

    supported_plugins = [{
        'name' : 'default',
        'module': ''
    }, {
        'name' : 'ssh',
        'module': SSH()
    }]

    for name in enumerate(plugin['name'] for plugin in supported_plugins):
        if argument == name:
            return True

    return False


class Plugin(object):
    ''' Connection Plugin support '''

    # def get(self):
    #     return self.plugin

    # def set(name):
    #     self.plugin = name

class Connection(object):
    ''' Connection '''
    def __init__(self, specs):
        self.name = specs['name']
        self.command = specs['command']
        self.attachments = specs['attachments']
        self.plugin = specs['plugin'] or 'default'

    def save(self):
        ''' Saving Connection to disk '''

        paths = Paths()
        paths.connection_lib(self.name)

        connection_specification = {
            'name' : self.name,
            'plugin' : self.plugin,
            'command' : self.command
        }

        metadata = {
            'attachments' : self.attachments
        }

        prepare_storage(metadata['attachments'], paths)

        store_connection(connection_specification, paths.connection_path)

def prepare_storage(attachments, paths):
    ''' creating the connection folder and moving attachments files to it '''
    create_connection_storage(paths)
    store_attachments(attachments, paths.connection_path)

def create_connection_storage(paths):
    ''' creating the connection folder '''
    try:
        os.system('sudo chmod -R 777 ' + paths.lib)
        os.makedirs(paths.connection_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def store_attachments(attachments, connection_store):
    ''' storing attachments '''
    for attachment in attachments:
        shutil.copy2(attachment, connection_store + '/' + attachment.split('/')[-1])

def store_connection(specs, path):
    ''' storing the connection file to it's folder '''

    map_path = Paths().map

    connection_file = path + '/' + specs['name']

    conn_specs = {specs['name'] : specs}

    try:
        with open(connection_file, 'w+') as connection_file:
            pickle.dump(conn_specs, connection_file)

            if os.path.exists(map_path):
                with open(map_path, 'r') as map_file:

                    connections_map = pickle.load(map_file)
                    connections_map[specs['name']] = specs

                    with open(map_path, 'w') as map_file:
                        pickle.dump(connections_map, map_file)
            else:
                with open(map_path, 'w+') as map_file:
                    pickle.dump(conn_specs, map_file)

    except IOError as error:
        print error


def connection_exists(name, plugin='default'):
    ''' does a connection folder by this name exists? '''
    return os.path.isdir(Paths().connection_lib(name))

def connect (name, plugin='default'):
    ''' executing a connection '''

    with open(Paths().map, 'r') as map_file:
        connections_map = pickle.load(map_file)
        command = connections_map[name]['command']
        os.system(command)

def connection_list():
    ''' prints all connections '''
    try:
        with open(Paths().map, 'r') as connection_list_file:
            connection_list = pickle.load(connection_list_file)

            print '\nConnections:\n'

            for connection in connection_list:
                print connection_list[connection]
    except IOError as error:
        print "\nNo Connections yet"

    print '\n'

def remove_connection():
    ''' removing the connection folder from lib '''
    #TODO: Remove connections
    pass

def create_connection(specs):
    ''' creating an alias connection '''

    connection = Connection(specs)
    connection.save()
    return

class Colors(object):
    ''' Used to color the module's output '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def argument_parser(argv):
    ''' Parsing the user command for parameters '''

    plugin = 'default'

    try:
        opts, args = getopt.getopt(argv, "hn:c:i:", ["help", "name=", "command=", "identity="])
    except getopt.GetoptError:
        print "connect: bad options"
        print 'try connect -help'
        sys.exit()

    if not opts:
        if is_using_plugin(args[0]):
            ''' check for the next argument after the plugin.
                If there is none then throw the plugin's manual
            '''
            if sys.argv[2]:
                plugin = args[0]
            else:
                # fetch plugin's menual
                pass
        else:
            # check for a connection on the default 'plugin'
            connection_name = args[0]
            if not connection_exists(connection_name, 'default'):
                error = "A connection by this name does not exist!"
                print Colors().WARNING + Colors().UNDERLINE + error + Colors().ENDC
                return
            connect(connection_name, plugin)
        return

    new_connection = {
        'name' : '',
        'command' : '',
        'attachments' : [],
        'plugin' : plugin
    }

    for opt, arg in opts:

        if opt in ('-h', '--help'):
            throw('python ' + Paths().help)
            sys.exit()

        elif opt in ("-n", "--name"):
            new_connection['name'] = arg
        elif opt in ("-i", "--identity"):
            new_connection['attachments'].append(arg)
        elif opt in ("-c", "--command"):
            new_connection['command'] = arg

    arrange_attachment_paths(new_connection['attachments'])

    create_connection(new_connection)


def arrange_attachment_paths(attachs):

    ''' resolve the correct paths for the requested attachments '''

    paths = Paths()

    for i, attachment in enumerate(attachs):
        if attachment.startswith('./'):
            attachs[i] = paths.invoker + '/' + attachment[2:]
            continue
        if not attachment.startswith('/'):
            attachs[i] = paths.invoker + '/' + attachment

def throw(command, shell=True):
    ''' executing commands on the shell '''
    subprocess.call(command, shell=shell)

if __name__ == "__main__":
    if sys.argv[1:]:
        argument_parser(sys.argv[1:])
    else:
        connection_list()

