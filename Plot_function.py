import sys
import numpy as np
from numexpr import evaluate

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib import pyplot as plt

class MyMplCanavas(FigureCanvasQTAgg):
    '''
    Класс холста Qt для помещения рисунка Matplotlib
    '''

    def __init__(self, fig):
        super().__init__(fig)
        self.setMinimumSize(200, 200)

def plot_single_empty_graph():
    '''
    Функция для подготовки рисунка с пустыми осями и предварительного их оформления, без задания данных
    '''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 7), dpi=85, facecolor='white', frameon=True, edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    axes.set_title('Заголовок диаграммы рассеяния', fontsize=10)
    axes.set_xlabel('X', fontsize=8)
    axes.set_ylabel('Y', fontsize=8)
    return fig, axes

def prepare_abstract_canvas_and_toolbar(layout = None):
    """
    Функция для инициализации рисунка Matplotlib и его размещения в виджете Qt, добавления панели навигаии
    """
    # Подготовка рисунка и осей
    fig, axes = plot_single_empty_graph()
    # Получение экземпляра класса холста с размещенным рисунком
    canvas = MyMplCanavas(fig)
    # Добавление виджета холста с рисунком в размещение
    layout.addWidget(canvas)
    # Добавление навигационной панели с привязкой к созданному холсту с рисунком Matplotlib
    toolbar = NavigationToolbar2QT(canvas, layout.parent())
    layout.addWidget(toolbar)
    return canvas, toolbar

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Тест'
        self.left = 60
        self.top = 60
        self.width = 800
        self.height = 600
        self.textboxValue: str = "x**2"
        self.m = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.CW = QWidget()
        self.setCentralWidget(self.CW)
        self.companovka = QVBoxLayout()
        self.CW.setLayout(self.companovka)

        self.MplWidget = QWidget()
        self.Vbox = QVBoxLayout()
        self.MplWidget.setLayout(self.Vbox)

        self.canvas, self.toolbar = prepare_abstract_canvas_and_toolbar(layout=self.Vbox)

        self.toolsWidget = QWidget()
        self.Hbox = QHBoxLayout()
        self.toolsWidget.setLayout(self.Hbox)

        self.textbox = QLineEdit(self)
        self.button = QPushButton('Показать', self)

        self.Hbox.addWidget(self.textbox)
        self.Hbox.addWidget(self.button)

        self.companovka.addWidget(self.MplWidget)
        self.companovka.addWidget(self.toolsWidget)

        self.button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        self.plot(self.textbox.text())

    def plot(self, equation):
        x = np.linspace(0, 10, 50)
        print(equation)
        y = evaluate(equation)
        print(y)
        ax = self.canvas.figure.get_children()[1]
        print(ax)
        ax.plot(x, y)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())