import numpy as np
from scipy.io.wavfile import write
import io

class MorseEnglishConvertor:

    def __init__(self):
        self.rate = 44100  # audio sample rate

        self.mapping = {
            "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
            "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
            "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
            "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--","X": "-..-",
            "Y": "-.--", "Z": "--..", "1": ".----", "2": "..---", "3": "...--",
            "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
            "9": "----.", "0": "-----", " ": "/"
        }

        self.rev_mapping = {v: k for k, v in self.mapping.items()}

    def _generate_tone(self, duration, frequency=440):
        t = np.linspace(0, duration, int(self.rate * duration), False)
        tone = np.sin(2 * np.pi * frequency * t)
        return tone
    
    def _generate_silence(self, duration):
        return np.zeros(int(self.rate * duration))



    def eng_to_morse_text(self, eng_text):
        eng_text = eng_text.upper()
        morse = ""
        for char in eng_text:
            morse = morse + self.mapping.get(char, "") + " "
        morse = morse.strip()
        return morse
    
    def morse_to_eng_text(self, morse_text):
        eng = ""
        codes = morse_text.split(" ")
        for code in codes:
            eng = eng + self.rev_mapping.get(code, "")
        return eng

    def eng_to_morse_audio(self, eng_text, output_file="morse.wav"):
        eng_text = eng_text.upper()
        morse_text = self.eng_to_morse_text(eng_text)

        audio = np.array([], dtype=np.float32)

        for symbol in morse_text:
            if symbol == ".":
                # bop (short)
                audio = np.concatenate((
                    audio,
                    self._generate_tone(0.1),
                    self._generate_silence(0.1)
                ))

            elif symbol == "-":
                # beep (long)
                audio = np.concatenate((
                    audio,
                    self._generate_tone(0.3),
                    self._generate_silence(0.1)
                ))

            elif symbol == " ":
                # letter gap
                audio = np.concatenate((
                    audio,
                    self._generate_silence(0.3)
                ))

            elif symbol == "/":
                # word gap
                audio = np.concatenate((
                    audio,
                    self._generate_silence(0.7)
                ))

        # Normalize and convert to 16-bit PCM
        audio = audio / np.max(np.abs(audio))
        audio_int16 = np.int16(audio * 32767)

        write(output_file, self.rate, audio_int16)
        # Write WAV to memory instead of disk
        buffer = io.BytesIO()
        write(buffer, self.rate, audio_int16)
        buffer.seek(0)

        return buffer
