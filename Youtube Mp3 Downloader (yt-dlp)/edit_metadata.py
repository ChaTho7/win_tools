import eyed3, sys

def edit(musif_file, title, artist):
    title_is_not_none = title is not None
    artist_is_not_none = artist is not None

    if title_is_not_none or artist_is_not_none:
        try:
            audiofile = eyed3.load(musif_file)
            if title_is_not_none:
                audiofile.tag.title = title

            if artist_is_not_none:
                audiofile.tag.artist = artist

            audiofile.tag.save()

            return "Metadata has been saved."
        except:
            error = sys.exc_info()[1]

            return str(error)
    else:
        return None
