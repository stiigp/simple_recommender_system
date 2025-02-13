from PyQt5.QtWidgets import QStackedWidget

def switch_to_scr(stacked_widget: QStackedWidget, index: int):
    stacked_widget.setCurrentIndex(index)
    current_screen = stacked_widget.currentWidget()
    for action in current_screen.toolBar.actions():
        # index * 2 pois para cada button tem um separator
        if current_screen.toolBar.actions().index(action) == index * 2:
            action.setDisabled(True)
        else:
            action.setDisabled(False)
    stacked_widget.setWindowTitle(f"Screen {index + 1}")
