############################################ Amir hossein Mansouri ######################################################################## 
import cv2
from kivy.lang import Builder
from kivymd.app import MDApp
import threading
from functools import partial
import cv2
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.taptargetview import MDTapTargetView
from kivy.metrics import dp
import sqlite3 as sql
from sqlite3.dbapi2 import Cursor, connect
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import time
import base64
from PIL import Image
import kivy.uix.image  as Imege
import sys
import io
import numpy as np
import re
from statistics import mode
import socket
import datetime
from kivymd.uix.datatables import MDDataTable

class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        if str(instance_item.text) == 'exit':
            exit()
        elif str(instance_item.text) == 'logout':
            ap.root.current = str(instance_item.text)
        else:
            ap.root.ids.ScreenManagerNav.current = str(instance_item.text).replace(' ', '_')

ap = ''
class MainApp(MDApp):
    path_of_database = os.getcwd()+'database1.db'
    do_vid = False
    gone = 0
    lst = ['ahm']
    def build(self):
        self.pcolor = self.theme_cls.primary_color
        Window.size = (400, 600)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_pallette = 'BlueWhite'
        threading.Thread(target=self.doit, daemon=True).start()
        global ap
        ap = self
        try:
            self.create_database(self.path_of_database)
        except sql.OperationalError:
            pass
        return Builder.load_file('gui.kv')


################logout Page Functions###################################################################

    def logger(self):
        self.root.ids.welcome_label.text = f'Hi {self.root.ids.user.text}!'
        p, u = self.root.ids.password.text, self.root.ids.user.text
        res = self.validate_password(self.path_of_database, u, p)
        if res:
            self.root.current = 'Home'
            self.ap_send(Param=1)
            img, email, username = self.load_profile_database(self.path_of_database, res, p)
            #img = cv2.resize(img,(200, 100))
            self.insert_login(self.path_of_database, u, p)
            self.root.ids.name_profile.text = username.decode("utf-8")
            self.root.ids.email_profile.text = email.decode("utf-8")
            cv2.imshow('jfie', img)
            cv2.waitKey(0)
            self.load_profile_gui(img)
        else:
            self.root.ids.welcome_label.font_size = 17
            self.root.ids.welcome_label.text = f'Hi {self.root.ids.user.text} ! Sorry, your username/password is invalid.'
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''

    def clear(self):
        self.root.ids.welcome_label.font_size = 40
        self.root.ids.welcome_label.text = 'Welcome!'
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''

    def load_profile_gui(self, frame):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.root.ids.avatar.texture = texture
####################video capture section for enter #####################################################################
    def doit(self):
        cam = cv2.VideoCapture(0)
        lst = []
        new_lst = []
        while (True):
            if self.do_vid:
                ret, frame = cam.read()
                if ret:
                    lst.append(frame)
                if len(lst) == 10:
                    for img in lst:
                        id, frame = self.detection(img)
                        Clock.schedule_once(partial(self.display_frame, frame))
                        new_lst.append(id)
                    modee = mode(new_lst)
                    if modee != -1:
                        self.root.current = 'Home'
                        self.root.ids.name_profile.text = modee
                        pic = lst[new_lst.index(modee, 4, 6)]
                        Clock.schedule_once(partial(self.display_pic, pic))
                        self.insert_login(self.path_of_database, modee, modee, mode=1)
                        break
                    else:
                        lst.clear()
                        new_lst.clear()
                Clock.schedule_once(partial(self.display_frame, frame))
            elif self.root.current == 'Home':
                break
            cv2.waitKey(20)
        cam.release()
        cv2.destroyAllWindows()


    def stop_vid(self):
        self.do_vid = False

    def start_vid(self):
        self.do_vid = True

    def display_frame(self, frame, dt):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.root.ids.vid.texture = texture
    def display_pic(self, frame, dt):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.root.ids.avatar.texture = texture
##################### navigation drawer ########################################################################
    def on_start(self):
        icons_item = {
            "account-plus": "add user",
            "account-remove": "delete user",
            "history": "activity log",
            "lock": "password management",
            "information-variant": "about us",
            "exit-to-app": "exit",
            "logout": "logout",
        }

        for icon_name in icons_item.keys():
            self.root.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )




################ file manager section #############################################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True


    def select_path(self, path):
        self.selected_path_for_profile = path
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True



