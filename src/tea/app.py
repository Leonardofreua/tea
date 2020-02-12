# -*- coding:utf-8 -*-

import logging
import sys
import threading
import webbrowser

from dynaconf import settings
from flask import Flask

from src.tea.ext import configuration
from src.tea.utils.ServerPort import find_free_port


def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app


def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app


class Tea:
    # def create_connection_with_database(self, logger):
    #     section = parser_settings()["support"]
    #     try:
    #         with psycopg2.connect(
    #             host=section["host"],
    #             database=section["database"],
    #             user=section["user"],
    #             password=section["passwd"],
    #             port=section["port"],
    #         ) as conn:
    #             cur = conn.cursor()
    #             cur.execute("SELECT 1")
    #     except psycopg2.OperationalError as e:
    #         self.generate_log(logger, "error", "Database Offline!", e)
    #         return False
    #     else:
    #         self.generate_log(logger, "info", "Database Online!")
    #         return True
    #
    # def check_network_status(self, logger):
    #     section = parser_settings()["site"]
    #     try:
    #         requests.get(section)
    #         return True
    #     except requests.ConnectionError as e:
    #         self.generate_log(logger, "error", "No Internet", e)
    #         return False
    #
    # def check_vpn_status(self, logger):
    #     ipr = pr.IPRoute()
    #     section = parser_settings()["vpn"]
    #
    #     for route in section["routes"]:
    #         value = ipr.route("show", dst=route)
    #         ipr.close()
    #         if len(value) > 0:
    #             return True
    #         else:
    #             self.generate_log(logger, "error", "VPN Offline!")
    #             return False
    #
    # def logger_settings(self):
    #     section = parser_settings()["log"]
    #     logger = logging.getLogger(__name__)
    #     formatter = logging.Formatter(self.stylize_message_level_name())
    #     file_handler = logging.FileHandler(section["file_name"])
    #     stream_handler = logging.StreamHandler()
    #
    #     file_handler.setFormatter(formatter)
    #     stream_handler.setFormatter(formatter)
    #
    #     logger.addHandler(file_handler)
    #     logger.addHandler(stream_handler)
    #
    #     return logger
    #
    # def generate_log(self, logger, level, message, details=None):
    #     if level == "info":
    #         logger.setLevel(logging.INFO)
    #         logger.info(self.stylize_message(message, level))
    #     elif level == "error":
    #         logger.setLevel(logging.ERROR)
    #         logger.error(self.stylize_message(message, level))
    #         if details is not None:
    #             logger.error(details)
    #
    # @staticmethod
    # def stylize_message(message, level):
    #     return (
    #         Style.BRIGHT
    #         + f"{Fore.GREEN if level == 'info' else Fore.RED}"
    #         + f"{message}"
    #     )
    #
    # @staticmethod
    # def stylize_message_level_name():
    #     return (
    #         Style.BRIGHT
    #         + Fore.WHITE
    #         + "["
    #         + "%(levelname)s"
    #         + Fore.WHITE
    #         + "] "
    #         + "%(asctime)s: %(message)s"
    #     )

    @staticmethod
    def create_web_server(server_host, server_port):
        app = create_app()
        try:
            app.run(
                host=server_host,
                port=server_port,
                use_reloader=settings.USE_RELOADER,
                debug=settings.DEBUG,
                threaded=settings.THREADED,
            )
        except IOError:
            app.logger.error(f"Error starting the app server: {sys.exc_info()}")

    @staticmethod
    def launch_browser(url):
        webbrowser_open_new = 2
        try:
            threading.Timer(
                1.25, lambda: webbrowser.open(url, webbrowser_open_new)
            ).start()
        except webbrowser.Error as e:
            logging.warning("No web browser found: %s." % e)


def main():
    server_host = settings.ALLOW_HOSTS[0]
    server_port = find_free_port()
    app_server_url = f"http://{server_host}:{server_port}/"

    tea = Tea()

    tea.launch_browser(app_server_url)
    tea.create_web_server(server_host, server_port)


if __name__ == "__main__":
    main()
