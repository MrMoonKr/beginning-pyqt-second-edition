

from asyncio.log import logger
import sys

from PyQt6.QtCore import * #( Qt, QSize )
from PyQt6.QtGui import * #( QIcon, QSurfaceFormat )
from PyQt6.QtWidgets import * # ( QApplication )
from PyQt6.QtOpenGL import * # ( QOpenGLWindow, QOpenGLVersionProfile )
from PyQt6.QtOpenGLWidgets import * #( QOpenGLWidget )

from OpenGL.GL import *
from OpenGL.GL.shaders import *

import numpy as np

import logging

# Uncomment below for terminal log messages
logging.basicConfig( level=logging.DEBUG, 
                     format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TextEditLogger( logging.Handler, QObject ):
    appendPlainText = pyqtSignal( str )

    def __init__( self, target_widget ) -> None:
        super().__init__()
        QObject.__init__( self )
        self.widget = target_widget
        self.widget.setReadOnly( True )
        self.appendPlainText.connect( self.widget.appendPlainText )

    def emit( self, record ) -> None:
        #msg = self.format( record )
        #self.appendPlainText.emit( "record" )
        msg = record.asctime + " : " + record.getMessage()
        self.appendPlainText.emit( msg )

class MainOpenGL( QOpenGLWidget ):

    def __init__( self ) -> None:
        super().__init__()

    def mousePressEvent( self, a0: QMouseEvent ) -> None:
        logger.debug( "mousePressEvent() : " + f"{a0.button()} , {a0.position()}, {a0.pos()}" )
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        logger.debug( "mouseMoveEvent() 호출됨" )
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        logger.debug( "mouseReleaseEvent() 호출됨" )
        return super().mouseReleaseEvent(a0)

    def initializeGL( self ) -> None:
        self.profile = QOpenGLVersionProfile()
        self.profile.setVersion( 3, 3 )
        self.profile.setProfile( QSurfaceFormat.OpenGLContextProfile.CoreProfile )

        print( f"OpenGL Version : { glGetString( GL_VERSION ) }" )

        vert_code = "Chapter21-QOpenGLWindow/vert.glsl"
        frag_code = "Chapter21-QOpenGLWindow/frag.glsl"

        with open( vert_code, 'r' ) as f:
            vert_src = '\n'.join( f.readlines() )
        with open( frag_code, 'r' ) as f:
            frag_src = '\n'.join( f.readlines() )

        self.program = compileProgram( compileShader( vert_src, GL_VERTEX_SHADER ),
                                       compileShader( frag_src, GL_FRAGMENT_SHADER ) )
        
        glUseProgram( self.program )

        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0 ,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0 ,
             0.5,  0.5, 0.0, 0.0, 0.0, 1.0 
        )
        self.vertices = np.array( self.vertices, dtype=np.float32 )

        self.vbo = glGenBuffers( 1 )
        self.vao = glGenVertexArrays( 1 )
        glBindVertexArray( self.vao )
        glBindBuffer( GL_ARRAY_BUFFER, self.vao )

        glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )

        glEnableVertexAttribArray( 0 )
        glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 0 ) )
        
        glEnableVertexAttribArray( 1 )
        glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 12 ) )



        glClearColor( 0.3, 0.3, 0.3, 1.0 )

        return super().initializeGL()

    def resizeGL( self, w: int, h: int ) -> None:
        #print( "resizeGL() 호출됨" )
        logger.debug( "resizeGL() 호출됨" )
        self.width = w
        self.height = h
        glViewport( 0 , 0, w, h )
        #return super().resizeGL(w, h)

    def paintGL(self) -> None:
        super().paintGL()

        glViewport( 0 , 0, self.width, self.height )
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        glUseProgram( self.program )
        glBindVertexArray( self.vao )
        glDrawArrays( GL_TRIANGLES, 0, 6 )

class MainWindow( QWidget ):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI( self ) -> None:
        self.setMinimumSize( 640, 480 )
        self.setWindowTitle( "OpenGL Widget" )

        self.tree_widget = QTreeWidget()
        #tree_widget.setColumnCount( 2 )
        self.tree_widget.setHeaderLabels( ["Assets"] )
        #self.tree_widget.setColumnWidth( 0, 320 )
        self.tree_widget.setAlternatingRowColors( True )
        self.tree_widget.setSortingEnabled( True )
        self.tree_widget.header().setSortIndicator( 0, Qt.SortOrder.AscendingOrder )

        self.opengl_widget = MainOpenGL()

        self.textedit_widget = QPlainTextEdit()

        self.log_widget = TextEditLogger( self.textedit_widget )
        self.log_widget.setFormatter( logging.Formatter )
        logging.getLogger().addHandler( self.log_widget )
        logging.getLogger().setLevel( logging.DEBUG )


        self.splitter = QSplitter( Qt.Orientation.Vertical )
        self.splitter.addWidget( self.opengl_widget )
        self.splitter.addWidget( self.textedit_widget )

        main_h_box = QHBoxLayout()
        main_h_box.addWidget( self.splitter )
        main_h_box.setContentsMargins( 6, 6, 6, 6 )
        self.setLayout( main_h_box )

        self.show()

        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')


if __name__ == "__main__":
    app         = QApplication( sys.argv )
    main_window = MainWindow()
    sys.exit( app.exec() )