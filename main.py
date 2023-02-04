# ________________imports______________
import tkinter as tk
from tkinter import filedialog
import pygame
import tkinter.ttk as ttk
import librosa
import numpy as np
import soundfile as sf
import pyaudio
import wave
from mutagen.mp3 import MP3
from pydub import AudioSegment
# from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from os import path
import time

# tkinter___________________________________
root = tk.Tk()
root.geometry('500x230+200+70')
tabControl = ttk.Notebook(root)
pygame.mixer.init()

# ________________var_______________________
varspeedaud = tk.StringVar()
varreversaud = tk.StringVar()
varechoaud = tk.StringVar()
varmp3playaud = tk.StringVar()

stopped = False
paused = False
muted = False
pausedwav = False
stoppedwav = False
global speedaud
global reversaud
global echoaud
global mp3playaud
global wavaud
global mp3aud


# _________________functions__________________
def add_song(x):
    if x == "speedaud":
        global speedaud
        speedaud = filedialog.askopenfilename(title="choose a Audio",
                                              filetypes=(("wav Files", "*.wav"), ("mp3 Files", "*.mp3")))
    elif x == "reversaud":
        global reversaud
        reversaud = filedialog.askopenfilename(title="choose a Audio",
                                               filetypes=(("wav Files", "*.wav"), ("mp3 Files", "*.mp3")))
    elif x == "echoaud":
        global echoaud
        echoaud = filedialog.askopenfilename(title="choose a Audio",
                                             filetypes=(("wav Files", "*.wav"), ("mp3 Files", "*.mp3")))
    elif x == "mp3playaud":
        global mp3playaud
        mp3playaud = filedialog.askopenfilename(title="choose a Audio",
                                                filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))

    elif x == "wavcon":
        global wavaud
        wavaud = filedialog.askopenfilename(title="choose a Audio",
                                            filetypes=(("wav Files", "*.wav"), ("mp3 Files", "*.mp3")))

    elif x == "mp3con":
        global mp3aud
        mp3aud = filedialog.askopenfilename(title="choose a Audio",
                                            filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))


def set_vol(val):
    volume = int(val) / 100
    pygame.mixer.music.set_volume(volume)


def mute_music(x):
    global muted
    if muted:  # Unmute the music
        pygame.mixer.music.set_volume(0.7)
        if x == "record":
            volumeBtnrec.configure(text="unmuted")  # image=volumePhoto
        elif x == "speed":
            volumeBtnspeed.configure(text="unmuted")  # image=volumePhoto
        elif x == "revers":
            volumeBtnrev.configure(text="unmuted")  # image=volumePhoto
        elif x == "echo":
            volumeBtnecho.configure(text="unmuted")  # image=volumePhoto
        elif x == "mp3":
            volumeBtn.configure(text="unmuted")  # image=volumePhoto
        scale.set(70)
        muted = False
    else:  # mute the music
        pygame.mixer.music.set_volume(0)
        if x == "record":
            volumeBtnrec.configure(text="muted")  # image=volumePhoto
        elif x == "speed":
            volumeBtnspeed.configure(text="muted")  # image=volumePhoto
        elif x == "revers":
            volumeBtnrev.configure(text="muted")  # image=volumePhoto
        elif x == "echo":
            volumeBtnecho.configure(text="muted")  # image=volumePhoto
        elif x == "mp3":
            volumeBtn.configure(text="muted")  # image=volumePhoto
        scale.set(0)
        muted = True


def plot(x):
    if x == "record":
        sig, sr = librosa.load("record.wav")
    elif x == "speed":
        global speedaud
        sig, sr = librosa.load(speedaud)
    elif x == "revers":
        global reversaud
        sig, sr = librosa.load(reversaud)
    elif x == "echo":
        global echoaud
        sig, sr = librosa.load(echoaud)

    duration = len(sig) / sr
    timee = np.arange(0, duration, 1 / sr)  # time vector
    plt.plot(timee, sig)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Signal')
    plt.show()


