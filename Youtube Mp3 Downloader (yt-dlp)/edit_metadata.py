import eyed3, sys, thumbnail


def edit(musif_file, title, artist, thumbnail_url):
    title_is_not_none = title is not None
    artist_is_not_none = artist is not None
    thumbnail_url_is_not_none = thumbnail_url is not None

    if title_is_not_none or artist_is_not_none or thumbnail_url_is_not_none:
        try:
            audiofile = eyed3.load(musif_file)
            if title_is_not_none:
                audiofile.tag.title = title
            if artist_is_not_none:
                audiofile.tag.artist = artist
            if thumbnail_url_is_not_none:
                thumbnail_content = thumbnail.download(thumbnail_url)
                audiofile.tag.images.set(
                    0, thumbnail_content, "image/jpeg", u"Thumbnail")

            audiofile.tag.save()

            return "Metadata has been saved."
        except:
            error = sys.exc_info()[1]

            return str(error)
    else:
        return None
