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


## goturn https://drive.google.com/a/terpmail.umd.edu/file/d/1OTovzFfKXolHZ1M7zwbFBTILNBXfRfSG/view?usp=sharing
## test   https://drive.google.com/a/terpmail.umd.edu/file/d/1DT6HXD5M20Y_RdWO5LgGdRTmwUCrBg1s/view?usp=sharing
## train  https://drive.google.com/a/terpmail.umd.edu/file/d/1uZ3PUYiFHNoAfAymfl1RtgyZLqsZQeMu/view?usp=sharing
## queue  https://drive.google.com/a/terpmail.umd.edu/file/d/1RBy1BE87ksvKhihiFOTscuU5Hjcc1zWe/view?usp=sharing

if __name__ == "__main__":

    if(not os.path.isdir("user1")):
        os.system('mkdir user1')

    if(not os.path.isdir("user2")):
        os.system('mkdir user2')

    if(not os.path.isdir("user3")):
        os.system('mkdir user3')

    if(not os.path.isdir("saved_models")):
        os.system('mkdir saved_models')

    if(not os.path.isdir("Training")):
        train_id = "1uZ3PUYiFHNoAfAymfl1RtgyZLqsZQeMu"
        download_file_from_google_drive(train_id, "Training.tar.gz")
        subprocess.call(["tar", "-zxvf", "Training.tar.gz", "-C", "./"])
        subprocess.call(["rm", "Training.tar.gz"])
        os.system('cp -r Training/ user1/')
        os.system('cp -r Training/ user2/')
        os.system('cp -r Training/ user3/')

    else:
        print("Training folder already exists. Not downloading")

    if(not os.path.isdir("Testing")):
        test_id = "1DT6HXD5M20Y_RdWO5LgGdRTmwUCrBg1s"
        download_file_from_google_drive(test_id, "Testing.tar.gz")
        subprocess.call(["tar", "-zxvf", "Testing.tar.gz", "-C", "./"])
        subprocess.call(["rm", "Testing.tar.gz"])

    else:
        print("Testing folder already exists. Not downloading")

    if(not os.path.isfile("goturn.caffemodel")) or (not os.path.isfile("goturn.prototxt")):
        goturn_id = "1OTovzFfKXolHZ1M7zwbFBTILNBXfRfSG"
        download_file_from_google_drive(goturn_id, "goturn.tar.gz")
        subprocess.call(["tar", "-zxvf", "goturn.tar.gz", "-C", "./"])
        subprocess.call(["rm", "goturn.tar.gz"])
    else:
        print("goturn models already exist. Not downloading")

    if(not os.path.isfile("queue")):
        queue_id = "1RBy1BE87ksvKhihiFOTscuU5Hjcc1zWe"
        download_file_from_google_drive(queue_id, "queue.tar.gz")
        subprocess.call(["tar", "-zxvf", "queue.tar.gz", "-C", "./"])
        subprocess.call(["rm", "queue.tar.gz"])
    else:
        print("queue already exists. Not downloading")


