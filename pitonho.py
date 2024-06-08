import os
from pydub import AudioSegment
import speech_recognition as sr

def transcrever_audio(audio_path, output_path, chunk_length_ms=30000):
    recognizer = sr.Recognizer()
    
    audio = AudioSegment.from_file(audio_path)
    
    audio_chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    transcricao_completa = ""

    print(enumerate(audio_chunks))
    
    for i, chunk in enumerate(audio_chunks):
        chunk_filename = f"chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")
        
        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="pt-BR")
            except sr.UnknownValueError:
                text = "Não foi possível reconhecer a fala no áudio."
            except sr.RequestError as e:
                text = f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}"

        print(text)
        
        transcricao_completa += text + " "
        os.remove(chunk_filename)
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(transcricao_completa)

audio_path = "audio.wav"
output_path = "transcrito.txt"

transcrever_audio(audio_path, output_path)
