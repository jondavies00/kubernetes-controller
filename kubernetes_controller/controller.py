"""Defines the controller abstract base class"""

from abc import ABC
from threading import Lock
import time

from kubernetes_controller.api import FauxAPI
from kubernetes_controller.consts import ResourceType

# Example job
"""
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
"""


class globalVars:
    pass


G = globalVars()  # empty object to pass around global state
G.lock = Lock()  # not really necessary in this case, but useful none the less
G.value = 0
G.kill = False


class Controller(ABC): ...


class JobController(Controller):
    def __init__(self, api: FauxAPI) -> None:
        super().__init__()
        self.api = api  # represents the api requests
        self.desired_state = {}

    def update_desired_state(self, desired: dict):
        self.desired_state.update(desired)

    def run_loop(self):
        """Sends API requests to change Pods in order to get the Job
        into a desired state."""
        while not G.kill:
            current_jobs_state = self.api.get_actual_state(ResourceType.JOB)
            desired_jobs_state = self.api.get_desired_state(ResourceType.JOB)
            print(current_jobs_state)
            print(desired_jobs_state)
            time.sleep(1)
        G.kill = False
