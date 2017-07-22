from ftpclient import download, upload
import ftplib
import sys


ftp = ftplib.FTP("fade-ftp-service") #host
ftp.login() # anonimous
#ftp.login("fade", "fade") # user, password
ftp.cwd('pub/fade-bucket') # change working directory


 # Dir listing
print (ftp.pwd())
data = []
ftp.dir(data.append)
for line in data:
    print ("-", line)


# Download file
download(ftp,'DOWNLOADME')


# Uploading files
upload(ftp, "UPLOADME")


ftp.quit()
