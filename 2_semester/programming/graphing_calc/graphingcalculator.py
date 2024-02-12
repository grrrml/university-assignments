import numpy as np
import matplotlib.pyplot as plt

import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy_garden.graph import Graph, MeshLinePlot


Config.set('graphics', 'desktop', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '900')
Config.write()

class GraphCalcGridLayout(GridLayout):

    def read_function(cls, input):
        """Takes an input and turns it into a function"""
        result = str(input)
        replacer = {'sin' : 'np.sin', 'cos' : 'np.cos', 'ctg' : '1/np.tan', 'tg' : 'np.tan', 'ln' : 'np.log', '^' : '**', '\u03C0' : 'np.pi', 'e' : 'np.e'}
        for key, value in replacer.items():
            result = result.replace(key, value)

        def func(x):
            try:
                return eval(result)
            except SyntaxError:
                return 0
            
        return func

    def draw_function(cls, f, xmin, xmax):
        """
        Draws a function. Returns a list of tuples.

        Keyword arguments:
        f        -- The function to be drawn
        xmin     -- The left bound of the plot
        xmax     -- The right bound of the plot
        """
        xmin = int(xmin)
        xmax = int(xmax)
        xs = np.linspace(xmin, xmax, (xmax-xmin)*10)
        return [(x, f(x)) for x in xs]

    def clear_graph(cls):
        for _ in range(len(cls.ids.graph.plots)):
            for plot in cls.ids.graph.plots:
                cls.ids.graph.remove_plot(plot)

    def update_graph2(cls, input, xmin, xmax):
        plot = MeshLinePlot(color=[np.random.rand(), np.random.rand(), np.random.rand(), 1])
        plot.points = (cls.draw_function(input, xmin, xmax))
        cls.ids.graph.add_plot(plot)

class GraphCalcApp(App):

    def build(self):
        return GraphCalcGridLayout()


if __name__ == "__main__":
    GraphCalcApp().run()