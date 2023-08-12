# SpeechRecognition
# Google -> Google Speech Recognition (reconhecimento em português)
# Google -> Google Cloud
# IBM Watson
# Bing da Microsoft
# Microsoft Azure Recognition
# Sphinx
# Wit.ai
# Snowboy
# Houndify
# Python Impressionador - Mentoria Hashtag: Reconhecimento de Fala - SpeechRecognition
# Código refatorado por mim

import speech_recognition as sr
import time

class ReconhecimentoFala():

    def __init__(self):
        self.pausa = 1
        self.device = 1
        self.acabou = False
        self.lingua = "pt-BR"
        self.rec = sr.Recognizer()

    def listar_microfones(self):
        for idx, mic in enumerate(sr.Microphone().list_microphone_names()):
            print(f"Dispositivo: {idx} - {mic}")

    def _abrir_microfone(self):

        with sr.Microphone(device_index=self.device) as microfone:
            self.rec.adjust_for_ambient_noise(microfone)
            self.rec.pause_threshold = self.pausa
            print("PODE COMEÇAR A FALAR!!")
            audio = self.rec.listen(microfone)
        return audio

    def mudar_pausa(self, pausa):
        self.pausa = pausa

    def mudar_microfone(self, mic):
        self.device = mic

    def ler_texto(self):
        audio = self._abrir_microfone()
        # reconhece o audio e traduz para texto em portugues
        try:
            texto = self.rec.recognize_google(audio, language=self.lingua)
            print(texto)
        except:
            print("Não capturei nenhum audio!")

    def criar_audio(self):
        audio = self._abrir_microfone()
        # salvar o audio
        with open("audio.wav", "wb") as arquivo:
            arquivo.write(audio.get_wav_data())

    def ler_arquivo_audio(self, arquivo):
        with sr.AudioFile(arquivo) as arquivo_audio:
            audio = self.rec.record(arquivo_audio)
            texto = self.rec.recognize_google(audio, language=self.lingua)
            print(texto)

    def tratar_audio(self, rec, audio):

        try:
            texto = rec.recognize_google(audio, language="pt-BR")
            if "encerrar gravação" in texto:
                self.acabou = True
        except:
            print("Não escutei!!")

    def reconhecer_audio_longo(self):

        with sr.Microphone(device_index=1) as microfone:
            self.rec.adjust_for_ambient_noise(microfone)
            self.rec.pause_threshold = 1  # pausa maior, finaliza a captura do audio
            self.rec.dynamic_energy_adjustment_ratio = 1.5
            print("PODE COMEÇAR A FALAR!!")

        # Multi Threads
        # Thread 1
        parar_ouvir = self.rec.listen_in_background(microfone, self.tratar_audio)

        # Thread 2
        while True:
            time.sleep(0.1)
            if self.acabou:
                break

        # Thread 1
        parar_ouvir(wait_for_stop=False)


if __name__ == '__main__':
    fala = ReconhecimentoFala()
    fala.listar_microfones()
    #fala.mudar_microfone(mic=1)
    #fala.mudar_pausa(pausa=2)
    #fala.ler_texto()
    #fala.criar_audio()
    #fala.ler_arquivo_audio("audio.wav")
    #fala.reconhecer_audio_longo()


