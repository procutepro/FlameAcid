#version 330
in vec3 in_position;
in vec2 in_uv;
out vec2 v_uv;
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

void main() {
    v_uv = in_uv;
    gl_Position = u_projection * u_view * u_model * vec4(in_position, 1.0);
}