import requests, os


def download(thumbnail_url):
    if thumbnail_url:
        # thumbnail_filename_with_extension = os.path.basename(
        #     thumbnail_url)  # Extract filename from URL
        # thumbnail_filename, thumbnail_extension = os.path.splitext(
        #     thumbnail_filename_with_extension)  # Extract extension from filename

        thumbnail_response = requests.get(thumbnail_url)
        if thumbnail_response.status_code == 200:
            # with open(thumbnail_filename + thumbnail_extension, 'wb') as f:
            #     f.write(thumbnail_response.content)
            return thumbnail_response.content
        else:
            raise Exception("Failed to download thumbnail.")
    else:
        raise Exception("No thumbnail found.")
