def load_obj(path):
    with open(path, "r") as f:
        data = f.readlines()

    name = ""

    vertexes = []
    faces = []
    uvs = []
    mtl_path = ""

    for i in data:

        if not i.strip():
            continue

        cmd = i.split(" ")[0]
        rest = i.split(" ")[1:]

        if cmd == "v":
            x = float(rest[0])
            y = float(rest[1])
            z = float(rest[2])
            vertexes.append((x, y, z))
        
        if cmd == "f":
            tri = []
            for i in rest:
                parts = i.split('/')
                v_idx = int(parts[0]) - 1
                uv_idx = int(parts[1]) - 1 if len(parts) > 1 and parts[1] else -1

                v = vertexes[v_idx]
                uv = uvs[uv_idx] if uv_idx >= 0 and uv_idx < len(uvs) else (0.0, 0.0)

                tri.extend([v[0], v[1], v[2], uv[0], uv[1]])

            faces.append(tri)
        
        if cmd == "vt":
            u = float(rest[0])
            v = float(rest[1])
            uvs.append((u, v))

        if cmd == "o":
            name = rest[0].strip()

        if cmd == "mtllib":
            mtl_path = rest[0].strip()

    return faces, name, mtl_path

if __name__ == "__main__":
    print(load_obj(r"C:\Users\user\Downloads\flame3D\Untitled.obj"))