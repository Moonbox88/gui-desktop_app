import io
import sys
import time
import pickle
import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import YT_stream_handler

thumb_size = 256, 256

# THREAD to run pacman animation

# TREAD to countdown life of yt obj and clear when expired

def download_stream():
    fileObj = open('data.obj', 'rb')
    yt = pickle.load(fileObj)

    for i in streams_list.curselection():
        info = streams_list.get(i).split(" - ")
        stream = yt.yt.streams.get_by_itag(info[0])
        stream.download()


    fileObj.close()

def get_YT_streams():
    url = yt_url.get()

    yt = YT_stream_handler.YTVideoDLOptions(url)

    try:
        if len(yt.yt.title) >= 66:
            clipped = yt.yt.title[:65]
            video_title["text"] = clipped + "..."
        else:
            video_title["text"] = yt.yt.title
        video_channel["text"] = yt.yt.author
        video_pub["text"] = yt.yt.publish_date
        video_length["text"] = yt.yt.length
        img_request = requests.get(yt.yt.thumbnail_url)

        if img_request.status_code == requests.codes.ok:

            thumb_img = Image.open(io.BytesIO(img_request.content))
            thumb_img.thumbnail(thumb_size, Image.ANTIALIAS)
            video_thumbn = ImageTk.PhotoImage(thumb_img)

            video_thumb.configure(image=video_thumbn)
            video_thumb.image = video_thumbn
        else:
            print(img_request.status_code)
    except Exception as e:
        print(str(e))

    count = 0

    print(f'Searching for progressive stream for {yt.url}')
    try:
        prog_streams = yt.yt.streams.filter(progressive=True).order_by('resolution').desc()
        streams_list.insert(count, '*** progressive ***')
        for each in prog_streams:
            count += 1
            streams_list.insert(count, f'{each.itag} - {each.filesize} - {each.resolution} - {each.subtype}')
    except AttributeError:
        print("1...No streams available...")
    except TypeError:
        print("2...No streams available...")


    print(f'Searching for adaptive stream for {yt.url}')
    try:
        adap_streams = yt.yt.streams.filter(adaptive=True).order_by('resolution').desc()
        count += 1
        streams_list.insert(count, '*** adaptive ***')
        for each in adap_streams:
            count += 1
            streams_list.insert(count, f'{each.itag} - {each.filesize} - {each.resolution} - {each.subtype}')
    except AttributeError:
        print("1...No streams available...")
    except TypeError:
        print("2...No streams available...")


    print(f'Searching for audio stream for {yt.url}')
    try:
        audio_streams = yt.yt.streams.filter(only_audio=True).desc()
        count += 1
        streams_list.insert(count, '*** audio ***')
        for each in audio_streams:
            count += 1
            streams_list.insert(count)
    except AttributeError:
        print("1...No streams available...")
    except TypeError:
        print("2...No streams available...")

    fileObj = open('data.obj', 'wb')
    pickle.dump(yt, fileObj)
    fileObj.close()

    url_entry.delete("0", "end")

    #submit_button.state(["disabled"])  # Disable the button.
    #time.sleep(10)
    #submit_button.state(["!disabled"])  # Enable the button.


root = tk.Tk()
root.title("tk YouTube Video Downloader")
root.option_add("*tearOff", False)
root.geometry("900x450")
root.resizable(False, False)

options = {'padx': 5, 'pady': 5}

# SET RELATIVE PATH FOR DEFAULT IMAGE
default_img = Image.open("D:/Users/seanm/PycharmProjects/gui-desktop_app/default_thumb.jpg")
default_img.thumbnail(thumb_size, Image.ANTIALIAS)
default_thumbn = ImageTk.PhotoImage(default_img)


main = ttk.Frame(root)
main.pack(side="left", fill="both", expand=True, padx=1, pady=(4, 0))
# No side, means 'side top' by default

yt_url = tk.StringVar()

url_label = ttk.Label(main, text="Enter a URL: ")
url_label.grid(column=0, row=0, sticky='W', **options)
url_entry = ttk.Entry(main, width=60, textvariable=yt_url)
url_entry.grid(column=1, row=0, sticky='W', **options)
url_entry.focus()

video_label = ttk.Label(main, text="Video details: ")
video_label.grid(column=0, row=1, sticky='W', **options)

submit_button = ttk.Button(main, text="Get video", command=get_YT_streams)
submit_button.grid(column=2, row=0, sticky='W', **options)

streams_label = ttk.Label(main, text="Available streams: ")
streams_label.grid(column=3, row=0, sticky='W', **options)
get_stream_button = ttk.Button(main, text="Download", command=download_stream)
get_stream_button.grid(column=3, row=0, sticky='E', **options)
streams_list = tk.Listbox(main, height=20, width=50, selectmode='extended', background="yellow")
streams_list.grid(column=3, row=1, rowspan=20, sticky='W', **options)

video_thumb = ttk.Label(main, image=default_thumbn)
video_thumb.grid(row=3, column=0, columnspan=3, sticky='W', **options)

title_label = ttk.Label(main, text="Title: ")
title_label.grid(row=4, column=0, sticky='W', **options)
video_title = ttk.Label(main, text="")
video_title.grid(row=4, column=1, sticky='W', **options)

channel_label = ttk.Label(main, text="Channel: ")
channel_label.grid(row=5, column=0, sticky='W', **options)
video_channel = ttk.Label(main, text="")
video_channel.grid(row=5, column=1, sticky='W', **options)

pub_label = ttk.Label(main, text="Published: ")
pub_label.grid(row=6, column=0, sticky='W', **options)
video_pub = ttk.Label(main, text="")
video_pub.grid(row=6, column=1, sticky='W', **options)

length_label = ttk.Label(main, text="Length: ")
length_label.grid(row=7, column=0, sticky='W', **options)
video_length = ttk.Label(main, text="")
video_length.grid(row=7, column=1, sticky='W', **options)

space = ttk.Label(main, text=" ---------------------------------------------------")
space.grid(column=0, row=8, columnspan=3, sticky='W', **options)
space = ttk.Label(main, text=" ---------------------------------------------------")
space.grid(column=0, row=9, columnspan=3, sticky='W', **options)

animation_bar = ttk.Label(main, width=141, background="black")
animation_bar.grid(column=0, row=10, rowspan=2, columnspan=4, sticky='W', **options)

root.mainloop()

# Create top level menu
menubar = tk.Menu()
root.config(menu=menubar)

# Create separate roots for functions
file_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")

root.mainloop()
