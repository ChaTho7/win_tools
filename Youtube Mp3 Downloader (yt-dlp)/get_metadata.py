# from difflib import SequenceMatcher
import requests, jellyfish


def similar(a, b):
    # return SequenceMatcher(None, a, b).ratio()
    return jellyfish.jaro_similarity(a, b)


def get_artist_from_track(track, track_name_with_artist):
    similarity = similar(track_name_with_artist, track["artist"])
    return {"track_name": track["name"], "artist_name": track["artist"], "similarity_ratio": similarity}


def get_metadata_from_api(track_name_with_artist):
    best_similar_value = 0
    best_similar_artist = ""
    best_similar_title = ""

    url = "https://ws.audioscrobbler.com/2.0/"
    query_params = {
        "api_key": "API_KEY",
        "track": track_name_with_artist,
        "format": "json",
        "method": "track.search"
    }
    headers = {"User-Agent": "insomnia/2023.5.8"}

    response = requests.get(url, params=query_params, headers=headers)

    if (response.status_code == 200):
        try:
            matched_tracks = list(
                response.json()["results"]["trackmatches"]["track"])
            if len(matched_tracks) < 1:
                raise
            artists = list(map(get_artist_from_track,
                           matched_tracks, track_name_with_artist))

            for artist in artists:
                if (artist["similarity_ratio"] > best_similar_value):
                    best_similar_value = artist["similarity_ratio"]
                    best_similar_artist = artist["artist_name"]
                    best_similar_title = artist["track_name"]

        except:
            raise Exception("No matched track found.")
    else:
        raise Exception(response.text)

    return {"similarity_value": best_similar_value, "title": best_similar_title, "artist": best_similar_artist}
