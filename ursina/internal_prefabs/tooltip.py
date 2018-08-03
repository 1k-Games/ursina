from ursina import *


class Tooltip(Text):

    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)

        self.size *= .1
        self.parent = camera.ui
        self.wordwrap = 40
        self.origin = (-.5, -.5)
        self.background = True
        self.margin = 2
        self.enabled = True

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, dt):
        self.position = mouse.position
        self.position = (
            (mouse.x * camera.aspect_ratio) + (self.margin[0] * self.size/2) + .01,
            mouse.y + (self.margin[1] * self.size/2) + .01
            )
        self.x = min(self.x, (.5 * window.aspect_ratio) - self.width - self.size - .005)
        self.y = min(self.y, .5 - (self.height + self.size + .005))


if __name__ == '__main__':
    app = Ursina()

    tooltip_test = Tooltip(
    '<scale:1.5><pink>' + 'Rainstorm' + '<scale:1> \n \n' +
'''Summon a <blue>rain
storm <default>to deal 5 <blue>water
damage <default>to <red>everyone, <default>including <orange>yourself. <default>
Lasts for 4 rounds.'''.replace('\n', ' '))

    tooltip_test.enabled = True
    app.run()