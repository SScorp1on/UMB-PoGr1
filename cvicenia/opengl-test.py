import sys

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader

if not glfw.init():
    sys.exit(1)

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
# glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(800, 600, "OpenGL Window", None, None)
if not window:
    glfw.terminate()
    sys.exit(1)

glfw.make_context_current(window)
glViewport(0, 0, 800, 600)

vertex_src = """
# version 330 core
in vec3 a_position;
void main() {
    gl_Position = vec4(a_position, 1.0);
}
"""

fragment_src = """
# version 330 core
out vec4 out_color;
void main() {
    out_color = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

shader = OpenGL.GL.shaders.compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                          compileShader(fragment_src, GL_FRAGMENT_SHADER))

vertices = np.array([-0.5, -0.5, 0.0,
                     0.5, -0.5, 0.0,
                     0.0, 0.5, 0.0],
                    dtype=np.float32)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

position = glGetAttribLocation(shader, "a_position")
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(position)

while not glfw.window_should_close(window):
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
