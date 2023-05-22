from pydub import AudioSegment
from scipy.io.wavfile import write
import musical_scales
import random
import numpy as np
import string

octave = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
samplerate = 44100

def get_piano_notes():
    base_freqs = {"0": 16.35, "1": 32.70, "2": 65.41, "3": 130.81, "4": 261.63, "5": 523.25, "6": 1046.50, "7": 2093.00, "8": 4186.01}
    base_freq = 261.63 #Frequency of Note C4
    note_freqs = {}
    for i in range(len(octave)):
      note_freqs[octave[i]] = base_freq * pow(2,(i/12))
    for freq in base_freqs.keys():
      for i in range(len(octave)):
        note_freqs[octave[i] + freq] = base_freqs[freq] * pow(2,(i/12))
    note_freqs[''] = 0.0
    note_freqs['blank'] = 0.0
    return note_freqs
    
def get_wave(freq, duration=0.5):
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave
    
def get_song_data(music_notes):
    note_freqs = get_piano_notes()
    song = []
    for note in music_notes.split("-"):
      if ":" in note:
        notesplit = note.split(":")
        note = notesplit[0]
        duration = float(notesplit[1])
      else:
        duration = 0.5
      song.append(get_wave(note_freqs[note], duration=duration))
    song = np.concatenate(song)
    return song.astype(np.int16)
    
def get_chord_data(chords):
    chords = chords.split('-')
    note_freqs = get_piano_notes()
    chord_data = []
    for chord in chords:
        if ":" in chord:
          chordsplit = chord.split(":")
          chord = chordsplit[0]
          duration = float(chordsplit[1])
        else:
          duration = 0.5
        data = sum([get_wave(note_freqs[note], duration=duration) for note in chord.split("+")])
        chord_data.append(data)
    chord_data = np.concatenate(chord_data, axis=0)    
    return chord_data.astype(np.int16)

def save_song_data(music_notes, filename):
  data = get_song_data(music_notes)
  data = data * (16300/np.max(data))
  write(filename, samplerate, data.astype(np.int16))

def save_chord_data(chords, filename):
  data = get_chord_data(chords)
  data = data * (16300/np.max(data))
  write(filename, samplerate, data.astype(np.int16))

def join_audio(sounds, output_path):
    sound1 = sounds[0]
    sound1 = AudioSegment.from_wav(sound1)
    sound2 = sounds[1]
    sound2 = AudioSegment.from_wav(sound2)
    combined = sound1.overlay(sound2)
    for i in range(2):
      del sounds[0]
    for sound in sounds:
      sound = AudioSegment.from_wav(sound)
      combined = combined.overlay(sound)
    combined.export(output_path, format='wav')

def melody_maker(tonality):
  scale_tonic = random.choice(octave)
  if tonality == "major":
    print("major")
    scale = musical_scales.scale(scale_tonic)
  else:
    print("minor")
    scale = musical_scales.scale(scale_tonic, "harmonic minor")
  length = random.choice([0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1.5, 1.5, 2])
  first_note = random.choice(scale)
  length_melody = length
  melody = f"{first_note}:{length}-"
  while length_melody < 13:
    length = random.choice([0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1.5, 1.5, 2])
    note = random.choice(scale)
    melody += f"{note}:{length}-"
    length_melody += length
  length = random.choice([0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1.5, 1.5, 2])
  melody += f"{first_note}:{length}"
  return melody

def random_id():
  characters = string.ascii_letters + string.digits
  password = ''.join(random.choice(characters) for i in range(15))
  return password