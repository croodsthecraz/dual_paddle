from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager,WipeTransition
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


class tennisPaddle(Widget):
    score = NumericProperty(0)

    #bouncing of ball from the paddle
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class tennisBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class tennisGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    #intiating the tennis class
    def __init__(self, *args, **kwargs):
        super(tennisGame, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    #intiating random flow of ball between te paddles
    def serve_ball(self, vel=Vector(4,0).rotate(randint(0,360))):
        self.ball.center = self.center
        self.ball.velocity = vel

    #Updating the ball moments
    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

    #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(Vector(-4,0).rotate(randint(0,360)))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(Vector(-4,0).rotate(randint(0,360)))
        if self.player1.score == 1:
            Manager()



    #touch screen parameters
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y



class Manager(ScreenManager):
    pass

class tennisApp(App):
    def build(self):
        self.icon = 'blackboard.png'
        self.load_kv('my.kv')

        # load the mp3 music
        music = SoundLoader.load('music.mp3')

        # check the exisitence of the music
        music.loop = True
        music.stop()

        #On request of Exiting section
        Window.bind(on_request_close=self.on_request_close)
        return Manager(transition=WipeTransition())

    #calling exiting function
    def on_request_close(self, *args):
        self.textpopup(title='Exit', text='Are you sure?')
        return True

    #Exiting kivy App class defined
    def textpopup(self, title='', text=''):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))
        mybutton1 = Button(text='yes', size_hint=(1, 0.25),pos_hint={'x':0,'y':.6})
        mybutton2 = Button(text='no', size_hint=(1, 0.25), pos_hint={'x':0, 'y': .6})
        box.add_widget(mybutton1)
        box.add_widget(mybutton2)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        mybutton1.bind(on_release = self.stop)
        mybutton2.bind(on_release = popup.dismiss)
        popup.open()


#intiating kivy App
if __name__ == '__main__':
    tennisApp().run()
