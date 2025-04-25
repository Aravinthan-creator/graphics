from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys

# Global variable for man arm animation
man_arm_angle = 0.0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)

def draw_cube():
    # Draw a standard cube centered at origin (each face drawn with immediate mode)
    glBegin(GL_QUADS)
    # Front face (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f( 1.0, 1.0,  1.0)
    glVertex3f(-1.0, 1.0,  1.0)
    glVertex3f(-1.0,-1.0,  1.0)
    glVertex3f( 1.0,-1.0,  1.0)

    # Back face (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f( 1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0,-1.0, -1.0)
    glVertex3f( 1.0,-1.0, -1.0)

    # Left face (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0,  1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0,-1.0, -1.0)
    glVertex3f(-1.0,-1.0,  1.0)

    # Right face (yellow)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f( 1.0, 1.0,  1.0)
    glVertex3f( 1.0, 1.0, -1.0)
    glVertex3f( 1.0,-1.0, -1.0)
    glVertex3f( 1.0,-1.0,  1.0)

    # Top face (magenta)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f( 1.0, 1.0,  1.0)
    glVertex3f(-1.0, 1.0,  1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f( 1.0, 1.0, -1.0)

    # Bottom face (cyan)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0,  1.0)
    glVertex3f(-1.0,-1.0,  1.0)
    glVertex3f(-1.0,-1.0, -1.0)
    glVertex3f( 1.0,-1.0, -1.0)
    glEnd()

def draw_man():
    """Draw a simple stick-man. The man is drawn small and his arms will oscillate using the global man_arm_angle."""
    glPushMatrix()
    # Position the man near the center and slightly forward (adjust as needed)
    glTranslatef(0.0, -1.5, 0.0)
    glScalef(0.2, 0.2, 0.2)  # Very small man

    glColor3f(1.0, 1.0, 1.0)
    # Head (circle)
    glPushMatrix()
    glTranslatef(0.0, 1.2, 0.0)
    glBegin(GL_LINE_LOOP)
    for i in range(30):
        theta = 2 * math.pi * i / 30
        glVertex2f(0.1 * math.cos(theta), 0.1 * math.sin(theta))
    glEnd()
    glPopMatrix()

    # Body
    glBegin(GL_LINES)
    glVertex3f(0.0, 1.1, 0.0)
    glVertex3f(0.0, 0.5, 0.0)
    glEnd()

    # Arms: One line that will swing left and right
    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    glRotatef(man_arm_angle, 0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(-0.3, 0.0, 0.0)
    glVertex3f(0.3, 0.0, 0.0)
    glEnd()
    glPopMatrix()

    # Legs
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.5, 0.0)
    glVertex3f(-0.2, 0.0, 0.0)
    glVertex3f(0.0, 0.5, 0.0)
    glVertex3f(0.2, 0.0, 0.0)
    glEnd()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Set the camera: position it slightly above and back so that the two tall cubes and man are visible
    gluLookAt(0.0, 2.0, 8.0,   # Eye position (elevated and back)
              0.0, 0.0, 0.0,   # Look at origin
              0.0, 1.0, 0.0)   # Up vector

    # Draw first tall cube (left)
    glPushMatrix()
    glTranslatef(-2.0, 0.0, 0.0)
    glScalef(1.0, 3.0, 1.0)  # Make it tall along Y axis
    draw_cube()
    glPopMatrix()

    # Draw second tall cube (right)
    glPushMatrix()
    glTranslatef(2.0, 0.0, 0.0)
    glScalef(1.0, 3.0, 1.0)  # Make it tall along Y axis
    draw_cube()
    glPopMatrix()

    # Draw the small man animation (static position with swinging arms)
    draw_man()

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Set up a perspective projection with a 45° field of view
    gluPerspective(45, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()

def timer(value):
    global man_arm_angle
    # Update the man arm angle oscillation for animation
    man_arm_angle = math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.005) * 30.0  # oscillate between -30 and +30 degrees
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Environment with Two Tall Cubes & Small Man Animation")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

main()