################ for the info part on the last slide  ################################################################
    def tap_target_start(self):

        self.tap_target_view = MDTapTargetView(
            widget=self.root.ids.info_for_upload,
            title_text="You can choose:",
            description_text="path of a folder: in this way all \n.jpeg .png .jpg .mp4 in this folder \nand subs will be added or you can \nsimply choose a file.",
            widget_position="right_top",
            outer_circle_color=(250/255, 250/255, 250/255),
            title_text_color = self.theme_cls.primary_color,
            description_text_color=(0,0,0),
            title_text_size="30sp",
            description_text_size="16sp",
        )
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()



##### connecter of gui and database section #############################################################################################################

################ add user subsection ####################################################################################################################

    def check_email(self, email):
        self.root.ids.email_of_user.error = not bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))
        if not self.root.ids.email_of_user.error:
            self.root.ids.email_of_user.current_hint_text_color = 1, 1, 1, 1
            self.root.ids.email_of_user.line_color_normal = 1,1,1,1
            self.root.ids.email_of_user.line_color_focus = 1,1,1,1


    def result_of_add_user(self):

        res = self.add_user(
                      self.root.ids.name_of_user.text,
                      self.root.ids.password_of_user.text,
                      self.root.ids.email_of_user.text,
                      self.selected_path_for_profile,
                      self.path_of_database)

        if res:
            self.root.ids.add_user_screen_manager.current = 'ausm6'
        else:
            self.root.ids.label_of_fail_screen_add.text = f"Sorry There is a {self.root.ids.name_of_user.text} in saved usernames, please choose a different one"
            self.root.ids.delete_user_screen_manager.current = 'ausm7'


################ delete user subsection ###############################################################################################################

    def result_of_delete_user(self):
        res = self.delete_user(
            self.path_of_database,
            self.root.ids.username_to_delete.text,
            self.root.ids.password_of_user_delete.text
            )

        if res:
            self.root.ids.delete_user_screen_manager.current = 'dusm5'
        else:
            self.root.ids.label_of_fail_screen_delete.text = f"Sorry your entered data is invalid"
            self.root.ids.delete_user_screen_manager.current = 'dusm6'
################ change password subsection ###########################################################################################################

    def result_of_change_password(self):
        res = self.change_password(
            self.path_of_database,
            self.root.ids.textfield_of_username_of_password_to_change.text,
            self.root.ids.textfield_of_previous_password_to_change.text,
            self.root.ids.textfield_of_new_password_to_change.text
            )

        if res:
            self.root.ids.change_password_screen_manager.current = 'cusm5'
        else:
            self.root.ids.label_of_fail_screen_change.text = f"Sorry your entered data is invalid"
            self.root.ids.change_password_screen_manager.current = 'cusm6'





