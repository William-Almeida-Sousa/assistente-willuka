import os
import sys
import speech_recognition as sr
import webbrowser as browser
from gtts import gTTS
from playsound import playsound
from datetime import datetime, timedelta
import subprocess
import threading

# Função para criar e tocar um arquivo de áudio
def cria_audio(nome_arquivo, mensagem, idioma='pt-br'):
    try:
        tts = gTTS(text=mensagem, lang=idioma)
        tts.save(nome_arquivo)
        playsound(nome_arquivo)
        os.remove(nome_arquivo)
    except Exception as e:
        print(f"Erro ao criar áudio: {e}")

# Função para monitorar o áudio do microfone
def monitora_audio():
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        recon.pause_threshold = 1
        recon.adjust_for_ambient_noise(source, duration=1)
        while True:
            print("Diga algo, estou te ouvindo")
            try:
                audio = recon.listen(source)
                mensagem = recon.recognize_google(audio, language='pt-BR').lower()
                print(f"Você disse: {mensagem}")
                executa_comandos(mensagem)
            except sr.UnknownValueError:
                print("Não entendi, poderia repetir?")
            except sr.RequestError:
                print("Erro na conexão.")

# Função para criar áudio a partir de um texto
def audio_texto():
    while True:
        escolha = input("Escolha uma opção: \n(1) Texto para Áudio\n(2) Sair")
        if escolha == "1":
            text_to_say = input("Digite seu texto: ")
            language = "pt"
            gtts_object = gTTS(text=text_to_say, lang=language, slow=False)
            gtts_object.save("gtts.mp3")
            playsound("gtts.mp3")
            os.remove("gtts.mp3")
        elif escolha == "2":
            return

# Função para realizar a busca no Youtube
def monitora_youtube(mensagem):
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        recon.pause_threshold = 1
        recon.adjust_for_ambient_noise(source, duration=1)
        while True:
            print("O que você quer procurar no Youtube?")
            cria_audio('you.mp3', 'O que você quer procurar no Youtube?')
            try:
                audio = recon.listen(source)
                mensagem = recon.recognize_google(audio, language='pt-BR').lower()
                print(f"Você disse: {mensagem}")
                executa_comandos(mensagem)
            except sr.UnknownValueError:
                print("Não entendi, poderia repetir?")
            except sr.RequestError:
                print("Erro na conexão.")
            return mensagem

# Função para executar comandos com base na mensagem recebida
def executa_comandos(mensagem):
    if 'fechar assistente' in mensagem:
        cria_audio('saindo.mp3', 'Estou saindo. Até mais!')
        sys.exit()
    elif 'horas' in mensagem:
        hora_atual = datetime.now().strftime('%H:%M')
        cria_audio('horas.mp3', f"Agora são {hora_atual}")
    elif 'desligar computador' in mensagem:
        if 'uma hora' in mensagem:
            os.system("shutdown -s -t 3600")
        elif 'meia hora' in mensagem:
            os.system("shutdown -s -t 1800")
    elif 'cancelar desligamento' in mensagem:
        os.system("shutdown -a")
    elif 'pesquisar' in mensagem:
        pesquisa_online(mensagem)
    elif 'abrir calculadora' in mensagem:
        subprocess.Popen(['calc.exe'])
    elif 'abrir bloco de notas' in mensagem:
        subprocess.Popen(['notepad.exe'])
    elif 'abrir site' in mensagem:
        mensagem = mensagem.replace('abrir site', '').strip()
        browser.open(mensagem)
    elif 'abrir youtube' in mensagem:
        keyword = monitora_youtube(mensagem)
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            browser.get().open(url)
    elif 'texto para áudio' in mensagem:
        audio_texto()

# Função para realizar pesquisas online
def pesquisa_online(mensagem):
    if 'google' in mensagem:
        mensagem = mensagem.replace('pesquisar', '').replace('google', '').strip()
        browser.open(f'https://google.com/search?q={mensagem}')
    elif 'youtube' in mensagem:
        mensagem = mensagem.replace('pesquisar', '').replace('youtube', '').strip()
        browser.open(f'https://youtube.com/results?search_query={mensagem}')

# Função principal
def main():
    cria_audio('ola.mp3', 'Olá sou sua assistente Willuka, em que posso te ajudar?')
    monitora_audio()

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
