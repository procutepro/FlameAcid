#version 330
in vec2 v_uv;
out vec4 f_color;
uniform sampler2D u_texture;

void main() {
    vec2 uv = clamp(v_uv, 0.0, 1.0);
    f_color = texture(u_texture, uv);
}