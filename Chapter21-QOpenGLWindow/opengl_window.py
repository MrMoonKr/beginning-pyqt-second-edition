

import sys

from PyQt6.QtCore import ( Qt, QSize )
from PyQt6.QtGui import ( QIcon, QSurfaceFormat )
from PyQt6.QtWidgets import ( QApplication )
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

out vec4 color;

void main()
{
    color = vec4( fragmentColor, 1.0 );
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


if __name__ == "__main__":
    app         = QApplication( sys.argv )
    main_window = MainWindow()
    sys.exit( app.exec() )