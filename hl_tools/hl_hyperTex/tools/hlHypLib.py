#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pprint

import config
reload(config)

import hlHypFuncs as hyp_funcs
reload(hyp_funcs)

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(config._logging_level)

import pymel.core as pm

DIRECTORY = os.path.join(os.path.dirname(__file__), 'hlHyp_data')

class HypLibrary(dict):
    def createDir(self, directory=DIRECTORY):
        """
        Create the directory path if not exists
        """
        if not os.path.exists(directory):
            os.mkdir(directory)
            _logger.debug("Directory created: {}".format(directory))

    def save(self, shader, directory=DIRECTORY, **info):
        """
        Save a maya and json files with information of each file to the directory
        """

        name = shader.name()

        self.createDir()
        mayaFile = "{}.ma".format(name)
        infoFile = "{}.json".format(name)

        filePath = os.path.join(directory, mayaFile)
        infoPath = os.path.join(directory, infoFile)

        connections = str(shader.listConnections(c=1))
        types = pm.objectType(pm.selected()[0])

        _logger.debug("Maya file saved to {}".format(filePath))
        _logger.debug("Info file saved to {}".format(infoPath))


        info['name'] = name
        info['path'] = mayaFile
        info['type'] = types
        # info['connections'] = connections

        ### export the maya file to the directory ###
        pm.exportSelected(filePath, exportSelected=1, type='mayaAscii', force=1)
        if os.path.isfile(filePath):
            _logger.info('Maya file exported to {}'.format(filePath))

        ## write the json file with information ###
        with open(infoPath, 'w') as f:
            json.dump(info, f , indent=4)
            _logger.debug("Info file saved to {}".format(infoPath))

    def _get_directory(self, directory=DIRECTORY):
        """
        Return the directory path
        """
        return directory

    def find(self, directory=DIRECTORY):
        """
        List the Maya and Info files from the directory path

        Args:
            directory ([type], optional): [description]. Defaults to DIRECTORY.

        Raises:
            InputException: [description]
        """
        if not os.path.exists(directory):
            raise InputException('Path not existing: {}'.format(directory))

        files = os.listdir(directory)

        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:

            name, ext = os.path.splitext(ma)
            mPath = os.path.join(directory, ma)


            infoFile = "{}.json".format(name)

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    data = json.load(f)
            else:
                data = {}

            data['name'] = name
            data['path'] = os.path.join(directory, ma)
            data['info'] = infoFile

            self[name] = data

            # _logger.debug(pprint.pformat(self))

    def load(self, name):
        """
        Import the file by name flag
        """
        path = self[name]['path']

        return pm.importFile(path, usingNamespaces=0, returnNewNodes=1)

    def reference(self, name):
        """
        Reference the file by name flag
        """
        path = self[name]['path']

        return pm.createReference(path, usingNamespaces=0, returnNewNodes=1)

    def delete(self, name):
        """
        Delete all the files from directory path by name flag
        """
        item = self.get(name)
        print(item)
        if item:
            for i, p in item.items():
                if os.path.isfile((p)):
                    try:
                        os.remove(p)
                        _logger.debug('{} was removed from disk'.format(p))
                    except:
                        __logger.debug('{} was not removed from disk'.format(p))
            return True
        return False