import librosa
import os
import asyncio
from moviepy import editor
from PIL import Image
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

from GoogleDrive import UploadFiles

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.OKGREEN + "Welcome to the audio to video converter!" + bcolors.ENDC)
# print(bcolors.OKGREEN + "Please enter the path to the audio file you want to convert to a video." + bcolors.ENDC)
print(bcolors.OKGREEN + "Do you want to move the files after? (y / n)" + bcolors.ENDC)
move = input()
print(f"{bcolors.WARNING}Do you want to upload the videos to Youtube? (y / n)!{bcolors.ENDC}")
upload = input()
print(f"{bcolors.WARNING}Do you want to upload the videos to Google Drive? (y / n)!{bcolors.ENDC}")
uploadDrive = input()

file_list = os.listdir("D:/Programação/Projetos/piton/automation/images")
soundFiles_list = os.listdir("D:/Programação/Projetos/piton/automation/songs")

image_list = list()
imageName_list = list()
sound_list = list()

print(f"{bcolors.WARNING}Identifying images...{bcolors.ENDC}")
for file_name in file_list:
    filename, file_extension = os.path.splitext('D:/Programação/Projetos/piton/automation/images/' + file_name)
    if(file_extension == '.jpg'):
        print(f"{bcolors.OKBLUE}Image: {filename}{bcolors.ENDC}")

        image = Image.open(filename + file_extension)
        image_list.append(image)
        imageName_list.append(filename + file_extension)

        image.close()

print(f"{bcolors.WARNING}Identifying sounds...{bcolors.ENDC}")
for sound_name in soundFiles_list:
    soundname, sound_extension = os.path.splitext('D:/Programação/Projetos/piton/automation/songs/' + sound_name)

    if(sound_extension == '.wav' or sound_extension == '.mp3'):
        print(f"{bcolors.OKBLUE}Sound: {soundname + sound_extension}{bcolors.ENDC}")
        sound_list.append(soundname + sound_extension)


# print(image_list)
# print(sound_list)

i = 0
for sound_name in sound_list:
    if i >= imageName_list.__len__():
        print(f"{bcolors.FAIL}Image not found for {sound_name}")
        i = i + 1
        continue

    print(f"{bcolors.OKCYAN}Generating video for " + sound_name + ' with ' + imageName_list[i])

    duration = format(librosa.get_duration(filename=sound_name)/60, ".2f")
    print(f"{bcolors.WARNING}Duration: {duration} minutes{bcolors.ENDC}")

    try:
        image = editor.ImageClip(imageName_list[i])
        
        video = editor.CompositeVideoClip(
            [
                image,
            ],
            size=image.size).set_duration(duration)

        audio = editor.AudioFileClip(sound_name)
        final_clip = video.set_audio(audio)
        final_clip.write_videofile('./videos/' + sound_name.split('/')[-1].split('.')[0] + '.mp4', fps=10)

    except Exception as e:
        print(f"{bcolors.FAIL}Error on {sound_name}")
        print({bcolors.FAIL} + e)

    print(f"{bcolors.OKGREEN}Video generated for {sound_name}{bcolors.ENDC}\n")

    if upload == 'y':
        print(f"{bcolors.OKGREEN}Uploading videos...{bcolors.ENDC}")

        CLIENT_SECRET_FILE = './client_secrets.json'
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

        request_body = {
            'snippet': {
                'categoryI': 19,
                'title': sound_name.split('/')[-1].split('.')[0],
                'description': 'Hello World Description',
                # 'tags': ['Travel', 'video test', 'Travel Tips']
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': upload_date_time,
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': True
        }

        mediaFile = MediaFileUpload('./videos/' + sound_name.split('/')[-1].split('.')[0] + '.mp4')

        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()


        service.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload(imageName_list[i])
        ).execute()

    if uploadDrive == 'y':
        print(f"{bcolors.OKGREEN}Uploading videos to Google Drive...{bcolors.ENDC}")

        asyncio.run(UploadFiles(['./videos/' + sound_name.split('/')[-1].split('.')[0] + '.mp4']))

        print(f"{bcolors.OKGREEN}Video uploaded to Google Drive!{bcolors.ENDC}")

    if move == 'y':
        print(f"{bcolors.OKGREEN}Moving files...{bcolors.ENDC}")
        os.replace(imageName_list[i], "./images/used/" + imageName_list[i].split('/')[-1])
        os.replace(sound_name, "./songs/used/" + sound_name.split('/')[-1])

    i = i + 1
