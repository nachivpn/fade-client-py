from ftpclient import download, upload
import ftplib
import sys

ftp = ftplib.FTP("fade-ftp-server")  # host
ftp.login()  # anonimous
# ftp.login("fade", "fade") # user, password

ftp.set_pasv("false")

# Dir listing
print(ftp.pwd())
data = []
ftp.dir(data.append)
for line in data:
    print("-", line)

ftp.cwd('test')  # change directory to /test/
print(ftp.pwd())
data = []
ftp.dir(data.append)
for line in data:
    print("-", line)

# Download file
download(ftp, 'a.txt')

# Uploading files
upload(ftp,
       "x.txt")  # FIXME check this tomorrow https://stackoverflow.com/questions/24586016/ftplib-error-perm-550-not-enough-privileges-while-storing-files-as-anonymous-us

ftp.quit()
