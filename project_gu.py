import pygame
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import os

class MusicPlayer:
    def __init__(self, root):
        # Initialize the MusicPlayer object.
        self.root = root
        self.root.title("Music Player")
        self.root.configure(bg="grey")

        # Initialize variables to manage the playlist and track state.
        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.start_time = 0

        # Initialize Pygame and its mixer module.
        pygame.init()
        pygame.mixer.init()

        # Create the user interface.
        self.create_ui()

    def create_ui(self):
        # Create the main user interface elements.

        # Label for the title.
        self.label = tk.Label(self.root, text="Music Player", font=("Helvetica", 16), bg="grey", fg="white")
        self.label.pack(pady=10)

        # Listbox for displaying the playlist.
        self.playlistbox = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="green", selectbackground="gray")
        self.playlistbox.pack(pady=20)

        # Button to add a song to the playlist.
        self.addButton = tk.Button(self.root, text="Add Song", command=self.add_song, bg="grey", fg="white")
        self.addButton.pack(side=tk.LEFT, padx=10)

        # Play button to play or resume music.
        self.playButton = ttk.Button(self.root, text="Play", command=self.play_resume_music, style='TButton', width=8, cursor="hand2")
        self.playButton.pack(side=tk.LEFT, padx=10)

        # Pause button to pause the music.
        self.pauseButton = ttk.Button(self.root, text="Pause", command=self.pause_music, style='TButton', width=8, cursor="hand2")
        self.pauseButton.pack(side=tk.LEFT, padx=10)

        # Stop button to stop the music.
        self.stopButton = tk.Button(self.root, text="Stop", command=self.stop_music, bg="grey", fg="white")
        self.stopButton.pack(side=tk.LEFT, padx=10)

        # Button to move to the previous track.
        self.prevButton = tk.Button(self.root, text="Previous", command=self.previous_track, bg="grey", fg="white")
        self.prevButton.pack(side=tk.LEFT, padx=10)

        # Button to move to the next track.
        self.nextButton = tk.Button(self.root, text="Next", command=self.next_track, bg="grey", fg="white")
        self.nextButton.pack(side=tk.LEFT, padx=10)

        # Button to toggle the volume control.
        self.volumeButton = tk.Button(self.root, text="Volume", command=self.toggle_volume, bg="grey", fg="white")
        self.volumeButton.pack(side=tk.LEFT, padx=10)

        # Frame for the volume control.
        self.volume_frame = tk.Frame(self.root, bg="grey")
        self.volume_frame.pack_forget()

        # Variable to track the volume level.
        self.volume_var = tk.DoubleVar()
        
        # Scale for adjusting the volume.
        self.volume_scale = tk.Scale(self.volume_frame, variable=self.volume_var, orient=tk.VERTICAL, showvalue=False,
                                     from_=1, to=0, resolution=0.01, command=self.update_volume, bg="black")
        self.volume_scale.pack()

    def add_song(self):
        # Open a file dialog to select and add a song to the playlist.
        song_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if song_path:
            # Add the selected song to the playlist and update the listbox.
            self.playlist.append(song_path)
            self.playlistbox.insert(tk.END, os.path.basename(song_path))

    def play_resume_music(self):
        # Play or resume the currently selected track.
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play(start=self.start_time)

    def pause_music(self):
        # Pause the currently playing track.
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            self.start_time = pygame.mixer.music.get_pos() / 1000.0

    def stop_music(self):
        # Stop the currently playing track.
        if pygame.mixer.music.get_busy() or self.paused:
            pygame.mixer.music.stop()
            self.paused = False
            self.start_time = 0

    def previous_track(self):
        # Move to the previous track in the playlist and play it.
        if self.current_track > 0:
            self.current_track -= 1
            self.play_resume_music()

    def next_track(self):
        # Move to the next track in the playlist and play it.
        if self.current_track < len(self.playlist) - 1:
            self.current_track += 1
            self.play_resume_music()

    def toggle_volume(self):
        # Toggle the visibility of the volume control frame.
        if self.volume_frame.winfo_ismapped():
            self.volume_frame.pack_forget()
        else:
            self.volume_frame.pack(side=tk.LEFT, padx=10)

    def update_volume(self, _):
        # Update the volume based on the current position of the volume scale.
        volume = self.volume_var.get()
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    # Create the Tkinter root window and the MusicPlayer instance.
    root = tk.Tk()
    music_player = MusicPlayer(root)
    
    # Start the Tkinter event loop.
    root.mainloop()