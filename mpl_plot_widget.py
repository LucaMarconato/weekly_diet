# to embed matplotlib plots into pyqt guis
# adapted from https://matplotlib.org/gallery/user_interfaces/embedding_in_qt5_sgskip.html

import matplotlib

from PyQt5 import QtWidgets

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

plt.style.use('dark_background')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from report import plot_into_axes
from diet import Diet


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.gray = (50 / 255, 50 / 255, 50 / 255)
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=self.gray)
        self.ax0 = self.fig.add_subplot(211)
        self.ax1 = self.fig.add_subplot(212)
        self.fig.subplots_adjust(bottom=0.15, top=0.95, left=0.06, right=0.99)
        self.ax0.set_facecolor(self.gray)
        self.ax1.set_facecolor(self.gray)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        diet = Diet('diet.json')
        plot_into_axes(diet, self.ax0, self.ax1, self.gray)

    def update_figure(self, diet):
        self.clear_canvas()
        # at least when testing, I prefer consistency over performance, that's why I reload diet
        diet = Diet('diet.json')
        plot_into_axes(diet, self.ax0, self.ax1, self.gray)
        self.draw()

    def clear_canvas(self):
        self.fig.clear()
        self.ax0 = self.fig.add_subplot(211)
        self.ax1 = self.fig.add_subplot(212)
        # self.fig.subplots_adjust(bottom=0.15, top=0.95) # needed?
        self.ax0.set_facecolor(self.gray)
        self.ax1.set_facecolor(self.gray)


class EmptyMplCanvas(MyMplCanvas):
    def compute_initial_figure(self):
        pass


class MplPlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.widget_layout = QtWidgets.QGridLayout()
        self.setLayout(self.widget_layout)
        self.mpl_canvas = EmptyMplCanvas()
        self.widget_layout.addWidget(self.mpl_canvas)

    def axes(self):
        return self.mpl_canvas.ax0, self.mpl_canvas.ax1

    def fig(self):
        return self.mpl_canvas.fig

    def clear_canvas(self):
        self.mpl_canvas.clear_canvas()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MplPlotWidget()
    widget.show()
    axes = widget.axes()
    fig = widget.fig()
    # for ax in axes:
    #     ax.scatter(list(range(10)), list(range(10)))
    # fig.colorbar()
    widget.mpl_canvas.draw()

    sys.exit(app.exec_())
