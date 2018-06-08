import json
import time
import os
import threading
import requests
import docker


from opengym import utility


class TesterAgent(object):
    """The Docker Agent that Connects to a Docker container where the character runs."""

    def __init__(self,
                 port,
                 server='http://localhost'):

        self._server = server
        self._port = port
        self._timeout = 32
        self.session = requests.Session()

    def act(self, obs, reward, done):

        request_url = "http://localhost:{}/action".format(self._port)
        obs_serialized = json.dumps(obs, cls=utility.PommermanJSONEncoder)
        done = json.dumps(done, cls=utility.PommermanJSONEncoder)
        reward = json.dumps(reward, cls=utility.PommermanJSONEncoder)
        try:
            req = self.session.post(
                request_url,
                timeout=0.15,
                json={
                    "obs":
                        obs_serialized,
                    "reward": reward,
                    "done": done
                })
            action = req.json()['action']
        except requests.exceptions.Timeout as e:
            print('Timeout!')
            # TODO: Fix this. It's ugly.
            action = [0]
            if len(action) == 1:
                action = action[0]
        return action

    def ping(self):
        request_url = "http://localhost:{}/ping".format(self._port)
        return requests.get(request_url)
