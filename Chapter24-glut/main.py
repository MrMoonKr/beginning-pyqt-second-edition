


"""
freeglut.dll 파일이 패키지와 같이 배포되않아 실행되지 않음.
glfw 로 전환.
"""

import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def main():
    glutInit()
    glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB )
    glutInitWindowSize( 640, 480 )
    glutCreateWindow( "" )

    glutMainLoop()
 

if __name__ == "__main__":
    main()