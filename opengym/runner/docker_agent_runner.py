import abc
import logging
import json
from flask import Flask, jsonify, request

logger = logging.getLogger(__name__)


class DockerAgentRunner(metaclass=abc.ABCMeta):

    """Abstract base class to implement Docker-based agent"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def act(self,observation, reward, done):
        """Given an observation, returns the action the agent should"""
        raise NotImplementedError()

    def run(self, host="0.0.0.0", port=10084):
        """Runs the agent by creating a webserver that handles action requests."""
        app = Flask(self.__class__.__name__)

        @app.route("/action", methods=["POST"])
        def action(): #pylint: disable=W0612
            data = request.get_json()
            observation = data.get("obs")
            observation = json.loads(observation)
            reward = data.get("reward")
            reward = json.loads(reward)
            done = data.get("done")
            done = json.loads(done)
            action = self.act(observation, reward, done)
            return jsonify({"action": action})

        @app.route("/ping", methods=["GET"])
        def ping(): #pylint: disable=W0612
            return jsonify(success=True)

        logger.info("Starting agent server on port %d", port)
        app.run(host=host, port=port)
