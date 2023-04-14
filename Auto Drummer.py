import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty
from pydub import AudioSegment
from pydub.playback import play
import threading

# Clear terminal function useful for debugging
def clear():
    print("\x1B\x5B2J", end="")
    print("\x1B\x5BH", end="")

bass = []
snare = []
low_tom = []
middle_tom = []
high_tom = []
closed_hat = []
opened_hat = []
ride = []
crash = []

bass_copied = []
snare_copied = []
low_tom_copied = []
middle_tom_copied = []
high_tom_copied = []
closed_hat_copied = []
opened_hat_copied = []
ride_copied = []
crash_copied = []

for a in range (0, 32):
    bass[a] = bass.append(0)
    snare[a] = snare.append(0)
    low_tom[a] = low_tom.append(0)
    middle_tom[a] = middle_tom.append(0)
    high_tom[a] = high_tom.append(0)
    closed_hat[a] = closed_hat.append(0)
    opened_hat[a] = opened_hat.append(0)
    ride[a] = ride.append(0)
    crash[a] = crash.append(0)

    bass[a] = 0
    snare[a] = 0
    low_tom[a] = 0
    middle_tom[a] = 0
    high_tom[a] = 0
    closed_hat[a] = 0
    opened_hat[a] = 0
    ride[a] = 0
    crash[a] = 0

    bass_copied[a] = bass_copied.append(0)
    snare_copied[a] = snare_copied.append(0)
    low_tom_copied[a] = low_tom_copied.append(0)
    middle_tom_copied[a] = middle_tom_copied.append(0)
    high_tom_copied[a] = high_tom_copied.append(0)
    closed_hat_copied[a] = closed_hat_copied.append(0)
    opened_hat_copied[a] = opened_hat_copied.append(0)
    ride_copied[a] = ride_copied.append(0)
    crash_copied[a] = crash_copied.append(0)

    bass_copied[a] = 0
    snare_copied[a] = 0
    low_tom_copied[a] = 0
    middle_tom_copied[a] = 0
    high_tom_copied[a] = 0
    closed_hat_copied[a] = 0
    opened_hat_copied[a] = 0 
    ride_copied[a] = 0
    crash_copied[a] = 0

drums_page = 1
drums_pages = 1
tempo = 80
metrum = 4
one_tick_time = 60/tempo/metrum
change_page_signal = False
sound_to_play = "drums"

# Drum samples for composing
audio_in_file_kick = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\KICK.wav"
audio_in_file_snare = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\SNARE.wav"
audio_in_file_low_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_LOW.wav"
audio_in_file_middle_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_MIDDLE.wav"
audio_in_file_high_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_HIGH.wav"
audio_in_file_closed_hat = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\CLOSE_HAT.wav"
audio_in_file_opened_hat = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\OPEN_HAT.wav"
audio_in_file_ride = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\RIDE.wav"
audio_in_file_crash = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\CRASH.wav"

# Drum samples for checking
audio_out_file_kick = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\KICK.mp3"
audio_out_file_snare = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\SNARE.mp3"
audio_out_file_low_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_LOW.mp3"
audio_out_file_middle_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_MIDDLE.mp3"
audio_out_file_high_tom = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\TOM_HIGH.mp3"
audio_out_file_closed_hat = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\CLOSE_HAT.mp3"
audio_out_file_opened_hat = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\OPEN_HAT.mp3"
audio_out_file_ride = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\RIDE.mp3"
audio_out_file_crash = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\samples\\CRASH.mp3"

audio_out_file = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\AutoDrummer.wav"
audio_out_file_mp3 = "C:\\Users\Majst\Documents\VS CODE\\Auto Drummer\\AutoDrummer.mp3"

