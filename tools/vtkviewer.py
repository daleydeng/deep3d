#!/usr/bin/env python
"""
CONTROLS:

left mouse button:  rotation
right mouse button:  zooming
middle mouse button:  panning
ctrl + left mouse button:  spinning

ctrl + shift + left mouse button:  zooming
shift + left mouse button:  panning

j:  joystick
t:  trackball

c:  camera mode
a:  actor mode

3: toggle  stereo mode

e: exit the application
e: quit the application

f: fly to the picked point
r: reset the camera

p: pick

s: surface representation
w: wireframe representation

Set the STEREO_TYPE environment variable to control stereo type.
        STEREO_TYPE=CRYSTAL_EYES
        STEREO_TYPE=RED_BLUE
        STEREO_TYPE=INTERLACED
        STEREO_TYPE=LEFT
        STEREO_TYPE=RIGHT
        STEREO_TYPE=DRESDEN
        STEREO_TYPE=ANAGLYPH
        STEREO_TYPE=CHECKERBOARD
        STEREO_TYPE=SPLITVIEWPORT_HORIZONTAL

Set the COLORMAP environment variable to change the scalar color map.
It should be the location of a ParaView-style xml colormap file.
"""

useage = """
Useage: vtkviewer.py FILE [MORE FILES...]
Supported File Formats:
  *.vtk - VTK Legacy File
  *.vtp - VTK Polygonal Data File
  *.vtu - VTK Unstructured Grid Data File
  *.ply - Stanford Polygon File
  *.obj - Wavefront Object file
  *.stl - Stereolithography File
Controls:
  's' - surface
  'w' - wireframe
  'r' - reset and center camera
  'q' - quit
  '3' - toggle stereo mode
More Info:
  https://github.com/HalCanary/vtkviewer
"""

import sys
import os
import glob
import vtk
from PyQt5.QtWidgets import QWidget, QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from deep3d_common.vtk_ import vtk_read_data

class QVTKWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.ren = vtk.vtkRenderer()
        self.ren_win = self.vtk_widget.GetRenderWindow()
        self.ren_win.AddRenderer(self.ren)
        self.iren = self.ren_win.GetInteractor()

        self.mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        self.ren.AddActor(actor)

    def add_poly_data(self, pd):
        self.mapper.SetInputData(pd)

    def add_file(self, file_name):
        fname = file_name.lower()
        self.add_poly_data(vtk_read_data(fname))

if __name__ == '__main__':
    import sys
    from fire import Fire

    def main(src_f):
        app = QApplication(sys.argv)
        w = QVTKWidget()
        w.add_file(src_f)
        w.show()
        w.iren.Initialize()
        app.exec_()

    Fire(main)

        # if len(sys.argv) == 1:
        #         print(useage)
        #         exit(1)
        # vtkviewer = VTKViewer()

        # if "COLORMAP" in os.environ:
        #         colormap = VTKViewer.LoadColorMap(os.environ["COLORMAP"])
        # else:
        #         colormap = None

        # for arg in sys.argv[1:]:
        #         fileNames = glob.glob(arg)
        #         if len(fileNames) == 0:
        #                 print("what:", arg)
        #         else:
        #                 for fileName in fileNames:
        #                         if os.path.isfile(fileName):
        #                                 vtkviewer.AddFile(fileName,colormap)
        #                         else:
        #                                 print("what:", fileName)
        # vtkviewer.Start()
