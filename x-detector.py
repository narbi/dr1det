#!/usr/bin/python
import time
from kivy.garden.mapview import MapView, MapMarker, MapLayer, MarkerMapLayer
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock

class ScreenTwo(Screen):
  # alert and play sound
  # log timestap and drone brand - append in log file
  # until it returns back to the main screen
  pass

class ScreenOne(Screen):
  map = MapView()
  layer = MapLayer()
  map.add_layer(layer)
  m1 = MapMarker()  # lon=3.057, lat=50.6394
  map.add_marker(m1)


  def callNext(self):
    self.manager.current = 'screen_two'

  def scanDrones():
    #do work here
    pass

  time.sleep(2)

class MainApp(App):
  def build(self):
    m = ScreenManager(transition= NoTransition())
    m.add_widget(ScreenOne(name='screen1'))
    m.add_widget(ScreenTwo(name='screen2'))
    return m
  
if __name__ == "__main__":
  MainApp().run()
