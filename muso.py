import os
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
import pygame
from tkinter import *

main=Tk()
main.minsize(800,400)
main.maxsize(800,400)
main.title= "Maddox Play Music"

class Music:
    def __init__(self,root):
        self.i=1
        self.curr=None
        self.all_songs=[]
        self.realnames=[]
        self.artist=[]
        self.album=[]
        self.current_dir='C:/Users/'
        self.mainMenu = Menu(root)
        root.config(menu=self.mainMenu)
        #self.mainMenu.add_cascade(label='Add Music', command=self.add_dir)
        self.infoFrame=Frame(root)
        self.infoFrame.pack(side='left',fill='x')
        self.listFrame=Frame(root)
        self.listFrame.pack(side='right',fill='x')
        self.listBox=Listbox(self.listFrame,selectmode='single',font=4,bd=0)
        self.listBox.pack(fill='y',side='right',ipadx=260,ipady=200,padx=15)
        self.BoxInListBox=Frame(self.listBox,bg='#FFEFD5')
        self.BoxInListBox.pack(side='bottom',ipadx=300,ipady=15)
        self.control_ui()
    def control_ui(self):
        self.ButtonFrame=Frame(self.BoxInListBox)
        self.ButtonFrame.pack(side='right')
        self.song_infoFrame=Frame(self.BoxInListBox,bg='#FFEFD5')
        self.song_infoFrame.pack(side='left')
        self.Play_btn = Button(self.ButtonFrame,padx=25,pady=15, text='Play')
        self.Play_btn.grid(row=3, column=3)
        self.Next_btn = Button(self.ButtonFrame, text='Next',padx=25, pady=15,command=lambda: self.play_next(self.i))
        self.Next_btn.grid(row=3, column=2)
        self.Back_btn = Button(self.ButtonFrame, text='Back', padx=25,pady=15,command=lambda: self.play_back(self.i - 1))
        self.Back_btn.grid(row=3, column=4,sticky='e')
        self.Recent_plays = Button(self.infoFrame, text='Recent Plays', command=self.add_dir)
        self.Recent_plays.grid(row=0, column=1,sticky='n')
        self.addmore = Button(self.infoFrame, text='Add More Music', command=self.add_dir)
        self.addmore.grid(row=1, column=1)
        self.s_name = StringVar()
        self.song_name = Label(self.song_infoFrame,font=5,bg='#FFEFD5',textvariable=self.s_name)
        self.song_name.grid(row=0, column=0,ipadx=10,sticky='w')
        self.a_name = StringVar()
        self.artist_name = Label(self.song_infoFrame, font=5, bg='#FFEFD5', textvariable=self.a_name)
        self.artist_name.grid(row=1, column=0, ipadx=10,sticky='w')
        self.albm_name = StringVar()
        self.album_name = Label(self.song_infoFrame, font=5, bg='#FFEFD5', textvariable=self.albm_name)
        self.album_name.grid(row=2, column=0, ipadx=10, sticky='w')
    def add_dir(self) :
        self.current_dir=askdirectory()
        if self.current_dir == '' :
            return
        os.chdir(self.current_dir)
        self.add_music(self.current_dir)
    def add_music(self,dir) :
        for files in os.listdir(dir) :
            if files.endswith('.mp3') or files.endswith('.m4a') or files.endswith('.flac') :
                #print(files)
                audio_dir=os.path.realpath(files)
                self.all_songs.append(audio_dir)
                audio=ID3(audio_dir)
                self.realnames.append(audio['TIT2'].text[0])
                self.artist.append(audio['TPE1'].text[0])
                self.album.append(audio['TALB'].text[0])
        self.list_music()
    #def add_to_file(self,dir) :
    def list_music(self):
        self.realnames.reverse()
        for songs in self.realnames :
            self.listBox.insert(0,songs)
            print(songs+"\n")
        self.realnames.reverse()
    def append_info(self,index):
        self.s_name.set(self.realnames[index])
        self.a_name.set(self.artist[index])
        self.albm_name.set(self.album[index])
    def play(self,index):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.all_songs[index])
            pygame.mixer.music.play()
            self.append_info(index)
            #print(self.realnames[index])
            #print(self.artist[index])
            self.curr = index
        except :
            print('Error')
    def play_back(self,index):
        if len(self.all_songs) !=0 :
            if self.i <= 0:
                self.i = len(self.all_songs)-1
                self.play(index)
                self.i-=1
            else :
                self.i-=1
                self.play(index)
        else :
            return
    def play_next(self,index):
        if len(self.all_songs) != 0 :
            if self.i + 1 == len(self.all_songs):
                self.i=1
                index=self.i
                self.play(index)
                self.i += 1
            else:
                self.play(index)
                self.i += 1
        else :
            return


music=Music(main)
#print(dir(os))
main.mainloop()