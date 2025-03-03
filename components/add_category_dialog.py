from typing import List

from qfluentwidgets import LineEdit, TextEdit, MessageBoxBase, SubtitleLabel
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame


class AddCategory(MessageBoxBase):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.extension_edit = None # text edit
        self.name_edit = None # line edit
        self.init_ui()
        self.hide()

    def init_ui(self):
        name_label = SubtitleLabel("Name", self)
        self.name_edit = LineEdit(self)
        self.name_edit.setPlaceholderText("Enter category name")

        extension_label = SubtitleLabel("Extensions", self)
        self.extension_edit = TextEdit(self)
        self.extension_edit.setPlaceholderText("Enter file extensions separated by space (py txt java etc)")
        self.extension_edit.setFixedHeight(100)
        self.extension_edit.setAcceptRichText(False)


        self.add_widget(name_label)
        self.add_widget(self.name_edit)
        self.add_widget(extension_label)
        self.add_widget(self.extension_edit)

    def add_widget(self, widget):
        self.viewLayout.addWidget(widget)

    def get_name(self)->str:
        return self.name_edit.text()

    def get_extensions(self)->List[str]:
        return self.extension_edit.toPlainText().split(" ")

    def clear_dialog(self):
        self.name_edit.clear()
        self.extension_edit.clear()


if __name__ == '__main__':
    app = QApplication([])
    frame = QFrame()
    w = AddCategory(frame)
    frame.show()
    app.exec()