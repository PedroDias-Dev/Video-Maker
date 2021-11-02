import asyncio

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)  

async def UploadFiles(files):
    for upload_file in files:
        gfile = drive.CreateFile({'parents': [{'id': '1ibspuE9mwlHqmxloLHLE5sfzRZB8zOz6'}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(upload_file)
        await gfile.Upload() # Upload the file.
        print(upload_file)
