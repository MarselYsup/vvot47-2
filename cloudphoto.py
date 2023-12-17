import argparse
import sys
import os
from task.functions import init, list, delete, download, upload, make_site
parser = argparse.ArgumentParser(prog='cloudphoto')

command_parser = parser.add_subparsers(title='command', dest='command')

command_init = command_parser.add_parser('init', help='create a settings file and create a package')

command_list = command_parser.add_parser('list', help='list photo albums')
command_list.add_argument('--album', metavar='ALBUM', type=str, help='Album name')

command_download = command_parser.add_parser('download', help="download photos")
command_download.add_argument('--album', metavar='ALBUM', type=str, help='Photo album name', required=True)
command_download.add_argument('--path', metavar='PHOTOS_DIR', type=str, default='.', help='Path to photos', required=False)


command_upload = command_parser.add_parser('upload', help='upload photos')
command_upload.add_argument('--album', metavar='ALBUM', type=str, help='Album name', required=True)
command_upload.add_argument('--path', metavar='PHOTOS_DIR', type=str, default='.', help='Path to photos', required=False)

command_delete = command_parser.add_parser('delete', help='delete album')
command_delete.add_argument('--album', metavar='ALBUM', type=str, help='Album name')
command_delete.add_argument('--photo', metavar='PHOTO', type=str, help='Photo name')

command_mksite = command_parser.add_parser('mksite', help='start website')

args = parser.parse_args()

try:
    if args.command == 'init':
        aws_access_key_id = input('aws_access_key_id is ')
        aws_secret_access_key = input('aws_secret_access_key is ')
        bucket_name = input('bucket_name is ')
        init(bucket_name, aws_access_key_id, aws_secret_access_key)
        print("init done\nExit with status 0")
        sys.exit(os.EX_OK)
    elif args.command == 'list':
        list(args.album)
        print("list done\nExit with status 0")
        sys.exit(os.EX_OK)
    elif args.command == 'upload':
        upload(args.album, args.path)
        print("upload done\nExit with status 0")
        sys.exit(os.EX_OK)
    elif args.command == 'delete':
        delete(args.album, args.photo)
        print("delete done\nExit with status 0")
        sys.exit(os.EX_OK)
    elif args.command == 'download':
        download(args.album, args.path)
        print("dowload done\nExit with status 0")
        sys.exit(os.EX_OK)
    elif args.command == 'mksite':
        make_site()
        print("mksite done\nExit with status 0")
        sys.exit(os.EX_OK)
except Exception as err:
    print(f"Error: {err}\nExit with status 1")
    sys.exit(1)        