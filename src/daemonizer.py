#!/usr/bin/env python
from sys import argv
from daemon import DaemonApplication
from logger import root_logger as logger
from daemon import runner
import signal
from multiprocessing import Event
from config import DAEMON_WORKING_DIRECTORY, DAEMON_PID_FILE


def attach_signal(signal_map, handler):
    skip = ['SIG_DFL', 'SIGSTOP', 'SIGKILL']
    for i in [x for x in dir(signal) if x.startswith("SIG")]:
        if not i in skip:
            signum = getattr(signal, i)
            signal_map[signum] = handler


if __name__ == '__main__':
    try:
        logger.info(argv)

        app = DaemonApplication(DAEMON_PID_FILE)

        daemon_runner = runner.DaemonRunner(app)
        daemon_runner.daemon_context.detach_process = not __debug__
        daemon_runner.daemon_context.files_preserve = [h.stream for h in logger.root.handlers]
        daemon_runner.daemon_context.working_directory = DAEMON_WORKING_DIRECTORY
        attach_signal(daemon_runner.daemon_context.signal_map, app.handle_exit)
        daemon_runner.daemon_context.stop_event = Event()

        app.setup_daemon_context(daemon_runner.daemon_context)

        daemon_runner.do_action()

    except Exception as e:
        logger.exception(e)