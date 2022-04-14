

import sys

from PyQt6.QtCore import * # ( Qt, QSize )
from PyQt6.QtGui import * # ( QIcon, QSurfaceFormat )
from PyQt6.QtWidgets import * # ( QApplication )
from PyQt6.QtOpenGL import * # ( QOpenGLWindow, QOpenGLVersionProfile )
from PyQt6.QtOpenGLWidgets import * #( QOpenGLWidget )

from OpenGL.GL import *
from OpenGL.GL.shaders import *

import numpy as np


vert_src = """
#version 330 core

layout ( location=0 ) in vec3 vertexPos;
layout ( location=1 ) in vec3 vertexColor;

out  vec3 fragmentColor ;

void main()
{
    gl_Position = vec4( vertexPos, 1.0 );
    fragmentColor = vertexColor;
}
"""

frag_src = """
#version 330 core

in vec3 fragmentColor;

void main()
{
    gl_FragColor = vec4( fragmentColor, 1.0 );
}
"""


class MainWindow( QOpenGLWindow ):
    
    def __init__( self ):
        super().__init__()
        self.initUI()

    def initUI( self ):
        self.setMinimumSize( QSize( 640, 480 ) )
        self.setTitle( "OpenGL Window" )

        self.show()


    def initializeGL( self ) -> None:
        self.profile = QOpenGLVersionProfile()
        self.profile.setVersion( 3, 3 )
        self.profile.setProfile( QSurfaceFormat.OpenGLContextProfile.CoreProfile )

        print( f"OpenGL Version : { glGetString( GL_VERSION ) }" )

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

    def resizeGL(self, w: int, h: int) -> None:
        print( "resizeGL() 호출됨" )
        return super().resizeGL(w, h)

    def paintGL(self) -> None:
        super().paintGL()

        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        glUseProgram( self.program )
        glBindVertexArray( self.vao )
        glDrawArrays( GL_TRIANGLES, 0, 6 )

class MainOpenGL( QOpenGLWidget ):

    def __init__( self ) -> None:
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect( self.Update )
        #self.timer.start( int( 1000 / 60 )  )
        self.timer.start( int( 0 )  )

        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()

        self.curr_time = self.elapsedTimer.elapsed()
        self.prev_time = self.curr_time
        self.frame_count = 0
        self.frame_time = self.curr_time

    def Update( self ):
        #print( "Update() 호출됨" + f" : {self.elapsedTimer.elapsed()}" )

        self.curr_time = self.elapsedTimer.elapsed()
        self.delt_time = self.curr_time - self.prev_time
        self.prev_time = self.curr_time

        self.frame_count += 1
        if ( self.curr_time - self.frame_time >= 1000 ):
            print( f"FPS : {self.frame_count}" )
            self.frame_count = 0
            self.frame_time  = self.curr_time

        self.update() # self.paintGL() 호출
        pass

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
        print( "resizeGL() 호출됨" )
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

class MainFrame( QWidget ):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI( self ) -> None:
        self.setMinimumSize( 640, 480 )
        self.setWindowTitle( "OpenGL Window" )

        self.tree_widget = QTreeWidget()
        #tree_widget.setColumnCount( 2 )
        self.tree_widget.setHeaderLabels( ["Assets"] )
        #self.tree_widget.setColumnWidth( 0, 320 )
        self.tree_widget.setAlternatingRowColors( True )
        self.tree_widget.setSortingEnabled( True )
        self.tree_widget.header().setSortIndicator( 0, Qt.SortOrder.AscendingOrder )

        self.opengl_widget = MainOpenGL()

        self.splitter = QSplitter( Qt.Orientation.Horizontal )
        self.splitter.addWidget( self.tree_widget )
        #self.splitter.addWidget( self.list_widget )
        self.splitter.addWidget( self.opengl_widget )

        main_h_box = QHBoxLayout()
        main_h_box.addWidget( self.splitter )
        self.setLayout( main_h_box )

        self.show()


if __name__ == "__main__":
    app         = QApplication( sys.argv )
    #main_window = MainWindow()
    main_frame  = MainFrame()
    sys.exit( app.exec() )