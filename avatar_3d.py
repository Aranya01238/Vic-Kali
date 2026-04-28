"""
avatar_3d.py

Runs a lightweight GPU avatar using moderngl and moderngl-window.
The renderer draws a ray-sphere in a fragment shader and exposes a
simple TCP JSON command interface for lip-sync and blink commands.

Run as a standalone process. It listens on localhost:52000 for JSON
commands like: {"cmd":"lipsync","level":0.6} or {"cmd":"blink"}.
"""
import json
import socket
import threading
import time
import sys

try:
    import moderngl
    import moderngl_window as mglw
    from moderngl_window import geometry
except Exception as exc:
    print("moderngl or moderngl_window not available:", exc)
    sys.exit(1)

HOST = '127.0.0.1'
PORT = 52000

# Shared state controlled by socket commands
state = {
    'mouth_open': 0.0,
    'blink': 0.0,
    'stop': False,
}


def _start_command_server(host=HOST, port=PORT):
    def _handle_client(conn):
        with conn:
            data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                try:
                    for line in data.splitlines():
                        if not line:
                            continue
                        obj = json.loads(line.decode('utf-8'))
                        cmd = obj.get('cmd')
                        if cmd == 'lipsync':
                            lvl = float(obj.get('level', 0.0))
                            state['mouth_open'] = max(0.0, min(1.0, lvl))
                        elif cmd == 'blink':
                            state['blink'] = 1.0
                        elif cmd == 'stop':
                            state['stop'] = True
                except Exception:
                    # keep reading until full json line
                    pass

    def _server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        s.settimeout(1.0)
        while not state['stop']:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            threading.Thread(target=_handle_client, args=(conn,), daemon=True).start()
        try:
            s.close()
        except Exception:
            pass

    t = threading.Thread(target=_server, daemon=True)
    t.start()
    return t


VERT_SHADER = """
#version 330
in vec2 in_vert;
out vec2 v_uv;
void main() {
    v_uv = in_vert * 0.5 + 0.5;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

FRAG_SHADER = """
#version 330
uniform float iTime;
uniform vec2 iResolution;
uniform float mouth_open; // 0..1
uniform float blink; // 0..1

in vec2 v_uv;
out vec4 fragColor;

// Simple ray-sphere intersection
float sphereSDF(vec3 p, float r) { return length(p) - r; }

vec3 lightDir = normalize(vec3(-0.4, 0.6, 0.7));

void main(){
    vec2 uv = (v_uv * 2.0 - 1.0) * vec2(iResolution.x / iResolution.y, 1.0);
    vec3 ro = vec3(0.0, 0.0, 2.6);
    vec3 rd = normalize(vec3(uv, -1.8));

    // sphere at origin
    float radius = 1.0 + 0.02 * sin(iTime * 1.5);
    // raymarching simple
    float t = 0.0;
    float d;
    for(int i=0;i<64;i++){
        vec3 p = ro + rd * t;
        d = length(p) - radius;
        if(d < 0.001) break;
        t += d * 0.8;
        if(t>10.0) break;
    }

    if(t>9.0){
        fragColor = vec4(0.02,0.02,0.025,1.0);
        return;
    }

    vec3 pos = ro + rd * t;
    vec3 n = normalize(pos);

    // lighting
    float diff = max(dot(n, lightDir), 0.0);
    float spec = pow(max(dot(reflect(-lightDir, n), -rd), 0.0), 32.0);
    vec3 base = mix(vec3(0.95), vec3(0.99), diff);
    vec3 col = base * (0.6 + 0.4*diff) + vec3(1.0)*spec*0.3;

    // project eyes positions in sphere local coords
    float eye_y = 0.12;
    float eye_x = 0.22;
    vec3 left_eye = vec3(-eye_x, eye_y, sqrt(max(0.0, radius*radius - eye_x*eye_x - eye_y*eye_y)));
    vec3 right_eye = vec3(eye_x, eye_y, sqrt(max(0.0, radius*radius - eye_x*eye_x - eye_y*eye_y)));

    // compute screen-space positions
    vec3 lp = left_eye - pos; // vector from surface point to eye point
    vec3 rp = right_eye - pos;

    // draw connector and eyes by screen distance
    float eye_sz = 0.035 * (1.0 - 0.6*blink);
    vec2 p_screen = (pos.xy / vec2(iResolution.x/iResolution.y,1.0));

    // simplest approach: if fragment is near eye directions, darken
    float ldist = length((pos.xy - left_eye.xy) );
    float rdist = length((pos.xy - right_eye.xy) );

    // mouth: draw a dark ellipse near lower hemisphere whose vertical size is mouth_open
    float mouth = smoothstep(0.02, 0.0, length((pos.xy - vec2(0.0, -0.28)) * vec2(1.6, 0.9))) * mouth_open;

    // darken for eyes and connector
    if(ldist < eye_sz){ col = mix(col, vec3(0.02), 0.98); }
    if(rdist < eye_sz){ col = mix(col, vec3(0.02), 0.98); }

    // connector: if near line between eyes in sphere local coords
    vec2 le = left_eye.xy;
    vec2 re = right_eye.xy;
    vec2 p2 = pos.xy;
    float line_d = abs((re.y-le.y)*p2.x - (re.x-le.x)*p2.y + re.x*le.y - re.y*le.x) / length(re-le);
    if(line_d < 0.02 && dot(p2, vec2(1.0,0.0)) > -0.1) col = mix(col, vec3(0.02), 0.92);

    // apply mouth darkening
    col = mix(col, vec3(0.03), mouth);

    fragColor = vec4(col,1.0);
}
"""


class AvatarApp(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Diya 3D Avatar"
    window_size = (640, 640)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader=VERT_SHADER, fragment_shader=FRAG_SHADER)
        self.quad = geometry.quad_2d(size=(2.0, 2.0))
        self.start_time = time.time()

    def render(self, time_delta):
        t = time.time() - self.start_time
        self.ctx.clear(0.02, 0.02, 0.025)
        self.prog['iTime'].value = t
        self.prog['iResolution'].value = tuple(map(float, self.window_size))
        # pass uniforms from state
        self.prog['mouth_open'].value = float(state.get('mouth_open', 0.0))
        # blink decays over time
        b = state.get('blink', 0.0)
        if b > 0.0:
            b = max(0.0, b - 0.12)
            state['blink'] = b
        self.prog['blink'].value = float(b)
        self.quad.render(self.prog)


def main():
    _start_command_server()
    mglw.run_window_config(AvatarApp)


if __name__ == '__main__':
    main()
