import fileinput
import os
from task.cloud_fun import make_bucket, get_albums, get_files, delete_album, delete_photo_in_album, download_album, upload_album, make_site_album

# Define the file path
file_path = f"~{os.sep}.config{os.sep}cloudphoto{os.sep}cloudphotorc"

def init(bucket_name, aws_access_key, aws_secret_access_key):
    with fileinput.FileInput( os.path.expanduser(file_path), inplace=True) as file:
        for line in file:
            line = line.replace("INPUT_BUCKET_NAME", bucket_name)
            line = line.replace("INPUT_AWS_ACCESS_KEY_ID", aws_access_key)
            line = line.replace("INPUT_AWS_SECRET_ACCESS_KEY", aws_secret_access_key)
            print(line, end='')
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()        
    make_bucket(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region)        

def list(album): 
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()

    if album is None: 
        get_albums(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region)
    else:
        get_files(bucket, aws_access_key_id, aws_secret_access_key, album, endpoint_url, region)    

def delete(album, photo):
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()
    if photo is None: 
        delete_album(bucket, aws_access_key_id, aws_secret_access_key, album, endpoint_url, region)
    else:
        delete_photo_in_album(bucket, aws_access_key_id, aws_secret_access_key, album, photo, endpoint_url, region)

def download(album, path):
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()
    download_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region)

def upload(album, path):
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()
    upload_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region)         

def make_site():
    bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region = get_params()
    make_site_album(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region)

def get_params():
    config = {}
    with open(os.path.expanduser(file_path), 'r') as file:
        for line in file:
            name, value = line.strip().split(' = ', 1)
            config[name] = value

    bucket = config['bucket']
    aws_access_key_id = config['aws_access_key_id']
    aws_secret_access_key = config['aws_secret_access_key']
    endpoint_url = config['endpoint_url']
    region = config['region']
    if (bucket == "INPUT_BUCKET_NAME" or aws_access_key_id == "INPUT_AWS_ACCESS_KEY_ID" or aws_secret_access_key== "INPUT_AWS_SECRET_ACCESS_KEY "):
        raise Exception("Config file is not valid")
    return bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region