###############play Audio########


def stop():
    pygame.mixer.music.stop()
    global stoppedwav
    stoppedwav = True


def pause(is_paused):
    global pausedwav
    pausedwav = is_paused
    if pausedwav:
        pygame.mixer.music.unpause()
        pausedwav = False
    else:
        pygame.mixer.music.pause()
        pausedwav = True


##########record#############
def start_recoud():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    print('stat recording')
    global new
    new = True
    while new:
        data = stream.read(1024)
        frames.append(data)
        root.update()

    print('end')
    stream.stop_stream()
    stream.close()
    p.terminate()
    sound_file = wave.open("record.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()


def stop_record():
    global new
    global audio
    new = False


def playrec():
    pygame.mixer.music.load("record.wav")
    pygame.mixer.music.play()


#############speed change########

def change_speed(aud, x):
    global speedaud
    sig, sr = librosa.load(aud)
    new_signal = librosa.effects.time_stretch(sig, x)
    sf.write("time scaling.wav", new_signal, sr)
    speedaud = "time scaling.wav"


def playspeed():
    global speedaud
    pygame.mixer.music.load(speedaud)
    pygame.mixer.music.play()


###########revers###############

def revers(aud):
    global reversaud
    sig, sr = librosa.load(aud)
    new = sig[::-1]
    sf.write("revers.wav", new, sr)
    reversaud = "revers.wav"


def playrev():
    global reversaud
    pygame.mixer.music.load(reversaud)
    pygame.mixer.music.play()


###########echo#################

def echo(aud, delaytime):
    global echoaud
    sig, sr = librosa.load(aud)
    delay_len = round(0.1 * sr)
    leading_zero = np.zeros(delay_len)
    delay = np.concatenate((leading_zero, sig))
    out1 = np.concatenate((sig, leading_zero))
    final = out1 + delaytime * delay
    sf.write("echo.wav", final, sr)
    echoaud = "C:/Users/nada/IdeaProjects/sms-tools-master/sms-tools-master/Audioprocessing/echo.wav"


def playecho():
    global echoaud
    pygame.mixer.music.load(echoaud)
    pygame.mixer.music.play()


###########mp3player############
def playmp3():
    global mp3playaud
    pygame.mixer.music.load(mp3playaud)
    pygame.mixer.music.play()
    play_time()
    # Update Slider To position
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)


def play_time():
    # Check for double timing
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    global mp3playaud

    song_mut = MP3(mp3playaud)
    # Get song Length
    global song_length
    song_length = song_mut.info.length
    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 second
    current_time = +1

    if int(my_slider.get()) == int(song_length):
        pass
        # status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)


def stopmp3():
    pygame.mixer.music.stop()
    global stopped
    stopped = True


