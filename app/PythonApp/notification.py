import os

def send_notification(title, message):
    os.system(f'cmd.exe /C "msg * {title}: {message}"')
    