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
        self.connection_map = self.lib + 'map.py'

    def connection_lib(self, name):
        ''' Returns the connection folder path '''
        self.connection_path = self.lib + name
        return self.connection_path

def is_plugin(argument):
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
    print 'storing files..'
    for attachment in attachments:
        shutil.copy2(attachment, connection_store)

def store_connection(specs, path):
    ''' storing the connection file to it's folder '''
    try:
        with open(path, 'a') as file:
            file.write(specs)
    except IOError as error:
        print error


def check_for_connection(name, plugin):
    ''' does a connection folder by this name exists? '''
    return os.path.isdir(Paths().connection_lib(name))

def add_connection(name, command):
    ''' Add a connection to the data file '''
    data = "%s,%s\n" % (name, command)
    try:
        with open(Paths.DATA_FILE, 'a') as file:
            file.write(data)
        print bcolors.BOLD + "Connection added successfully!" + bcolors.ENDC
    except IOError as e:
        print bcolors.WARNING + bcolors.UNDERLINE + "try using sudo to add connections!" + bcolors.ENDC


def connect (name, plugin):
    ''' executing a connection '''
    connection = Connection('a', 'b', 'c', 'd')
    connection.show_paths()

    with open(Paths.DATA_FILE, 'r') as file:
        for line in file.readlines():
            connection = line.split(',')
            if connection[0] == name:
                print 'Connecting to', connection[0] + '...'
                os.system(connection[1])


def connection_list ():
    ''' prints all connections '''
    print 'Connections list\n'
    
    with open(Paths().connection_map, 'r') as file:
        for line in file.readlines():
            print line

def remove_connection ():
    ''' removing the connection folder from lib '''
    #TODO: Remove connections
    a = 1

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

    used_plugin = 'default'
    try:
        opts, args = getopt.getopt(argv, "hn:c:i:", ["help", "name=", "command=", "identity="])
    except getopt.GetoptError:
        print "connect: bad options"
        print 'try connect -help'
        sys.exit()

    if is_plugin(sys.argv[1]):
        # check for the next argument after the plugin. If there is none then throw the plugin's manual
        if sys.argv[2]:
            used_plugin = sys.argv[1]
    else:
        # check for a connection on the default 'plugin'
        connection_name = sys.argv[1]

    if not check_for_connection(connection_name, 'default'):
        print Colors().WARNING + Colors().UNDERLINE + "A connection by this name does not exist!" + Colors().ENDC 
        return

    new_connection = {
        'name' : '',
        'command' : '',
        'attachments' : [],
        'plugin' : used_plugin
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

    arrange_attachment_paths(new_connection['name'], new_connection['attachments'])

    create_connection(new_connection)


def arrange_attachment_paths(connection_name, attachs):

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

