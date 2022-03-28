

from PyQt6.QtWidgets import QWidget

def center_window( widget: QWidget ) -> None:
    """ 화면 중앙으로 이동 """
    rect    = widget.frameGeometry()
    screen  = widget.screen()
    center  = screen.availableGeometry().center()
    rect.moveCenter( center )
    widget.move( rect.topLeft() )
