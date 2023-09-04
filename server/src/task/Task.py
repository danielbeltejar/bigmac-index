class Task(object):

    def __init__(self):
        self._start()
        self._stop()

    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError
