#!/usr/bin/env python3
"""

"""
import re
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin
from ws4py.websocket import WebSocket

# configure the ws4py logger
import logging
from ws4py import configure_logger
configure_logger(level=logging.DEBUG)
logger = logging.getLogger('ws4py')

import modules.match_manager as match_manager


class MatchManagerPlugin(WebSocketPlugin):
    """
    The WebSocket plugin added to the servers bus.

    """
    def start(self):
        """
        Start the websocket plugin and add (subscribe) routines to add, remove
        or send to a client.

        """
        WebSocketPlugin.start(self)
        self.bus.subscribe('websocket-add', self.websocket_add)
        self.bus.subscribe('websocket-remove', self.websocket_remove)
        self.bus.subscribe('websocket-send', self.websocket_send)

    def stop(self):
        """
        Stop the websocket plugin and remove (unsubscribe) the routines to add,
        remove or send to the client.

        """
        WebSocketPlugin.stop(self)
        self.bus.unsubscribe('websocket-add', self.websocket_add)
        self.bus.unsubscribe('websocket-remove', self.websocket_remove)
        self.bus.unsubscribe('websocket-send', self.websocket_send)

    def websocket_add(self, match_id, websocket):
        """
        Add a websocket connection to a scene.

        Args:
         scene_hash (str): The hash of the scene to which we want to append a
          websock connection.
         websocket (ws4py.websocket.WebSocket): The WebSocket instance that
          connects to the scene.

        """
        target_match = match_manager.matches.match(match_id)

        # scene does not exist
        if target_match is None:
            return None

        target_match.websocket_add(websocket)

    def websocket_remove(self, match_id, websocket):
        """
        Remove a websocket connection from a scene.

        Args:
         scene_hash (str): The hash of the scene from which we want to remove a
          websock connection.
         websocket (ws4py.websocket.WebSocket): The WebSocket instance that
          connected to the scene.

        """
        target_match = match_manager.matches.match(match_id)

        # scene does not exist
        if target_match is None:
            return None

        target_match.websocket_remove(websocket)

    def websocket_send(self, match_id, message):
        """
        Send a message to all the WebSocket instances that connect to the
        scene.

        Args:
         scene_hash (str): The hash of the scene to which we want to send a
          message.
         message (JSON parsable object): Something we want to transmit to all
          the connected WebSocket instances. Must be parsable by json.dumps(),
          so strings, dicts, arrays and so on.

        """
        target_match = match_manager.matches.match(match_id)

        # scene does not exist
        if target_match is None:
            return None

        target_match.websocket_send(message)


class WebSocketHandler(WebSocket):
    """
    Handler for the WebSocket connections.

    Takes care of adding and removing websocket instances to a scene.

    """
    def opened(self):
        """
        Add a WebSocket instance to a scene when a websocket is opened.

        """
        # check if scene_hash has been added to the websocket
        if hasattr(self, 'match_id'):
            cherrypy.engine.publish('websocket-add', self.match_id, self)
        else:
            pass

    def closed(self, code, reason):
        """
        Remove a WebSocket instance from a scene when the socket is closed.

        """
        # check if scene_hash has been added to the websocket
        if hasattr(self, 'match_id'):
            cherrypy.engine.publish('websocket-remove', self.match_id, self)
        else:
            pass

    # # A hook for receiving messages from the client. Maybe used later
    # def received_message(self, message):
    #     cherrypy.engine.publish('websocket-send', self.scene_hash, message)


class WebSocketAPI(object):
    """
    The app for WebSocket support. Essentially just dispatches urls.

    """
    def _cp_dispatch(self, vpath):
        """
        The dispatcher method for calling .../websocket/(#scene_hash)

        Strips the first argument from the vpath. Checks if that argument is
        in the form of a sha1 hash. If it is, returns a WebSocketSession, else
        returns None.

        Args:
         vpath (list): A list of url segments after .../websocket/

        """
        match_id = vpath.pop(0)

        if (re.search('^[0-9a-f]{40}$', match_id)):
            cherrypy.request.params['match_id'] = match_id
            return WebSocketSession()
        else:
            return None


class WebSocketSession:
    """
    The dispatched WebSocketSession.

    Exposes one default page that gets called with the scene_hash.

    """
    @cherrypy.expose
    def default(self, match_id):
        """
        The only method that gets exposed.

        Compares the scene_hash with the existing scenes on the server. If the
        scene_hash is found we attach a WebSocketHandler and add the scene_hash
        to the handler.

        Args:
         match_id (str): The hash of the scene we want to append.

        """
        active_matches = match_manager.matches.active_matches()

        if match_id in active_matches:
            # save the scene hash
            cherrypy.request.ws_handler.match_id = match_id

        return None