########database section##########################################################################################################################


    ################  cryptography subsection  ###################################################################################################

    def encrypt_first_layer(self,password):
        salt = b'mkfmkvbmomj'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key


    def encrypt(self,message, key):
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return encrypted


    def decrypt(self,message, key):
        f = Fernet(key)
        try:
            return f.decrypt(message)
        except InvalidToken as e:
            return 0




    ##############  converters subsection    #####################################################################################################

    def convert_blob_to_pillow_image(self,image):
        binary_data = base64.b64decode(image)
        return np.array(Image.open(io.BytesIO(binary_data)))

    def convert_str_to_binary(self,lst):
        return [bytes(i, 'ascii') if type(i) != type(b'') else i for i in lst]

    def convert_file_to_binary(self,path):
        with open(path, 'rb') as r:
            file = r.read()
            file = base64.b64encode(file)
        return file




    ######## main database manipulation subsection ###############################################################################################

    def create_database(self,path):
        connect = sql.connect(path)  # +'datebase.db')
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE basetable(username TEXT, email TEXT, profile BLOB)")
        connect.commit()
        cursor.execute("CREATE TABLE sectable(username TEXT, dtime TEXT)")
        connect.commit()
        connect.close


    def add_user(self,username, password, email, path_of_profile, path):
        username, password, email = self.convert_str_to_binary((username, password, email))
        try:
            file = self.convert_file_to_binary(path_of_profile)
        except:
            return -1

        key = self.encrypt_first_layer(password)

        username = self.encrypt(username, key)
        email = self.encrypt(email, key)
        file = self.encrypt(file, key)

        connect = sql.connect(path)
        cursor = connect.cursor()
        cursor.execute("SELECT username FROM basetable WHERE username = ?", (username,))
        lst = cursor.fetchall()
        if len(lst): return 0
        cursor.execute("INSERT INTO basetable VALUES (?,?,?)", (username, email, file))
        connect.commit()
        connect.close()
        return 1


    def validate_password(self,path, username, password):
        username, password = self.convert_str_to_binary((username, password))

        key = self.encrypt_first_layer(password)
        connect = sql.connect(path)  # +'datebase.db')
        cursor = connect.cursor()
        cursor.execute("SELECT rowid,username FROM basetable")
        user = cursor.fetchall()
        connect.close
        f = Fernet(key)
        for u in user:
            try:
                if username == f.decrypt(u[1]):
                    return u[0]
            except InvalidToken as e:
                pass
        return 0

    def delete_user(self,path, username, password):
        username, password = self.convert_str_to_binary((username, password))
        row = self.validate_password(path, username, password)
        if row == 0: return 0

        key = self.encrypt_first_layer(password)

        connect = sql.connect(path)  # +'datebase.db')
        cursor = connect.cursor()
        cursor.execute("DELETE FROM basetable WHERE rowid = ?", (row,))
        connect.commit()
        connect.close
        return 1


    def change_password(self,path, username, old_password, new_password):
        username, old_password, new_password = self.convert_str_to_binary((username, old_password, new_password))

        row = self.validate_password(path, username, old_password)
        if row == 0: return 0

        old_key = self.encrypt_first_layer(old_password)
        new_key = self.encrypt_first_layer(new_password)

        connect = sql.connect(path)  # +'datebase.db')
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM basetable WHERE rowid = ?", (row,))
        user = cursor.fetchone()
        new_user = []
        for u in user[:]:
            new_user.append(self.encrypt(self.decrypt(u, old_key), new_key))
        new_user.append(row)

        cursor.execute("UPDATE basetable SET username = ?, email = ?, profile = ? WHERE rowid = ?", new_user)
        connect.commit()

        connect.close()
        return 1

    def load_profile_database(self, path, row, password):
        password = self.convert_str_to_binary([password])[0]
        key = self.encrypt_first_layer(password)
        connect = sql.connect(path)
        cursor = connect.cursor()
        cursor.execute("SELECT profile,email,username FROM basetable WHERE rowid = ?", (row,))
        user = cursor.fetchone()
        connect.close
        user = [self.decrypt(i, key) for i in user]
        return self.convert_blob_to_pillow_image(user[0]), user[1], user[2]


############### face detection #########################################################################################
    def detection(self, img):
        id = 0
        face_detection = cv2.CascadeClassifier(os.path.join(os.getcwd(),"haarcascade_frontalface_alt2.xml"))
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read(os.path.join(os.getcwd(),'trainingData.yml'))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        try:
            faces = face_detection.detectMultiScale(gray, 1.3, 5)
        except:#if len(faces) == 0:
            return -1, img

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])
            if id == 9:
                id = 'ahm'
            elif id == 2:
                id = "mohammad"
            elif id == 3:
                id = "ali"
            elif id == 4:
                id = "armin"
            else:
                id = 'no_one'
            cv2.putText(img, str(id), (x, y + h), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 255, 0), 3, cv2.LINE_4)
            return id, img
        return -1, img
############ connect to arm ############################################################################################

    def ap_send(self, Host=socket.gethostname(),Port=1024,Param=False):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((Host,Port))
        if Param:
            s.send(bytes("1",'utf-8'))
        else:
            s.send(bytes("0",'utf-8'))
        s.close

############ datetime section ##########################################################################################

    def insert_login(self, path, username, password, mode=0):
        dt = str(datetime.datetime.now())
        username, password, dt = self.convert_str_to_binary((username, password, dt))
        if mode:
            password = self.encrypt_first_layer(password)
        key = self.encrypt_first_layer(password)
        connect = sql.connect(path)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO sectable VALUES (?,?)", (self.encrypt(username, key), self.encrypt(dt, key)))
        connect.commit()

        cursor.execute("SELECT * FROM sectable")
        user = cursor.fetchall()
        connect.close
        f = Fernet(key)
        new_lst = []
        for u in user:
            try:
                if username == f.decrypt(u[0]):
                    new_lst.append([self.decrypt(j, key).decode("utf-8") for j in u])
            except InvalidToken as e:
                pass
        if len(new_lst) == 0: return 0
        self.root.ids.data_table.add_widget(MDDataTable(column_data = [(i, dp(40)) for i in ['username', 'datetime']], row_data = new_lst))
        return 1


MainApp().run()