# Drum sample sounds - for composing
kick_s = AudioSegment.from_wav(audio_in_file_kick)
snare_s = AudioSegment.from_wav(audio_in_file_snare)
low_tom_s = AudioSegment.from_wav(audio_in_file_low_tom)
middle_tom_s = AudioSegment.from_wav(audio_in_file_middle_tom)
high_tom_s = AudioSegment.from_wav(audio_in_file_high_tom)
closed_hat_s = AudioSegment.from_wav(audio_in_file_closed_hat)
opened_hat_s = AudioSegment.from_wav(audio_in_file_opened_hat)
ride_s = AudioSegment.from_wav(audio_in_file_ride)
crash_s = AudioSegment.from_wav(audio_in_file_crash)

# Drum sounds - for checking
kick_sound = AudioSegment.from_mp3(audio_out_file_kick)
snare_sound = AudioSegment.from_mp3(audio_out_file_snare)
low_tom_sound = AudioSegment.from_mp3(audio_out_file_low_tom)
middle_tom_sound = AudioSegment.from_mp3(audio_out_file_middle_tom)
high_tom_sound = AudioSegment.from_mp3(audio_out_file_high_tom)
closed_hat_sound = AudioSegment.from_mp3(audio_out_file_closed_hat)
opened_hat_sound = AudioSegment.from_mp3(audio_out_file_opened_hat)
ride_sound = AudioSegment.from_mp3(audio_out_file_ride)
crash_sound = AudioSegment.from_mp3(audio_out_file_crash)

# Silence between the sounds = one tick time - sound time length [ms]
silent_kick = AudioSegment.silent(duration=one_tick_time*1000-len(kick_s))
silent_snare = AudioSegment.silent(duration=one_tick_time*1000-len(snare_s))
silent_low_tom = AudioSegment.silent(duration=one_tick_time*1000-len(low_tom_s))
silent_middle_tom = AudioSegment.silent(duration=one_tick_time*1000-len(middle_tom_s))
silent_high_tom = AudioSegment.silent(duration=one_tick_time*1000-len(high_tom_s))
silent_closed_hat = AudioSegment.silent(duration=one_tick_time*1000-len(closed_hat_s))
silent_opened_hat = AudioSegment.silent(duration=one_tick_time*1000-len(opened_hat_s))
silent_ride = AudioSegment.silent(duration=one_tick_time*1000-len(ride_s))
silent_crash = AudioSegment.silent(duration=one_tick_time*1000-len(crash_s))

silent_empty = AudioSegment.silent(duration=one_tick_time*1000)
silent_long = AudioSegment.silent(duration=one_tick_time*1000*128)

kivy.require('2.1.0')                             # Set Kivy version

