from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from loguru import logger
from qfluentwidgets import LineEdit, TextEdit, MessageBoxBase, SubtitleLabel, SwitchButton
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QHBoxLayout


class OptionDialog(MessageBoxBase):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.hide()
        temp = self._create_switch_button("test", False)
        self.add_widget(temp)

    def _create_switch_button(self, text, checked=False):
        """

        :param text: label of switch or switch name
        :param checked: switch state
        :return: container(qFrame) with label and swtich with mousepressEvent to setchecked on click
        """

        def on_switch_clicked(event: QMouseEvent):
            logger.debug("Switch clicked")
            if event.button() != Qt.MouseButton.LeftButton:
                return
            switch_button.setChecked(not switch_button.isChecked())


        container = QFrame(self)
        container.setMinimumWidth(300)
        container_layout = QHBoxLayout(container)
        switch_label = SubtitleLabel(text, container)
        switch_button = SwitchButton(container)
        switch_button.setChecked(checked)

        container_layout.addWidget(switch_label, stretch=1, alignment=Qt.AlignmentFlag.AlignLeft)
        container_layout.addWidget(switch_button, alignment=Qt.AlignmentFlag.AlignRight)

        container.mousePressEvent = on_switch_clicked

        return container

    def add_widget(self, widget):
        self.viewLayout.addWidget(widget)




if __name__ == '__main__':
    app = QApplication([])
    frame = QFrame()
    w = OptionDialog(frame)
    frame.show()
    app.exec()