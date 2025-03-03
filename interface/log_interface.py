from PySide6.QtCore import Qt
from qfluentwidgets import TextBrowser
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from loguru import logger
from enum import Enum
import html


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    SUCCESS = 'SUCCESS'

    @property
    def color(self):
        return {
            LogLevel.DEBUG: "#e2734a",
            LogLevel.INFO: "#DCDCDC",
            LogLevel.WARNING: "#FFA500",
            LogLevel.ERROR: "#FF0000",
            LogLevel.CRITICAL: "#8B0000",
            LogLevel.SUCCESS: "#00FF00"
        }.get(self, "gray")

class LogBrowser(TextBrowser):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("logBrowser")
        self.setPlaceholderText("Log messages will appear here...")


    def add_log(self, message):
        # Create an HTML string with the chosen color
        log_msg = self.format_log(message)
        self.append(log_msg)

    def clear_logs(self):
        self.clear()

    def format_log(self, message):
        record = message.record
        # Extract log parts
        msg = record.get("message")
        lvl = record.get("level").name
        fun = record.get("function")
        time = record.get("time").strftime("%Y-%m-%d %H:%M:%S")
        line = record.get("line")
        name = record.get("name")

        # Escape HTML characters to prevent issues
        msg = html.escape(msg)
        fun = html.escape(fun)
        name = html.escape(name)

        # Color Definitions
        time_color = "green"
        module_color = "cyan"
        try:
            lvl_color = LogLevel(lvl).color  # Function to map log level to color
        except ValueError as e:
            logger.error(f"Error mapping log level to color: {e}")
            lvl_color = "black"
        msg_color = lvl_color  # Keep message color same as level


        # Preserve spaces with <pre>
        formatted_log = (
            f"<pre style='font-family: Consolas, monospace; font-size: 16px; font-weight: bold;'>"
            f"<span style='color:{time_color};'>{time}</span> | "
            f"<span style='color:{lvl_color}; font-weight: bold;'>{lvl:<8}</span> | "
            f"<span style='color:{module_color};'>{name:<{len(name)}}:{fun:<10}:{line:<4}</span> - "
            f"<span style='color:{msg_color};'>{msg}</span>"
            f"</pre>"
        )

        return formatted_log


if __name__ == "__main__":
    app = QApplication([])
    log_browser = LogBrowser()


    # Define a custom sink for Loguru that will send logs to the GUI
    def gui_sink(message):
        log_browser.add_log(message)

    logger.add(gui_sink, level="DEBUG")
    # Generate some test log messages
    logger.debug("Debug message")
    logger.info("Information message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    logger.success("Success message")
    logger.exception("Exception message", exc_info=True)

    log_browser.show()
    app.exec()
