"""Listing 2-1 and Listing 2-2
Written by Joshua Willman
Featured in "Beginning PyQt - A Hands-on Approach to GUI Programming, 2nd Ed."
"""

import sys 
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

#print( sys.path )
#sys.path.append( r"D:/mySolutions2022Private/beginning-pyqt-second-edition" )
#sys.path.append( r'../' )상대경로인지못함

import common.widget_helpers as helpers


class MainWindow( QWidget ):

    def __init__( self ):
        """ 생성자 """
        super().__init__()
        self.initializeUI()
        helpers.center_window( self )

    def initializeUI(self):
        """ UI 초기화, 생성자에서 호출됨"""
        #self.setGeometry(100, 100, 250, 250)
        self.setMinimumSize( 640, 480 )
        self.setWindowTitle("QLabel Example")

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Create QLabel to be displayed in the main window."""
        hello_label = QLabel(self)
        hello_label.setText("Hello")
        hello_label.move(105, 15)

        # image = "./images/world.png"
        # image = "Chapter02/images/world.png"
        image = "data\creature\humanmalekid\humanmalekidskinbrown.blp"
        try:
            # with open(image):
            #     world_label = QLabel(self)
            #     pixmap = QPixmap(image)
            #     world_label.setPixmap(pixmap)
            #     world_label.move(25, 40)

            from PIL.ImageQt import ImageQt
            qim = ImageQt( image )
            pix = QPixmap.fromImage( qim )
            world_label = QLabel( self) 
            world_label.setPixmap( pix )
            world_label.move( 25, 40 )

        except FileNotFoundError as error:
            print(f"Image not found.\nError: {error}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
