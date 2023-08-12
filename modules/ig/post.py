import re
import os
from instaloader import Instaloader, Post
loader = Instaloader(download_videos=True, download_geotags=False, download_comments=False, compress_json=False)


def download_instagram_post(url):
    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/(?:p|reel)\/([^\/?]+)", url)
    if not match:
        print("Invalid Instagram URL")
    shortcode = match.group(1)
    post = Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target="ig_images")
    media_file = None
    for file in os.listdir("ig_images"):
        print(file)
        if file.endswith(".jpg"):
            media_file = "ig_images/"+file
            break
    return media_file

