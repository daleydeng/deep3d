from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qtconsole.rich_ipython_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager

class ConsoleWidget(QWidget):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        self.km = QtInProcessKernelManager()
        self.km.start_kernel()
        self.kernel = self.km.kernel
        self.kshell = self.kernel.shell
        self.km_client = self.km.client()
        self.km_client.start_channels()

        self.ipyw = RichJupyterWidget(self)
        self.ipyw.kernel_manager = self.km
        self.ipyw.kernel_client = self.km_client
        self.ipyw.setMinimumWidth(300)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ipyw, 0.2)

    def add_widget(self, v, *args, **kws):
        self.layout.addWidget(v, *args, **kws)

    def closeEvent(self, e):
        self.km_client.stop_channels()
        self.km.shutdown_kernel()

    def expose(self, **kws):
        self.kshell.push(kws)
