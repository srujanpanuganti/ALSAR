import requests
import shutil
import subprocess
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    print("Downloading file from google drive...")
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_legacy(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    print("Downloading file from google drive...")
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


## eye https://drive.google.com/open?id=1FC5V2JVTmymIeo6snY8Kjgzp3Z_GYq_o

if __name__ == "__main__":

    if(not os.path.isfile("resources/eye.mp4")):

        eye_id = "1FC5V2JVTmymIeo6snY8Kjgzp3Z_GYq_o"
        download_file_from_google_drive(eye_id, "eye.mp4")
        os.system('cp eye.mp4 resources/')
        os.system('rm eye.mp4')

    else:
        print("eye video already exists. Not downloading")
