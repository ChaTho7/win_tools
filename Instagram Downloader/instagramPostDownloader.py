import sys, os, shutil
import instaloader
from instaloader.structures import Post

def download():
    instance = instaloader.Instaloader()
    instance.login(user="",passwd="")

    post_code = ""
    post = Post.from_shortcode(instance.context,post_code)

    desktop_location = os.path.expanduser("~/Desktop") + "/"
    instance.download_post(post,"temp")
    files = os.listdir("./temp")
    for file in files:
        base_name, extension = os.path.splitext(file)
        if extension == ".jpg" or extension == ".mp4":  
            is_exists = os.path.exists(desktop_location + "Insta Downloads")
            if is_exists:
                os.rename(os.path.abspath(os.getcwd()) + "\\temp\\" + file,desktop_location + "Insta Downloads/"+ file)
            else:
                os.makedirs(desktop_location + "Insta Downloads")
                os.rename(os.path.abspath(os.getcwd()) + "\\temp\\" + file,desktop_location + "Insta Downloads/"+ file)
    shutil.rmtree("temp")

try:
    download()

except:
    if (str(sys.exc_info()[1]) == 'Login error: "fail" status, message "feedback_required".'):
        download()
    else:
        print(sys.exc_info()[1])
    