from kivy.garden.mapview import MapView
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

class DetectingDrones(App):
  def build(self):
    layout = BoxLayout(orientation='vertical')
    mapview = MapView(zoom=15, lat=38.0503249, lon=23.8064504)
    layout.add_widget(mapview)
    button = Button(text='scan drones')
    layout.add_widget(button)
    return layout

  
if __name__ == "__main__":
  DetectingDrones().run()
