import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

words_by_level = {
    "easy": ["gato", "cachorro", "maçã", "leite", "sol"],
    "medium": ["casa", "escola", "amigo", "janela", "amarelo"],
    "hard": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]}
diff = input("Qual difficuldade você gostaria? [easy, medium, hard]")
word = random.choice(words_by_level[diff])

print("traduze " +  word + " para o inglês.")
duration = 5  # segundos de gravação
sample_rate = 44100
print("Fale agora...")
recording = sd.rec(
  int(duration * sample_rate), # o número de amostras a serem registradas
  samplerate=sample_rate,      # taxa de amostras
  channels=1,                  # 1 significa gravação mono
  dtype="int16")               # tipo de dados para as amostras registradas
sd.wait()  # aguardando o término da gravação
wav.write("output.wav", sample_rate, recording)
print("Gravação concluída, estou reconhecendo...")
recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)
try:
    text = recognizer.recognize_google(audio, language="pt-BR")
    print("Você disse:", text)
    translator = Translator()
    translated = translator.translate(word, dest = "en")  # O 'en' aqui é um código para inglês
    print("🌍 Como é:", translated.text)
except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
    print("A fala não pôde ser reconhecida.")
except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
    print(f"Service error: {e}")