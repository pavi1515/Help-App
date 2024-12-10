#importing the required libraries(Here, Kivy)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import time
import speech_recognition as pq
from twilio.rest import Client
import pyttsx3
import sqlite3
import Credentials



auth_token=Credentials.auth_token
secondary_token=Credentials.secondary_token
ab=Client(auth_token,secondary_token)
lp=pq.Recognizer()

#mycon=mysql.connector.connect(host='localhost',user='root',database='app_db_pavitra',passwd='pavitra')

#mycursor=mycon.cursor()



current_connection_tosql_database = sqlite3.connect("help_app_users.db")

help_app_cur = current_connection_tosql_database.cursor()

create_table_initial_command = """CREATE TABLE IF NOT EXISTS help_app_users(first_name TEXT, last_name TEXT, username TEXT, phone_number INT, relative_number INT, location TEXT, password TEXT NOT NULL)"""
help_app_cur.execute(create_table_initial_command)

#Declaring the main class for our kivy app

class Page1(Screen):
    pass
class Page2(Screen):
    pass
class Page3(Screen):
    pass
class Page4(Screen):
    pass
class Page5(Screen):
    pass    
class Page7(Screen):
    pass

username_in_session = ""
class pavitra_app(MDApp):
    def build(self):
        new=Builder.load_file('kivy_app1_pavitra.kv')
        abc=ScreenManager()
        abc.add_widget(Page1(name='page1'))
        abc.add_widget(Page2(name='page2'))
        abc.add_widget(Page3(name='page3'))
        abc.add_widget(Page4(name='page4'))
        abc.add_widget(Page5(name='page5'))
        abc.add_widget(Page7(name='page7'))
        return new



    def register_user(self):
        self.fn = repr(self.root.get_screen('page3').ids.fname.text).strip("'")
        print(self.fn)
        self.ln= repr(self.root.get_screen('page3').ids.lname.text).strip("'")
        self.user= repr(self.root.get_screen('page3').ids.username.text).strip("'")
        self.pn= (self.root.get_screen('page3').ids.pnumber.text)
        self.rn= (self.root.get_screen('page3').ids.rnumber.text)
        self.lo= repr(self.root.get_screen('page3').ids.location.text).strip("'")
        self.pas= repr(self.root.get_screen('page3').ids.password.text).strip("'")
        
        q1="insert into help_app_users values ('{}','{}','{}',{},{},'{}','{}')".format(self.fn,self.ln,self.user,self.pn,self.rn,self.lo,self.pas)
        help_app_cur.execute(q1)
        current_connection_tosql_database.commit()
         
        self.root.get_screen('page3').ids.fname.text = ""
        self.root.get_screen('page3').ids.lname.text = ""
        self.root.get_screen('page3').ids.username.text = ""
        self.root.get_screen('page3').ids.pnumber.text = ""
        self.root.get_screen('page3').ids.rnumber.text = ""
        self.root.get_screen('page3').ids.location.text = ""
        self.root.get_screen('page3').ids.password.text = ""


    def login_user(self):
        self.lguser = self.root.get_screen('page2').ids.username.text
        self.lgpass=self.root.get_screen('page2').ids.password.text
        q1="select username, password from help_app_users"
        help_app_cur.execute(q1)
        new_app=help_app_cur.fetchall()

        for i in new_app:
            if i[0]==self.lguser and i[1]==self.lgpass:
                username_in_session = self.lguser
                return True
        else:
            print("false returned")
            self.root.get_screen('page2').ids.username.text = ""
            self.root.get_screen('page2').ids.password.text = ""
            return False    
    def turn_off(self):
        print("Work done")            
               
    def turn_on(self):
        self.durati = self.root.get_screen('page5').ids.dur.text
        self.username= (self.root.get_screen('page2').ids.username.text)
        self.location = (self.root.get_screen('page5').ids.location_new.text)
        self.startTime = time.time()



        #new1=ab.messages.create(to='+15062821168',from_='+19183803194',body="Test message app")
        count = 0
        while (time.time()-self.startTime)<=int(self.durati):
            try:
                with pq.Microphone() as self.an:
                    self.listened_audio=lp.listen(self.an)
                    self.speech_text=lp.recognize_google(self.listened_audio)
                    #print(self.speech_text.lower())
                    if 'help help help' in self.speech_text.lower():
                        count = count+1
                        #print(self.pavi_qw.lower())
                        final_message = self.username+" is in trouble. Please provide the necessary help as soon as possible. "+self.username+" is at the location: "+self.location
                        new1=ab.messages.create(to='+18777804236',from_='+19183803194',body=final_message)
                        print("Message Sent")
                        break

            except:
                print("Error with detecting voice") 
        return True      



if __name__=="__main__":
    app_new = pavitra_app()
    app_new.run()
     