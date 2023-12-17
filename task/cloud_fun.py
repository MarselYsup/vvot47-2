#!pip install boto3
#!pip install jinja2
import boto3
from botocore.client import ClientError
from os import path
import os
import random
import shutil
import string
import pathlib
import jinja2
from pathlib import Path
from jinja2 import Template

ROOT_DIRECTORY = path.dirname(pathlib.Path(__file__).parent)

SITE_CONFIGURATION = {
    "ErrorDocument": {"Key": "error.html"},
    "IndexDocument": {"Suffix": "index.html"},
}

IMG_EXTENSIONS = [".jpg", ".jpeg"]
ACL = 'public-read'


def make_bucket(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    
    try:
        # Проверка существует ли bucket
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exists.")
    except ClientError as e:   
        s3.create_bucket(Bucket=bucket_name, ACL = ACL)

def get_albums(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url= endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    try:
        s3.list_objects(Bucket=bucket_name)['Contents']
    except:
        raise Exception("Bucket is empty")    
    unique_albums = []
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        if key['Key'].endswith("/") and key['Key'].split("/")[0] not in unique_albums:
            unique_albums.append(key['Key'].split("/")[0])
    for value in unique_albums:
        print(value)               

def get_files(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url= endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    my_bucket = s3.Bucket(bucket_name)
    count_objects = 0
    count_files = 0
    
    for my_bucket_object in my_bucket.objects.filter(Prefix=f'{album}/', Delimiter='/'):
        count_objects = count_objects + 1
        if  my_bucket_object.key.endswith(".jpg") or my_bucket_object.key.endswith(".jpeg"):
            print(my_bucket_object.key.split(f'{album}/')[1]) 
            count_files = count_files + 1

    if count_objects == 0: 
        raise Exception(f"{album} does not exist")  
    if count_files == 0:
       raise Exception(f"{album} does not have files")        

def delete_album(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    ) 
    my_bucket = s3.Bucket(bucket_name)
    try:
        obj = s3.Object(bucket_name, f'{album}/').get()
        for my_bucket_object in my_bucket.objects.filter(Prefix=f'{album}/'):
            s3.Object(bucket_name, my_bucket_object.key).delete()
    except:
        raise Exception(f"Album '{album}' does not exist")


def delete_photo_in_album(bucket_name, aws_access_key, aws_secret_access_key, album, photo, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url= endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    ) 
    my_bucket = s3.Bucket(bucket_name)
    try:
        obj = s3.Object(bucket_name, f'{album}/').get()
    except: 
        raise Exception(f"Album '{album}' does not exist")
    try:
        path = f'{album}/{photo}'
        obj = s3.Object(bucket_name, path).get()
        s3.Object(bucket_name, path).delete()
    except: 
        raise Exception(f"Photo '{photo}' does not exist")

def download_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    path = Path(path)
    if not is_album_exist(s3, bucket, album):
        raise Exception(f"Album {album} does not exist")

    if not path.is_dir():
        raise Exception(f"{str(path)} is not directory")

    list_object = s3.list_objects(Bucket=bucket, Prefix=album + '/', Delimiter='/')
    for key in list_object["Contents"]:
        if not key["Key"].endswith("/"):
            obj = s3.get_object(Bucket=bucket, Key=key["Key"])
            filename = Path(key['Key']).name

            filepath = path / filename
            with filepath.open("wb") as file:
                file.write(obj["Body"].read())

def upload_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    path = Path(path)
    check_album(album)
    count = 0

    if not path.is_dir():
        raise Exception(f"{str(path)} album does not exist")

    if not is_album_exist(s3, bucket, album):
        s3.put_object(Bucket=bucket, Key=(album+'/'))
        print(f"{album} album creating...")

    for file in path.iterdir():
        if is_image(file):
            try:
                print(f"{file.name} photo uploading...")
                key = f"{album}/{file.name}"
                s3.upload_file(str(file), bucket, key)
                count += 1
            except Exception as ex:
                raise Exception(f"{str(path)} got error with uploading")


def is_image(file):
    return file.is_file() and file.suffix in IMG_EXTENSIONS


def get_albums_data(session, bucket: str):
    albums = {}
    list_objects = session.list_objects(Bucket=bucket)
    for key in list_objects["Contents"]:
        album_img = key["Key"].split("/")
        if len(album_img) != 2:
            continue
        album, img = album_img
        if img == '':
            continue
        if album in albums:
            albums[album].append(img)
        else:
            albums[album] = [img]

    return albums


def get_template(name):
    template_path = Path(ROOT_DIRECTORY) / "resources" / name
    with open(template_path, "r") as file:
        return file.read()


def save_temporary_template(template) -> str:
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".html"
    path = Path(ROOT_DIRECTORY) / "temp" / filename
    if not path.parent.exists():
        os.mkdir(path.parent)

    with open(path, "w") as file:
        file.write(template)

    return str(path)


def remove_temporary_dir():
    path = Path(ROOT_DIRECTORY) / "temp"
    shutil.rmtree(path)


def make_site_album(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name = region
    )  
    url = f"https://{bucket}.website.yandexcloud.net"
    albums = get_albums_data(s3, bucket)

    template = get_template("album.html")

    albums_rendered = []
    i = 1
    for album, photos in albums.items():
        print(photos)    
        template_name = f"album{i}.html"
        rendered_album = Template(template).render(album=album, images=photos, url=url)
        path = save_temporary_template(rendered_album)

        s3.upload_file(path, bucket, template_name)
        albums_rendered.append({"name": template_name, "album": album})
        i += 1

    template = get_template("index.html")
    rendered_index = Template(template).render(template_objects=albums_rendered)
    path = save_temporary_template(rendered_index)
    s3.upload_file(path, bucket, "index.html")

    template = get_template("error.html")
    path = save_temporary_template(template)
    s3.upload_file(path, bucket, "error.html")

    s3.put_bucket_website(Bucket=bucket, WebsiteConfiguration=SITE_CONFIGURATION)
    remove_temporary_dir()
    print(url)


def is_album_exist(session, bucket, album):
    list_objects = session.list_objects(
        Bucket=bucket,
        Prefix=album + '/',
        Delimiter='/',
    )
    if "Contents" in list_objects:
        for _ in list_objects["Contents"]:
            return True
    return False

def check_album(album: str):
    if album.count("/"):
        raise Exception("album cannot contain '/'")