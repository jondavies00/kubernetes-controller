from kubernetes_controller.consts import ResourceType


class FauxAPI:
    """Models the K8s API Server"""

    def __init__(self) -> None:
        self.current_state: dict = {ResourceType.JOB: {}, ResourceType.POD: {}}
        self.desired_state: dict = {ResourceType.JOB: {}, ResourceType.POD: {}}

    def get_actual_state(self, type_: ResourceType) -> dict:
        """Returns the actual state of the given resource type"""
        return self.current_state[type_]

    def get_desired_state(self, type_: ResourceType):
        return self.desired_state[type_]

    def update_desired_state(self, type_: ResourceType, new_state: dict) -> None:
        self.desired_state[type_].update(new_state)
