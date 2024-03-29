# refs https://pythonspot.com/en/ftp-client-in-python/
import ftplib
import sys
import os
import ftplib


def setup():
    ftp = ftplib.FTP("fade-ftp-service")
    ftp.login()  # anonimous
    ftp.set_pasv("false")

    return ftp


def download(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
    except:
        print("Error downloading" + filename)


def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
