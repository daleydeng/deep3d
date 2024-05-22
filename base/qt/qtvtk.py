from PyQt5.QtWidgets import QFrame, QVBoxLayout
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class VTKViewer(QFrame):
    def __init__(self, parent=None, embed_parent=True, init=True, margin=0):
        super().__init__(parent)
        if type(margin) == int:
             margin = [margin]*4
        self.vl = QVBoxLayout()
        self.vl.setContentsMargins(*margin)

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vl.addWidget(self.vtkWidget)
        self.setLayout(self.vl)

        if embed_parent:
            vl = QVBoxLayout()
            vl.setContentsMargins(*margin)
            vl.addWidget(self)
            parent.setLayout(vl)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.actors = []
        if init:
            self.init()

    def init(self):
        self.iren.Initialize()

    def update_view(self):
        self.ren.ResetCamera()
        self.vtkWidget.repaint()

    def clear_actors(self, update=True):
        for actor in self.actors:
            self.ren.RemoveActor(actor)
        self.actors = []
        if update:
            self.update_view()

    def add_actors(self, actors, update=True):
        if type(actors) != list:
            actors = [actors]
        self.actors.extend(actors)
        for i in actors:
            self.ren.AddActor(i)
        if update:
            self.update_view()

    def set_actors(self, *args, **kws):
        self.clear_actors(update=False)
        self.add_actors(*args, **kws)
