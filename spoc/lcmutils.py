#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#* this program is free software: you can redistribute it and/or
#* modify it under the terms of the GNU General Public License as
#* published by the Free Software Foundation, either version 3 of the
#* License, or (at your option) any later version.
#*
#* this program is distributed in the hope that it will be useful, but
#* WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#* General Public License for more details.
#*
#* You should have received a copy of the GNU General Public License
#* along with this program.  If not, see
#* <http://www.gnu.org/licenses/>.
#*
#* Library    : the Lizard Configuration Manager library
#*
#* Project    : K0004
#* Project    : L0076
#* Project    : M0030
#*
#* $Id: lcmlib.py 24231 2011-09-22 12:52:40Z mario.frasca $
#*
#* initial programmer :  Mario Frasca
#* initial date       :  20090531
#**********************************************************************


def read_configuration(config_file_name, slashify_section=None):
    """reads a INI file and returns it as a dictionary of dictionaries.

    this function returns a 2-tuple, first coordinate is the order of
    the sections.
    """

    import ConfigParser
    # read the configuration (passed as parameter to the script)
    configParser = ConfigParser.ConfigParser()
    configParser.read(config_file_name)
    config = dict([(i, dict(configParser.items(i))) for i in configParser.sections()])
    ## TODO: not necessary in python 2.7 and 3.1, where the
    ## ConfigParser module uses collections.OrderedDict by default
    config_order = [i.strip("[] \r\n")
                    for i in file(config_file_name).readlines()
                    if i.strip().startswith('[')]

    if slashify_section is not None:
        # make sure directory names end with a '/'
        for key, value in list(config[slashify_section].items()):
            config[slashify_section][key] = slashify(value)

    return config_order, config


def slashify(somepathname):
    """corrects and completes the path name with forward slashes.

    replaces all backslashes to forward slashes, makes sure the path
    ends with one, causes an exception if the path name does not
    identify a directory.

    >>> slashify('/')
    '/'
    >>> slashify('/bin')
    '/bin/'
    >>> slashify('')
    '/'
    """

    somepathname = somepathname.replace("\\", '/')
    if not somepathname.endswith('/'):
        somepathname += '/'
    return somepathname
