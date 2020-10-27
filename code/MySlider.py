from PyQt5.QtWidgets import QSlider

class MySlider(QSlider):

    def mousePressEvent(self, ev):
        current = ev.pos().x()
        per = current * 1.0 / self.width()
        value = per * (self.maximum() - self.minimum()) + self.minimum()
        self.setValue(value)
        

