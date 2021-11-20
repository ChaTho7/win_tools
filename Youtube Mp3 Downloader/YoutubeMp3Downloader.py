from pytube import YouTube
import os
import music_tag
import ffmpeg

file = open('links.txt', 'r')

for line in file:

    url = line

    try:
        yt = YouTube(url=url)

        audio = yt.streams.get_audio_only(subtype='mp4')

        audio.download(output_path='.', filename='temp.mp3')
        #base, ext = os.path.splitext(out_file)

        final_file = rf"{audio.title}" + ".mp3"
        invalid = '<>:"/\|?*'
        for char in invalid:
            final_file = final_file.replace(char, '')

        stream = ffmpeg.input('temp.mp3')
        stream = ffmpeg.output(stream, final_file,
                               acodec="libmp3lame", audio_bitrate=192000)
        ffmpeg.run(stream)
        os.remove("temp.mp3")

        yt.metadata.metadata.append(1)
        if(yt.metadata.metadata != [1]):
            tag_file = music_tag.load_file(final_file)
            if("Song" in yt.metadata.metadata[0]):
                tag_file['tracktitle'] = yt.metadata.metadata[0]["Song"]
            if("Artist" in yt.metadata.metadata[0]):
                tag_file['artist'] = yt.metadata.metadata[0]["Artist"]
            if("Album" in yt.metadata.metadata[0]):
                tag_file['album'] = yt.metadata.metadata[0]["Album"]
            tag_file.save()

        print(yt.title + " has been successfully downloaded.")
    except Exception as error:
        print(error)
        pass

file.close()
input("Press enter key to close downloader...")
