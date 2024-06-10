from threading import Lock, Thread
import time
import pytest

from kubernetes_controller.api import FauxAPI
from kubernetes_controller.consts import ResourceType
from kubernetes_controller.controller import G, JobController


API = FauxAPI()


@pytest.fixture
def api():
    yield API


@pytest.fixture
def job_controller(api):
    yield JobController(api)


def start_job_controller(jc: JobController):  # function doing intense computation
    jc.run_loop()


def test_spinup_pod(job_controller):
    t = Thread(target=start_job_controller, args=(job_controller,))
    t.start()

    API.update_desired_state(ResourceType.JOB, {"job1": {"completed": True}})
    time.sleep(5)
    assert API.get_desired_state(ResourceType.JOB) == {"job1": {"completed": True}}
    assert API.get_actual_state(ResourceType.POD) == {"running": ["pod-job1"]}
    G.kill = True
