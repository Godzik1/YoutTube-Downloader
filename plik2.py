import tkinter
import tkinter as tk
from tkinter import ttk
from plik1 import YoutubeDownloader
from PIL import Image, ImageTk
import requests
from io import BytesIO
import sys

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        #main setup
        self.title('YouTube Downloader By Student')
        self.geometry('600x600')
        self.resizable(width = False , height = False)
        self.configure(bg='white')

        #StringVar
        self.yt_link = tk.StringVar()
        self.selected_option = tk.StringVar()

        #variabless_
        self.options_list = []
        self.is_pressed = False
        self.error_text = tkinter.Label()
        self.success_text = tkinter.Label()
        self.info_text = tkinter.Label()

        #Title text
        self.font_title = ("Comic Sans MS", 20)
        self.title_text = tk.Label(text = "YouTube Downloader" , font=self.font_title , bg= "white")
        self.title_text.pack()

        #images
        self.upl_but_temp = Image.open("upload_button.png")
        self.upl_but = ImageTk.PhotoImage(self.upl_but_temp)

        self.YouTube_image_temp = Image.open("YouTube Downloader Image.png")
        self.YouTube_image_temp = self.YouTube_image_temp.resize((200,200))
        self.YouTube_image = ImageTk.PhotoImage(self.YouTube_image_temp)

        #Main photo
        self.logo = tk.Label(image=self.YouTube_image , borderwidth=0)
        self.logo.pack()


        #yt_link
        self.get_a_yt_link()

        #exit
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        #mainloop
        self.mainloop()

    def button_link(self):
        self.link = self.yt_link.get()

        try:
            self.hide_success_text()
            self.hide_error_text()

            obj = YoutubeDownloader(self.link)

            x = obj.video_audio()
            url = obj.get_thumbnail_url()
            info = obj.other_information()

            z = list(map(lambda i: list(map(str, i)), x))

            self.options_list = [' '.join(i) for i in z]



            if self.is_pressed == True:
                self.hide_question_menu()
                self.hide_button_option()
                self.hide_thumbnail()
                self.hide_info_text()

                self.get_a_thumbnail(url)
                self.info_yt(info)
                self.options()
                return

            self.pressed()
            self.get_a_thumbnail(url)
            self.info_yt(info)
            self.options()

        except Exception as e:

            self.error_text.pack()
            self.is_pressed = False

            try:
                self.hide_question_menu()
                self.hide_button_option()
                self.hide_thumbnail()
                self.hide_info_text()

            except:
                pass
            print(e)
            font_temp = ("Comic Sans MS", 15)
            if self.link == "":
                self.error_text.configure(text = "Najpierw musisz podac link" , bg='white' , fg='red' , font= font_temp , pady=30)
            else:
                self.error_text.configure(text = "Wprowadzono bledny link/Brak polaczenia internetowego" , bg='white' , fg='red' , font= font_temp , pady= 30)


    def button_opt(self):

        self.hide_success_text()

        self.opt = self.selected_option.get()
        obj = YoutubeDownloader(self.link)

        itag = ""

        for i in range(-1,len(self.opt)-1):
            if self.opt[i+1] == " ":
                break
            itag += self.opt[i+1]

        x = obj.video_audio()
        choice = -1
        iterator = -1
        for i in x:
            iterator += 1
            if str(i[0]) == itag:
                choice = iterator
        obj.download(choice)

        self.success_text.pack()
        font_temp = ("Comic Sans MS", 40)
        self.success_text.configure(text = "Success" , bg='white' , fg='lightgreen' , font= font_temp , pady= 50)
        self.hide_thumbnail()
        self.hide_info_text()

    #hide section
    def hide_question_menu(self):
        self.question_menu.pack_forget()

    def hide_button_option(self):
        self.button_option.pack_forget()

    def hide_error_text(self):
        self.error_text.pack_forget()

    def hide_success_text(self):
        self.success_text.pack_forget()

    def hide_thumbnail(self):
        self.image_label.pack_forget()

    def hide_info_text(self):
        self.info_text.pack_forget()

    def options(self):

        self.selected_option.set(self.options_list[0])

        self.question_menu = tk.OptionMenu(self,self.selected_option ,*self.options_list)
        self.question_menu.configure(bg='white')
        self.question_menu.pack()

        self.button_option = ttk.Button(self, image=self.upl_but, command = lambda: [self.button_opt(), self.hide_button_option() , self.hide_question_menu()])
        self.button_option.pack()

    def get_a_yt_link(self):
        temp_font = ("Comic Sans MS", 20)
        self.label = tk.Label(text="Wprowadz link:" , bg='white' , font=temp_font)
        self.label.pack()

        self.entry = ttk.Entry(textvariable = self.yt_link , width=60)
        self.entry.pack()


        self.button_upload = ttk.Button( command = self.button_link , image=self.upl_but)
        self.button_upload.pack()

    def get_a_thumbnail(self , url):

        try:

            self.response = requests.get(url)
            self.response.raise_for_status()

            self.image = Image.open(BytesIO(self.response.content))

            target_size = (208,117)
            self.resized_image = self.image.resize(target_size)

            self.final_image = ImageTk.PhotoImage(self.resized_image)

            self.image_label = tk.Label(self , image = self.final_image , borderwidth=0)

            self.image_label.pack()

        except:
            pass


    def info_yt(self , content):
        self.info_text.pack()
        font_temp = ("Comic Sans MS", 10)
        self.info_text.confgure(text = content , bg='white' , font= font_temp)

    def pressed(self):
        self.is_pressed = True

    def on_close(self):
        self.destroy()
        sys.exit()

GUI()
