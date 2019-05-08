from random import random
from kivy.app import App
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget


# https://www.violettime.com/kivy/4.html


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class HelloApp(App):
    pass

    def build(self):
        root = Widget()
        root.add_widget(Button())
        slider = Slider()
        root.add_widget(slider)
        # root.add_widget(MyPaintWidget())
        return root


if __name__ == '__main__':
    HelloApp().run()
