from kivy.garden.mapview import MapView
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty

class ScreenTwo(Screen):
  pass

class ScreenOne(Screen):
  mapview = MapView()


class Manager(ScreenManager):
  main_screen = ObjectProperty(None)
  results_screen = ObjectProperty(None)

class MainApp(App):
  def build(self):
    m = Manager(transition=NoTransition())
    return m
  
if __name__ == "__main__":
  MainApp().run()
