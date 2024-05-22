import numpy as np
import common_pb2 as pb2
import zlib
from io import BytesIO
from PIL import Image

type_dict = {
    str: pb2.String,
    int: pb2.Int64,
}

def make_data(v):
    return type_dict[type(v)](data=v)

def to_NDArray(v, fmt='', **kws):
    v = np.ascontiguousarray(v)
    h = np.lib.format.header_data_from_array_1_0(v)
    data = v.tobytes()
    if fmt == 'z':
        data = zlib.compress(data)
    elif fmt in ('jpg', 'jpeg', 'png'):
        if fmt == 'jpg':
            fmt = 'jpeg'
        assert v.ndim == 2 or v.shape[-1] == 3
        img = Image.fromarray(v)
        bio = BytesIO()
        img.save(bio, format=fmt, **kws)
        bio.seek(0)
        data = bio.read()

    a = pb2.NDArray(
        descr=h['descr'],
        fortran_order=h['fortran_order'],
        shape=v.shape,
        format=fmt,
        data=data,
    )
    return a

def from_NDArray(v):
    fmt = v.format
    data = v.data
    if fmt in ('', 'z'):
        if fmt == 'z':
            data = zlib.decompress(data)
        a = np.frombuffer(data, dtype=np.dtype(v.descr))
        a = a.reshape(v.shape, order=('F' if v.fortran_order else 'C'))

    elif fmt in ('jpg', 'jpeg', 'png'):
        bio = BytesIO(data)
        bio.seek(0)
        img = Image.open(bio)
        a = np.array(img)

    return a

def to_Mesh(m, pbo):
    pbo.xyzs.extend([pb2.Point3(x=x, y=y, z=z) for x, y, z in m['xyzs']])
    if 'faces' in m:
        pbo.faces.extend([pb2.Face(idxs=idxs) for idxs in m['faces']])

def from_Mesh(m):
    out = {'xyzs': [[i.x, i.y, i.z] for i in m.xyzs]}
    if m.faces:
        out['faces'] = [[j for j in i.idxs] for i in m.faces]
    return out

if __name__ == "__main__":
    img = np.array(Image.open('lena.png'))
    assert img.shape == (512, 512, 3)
    out = from_NDArray(to_NDArray(img))
    assert (out == img).all()
    out = from_NDArray(to_NDArray(img, fmt='z'))
    assert (out == img).all()
    out = from_NDArray(to_NDArray(img, fmt='jpg', quality=100, subsampling=0))
    assert np.allclose(out, img, atol=5)
    out = from_NDArray(to_NDArray(img, fmt='png'))
    assert (out == img).all()
