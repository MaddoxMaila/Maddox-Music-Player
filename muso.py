import os
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from mutagen.flac import FLAC
import pygame
from tkinter import *

main=Tk()
main.minsize(800,400)

main.title= "Maddox Play Music"
class Music:
    def __init__(maddox,root):
        maddox.root=root
        maddox.i=0
        maddox.curr=None
        maddox.all_songs=[]
        maddox.realnames=[]
        maddox.artist=[]
        maddox.album=[]
        maddox.on_start=[]
        maddox.albms=[]
        maddox.search_items_songs=[]
        maddox.search_index=[]
        maddox.current_dir=''
        maddox.main_ui()
        maddox.control_ui()
        maddox.listBox.bind('<Button-1>',maddox.play_press())
    #def draw_ui(maddox):
    def main_ui(maddox):
        maddox.curr = None
        maddox.all_songs.clear()
        maddox.realnames.clear()
        maddox.artist.clear()
        maddox.album.clear()
        maddox.on_start.clear()
        maddox.albms.clear()
        maddox.search_items_songs.clear()
        maddox.search_index.clear()
        maddox.current_dir = ''
        maddox.infoFrame = Frame(maddox.root)
        maddox.infoFrame.pack(side='left', ipadx=20, ipady=300)
        maddox.listFrame = Frame(maddox.root)
        maddox.listFrame.pack(side='right', ipadx=347, ipady=0)
        maddox.listBox = Listbox(maddox.listFrame, selectmode='single', font=4, bd=0)
        maddox.listBox.pack(fill='y', side='top', ipadx=390, ipady=190)
        maddox.scroll = Scrollbar()
        maddox.scroll.config(command=maddox.listBox.yview)
        maddox.BoxInListBox = Frame(maddox.listFrame, bg='#FFEFD5')
        maddox.BoxInListBox.pack(side='bottom', ipadx=347, ipady=15)
        maddox.list_music_on_start()
        maddox.listBox.config(yscrollcommand=maddox.scroll.set(0, len(maddox.all_songs)))
        maddox.sort_albums(maddox.album)
    def control_ui(maddox):

        maddox.ButtonFrame=Frame(maddox.BoxInListBox)
        maddox.ButtonFrame.pack(side='right')
        maddox.song_infoFrame=Frame(maddox.BoxInListBox,bg='#FFEFD5')
        maddox.song_infoFrame.pack(side='left')
        maddox.Play_btn = Button(maddox.ButtonFrame,padx=25,pady=15, text='Play',command=lambda :maddox.play(maddox.i),border=0)
        maddox.Play_btn.grid(row=3, column=3)
        maddox.Next_btn = Button(maddox.ButtonFrame, text='Next',padx=25, pady=15,command=lambda: maddox.play_next(maddox.i),border=0)
        maddox.Next_btn.grid(row=3, column=2)
        maddox.Back_btn = Button(maddox.ButtonFrame, text='Back', padx=25,pady=15,command=lambda: maddox.play_back(maddox.i - 1),border=0)
        maddox.Back_btn.grid(row=3, column=4,sticky='e')
        #Player Control Track Info Append Layout

        maddox.s_name = StringVar()
        maddox.song_name = Label(maddox.song_infoFrame,font=5,bg='#FFEFD5',textvariable=maddox.s_name)
        maddox.song_name.grid(row=0, column=0,ipadx=10,sticky='w')
        maddox.a_name = StringVar()
        maddox.artist_name = Label(maddox.song_infoFrame, font=5, bg='#FFEFD5', textvariable=maddox.a_name)
        maddox.artist_name.grid(row=1, column=0, ipadx=10,sticky='w')
        maddox.albm_name = StringVar()
        maddox.album_name = Label(maddox.song_infoFrame, font=5, bg='#FFEFD5', textvariable=maddox.albm_name)
        maddox.album_name.grid(row=2, column=0, ipadx=10, sticky='w')

        #Info Frame Layout
        maddox.allsongs=Button(maddox.infoFrame,text="ALL SONGS\n" + str(len(maddox.all_songs)),font=5,border=0,command=lambda :maddox.main_ui()).grid(row=0,column=0,sticky='w')
        maddox.albums=Button(maddox.infoFrame,text="ALBUMS\n" + str(len(maddox.albms)),font=5,border=0,command=lambda :maddox.album_ui()).grid(row=0,column=1,sticky='w')
        maddox.allart=Button(maddox.infoFrame,text="ARTISTS ",border=0).grid(row=0,column=2,sticky='w')
        maddox.SearchFrame = Frame(maddox.infoFrame)
        maddox.SearchFrame.grid(row=1,columnspan=3)
        maddox.search_query = StringVar()
        maddox.Search = Entry(maddox.SearchFrame, textvariable=maddox.search_query).grid(row=0,column=0,ipadx=80,ipady=10,sticky='w')
        maddox.SearchBtn=Button(maddox.SearchFrame,text='Search', bg='#FFEFD5',command=lambda :maddox.search(maddox.search_query.get()))
        maddox.SearchBtn.grid(row=0,column=1,sticky='e',ipady=8,ipadx=10)
    def album_ui(maddox):
        maddox.listBox.destroy()
    def traverse_arry(maddox,array,q):
        x=0
        for arry_item in array :
            #arry_item =str(arry_item)
            if str(arry_item)[0:len(q)].lower() == q.lower() :
                maddox.search_items_songs.append(arry_item)
                maddox.search_index.append(x)
            x += 1
    def find_song(maddox,name) :
        x = 0
        for this_song in maddox.realnames :
            if str(this_song).lower() == name.lower() :
                return x
            x = x + 1
    def search(maddox,query):
        if len(maddox.search_items_songs) > 0 :
            maddox.search_items_songs.clear()
        if query == '' :
            print('You Fucken Dumbesss')
        else :
            maddox.traverse_arry(maddox.realnames,query)
            if len(maddox.search_items_songs) > 0 :
                x = 2
                for item in maddox.search_items_songs :
                    print(item)
                    Button(maddox.SearchFrame,text=str(item),border=0,command=lambda : maddox.play(maddox.find_song(item))).grid(row=x,column=0,sticky='w',ipady=8,ipadx=10,padx=20)
                    x = x + 1
            else :
                Label(maddox.SearchFrame,text='Song In This Playlist').grid(row=2,column=0)
    def add_dir(maddox) :
        maddox.current_dir=askdirectory()
        if maddox.current_dir == '' :
            return
        else :
            os.chdir(maddox.current_dir)
            maddox.add_music(maddox.current_dir)
            maddox.add_to_file(maddox.current_dir)
            if maddox.listBox.delete(0,len(maddox.all_songs)) :
                maddox.list_music_on_start()
    def inflate(maddox,atr_data,albm_data,rlmn_data):
        maddox.artist.append(atr_data)
        maddox.album.append(albm_data)
        maddox.realnames.append(rlmn_data)
    def sort_albums(maddox,albms):
        bool = False
        for this_albm in albms :
            if len(maddox.albms) == 0:
                maddox.albms.append(this_albm)
            for my_albm in maddox.albms :
                if my_albm == this_albm :
                    bool = True
                else:
                    bool = False
            if bool == True :
                continue
            else :
                maddox.albms.append(this_albm)
        for alb in maddox.albms :
            print(alb)
    def file_extnxion(maddox,aud_dir):
        if aud_dir.endswith('.flac') :
            try :
                audio=FLAC(aud_dir)
                maddox.inflate(audio['artist'][0],audio['album'][0],audio['title'][0])
            except :
                print('Mutagen Flac Error')
        else :
            try :
                audio = ID3(aud_dir)
                maddox.inflate(audio['TPE1'].text[0],audio['TALB'].text[0],audio['TIT2'].text[0])
            except :
                print('Mutagen ID3 Error')
    def add_music(maddox,dir) :
        for files in os.listdir(dir) :
            if files.endswith('.mp3') or files.endswith('.flac') :
                #print(files)
                audio_dir=os.path.realpath(files)
                maddox.all_songs.append(audio_dir)
                maddox.file_extnxion(audio_dir)
        maddox.list_music()
    def play_press(maddox):
        pressed=maddox.listBox.curselection()
        #if str(maddox.realnames[pressed]) == str(maddox.listBox.get(pressed)) :
         #   maddox.play(pressed)
          #  maddox.i=pressed
        print(pressed)
    def is_dir_in_file(maddox,dir):
        bool=False
        try :
            with open(os.environ.get('HOMEPATH') + '\\Maddox Music\\directory.txt','r') as dir_in_file :
                for directory in dir_in_file :
                    if directory == dir+'\n' :
                        bool=True
            dir_in_file.close()
        except IOError :
            print("Error Checking For Duplicate Directory")
            bool=True
        return bool
    def write_to_file(maddox,dir) :
        if os.path.isfile(os.environ.get('HOMEPATH')+'\\Maddox Music\\directory.txt') :
            if maddox.is_dir_in_file(dir) :
                return
            else :
                try :
                    with open(os.environ.get('HOMEPATH') + '\\Maddox Music\\directory.txt','a') as directories :
                        directories.write(dir+'\n')
                    directories.close()
                except IOError :
                    print("Error Appending Directory")
        else :
            try :
                with open(os.environ.get('HOMEPATH') + '\\Maddox Music\\directory.txt','w') as dir_file :
                    dir_file.write(dir+'\n')
                dir_file.close()
            except IOError(e) :
                print(e)
    def add_to_file(maddox,dir) :
        if os.path.isdir(os.environ.get('HOMEPATH')+'\\Maddox Music') :
            maddox.write_to_file(dir)
        else:
            os.mkdir(os.environ.get('HOMEPATH') + '\\Maddox Music')
            maddox.add_to_file(dir)
    def list_music_on_start(maddox) :
        if os.path.isdir(os.environ.get('HOMEPATH')+'\\Maddox Music') and os.path.isfile(os.environ.get('HOMEPATH') + '\\Maddox Music\\directory.txt') :
            try :
                with open(os.environ.get('HOMEPATH') + '\\Maddox Music\\directory.txt','r') as directories :
                    for audio_dir in directories :
                        maddox.on_start.append(audio_dir)
                directories.close()
                maddox.on_start.reverse()
                for directory in maddox.on_start :
                    directory = directory.strip('\n')
                    os.chdir(directory)
                    maddox.add_music(directory)
            except IOError :
                print('Unable To Read From File')
    def list_music(maddox):
        maddox.realnames.reverse()
        for songs in maddox.realnames :
            maddox.listBox.insert(0,str(songs))
            #print(songs+"\n")
        maddox.realnames.reverse()
    def append_info(maddox,index):
        maddox.s_name.set(maddox.realnames[index])
        maddox.a_name.set(maddox.artist[index])
        maddox.albm_name.set(maddox.album[index])
    def play(maddox,index):
        try :
            pygame.mixer.init()
            pygame.mixer.music.load(maddox.all_songs[index])
            pygame.mixer.music.play()
            #pygame.mixer.music.queue(maddox.all_songs[index+1])
            maddox.append_info(index)
            maddox.curr = index
        except :
            print('Error Playing This Song')
            print(maddox.all_songs[index])
    def play_back(maddox,index):
        if len(maddox.all_songs) != 0 :
            if maddox.i <= 0 :
                maddox.i=len(maddox.all_songs)-1
                maddox.play(index)
                maddox.i-= 1
            else :
                maddox.i-= 1
                maddox.play(index)
        else :
            return
    def play_next(maddox,index):
        if len(maddox.all_songs) != 0 :
            if maddox.i + 1 == len(maddox.all_songs):
                maddox.i= 1
                index=maddox.i
                maddox.play(index)
                maddox.i += 1
            else:
                maddox.play(index)
                maddox.i += 1
        else :
            return


music=Music(main)
#print(dir(os))
main.mainloop()
