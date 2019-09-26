#!/usr/bin/env python3
"""
The web server instance for mago.

"""
import pathlib
import cherrypy
from ws4py.server.cherrypyserver import WebSocketTool

from modules.match_websocket import (
    MatchManagerPlugin, WebSocketHandler, WebSocketAPI
)


class WebServer:

    def __init__(self, port=None):

        if port is None:
            self.__del__()

        self.port = port

        cwd = pathlib.Path(__file__).cwd()
        frontend_dir = cwd.parent / 'frontend'

        self._menu_conf = {
            '/': {
                'tools.gzip.on': True,
                # 'tools.staticdir.debug' : True,
                'tools.staticdir.on': True,
                'tools.staticdir.dir': frontend_dir
                # No default file. The index file is provided by the dispatcher.
            }
        }
        self._websocket_conf = {
            '/': {
                'tools.websocket.on': True,
                'tools.websocket.handler_cls': WebSocketHandler
            }
        }


    def start(self):

        cherrypy.config.update(
            {'server.socket_port': self.port,
             'server.socket_host': '0.0.0.0'  # Can be reached from everywhere
            }
        )

        # Add the SceneManagerPlugin to the server bus
        MatchManagerPlugin(cherrypy.engine).subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        cherrypy.tree.mount(
            GoMenu(), '/', self._menu_conf
        )
        # cherrypy.tree.mount(
        #     GoMatchDispatcher(), '/match', self._match_conf
        # )
        cherrypy.tree.mount(
            WebSocketAPI(), '/websocket', self._websocket_conf
        )
        # cherrypy.tree.mount(
        #     GoMenuApi(), '/api', self._menu_api_conf
        # )

        # Start the server
        cherrypy.engine.start()
        cherrypy.engine.block()

        return None

