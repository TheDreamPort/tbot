import os
from celery.utils.log import get_logger
from celery.worker.autoscale import Autoscaler
from django.conf import settings

logger = get_logger(__name__)


class MinnowAutoScaler(Autoscaler):
    def __init__(self,  *args, **kwargs):
        super(MinnowAutoScaler, self).__init__(*args, **kwargs)
        self.min_concurrency = 0
        self.max_concurrency = os.cpu_count()

    def _maybe_scale(self, req=None):
        current_load = self._get_current_load()
        logger.debug(f"MinnowAutoScale settings {self.info()} current load is {current_load}")

        if current_load < settings.MINNOW_AUTOSCALER_MIN_LOAD and self.processes < self.max_concurrency:
            self.scale_up(1)
            return True
        elif current_load > settings.MINNOW_AUTOSCALER_MAX_LOAD and self.processes > self.min_concurrency:
            self.scale_down(1)
            return True

    # noinspection PyMethodMayBeStatic
    def _get_current_load(self):
        cpu_load_1_min, cpu_load_5_min, cpu_load_15_min = os.getloadavg()
        return cpu_load_1_min / (os.cpu_count() or 1)
