from vosk import Model, KaldiRecognizer
import os
import pyaudio
import json 
import pyttsx3
import webbrowser
import random  
class OwnerPerson:
    """
    Информация о владельце, включающие имя, город проживания, родной язык речи, изучаемый язык (для переводов текста)
    """
    name = ""
    home_city = ""

class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def play_hellow(*args: tuple):
    """
    Проигрывание приветственной речи
    """
    play_voice_assistant_speech('Вас приветвтвует, {} ;примитивная терминальная служба! Чем я могу помочь?'.format(assistant.name))

def play_quit(*args: tuple):
    """
    Проигрывание прощательной речи и выход
    """
    farewells = ['хорошего дня,{}'.format(person.name),'{}рада была помочь'.format(assistant.name)] 
    play_voice_assistant_speech(farewells[random.randint(0, len(farewells) - 1)])
    quit()

def search_for_term_on_google(*args: tuple):
    """
    Поиск в Google с автоматическим открытием ссылок (на список результатов и на сами результаты, если возможно)
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])

    # открытие ссылки на поисковик в браузере
     
    url = "https://yandex.ru/search/?text=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech('сайты по запросу {} найдено'.format(search_term))


def search_for_video_on_youtube(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech('видио по запросу {} найдено'.format(search_term))

def login (*args: tuple):
    log_n = open('log_name.txt','w')
    log_n.write(str(args[0]))
    log_n.close()

def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды и аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в метод
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass  # print("Command not found")




# перечень команд для использования
commands = {
    ( "привет","хай","хэллоу"): play_hellow,
    ("завершение","завершения","завершении","завершить"): play_quit,
    ("найди","поищи","найти"): search_for_term_on_google,
    ("видео"): search_for_video_on_youtube,
    ("логин","регистрация","зарегистрироваться","зарегистрировать"):login
}
'''
with open('12.json','r') as j_file:
    j_comand = json.load(j_file)
    print('<<<<<<<',j_file)
'''



if __name__ == "__main__":
    # инициализация инструментов распознавания и ввода речи
    model = Model(r"vosk-model-small-ru") # полный путь к модели  
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(
     format=pyaudio.paInt16,
     channels=1,
     rate=16000,
     input=True,
     frames_per_buffer=8000
    )
    stream.start_stream()

    # настройка данных пользователя
    person = OwnerPerson()
    log_name = open('log_name.txt','r')
    lgn = log_name.readline()
    if lgn != '':
        person.name = lgn
    else:
        person.name = ""
    log_name.close()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = 'Юми'  # "Youmi" 'Юми'
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # установка голоса по умолчанию
    voices = ttsEngine.getProperty("voices")
    assistant.recognition_language = "ru-RU"
    # Microsoft Irina Desktop - Russian
    ttsEngine.setProperty("voice", voices[0].id)
    play_hellow('')
    if person.name =="":
        play_voice_assistant_speech('Пожалуйста зарегестрируйтесь!')
    else:
        play_voice_assistant_speech('С возвращением {}!'.format(person.name))
    while True:
        data = stream.read(4000,exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data)>0):
            voice_input = json.loads(rec.Result())
            voice_input =voice_input['text']
            voice_input = voice_input.split(" ")
            print('>>>',voice_input)
            
            if voice_input ==['']:
                pass
            else:
                command = voice_input[0]
                command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
                execute_command_with_name(command, command_options)