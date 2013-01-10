#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import imp

class SpritzBot:
    """Twitter bot framework, loads extensions, connects via streaming
    API and hands over incoming statuses/events to extensions after
    converting json to pythonic objects.
    """
    extensions = {} # list of extensions loaded from directory.
    extensions_directory = os.getenv('EXTENSION_DIRECTORY',
                                     default='extensions')

    def __init__(self):
        """Loads all plugins found in ``self.extensions_directory``
        into a dictionary at ``self.extensions``."""
        re_extension = re.compile('[^.].*\.py$') # match => [name].py
        for extension_file in os.listdir(self.extensions_directory):
            if re_extension.match(extension_file):
                name = extension_file[:-3]
                ext_info = imp.find_module(name, [self.extensions_directory])
                extension = imp.load_module(name, *ext_info)
                self.extensions[name] = extension


if __name__ == '__main__':
    bot = SpritzBot()
    print bot.extensions
