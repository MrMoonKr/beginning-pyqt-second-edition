"""Listing 1-1
Written by Joshua Willman
Featured in "Beginning PyQt - A Hands-on Approach to GUI Programming, 2nd Ed."
"""

import sys 
from PyQt6.QtWidgets import QApplication, QWidget

# print( sys.path )

class EmptyWindow( QWidget ):

    def __init__( self ):
        """ 생성자 """
        super().__init__()
        self.initializeUI()
        self.moveToCenter()

    def initializeUI( self ):
        """ UI 초기화, 생성자에서 호출됨 """
        self.setGeometry( 200, 100, 800, 600 )
        self.setWindowTitle( "Chapter01-01 기본윈도우 생성 in PyQt" )
        self.show()
        # self.moveToCenter()

    def moveToCenter( self ):
        """ 화면 중앙으로 이동 """
        rect    = self.frameGeometry()
        screen  = self.screen()
        center  = screen.availableGeometry().center()
        rect.moveCenter( center )
        self.move( rect.topLeft() )


if __name__ == '__main__':
    app         = QApplication( sys.argv )
    main_window = EmptyWindow()
    sys.exit( app.exec() )
