"""Implementation of a simple deterministic agent using Docker."""

"""Implementation of a simple deterministic agent using Docker."""

from opengym import agents
from opengym.runner import DockerAgentRunner
import sys


class MyAgent(DockerAgentRunner):
    def __init__(self, env_gym = "CartPole-v0"):
        self._agent = agents.GymAgent(env_gym)

    def act(self,  observation, reward, done):
        return self._agent.act(observation, reward, done)


def main():
    if len(sys.argv) > 1:
        env_gym = sys.argv[1]
        agent = MyAgent(env_gym)
    else:
        agent = MyAgent()
    agent.run()


if __name__ == "__main__":
    main()