# Drums composing screen
class DrumsScreen(Screen):

    checkbox_active = ListProperty([BooleanProperty(False) for i in range(1000)])

    def refresh_page(self):
        for i in range (0, 32):
            if snare[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+211] = True
            else:
                self.checkbox_active[i+211] = False
            if bass[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+111] = True
            else:
                self.checkbox_active[i+111] = False
            if low_tom[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+311] = True
            else:
                self.checkbox_active[i+311] = False
            if middle_tom[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+411] = True
            else:
                self.checkbox_active[i+411] = False
            if high_tom[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+511] = True
            else:
                self.checkbox_active[i+511] = False
            if closed_hat[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+611] = True
            else:
                self.checkbox_active[i+611] = False
            if opened_hat[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+711] = True
            else:
                self.checkbox_active[i+711] = False
            if ride[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+811] = True
            else:
                self.checkbox_active[i+811] = False 
            if crash[i+(drums_page-1)*32] == 1:
                self.checkbox_active[i+911] = True
            else:
                self.checkbox_active[i+911] = False 

    def checkbox_click(self, instance, value, index):
        global drums_page

        index = int(index)

        if value is True and index > 0:
            if index < 200:
                bass[int(index)-111 + 32*(drums_page-1)] = 1
            elif index < 300:
                snare[int(index)-211 + 32*(drums_page-1)] = 1
            elif index < 400:
                low_tom[int(index)-311 + 32*(drums_page-1)] = 1
            elif index < 500:
                middle_tom[int(index)-411 + 32*(drums_page-1)] = 1
            elif index < 600:
                high_tom[int(index)-511 + 32*(drums_page-1)] = 1
            elif index < 700:
                closed_hat[int(index)-611 + 32*(drums_page-1)] = 1
            elif index < 800:
                opened_hat[int(index)-711 + 32*(drums_page-1)] = 1
            elif index < 900:
                ride[int(index)-811 + 32*(drums_page-1)] = 1
            elif index < 1000:
                crash[int(index)-911 + 32*(drums_page-1)] = 1

        elif value is False and index > 0:
            if index < 200:
                bass[int(index)-111 + 32*(drums_page-1)] = 0
            elif index < 300:
                snare[int(index)-211 + 32*(drums_page-1)] = 0
            elif index < 400:
                low_tom[int(index)-311 + 32*(drums_page-1)] = 0
            elif index < 500:
                middle_tom[int(index)-411 + 32*(drums_page-1)] = 0
            elif index < 600:
                high_tom[int(index)-511 + 32*(drums_page-1)] = 0
            elif index < 700:
                closed_hat[int(index)-611 + 32*(drums_page-1)] = 0
            elif index < 800:
                opened_hat[int(index)-711 + 32*(drums_page-1)] = 0
            elif index < 900:
                ride[int(index)-811 + 32*(drums_page-1)] = 0
            elif index < 1000:
                crash[int(index)-911 + 32*(drums_page-1)] = 0

    def change_page(self, *args):
        global drums_page, drums_pages, bass, snare, low_tom, middle_tom, high_tom, closed_hat, opened_hat, ride, crash 

        if drums_page > 1 and args[1] == "back":
            drums_page = drums_page - 1
        elif args[1] == "forward":
            drums_page = drums_page + 1
            if drums_page > drums_pages:
                drums_pages = drums_page

                for a in range (32*(drums_pages-1), 32*(drums_pages-1)+32):
                    bass[a] = bass.append(0)
                    snare[a] = snare.append(0)
                    low_tom[a] = low_tom.append(0)
                    middle_tom[a] = middle_tom.append(0)
                    high_tom[a] = high_tom.append(0)
                    closed_hat[a] = closed_hat.append(0)
                    opened_hat[a] = opened_hat.append(0)
                    ride[a] = ride.append(0)
                    crash[a] = crash.append(0)

                    bass[a] = 0
                    snare[a] = 0
                    low_tom[a] = 0
                    middle_tom[a] = 0
                    high_tom[a] = 0
                    closed_hat[a] = 0
                    opened_hat[a] = 0
                    ride[a] = 0
                    crash[a] = 0

        self.ids.drums_pg.text = str(drums_page)

        self.refresh_page()

    def copy_page(self):
        for a in range (0, 32):
            bass_copied[a] = bass[a + (drums_page-1)*32]
            snare_copied[a] = snare[a + (drums_page-1)*32]
            low_tom_copied[a] = low_tom[a + (drums_page-1)*32]
            middle_tom_copied[a] = middle_tom[a + (drums_page-1)*32]
            high_tom_copied[a] = high_tom[a + (drums_page-1)*32]
            closed_hat_copied[a] = closed_hat[a + (drums_page-1)*32]
            opened_hat_copied[a] = opened_hat[a + (drums_page-1)*32]
            ride_copied[a] = ride[a + (drums_page-1)*32]
            crash_copied[a] = crash[a + (drums_page-1)*32]
    
    def paste_page(self):
        for a in range (0, 32):
            bass[a + (drums_page-1)*32] = bass_copied[a]
            snare[a + (drums_page-1)*32] = snare_copied[a]
            low_tom[a + (drums_page-1)*32] = low_tom_copied[a]
            middle_tom[a + (drums_page-1)*32] = middle_tom_copied[a]
            high_tom[a + (drums_page-1)*32] = high_tom_copied[a]
            closed_hat[a + (drums_page-1)*32] = closed_hat_copied[a]
            opened_hat[a + (drums_page-1)*32] = opened_hat_copied[a]
            ride[a + (drums_page-1)*32] = ride_copied[a]
            crash[a + (drums_page-1)*32] = crash_copied[a]

        self.refresh_page()
    
    def clear_page(self):
        for a in range (0, 32):
            bass[a + (drums_page-1)*32] = 0
            snare[a + (drums_page-1)*32] = 0
            low_tom[a + (drums_page-1)*32] = 0
            middle_tom[a + (drums_page-1)*32] = 0
            high_tom[a + (drums_page-1)*32] = 0
            closed_hat[a + (drums_page-1)*32] = 0
            opened_hat[a + (drums_page-1)*32] = 0
            ride[a + (drums_page-1)*32] = 0
            crash[a + (drums_page-1)*32] = 0
            
        self.refresh_page()

    def delete_page(self):
        global drums_pages, drums_page

        self.clear_page()

        if drums_pages > 1:
            if drums_page != drums_pages:
                for b in range (0, drums_pages-drums_page):
                    for a in range (0, 32):
                        bass[a + (b+drums_page-1)*32] = bass[a + 32 + (b+drums_page-1)*32]
                        snare[a + (b+drums_page-1)*32] = snare[a + 32 + (b+drums_page-1)*32]
                        low_tom[a + (b+drums_page-1)*32] = low_tom[a + 32 + (b+drums_page-1)*32]
                        middle_tom[a + (b+drums_page-1)*32] = middle_tom[a + 32 + (b+drums_page-1)*32]
                        high_tom[a + (b+drums_page-1)*32] = high_tom[a + 32 + (b+drums_page-1)*32]
                        closed_hat[a + (b+drums_page-1)*32] = closed_hat[a + 32 + (b+drums_page-1)*32]
                        opened_hat[a + (b+drums_page-1)*32] = opened_hat[a + 32 + (b+drums_page-1)*32]
                        ride[a + (b+drums_page-1)*32] = ride[a + 32 + (b+drums_page-1)*32]
                        crash[a + (b+drums_page-1)*32] = crash[a + 32 + (b+drums_page-1)*32]
                        bass[a + 32 + (b+drums_page-1)*32] = 0
                        snare[a + 32 + (b+drums_page-1)*32] = 0
                        low_tom[a + 32 + (b+drums_page-1)*32] = 0
                        middle_tom[a + 32 + (b+drums_page-1)*32] = 0
                        high_tom[a + 32 + (b+drums_page-1)*32] = 0
                        closed_hat[a + 32 + (b+drums_page-1)*32] = 0
                        opened_hat[a + 32 + (b+drums_page-1)*32] = 0
                        ride[a + 32 + (b+drums_page-1)*32] = 0
                        crash[a + 32 + (b+drums_page-1)*32] = 0
            else:
                drums_page = drums_page - 1
                self.ids.drums_pg.text = str(drums_page)

            drums_pages = drums_pages - 1

        self.refresh_page()