def pausemp3(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def slide(x):
    global mp3playaud

    pygame.mixer.music.load(mp3playaud)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


##########converter##################3

def convert_wavtomp3(aud):
    output_file = "converted from wav.mp3"
    sound = AudioSegment.from_wav(aud)
    sound.export(output_file, format="mp3")


def convert_mp3towav(aud):
    output_file = "converted from mp3.wav"
    sound = AudioSegment.from_mp3(aud)
    sound.export(output_file, format="wav")


# _____________main taps___________________
record = ttk.Frame(tabControl)
speedch = ttk.Frame(tabControl)
Revers = ttk.Frame(tabControl)
Echo = ttk.Frame(tabControl)
mp3player = ttk.Frame(tabControl)
converter = ttk.Frame(tabControl)

tabControl.add(record, text='Record')
tabControl.add(speedch, text='Speed change')
tabControl.add(Revers, text='Revers')
tabControl.add(Echo, text='echo')
tabControl.add(mp3player, text='mp3 player')
tabControl.add(converter, text='Converter')

tabControl.pack(expand=1, fill="both")



# _____________record tap__________________

startbt = tk.Button(record, text="Start Recording", command=lambda: start_recoud())
stopbt = tk.Button(record, text="Stop Recording", command=lambda: stop_record())

startbt.place(x=160, y=30)
stopbt.place(x=160, y=70)

##########play it###########
playrec_button = tk.Button(record, text="play", command=playrec)
playrec_button.place(x=110, y=125)

stoprec_button = tk.Button(record, text="stop", command=stop)
stoprec_button.place(x=180, y=125)

pauserec_button = tk.Button(record, text="pause", command=lambda: pause(pausedwav))
pauserec_button.place(x=250, y=125)

plotbt = tk.Button(record, text="PLot", relief="flat", command=lambda: plot("record"), bg="gray")
plotbt.place(x=200, y=160)

volumeBtnrec = tk.Button(record, command=lambda: mute_music("record"), text="unmuted")
volumeBtnrec.place(x=380, y=125)

# volum scal___________
scale = tk.Scale(record, from_=0, to=100, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)
scale.place(x=380, y=12)

# _____________speed change__________________

speed_up_bt = tk.Button(speedch, text="speed up", command=lambda: change_speed(speedaud, 1.5))
speed_up_bt.place(x=130, y=70)

speed_down_bt = tk.Button(speedch, text="speed down", command=lambda: change_speed(speedaud, 0.7))
speed_down_bt.place(x=250, y=70)

select_button_speed = tk.Button(speedch, text="Add song", command=lambda: add_song("speedaud"))
select_button_speed.place(x=240, y=20)
speedent = tk.Entry(speedch, relief="flat", textvariable=varspeedaud, highlightthickness=1, highlightbackground="gray",
                    highlightcolor="cyan")
speedent.place(x=20, y=20, width=210)

##########play it###########

playspeed_button = tk.Button(speedch, text="play", command=playspeed)
playspeed_button.place(x=180, y=125)

stopspeed_button = tk.Button(speedch, text="stop", command=stop)
stopspeed_button.place(x=110, y=125)

pausespeed_button = tk.Button(speedch, text="pause", command=lambda: pause(pausedwav))
pausespeed_button.place(x=250, y=125)

plotbt = tk.Button(speedch, text="PLot", command=lambda: plot("speed"))
plotbt.place(x=200, y=160)

volumeBtnspeed = tk.Button(speedch, command=lambda: mute_music("speed"), text="unmuted")
volumeBtnspeed.place(x=380, y=125)

# volum scal___________
scale = tk.Scale(speedch, from_=0, to=100, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)
scale.place(x=380, y=12)

# _____________revers__________________
reves = tk.Button(Revers, text="revers", command=lambda: revers(reversaud))
reves.place(x=200, y=70)

select_button_revers = tk.Button(Revers, text="Add song", command=lambda: add_song("reversaud"))
select_button_revers.place(x=240, y=20)

reversent = tk.Entry(Revers, relief="flat", textvariable=varreversaud, highlightthickness=1, highlightbackground="gray",
                     highlightcolor="cyan")
reversent.place(x=20, y=20, width=210)

##########play it###########

playrev_button = tk.Button(Revers, text="play", command=playrev)
playrev_button.place(x=180, y=125)

stoprev_button = tk.Button(Revers, text="stop", command=stop)
stoprev_button.place(x=110, y=125)

pauserev_button = tk.Button(Revers, text="pause", command=lambda: pause(pausedwav))
pauserev_button.place(x=250, y=125)

plotbt = tk.Button(Revers, text="PLot", command=lambda: plot("revers"))
plotbt.place(x=200, y=160)

volumeBtnrev = tk.Button(Revers, command=lambda: mute_music("revers"), text="unmuted")
volumeBtnrev.place(x=380, y=125)

# volum scal___________
scale = tk.Scale(Revers, from_=0, to=100, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)
scale.place(x=380, y=12)

# _____________echo__________________
echo_bt = tk.Button(Echo, text="echo", command=lambda: echo(echoaud, 2))
echo_bt.place(x=200, y=70)

select_button_echo = tk.Button(Echo, text="Add song", command=lambda: add_song("echoaud"))
select_button_echo.place(x=240, y=20)

echoent = tk.Entry(Echo, relief="flat", textvariable=varechoaud, highlightthickness=1, highlightbackground="gray",
                   highlightcolor="cyan")
echoent.place(x=20, y=20, width=210)

##########play it###########

playecho_button = tk.Button(Echo, text="play", command=playecho)
playecho_button.place(x=180, y=125)

stopecho_button = tk.Button(Echo, text="stop", command=stop)
stopecho_button.place(x=110, y=125)

pauseecho_button = tk.Button(Echo, text="pause", command=lambda: pause(pausedwav))
pauseecho_button.place(x=250, y=125)

plotbt = tk.Button(Echo, text="PLot", command=lambda: plot("echo"))
plotbt.place(x=200, y=160)

volumeBtnecho = tk.Button(Echo, command=lambda: mute_music("echo"), text="unmuted")
volumeBtnecho.place(x=380, y=125)

# volum scal___________
scale = tk.Scale(Echo, from_=0, to=100, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)
scale.place(x=380, y=12)
# _____________mp3player__________________
select_button_playmp3 = tk.Button(mp3player, text="Add song", command=lambda: add_song("mp3playaud"))
select_button_playmp3.pack()
select_button_playmp3.place(x=240, y=20)

mp3ent = tk.Entry(mp3player, relief="flat", textvariable=varmp3playaud, highlightthickness=1,
                  highlightbackground="gray",
                  highlightcolor="cyan")
mp3ent.pack()
mp3ent.place(x=20, y=20, width=210)

playmp3_button = tk.Button(mp3player, text="play", command=playmp3)
playmp3_button.pack()
playmp3_button.place(x=110, y=125)

stopmp3_button = tk.Button(mp3player, text="stop", command=stopmp3)
stopmp3_button.pack()
stopmp3_button.place(x=180, y=125)

pausemp3_button = tk.Button(mp3player, text="pause", command=lambda: pausemp3(paused))
pausemp3_button.pack()
pausemp3_button.place(x=250, y=125)

volumeBtn = tk.Button(mp3player, command=mute_music, text="unmuted")
volumeBtn.pack()
volumeBtn.place(x=380, y=125)

# volum scal___________
scale = tk.Scale(mp3player, from_=100, to=0, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)
scale.pack()
scale.place(x=380, y=12)

my_slider = ttk.Scale(mp3player, from_=0, to=100, orient="horizontal", value=0, command=slide, length=290)
my_slider.pack()
my_slider.place(x=20, y=70)

root.mainloop()

# _____________converter__________________
convert_wav_to_mp3 = tk.Button(converter, text="Convert WAV", command=lambda: convert_wavtomp3(wavaud))
convert_wav_to_mp3.pack()

convertmp3towav = tk.Button(converter, text="Convert MP3", command=lambda: convert_mp3towav(mp3aud))
convertmp3towav.pack()

select_button_convertwav = tk.Button(converter, text="Add song", command=lambda: add_song("wavcon"))
select_button_convertwav.pack()

wavent = tk.Entry(converter, relief="flat", textvariable=varmp3playaud, highlightthickness=1,
                  highlightbackground="gray",
                  highlightcolor="cyan")
wavent.place(x=20, y=630)

select_button_convertmp3 = tk.Button(converter, text="Add song", command=lambda: add_song("mp3con"))
select_button_convertmp3.pack()

mp3ent = tk.Entry(converter, relief="flat", textvariable=varmp3playaud, highlightthickness=1,
                  highlightbackground="gray",
                  highlightcolor="cyan")
mp3ent.place(x=20, y=630)

root.mainloop()
