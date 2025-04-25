from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# List of shapes and corresponding colors
shapes = ['triangle', 'rectangle', 'pentagon', 'hexagon', 'star']
colors = [
    (1.0, 0.0, 0.0),   # Red - triangle
    (0.0, 0.5, 1.0),   # Sky Blue - rectangle
    (0.0, 0.8, 0.0),   # Green - pentagon
    (1.0, 0.5, 0.0),   # Orange - hexagon
    (0.8, 0.0, 0.8)    # Purple - star
]
current_shape = 0
next_shape = 0

# Animation parameters
phases = ['waiting', 'rotating', 'transition']
phase_durations = {
    'rotating': 2000,   # 2 seconds for rotation
    'transition': 1000  # 1 second for transition
}
phase = 'waiting'
phase_start_time = 0
button_pos = (-0.2, -0.9, 0.4, 0.2)  # x, y, width, height

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_shape(shape, scale, rotation=0.0):
    glPushMatrix()
    glRotatef(rotation, 0, 0, 1)
    glScalef(scale, scale, 1)
    color = colors[shapes.index(shape)]
    glColor3f(*color)
    
    if shape == 'triangle':
        glBegin(GL_TRIANGLES)
        for i in range(3):
            angle = 2 * math.pi * i / 3
            glVertex2f(0.3*math.cos(angle), 0.3*math.sin(angle))
        glEnd()
    
    elif shape == 'rectangle':
        glBegin(GL_QUADS)
        size = 0.3
        glVertex2f(-size, -size)
        glVertex2f(size, -size)
        glVertex2f(size, size)
        glVertex2f(-size, size)
        glEnd()
    
    elif shape == 'pentagon':
        glBegin(GL_POLYGON)
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi/2
            glVertex2f(0.3*math.cos(angle), 0.3*math.sin(angle))
        glEnd()
    
    elif shape == 'hexagon':
        glBegin(GL_POLYGON)
        for i in range(6):
            angle = 2 * math.pi * i / 6
            glVertex2f(0.3*math.cos(angle), 0.3*math.sin(angle))
        glEnd()
    
    elif shape == 'star':
        glBegin(GL_POLYGON)
        for i in range(10):
            angle = 2 * math.pi * i / 10
            radius = 0.3 if i%2 == 0 else 0.15
            glVertex2f(radius*math.cos(angle), radius*math.sin(angle))
        glEnd()
    glPopMatrix()

def draw_button():
    # Button background
    glColor3f(0.2, 0.6, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(button_pos[0], button_pos[1])
    glVertex2f(button_pos[0]+button_pos[2], button_pos[1])
    glVertex2f(button_pos[0]+button_pos[2], button_pos[1]+button_pos[3])
    glVertex2f(button_pos[0], button_pos[1]+button_pos[3])
    glEnd()
    
    # Button text
    glColor3f(1, 1, 1)
    glRasterPos2f(button_pos[0]+0.1, button_pos[1]+0.05)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Rotate")

def display():
    global current_shape, phase, phase_start_time, next_shape
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    current_time = glutGet(GLUT_ELAPSED_TIME)
    elapsed = current_time - phase_start_time
    progress = min(elapsed / phase_durations.get(phase, 1000), 1.0) if phase in phase_durations else 0
    
    if phase == 'waiting':
        draw_shape(shapes[current_shape], 1.0)
    elif phase == 'rotating':
        draw_shape(shapes[current_shape], 1.0, 360 * progress)
        if progress >= 1.0:
            phase_transition('transition')
    elif phase == 'transition':
        current_scale = 1 - progress
        next_scale = progress
        draw_shape(shapes[current_shape], current_scale)
        draw_shape(shapes[next_shape], next_scale)
        if progress >= 1.0:
            current_shape = next_shape
            phase_transition('waiting')
    
    draw_button()
    glutSwapBuffers()

def phase_transition(new_phase):
    global phase, phase_start_time, next_shape
    if new_phase == 'transition':
        next_shape = (current_shape + 1) % len(shapes)
    phase = new_phase
    phase_start_time = glutGet(GLUT_ELAPSED_TIME)

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert to OpenGL coordinates
        win_width = glutGet(GLUT_WINDOW_WIDTH)
        win_height = glutGet(GLUT_WINDOW_HEIGHT)
        gl_x = (x/win_width)*2 - 1
        gl_y = 1 - (y/win_height)*2
        
        # Check button click
        bx, by, bw, bh = button_pos
        if (bx <= gl_x <= bx+bw) and (by <= gl_y <= by+bh):
            if phase == 'waiting':
                phase_transition('rotating')

def update(value):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Professional Shape Transitions")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()