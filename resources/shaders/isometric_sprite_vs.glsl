#version 330

uniform vec3 scale;

in vec3 in_pos;
in float in_angle;
in vec2 in_size;
in float in_texture;
in vec4 in_color;

out float v_angle;
out vec4 v_color;
out vec2 v_size;
out float v_texture;

void main() {
    vec3 pos = vec3(
        (in_pos.x - in_pos.y) * scale.x,
        (in_pos.y + in_pos.x) * scale.y + in_pos.z * scale.z + in_size.y / 2.0,
        in_pos.z * scale.z - (in_pos.y + in_pos.x) * scale.y
    );

    gl_Position = vec4(pos, 1.0);
    v_angle = in_angle;
    v_color = in_color;
    v_size = in_size;
    v_texture = in_texture;
}
