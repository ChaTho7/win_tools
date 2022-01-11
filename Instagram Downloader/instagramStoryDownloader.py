import sys,os, shutil
from typing import Iterator
import instaloader
from instaloader.structures import Profile, Story

def download():
    instance = instaloader.Instaloader()
    instance.login(user="",passwd="")

    link = ""
    spiltted_link = link.split("/")
    profile_name = spiltted_link[4]
    story_id = spiltted_link[5]

    profile_id:Profile = instance.check_profile_id(profile_name)
    stories:Iterator[Story] = instance.get_stories([profile_id.userid])
    for story in stories:
        for item in story.get_items():
            if item.mediaid == int(story_id):
                instance.download_storyitem(item,"temp")

    desktop_location = os.path.expanduser("~/Desktop") + "/"
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
    shutil.rmtree(profile_name)

try:
    download()

except:
    if (str(sys.exc_info()[1]) == 'Login error: "fail" status, message "feedback_required".'):
        download()
    else:
        print(sys.exc_info()[1])