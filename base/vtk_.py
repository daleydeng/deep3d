from os import path
import vtk
import numpy as np
import numpy.linalg as npl

_type_dic = {
    np.float32: vtk.VTK_FLOAT,
    np.float64: vtk.VTK_DOUBLE,
    np.uint8: vtk.VTK_UNSIGNED_CHAR,
    np.int16: vtk.VTK_SHORT,
}

def from_vtkIdList(v):
    return [int(v.GetId(i)) for i in range(v.GetNumberOfIds())]

def vtkPolyData_get_points(p):
    return [list(p.GetPoint(i)) for i in range(p.GetNumberOfPoints())]

def vtkPolyData_get_cells(p):
    return [from_vtkIdList(p.GetCell(i).GetPointIds()) for i in range(p.GetNumberOfCells())]

_io_cls_dic = {
    '.ply': 'PLY',
    '.nrrd': 'Nrrd',
    '.vtp': 'XMLPolyData',
    '.vti': 'XMLImageData',
}

def vtk_read_data(fname):
    ext = path.splitext(fname)[-1]
    r = getattr(vtk, 'vtk'+_io_cls_dic[ext]+'Reader')()
    r.SetFileName(fname)
    r.Update()
    return r.GetOutput()

def vtk_write_data(fname, v):
    ext = path.splitext(fname)[-1]
    w = getattr(vtk, 'vtk'+_io_cls_dic[ext]+'Writer')()
    w.SetInputData(v)
    w.SetFileName(fname)
    w.Write()

def vtk_new_polydata(xyzs, normals=[], lines=[], faces=[], colors={}, polydata=None):
    if polydata is None:
        polydata = vtk.vtkPolyData()

    vtk_points = vtk.vtkPoints()
    ca = vtk.vtkCellArray()
    points = np.asarray(xyzs)
    for p in points:
        pid = vtk_points.InsertNextPoint(*p[:3])
        ca.InsertNextCell(1)
        ca.InsertCellPoint(pid)
    polydata.SetPoints(vtk_points)
    polydata.SetVerts(ca)

    if len(normals):
        normals = np.asarray(normals)
        assert len(normals) == len(points)
        if normals.dtype == np.float32:
            a = vtk.vtkFloatArray()
        else:
            a = vtk.vtkDoubleArray()
        a.SetNumberOfComponents(3)
        for i in normals:
            a.InsertNextTuple3(*i[:3])
        polydata.GetPointData().SetNormals(a)

    if len(lines):
        ca = vtk.vtkCellArray()
        for i, j in lines:
            item = vtk.vtkLine()
            lpids = item.GetPointIds()
            lpids.SetId(0, i)
            lpids.SetId(1, j)
            ca.InsertNextCell(item)
        polydata.SetLines(ca)

        if 'lines' in colors:
            cs = colors['lines']
            if len(cs) != len(lines) and type(cs[0]) == int:
                cs = [cs]*len(lines)
            a = vtk.vtkUnsignedCharArray()
            a.SetNumberOfComponents(3)
            a.SetName("Colors")
            for i in cs:
                a.InsertNextTypedTuple(i)
            # how to specific to this field
            #polydata.GetLines().GetCellData().SetScalars(a)

    if len(faces):
        ca = vtk.vtkCellArray()
        for i, j, k in faces:
            item = vtk.vtkTriangle()
            lpids = item.GetPointIds()
            lpids.SetId(0, i)
            lpids.SetId(1, j)
            lpids.SetId(2, k)
            ca.InsertNextCell(item)
        polydata.SetPolys(ca)

    return polydata

def create_polydata_actor(pd):
    mapper = vtk.vtkPolyDataMapper()
    mapper.ScalarVisibilityOff()
    mapper.SetInputData(pd)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor
