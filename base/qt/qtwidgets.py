from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QSlider, QGraphicsScene, QGraphicsPixmapItem
from .qt import npa_to_QImage, resize_img

def bind_prop(o, setter, tp=None, init=True):
    if isinstance(o, QLineEdit):
        if not tp:
            tp = str
        def handle_editingFinished():
            setter(tp(o.text()))

        o.editingFinished.connect(handle_editingFinished)
        if init:
            setter(tp(o.text()))

    elif isinstance(o, QCheckBox):
        if not tp:
            tp = bool
        def handle_stateChanged(state):
            setter(tp(state))
        o.stateChanged.connect(handle_stateChanged)
        if init:
            setter(tp(o.isChecked()))

    elif isinstance(o, QComboBox):
        if not tp:
            tp = str

        def handle_activated(txt):
            if type(txt) == str:
                setter(tp(txt))

        o.activated.connect(handle_activated)
        if init:
            setter(o.currentText())

    elif isinstance(o, QSlider):
        if not tp:
            tp = int

        def handle_event(v):
            setter(tp(v))
        o.valueChanged.connect(handle_event)
        if init:
            setter(tp(o.value()))
    else:
        raise

class ImageScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_item = QGraphicsPixmapItem()
        self.addItem(self.pixmap_item)

    def set_image(self, img, resized=True):
        if resized:
            s = self.parent().size()
            img = resize_img(img, s.width(), s.height())

        self.img = img
        self.update_view_img(img)

    def update_view_img(self, img):
        self.pixmap_item.setPixmap(QPixmap(npa_to_QImage(img)))
