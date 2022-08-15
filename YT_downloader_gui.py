import io
import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import YT_stream_handler


thumb_size = 256, 256


def get_YT_streams():
    url = yt_url.get()

    yt = YT_stream_handler.YTVideoDLOptions(url)

    print("Title: ", yt.yt.title)
    print("Length of video: ", yt.yt.length, "seconds")
    print("Channel: ", yt.yt.channel_id.title())
    print("Published: ", yt.yt.publish_date)
    print("Thumb: ", yt.yt.thumbnail_url)

    try:
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
    except AttributeError:
        print("1...No streams available...")
    except TypeError:
        print("2...No streams available...")

    for each in prog_streams:
        print(each)
        print(each.filesize, each.resolution)

        streams_list.insert(count, f'{each.filesize} - {each.resolution}')
        count += 1

    print(f'Searching for adaptive stream for {yt.url}')
    try:
        adap_streams = yt.yt.streams.filter(adaptive=True).order_by('resolution').desc()
    except AttributeError:
        print("1...No streams available...")
    except TypeError:
        print("2...No streams available...")

    for each in adap_streams:
        print(each)

    # ... .filter(progressive=True, file_extension='mp4')
    # ... .order_by('resolution')
    # ... .desc()
    # ... .first()
    # ... .download()

    '''
    stream = yt.yt.streams.filter(progressive=True).get_highest_resolution()

    if not stream:
        print(f'No progressive stream found for {yt.url}')
        
        print(f'Searching for adaptive stream for {yt.url}')
        stream = yt.yt.streams.filter(adaptive=True).get_highest_resolution()
        if stream == None:
            print(f'No adaptive stream available for {yt.url}')
            return None
        else:
            audio = yt.yt.streams.filter(only_audio=True).first()
            if audio == None:
                print(f'No audio stream found for {yt.url}')
            else:
                stream.stream_to_buffer()
                print("merging video and audio")
                # DOWNLOAD VIDEO AND AUDIO FILE
                # MERGE VIDEO AND AUDIO

                # ff = FFmpeg(
                # ...     inputs={'video.mp4': None, 'audio.mp3': None},
                # ...     outputs={'output.ts': '-c:v h264 -c:a ac3'}
                # ... )
                # >>> ff.cmd
                # 'ffmpeg -i audio.mp4 -i video.mp4 -c:v h264 -c:a ac3 output.ts'
                # >>> ff.run()
        
        return None
    else:
        return f'Progressive stream found for {yt.url}'
        
    '''
    url_entry.delete("0", "end")


root = tk.Tk()
root.title("tk YouTube Video Downloader")
root.option_add("*tearOff", False)
root.geometry("900x400")
root.resizable(False, False)

options = {'padx': 5, 'pady': 5}

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
pub_label = ttk.Label(main, text="Published: ")
pub_label.grid(row=6, column=0, sticky='W', **options)
length_label = ttk.Label(main, text="Length: ")
length_label.grid(row=7, column=0, sticky='W', **options)

root.mainloop()

# Create top level menu
menubar = tk.Menu()
root.config(menu=menubar)

# Create separate roots for functions
file_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")

root.mainloop()
