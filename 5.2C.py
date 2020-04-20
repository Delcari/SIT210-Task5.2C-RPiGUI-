import kivy
import RPi.GPIO as GPIO


kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.config import Config

from kivy.uix.widget import Widget

GPIO.setmode(GPIO.BOARD)


GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

#RED
GPIO.output(7, 1)
#YELLOW
GPIO.output(11, 0)
#GREEN
GPIO.output(13, 0)

#Set Window Size
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '150')

class Controller(GridLayout):


    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)

        #initialised as 'red' being the first LED to glow
        self.last = 'red'

        #Sets the # of Columns the Window Contains
        self.cols = 3

        #blank Label
        self.add_widget(Label(text=''))

        #Heading 
        self.heading = Label()
        self.heading.font_size = 30
        self.heading.text = "Select LED"
        self.heading.bold = True
        #Color dependant on LED selected
        #Starts as RED
        self.heading.color = (1, 0, 0, 1)
        self.add_widget(self.heading)

        #blank Label
        self.add_widget(Label(text=''))

        #RadioButtons

        redRadio = CheckBox()
        #color = RED
        redRadio.color = (1, 0, 0, 1)
        redRadio.active = True
        redRadio.value = 'red'
        redRadio.group = 'LED'
        #On Press call function
        redRadio.bind(active=self.radio_pressed)
        self.add_widget(redRadio)

        yellowRadio = CheckBox()
        #color = YELLOW
        yellowRadio.color = (1, 1, 0.2, 1)
        yellowRadio.value = 'yellow'
        yellowRadio.group = 'LED'
        #On Press call function
        yellowRadio.bind(active=self.radio_pressed)
        self.add_widget(yellowRadio)

        greenRadio = CheckBox()
        #color = GREEN
        greenRadio.color = (0, 1, 0, 1)
        greenRadio.value = 'green'
        greenRadio.group = 'LED'
         #On Press call function
        greenRadio.bind(active=self.radio_pressed)
        self.add_widget(greenRadio)


        #NOTE: grouping CheckBoxes makes them RadioButtons


        
    def radio_pressed(self, instance, checked):
            #7 11 13
            #r y g 

        #If the radiobutton has been checked
        if (checked):
            #Checks the color of the radiobutton
            #and turns on the LED respective
            if (instance.value == 'red'):
                GPIO.output(7, 1)
                GPIO.output(11, 0)
                GPIO.output(13, 0)
                self.heading.color = (1, 0, 0, 1)
            elif(instance.value == 'yellow'):
                GPIO.output(7, 0)
                GPIO.output(11, 1)
                GPIO.output(13, 0)
                self.heading.color = (1, 1, 0, 1)
            elif(instance.value == 'green'):
                GPIO.output(13, 1)
                GPIO.output(7, 0)
                GPIO.output(11, 0)
                self.heading.color = (0, 1, 0, 1)

            #Prevent turning off Radio Buttons
            self.last = instance.value
            
        #if last rdo pressed was is the same as this one 
        #then turn back on rdo
        if (self.last == instance.value):
            instance.active = True
                 

#Creates the Application
class MyApp(App):
    def build(self):
        self.title = '5.2C'
        return Controller()

#Runs the Application
MyApp().run()
GPIO.cleanup()
