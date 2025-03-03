from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QFrame,
                               QSpacerItem, QSizePolicy, QFileDialog)
from PySide6.QtGui import QColor, QPainter, QDesktopServices
from PySide6.QtCore import Qt, QSize, QUrl
from qframelesswindow import FramelessWindow, TitleBar
from qfluentwidgets import (
    FluentWindow, setTheme, Theme, isDarkTheme, TreeWidget, TableWidget, FluentIcon, ToolButton,
    TransparentToolButton
)
import json
from typing import List, Dict
from loguru import logger
from components.add_category_dialog import AddCategory
from interface.log_interface import LogBrowser


def read_config(path: str = "config.json") -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def open_in_web(url):
    if url:
        QDesktopServices.openUrl(QUrl(url))

def open_git_page():
    url = "https://github.com/dontknow492/Smart-File-Organizer"
    open_in_web(url)

def open_help_page():
    url = "https://github.com/dontknow492/Smart-File-Organizer"
    open_in_web(url)


class SFOTable(TableWidget):
    def __init__(self, columns: List[str], parent=None):
        super().__init__(parent)
        self.columns = [col.capitalize() for col in columns if col]
        self.setColumnCount(len(self.columns))  # Set column count dynamically
        self.setHorizontalHeaderLabels(self.columns)  # Set column names

        self.horizontalHeader().setStretchLastSection(True)  # Stretch last column
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.verticalHeader().setVisible(False)  # Hide vertical header

    def add_row(self, row_data: Dict[str, str]):
        """Add a row to the table with data matching the column names."""
        row_position = self.rowCount()
        self.insertRow(row_position)

        for column_index, column_name in enumerate(self.columns):  # Ensure correct order
            value = row_data.get(column_name.capitalize(), "")  # Get value or empty string
            logger.debug(f"Adding {column_name} - with value - {value} in index - {column_index}")
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make it read-only
            self.setItem(row_position, column_index, item)
        self.resizeColumnsToContents()  # resizing column based on content


class SFOWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Smart File Organizer')
        self.config = read_config()
        self.categories = dict()
        self.get_categories()

        self.main_container = QFrame(self)
        self.main_container.setObjectName("mainContainer")

        self.addSubInterface(self.main_container, FluentIcon.HOME, "All Files")
        self.switchTo(self.main_container)

        self.init_navigation()

        self.main_layout = QVBoxLayout(self.main_container)

        self.option_container = QFrame(self.main_container)
        self.option_container.setObjectName("optionContainer")
        self.option_layout = QHBoxLayout(self.option_container)
        # self.option_container.setStyleSheet("QFrame#optionContainer { background-color: #f0f0f0; }")
        self.sfo_table = SFOTable(self.config.get("columns", []), self.main_container)

        self.main_layout.addWidget(self.option_container)
        self.main_layout.addWidget(self.sfo_table)

        self._init_options()

        self.add_category_dialog = AddCategory(self)
        self.log_browser = LogBrowser(self)
        self.stackedWidget.addWidget(self.log_browser)

    def _init_options(self):
        self.option_layout.setSpacing(50)
        self.option_container.setFrameStyle(QFrame.Shape.NoFrame)

        add_category_btn = self._create_option(FluentIcon.ADD, self.add_category, "Add Category")
        add_scan_dir_btn = self._create_option(FluentIcon.FOLDER_ADD, self.add_scan_folder, "Add Scan Directory")
        settings_btn = self._create_option(FluentIcon.SETTING, self.on_setting_clicked, "Settings")
        log_btn = self._create_option(FluentIcon.HISTORY, self.on_log_clicked, "Log")
        help_btn = self._create_option(FluentIcon.HELP, open_help_page, "Help")
        git_redirect_btn = self._create_option(FluentIcon.GITHUB, open_git_page, "GitHub")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.option_layout.addWidget(add_category_btn)
        self.option_layout.addWidget(add_scan_dir_btn)
        self.option_layout.addWidget(settings_btn)
        self.option_layout.addWidget(log_btn)
        self.option_layout.addWidget(help_btn)
        self.option_layout.addWidget(git_redirect_btn)
        self.option_layout.addItem(spacer)

    def _create_option(self, icon: FluentIcon, on_click=None, tool_tip: str = None):
        option = TransparentToolButton(self.option_container)
        option.setIcon(icon)
        option.setIconSize(QSize(32, 32))
        option.setMinimumHeight(37)
        option.setCursor(Qt.CursorShape.PointingHandCursor)
        if tool_tip:
            option.setToolTip(tool_tip)
        option.clicked.connect(on_click)
        return option

    def add_category(self):
        if self.add_category_dialog.exec():
            logger.info("Adding category")
        else:
            logger.info("Cancelled")

    def on_setting_clicked(self):
        logger.debug("Settings clicked")

    def on_log_clicked(self):
        self.switchTo(self.log_browser)

    def add_scan_folder(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        file_dialog.fileSelected.connect(lambda path: logger.debug(f"Selected folder: {path}"))
        file_dialog.exec()

    def get_categories(self):
        categories = self.config.get("categories", [])
        for category in categories:
            self.categories[category.get("name")] = category.get("extensions")

    def init_navigation(self):
        self.navigationInterface.addItem("category", FluentIcon.DICTIONARY_ADD, "Categories")
        for name, value in self.categories.items():
            self.create_category(name, FluentIcon.ALBUM, None)

    def create_category(self, category_name: str, icon, on_click=None):
        key = "category_" + category_name
        self.navigationInterface.addItem(key, icon, category_name, onClick=on_click, parentRouteKey="category")

    def closeEvent(self, event, /):
        logger.info("Closing application")
        super().closeEvent(event)


def main():
    setTheme(Theme.LIGHT)
    logger.add(
        "logs/app.log",
        rotation="10 MB",  # Automatically rotates log files when they reach 10 MB
        retention="1 week",  # Keeps logs for 1 week before deleting old ones
        level="DEBUG",
        encoding="utf-8",
        backtrace=True,  # Shows extended traceback
        diagnose=True  # Adds debug info for exceptions
    )
    app = QApplication([])
    logger.info("Starting application")
    window = SFOWindow()
    window.show()
    logger.add(sink=window.log_browser.add_log)
    app.exec()


if __name__ == "__main__":
    main()
