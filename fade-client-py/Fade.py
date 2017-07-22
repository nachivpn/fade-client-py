import threading
import queue
import ftpclient
import requests
import json
import FadeBuilder
import pickle as pickle


class FadeExecutor(object):
    def __init__(self):
        """"Initiating a new FadeExecutor"""
        self._shutdown_lock = threading.Lock()
        self._work_queue = queue.Queue()
        self.ftp_server = ftpclient.setup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def submit(self, fn, *args, **kwargs):
        """"Submit a new task to the queue

        1. Serialize fn(ser, kwargs)
        2. Package all dependencies
        3. Build executable
        4. Send to server
        """

        with self._shutdown_lock:
            name = FadeBuilder.serialize(fn, args, kwargs)
            module = fn.__module__

            exe_name = None  # Badisa.build(ser)

            exe_key = ftpclient.upload(self.ftp_server, exe_name)  # Fabio.upload(exe)
            url = "www.Nachi.com"
            payload = {"name": "exe name","args": name, "module": module, "key": exe_key}
            requests.post(url=url, data=json.dumps(payload))  # send exe to Nachi

            results_key = requests.get(url)  # get results key from Nachi
            f = FadeFuture(results_key.text, self.ftp_server)  # apply future to our needs? requires FadeFuture?

            return f


# class _FadeWorkItem(object):
#     def __init__(self, future, fn, ser, kwargs):
#         self.future = future
#         self.fn = fn
#         self.ser = ser
#         self.kwargs = kwargs
#
#     def run(self):
#
#         # 1. post (allert new job)
#         # 2. send (transfer JSON of exec name and exec)
#         # 3. get (ask for job id)
#         # 4. receive (use job id to get results)
#
#         # flow is threading
#         try:
#             result = self.fn(*self.ser, **self.kwargs)
#         except BaseException as e:
#             self.future.set_exception(e)
#         else:
#             self.future.set_result(result)


class FadeFuture:
    """Represents the result of an asynchronous computation."""
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'

    def __init__(self, results_key, ftp_server):
        """Initializes the future. Should not be called by clients."""
        self._condition = threading.Condition()
        self._state = FadeFuture.PENDING
        self._result = None
        self._exception = None
        self.results_key = results_key
        self.ftp_server = ftp_server

    def __repr__(self):
        with self._condition:
            if self._state == FadeFuture.FINISHED:
                if self._exception:
                    return '<{:>} at {:#x} state={:>} raised {:>}>'.format(
                        self.__class__.__name__,
                        id(self),
                        self._state.lower(),
                        self._exception.__class__.__name__)
                else:
                    return '<{:>} at {:#x} state={:>} raised {:>}>'.format(
                        self.__class__.__name__,
                        id(self),
                        self._state.lower(),
                        self._result.__class__.__name__)
            return '<{:>} at {:#x} state={}>'.format(
                self.__class__.__name__,
                id(self),
                self._state.lower())

    def done(self):
        """Return True of the future was cancelled or finished executing."""
        with self._condition:
            return self._state in [FadeFuture.FINISHED]

    def running(self):
        """Return True if the future is currently executing."""
        with self._condition:
            return self._state == FadeFuture.RUNNING

    def __get_result(self):
        if self._exception:
            raise self._exception
        else:
            return self._result

    def fetch(self):
        """Asks the server (NACHI) for results, block until results returned"""

        ftpclient.download(self.ftp_server, self.results_key)  # get results from nachi

        result = FadeBuilder.deserialize(self.results_key)

        if result is BaseException:
            self.set_exception(result)
        else:
            self.set_result(result)

        self._state = FadeFuture.FINISHED

        return

    def result(self):
        """Return the result of the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the result if the future
                isn't done. If None, then there is no limit on the wait time.
        """
        with self._condition:
            self.fetch()
            return self.__get_result()

    def exception(self):
        """Return the exception raised by the call that the future represents.

        Returns:
            The exception raised by the call that the future represents or None
            if the call completed without raising.
        """

        with self._condition:
            self.fetch()
            return self._exception

    def set_result(self, result):
        """Sets the return value of work associated with the future.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            self._result = result
            self._state = FadeFuture.FINISHED
            self._condition.notify_all()

    def set_exception(self, exception):
        """Sets the result of the future as being the given exception.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            self._exception = exception
            self._state = FadeFuture.FINISHED
            self._condition.notify_all()


class Error(Exception):
    """Base class for all future-related exceptions."""
    pass


class TimeoutError(Error):
    """The operation exceeded the given deadline."""
    pass
