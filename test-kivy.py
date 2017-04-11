from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,FallOutTransition
from kivy.properties import ObjectProperty,NumericProperty
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.clock import Clock


gui_v3 = '''
<PlayScreen>:
    play_Button: playButton
    canvas.before:
        Color:
            rgb: (0, 0, 1)
    GridLayout:
        rows:1
        size_hint: .1,.1
        pos_hint: {'center_x': .5, 'center_y': .5}
        Button:
            id: playButton
            size_hint_x: None
            width: 100
            text: 'Play !'
            font_size: 12
            bold: True
            italic: False
            border: 10,10,10,10
            color: (0.5, 1, 0.5, 1)

            on_press: root.playButton_press()
<LoadingScreen>:
    on_enter: Clock.schedule_once(self.callNext, 3)
    canvas:
        Color:
            rgba: 0.4, 0.4, 0.4, 1
        Rectangle:
            pos: root.center
            size: (32, 32)
    BoxLayout:
        Label:
            text: 'JB'
            font_size: 100
        Label:
            text: 'Loading...'
            font_size: 10

'''


class PlayScreen(Screen):
    play_Button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/2)

    def update(self,dt):
        print('Current screen is %s' % self.manager.current)


    def playButton_press(self):
        print('Hi Play button is pressed')
        sm.current = 'loading'


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.callNext, 3)


    def callNext(self,dt):
        self.manager.current = 'play'
        print ("Hi this is call Next Function of loading 1")


# Create the screen manager
Builder.load_string(gui_v3)
sm = ScreenManager(transition= FallOutTransition())
sm.add_widget(LoadingScreen(name='loading'))
sm.add_widget(PlayScreen(name='play'))


class MyJB(App):
    def build(self):
        print (sm.screen_names)
        return sm

if __name__ == '__main__':
    MyJB().run()