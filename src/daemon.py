from logger import root_logger as logger
from threading import Timer


class DaemonApplication():

    def __init__(self, pid_file):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = pid_file
        self.pidfile_timeout = 5
        self.presented = False
        self.stopped = False

    def setup_daemon_context(self, daemon_context):
        self.daemon_context = daemon_context

    def handle_exit(self, signum, frame):
        try:
            if not self.stopped:
                logger.info('Daemon is stopping on signal {0}'.format(signum))
                t = Timer(0.1, self.__handle_exit2)
                t.start()

        except Exception as e:
            logger.exception(e)

    def __handle_exit2(self):
        logger.info('Setting up stop event...')
        self.stopped = True
        self.daemon_context.stop_event.set()

    def run(self):

        while not self.daemon_context.stop_event.wait(1):

            if self.stopped:
                break

            try:
                try:

                    logger.info("Running...")

                except Exception as e:
                    logger.exception(e)

            finally:
                logger.debug("Sleeping...")

        logger.info('Daemon has been stopped')