# Switching between screens (in .kv file)
class ScreenManagement(ScreenManager):
    pass

# User interaction program logic
class MainMenuScreen(Screen):

    def generate(self):
        global kick_s, snare_s, silent_empty, silent_long, silent_kick, silent_snare, bass, snare

        # Initialize the drums
        drums = AudioSegment.silent(duration=one_tick_time*1000*128)
        kicks = AudioSegment.silent(duration=one_tick_time*1000*128)
        snares = AudioSegment.silent(duration=one_tick_time*1000*128)
        low_toms = AudioSegment.silent(duration=one_tick_time*1000*128)
        middle_toms = AudioSegment.silent(duration=one_tick_time*1000*128)
        high_toms = AudioSegment.silent(duration=one_tick_time*1000*128)
        closed_hats = AudioSegment.silent(duration=one_tick_time*1000*128)
        opened_hats = AudioSegment.silent(duration=one_tick_time*1000*128)
        rides = AudioSegment.silent(duration=one_tick_time*1000*128)
        crashes = AudioSegment.silent(duration=one_tick_time*1000*128)

        # Generate the drums sound
        for x in range (0, drums_pages):
            for i in range (32 * x, 32 * x + 32):

                if bass[i] == 1:
                    kicks = kicks[:(i * one_tick_time*1000)]
                    kicks = kicks + kick_s + silent_long

                if snare[i] == 1:
                    snares = snares[:(i * one_tick_time*1000)]
                    snares = snares + snare_s + silent_long

                if low_tom[i] == 1:
                    low_toms = low_toms[:(i * one_tick_time*1000)]
                    low_toms = low_toms + low_tom_s + silent_long

                if middle_tom[i] == 1:
                    middle_toms = middle_toms[:(i * one_tick_time*1000)]
                    middle_toms = middle_toms + middle_tom_s + silent_long

                if high_tom[i] == 1:
                    high_toms = high_toms[:(i * one_tick_time*1000)]
                    high_toms = high_toms + high_tom_s + silent_long

                if closed_hat[i] == 1:
                    closed_hats = closed_hats[:(i * one_tick_time*1000)]
                    closed_hats = closed_hats + closed_hat_s + silent_long

                if opened_hat[i] == 1:
                    opened_hats = opened_hats[:(i * one_tick_time*1000)]
                    opened_hats = opened_hats + opened_hat_s + silent_long

                if ride[i] == 1:
                    rides = rides[:(i * one_tick_time*1000)]
                    rides = rides + ride_s + silent_long

                if crash[i] == 1:
                    crashes = crashes[:(i * one_tick_time*1000)]
                    crashes = crashes + crash_s + silent_long

        drums = (((((((kicks.overlay(snares)).overlay(low_toms)).overlay(middle_toms)).overlay(high_toms)).overlay(closed_hats)).overlay(opened_hats)).overlay(rides)).overlay(crashes)

        drums = drums[:(drums_pages * one_tick_time * 32 * 1000 + 1000)]

        print("Drums duration: " + str(drums.duration_seconds - 1.0))

        drums.export(audio_out_file_mp3, format="mp3")
        
    def play_sound(self, value):
        global sound_to_play

        sound_to_play = value
        play_sound_thread = threading.Thread(target=self.play_in_background)
        play_sound_thread.start()

    def play_in_background(self):
        if sound_to_play == "drums":
            play(AudioSegment.from_mp3(audio_out_file_mp3))
        elif sound_to_play == "kick":
            play(kick_sound)
        elif sound_to_play == "snare":
            play(snare_sound)
        elif sound_to_play == "low_tom":
            play(low_tom_sound)
        elif sound_to_play == "middle_tom":
            play(middle_tom_sound)
        elif sound_to_play == "high_tom":
            play(high_tom_sound)
        elif sound_to_play == "closed_hat":
            play(closed_hat_sound)
        elif sound_to_play == "opened_hat":
            play(opened_hat_sound)
        elif sound_to_play == "ride":
            play(ride_sound)
        elif sound_to_play == "crash":
            play(crash_sound)
    
    def tempo(self):
        global tempo, one_tick_time, metrum

        tempo = int(self.tempo_set.text)
        one_tick_time = 60/tempo/metrum
    
    def metrum(self, value):
        global metrum, one_tick_time, tempo

        metrum = int(value)
        one_tick_time = 60/tempo/metrum
        print("metrum: ", metrum)
            
kv = Builder.load_file('AutoDrummerScreen.kv')  # Load app interface from .kv file

# Build application
class MyApp(App):
    def build(self):
        return kv

# Run application
if __name__ == '__main__':
    MyApp().run()