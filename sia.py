import os
import time
import datetime
import ffmpeg
import logging
import requests
import yt_dlp as youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatAction
from pyrogram import *
import json
import re
from instaloader import Instaloader, Post, TwoFactorAuthRequiredException
import httpx
import config
from modules.time import time_to_seconds
from modules.ig.post import download_instagram_post
from modules.ig.reel import download_instagram_video
import os

if config.bot_token == "":
    bot_token = os.environ.get("BOT_TOKEN")
else:
    bot_token= config.bot_token
        
if config.api_id=="":
    api_id = int(os.environ.get("API_ID"))
else:
    api_id = int(config.api_id)
       
if config.api_hash=="":
    api_hash = os.environ.get("API_HASH")
else:
    api_hash = config.api_hash    
        
if config.username=="":
    username_ig = os.environ.get("INSTA_USERNAME")
else:
    username_ig = config.username    

if config.password=="":
    password_ig = os.environ.get("INSTA_PASSWORD")
else:
    password_ig = config.password 

ydl_opts = {"format": "bestaudio[ext=m4a]"}


loader = Instaloader(download_videos=True, download_geotags=False, download_comments=False, compress_json=False)

try:
    loader.load_session_from_file(f"{username}", filename=f"./{username_ig}")
    print( "Successfully loaded sessionfile to the Bot")
except:
    try:
        loader.login(username, password)
        loader.save_session_to_file(filename=f"./{username}")
        print( "Successfully Configured the Bot")
    except TwoFactorAuthRequiredException:
        print( "Disable Two Factor Authentication and try again")
    except Exception as e:
        print(e)
        print("Invalid Username or Password.\n\n__If you're facing Still this Issue Report @riz4d")

app = Client("siaahsession",api_id=api_id,api_hash=api_hash,bot_token=bot_token)


@app.on_message(filters.command('start'))
async def start_msg(client,message):
    name=str(message.from_user.first_name)
    try:
        await message.reply(f"__**Hey {name}👋🏻**\n\nI'm **Sia!!**, I'm Chatbot that has been developed by [Mohamed Rizad](https://t.me/riz4d) designed to assist with a wide range of tasks \n\n 👉🏻 Downloading songs\n👉🏻 Download Youtube Videos\n👉🏻 Downloading Instagram Media's")
    except:
        pass
      

@app.on_message(filters.command('help'))
async def start_msg(client,message):
    
      try:
        await message.reply("""Uhh❕

It's too easy to understand me😌 Anyway I'm Introduce myself and my Qualities one by one 🥹

Myself Siaah 🖤 I'm a chat bot Currently Lives in a Secret Server📟

**Qualities of mehh🫣**

If you wants to listen or download a song🎵 just type the song name after /play for example `/play baby doll`

If you wants to download YouTube video or an Instagram post or reels just send link it to meh i will be here to download it for uhh🥹

""",
                                 reply_markup=InlineKeyboardMarkup(
                                             [
                                                 [
                            InlineKeyboardButton('Queries & Suggestions', url='https://t.me/riz4d')
                                   ]       
                                             ]))
      except:
          pass

about_video=[]
@app.on_message(filters.command("play"))
async def a(client, message):
        querry=str(message.text)
        if querry == "/play":
            await message.reply("Uh!\nSend Song Name Along With Command Like \n**/play |Songname|**\n\n__Example__ : `/play In This Shirt`")
        elif querry=="/PLAY":
            await message.reply("Uh!\nSend Song Name Along With Command Like \n**/play <Songname>**\n\n__Example__ : `/play In This Shirt`")
        else:    
              query=querry.lower().replace("/play", "")
              print(query)
              user_id=str(message.from_user.id)
              await message.reply_chat_action(action=ChatAction.TYPING)
              m = await message.reply('Searching the song...')
              
              try:
                  results = []
                  count = 0
                  while len(results) == 0 and count < 6:
                      if count>0:
                          time.sleep(1)
                      results = YoutubeSearch(query, max_results=1).to_dict()
                      count += 1
                      try:
                        link = f"https://youtube.com{results[0]['url_suffix']}"
                        url_suff=results[0]['url_suffix']
                        title = results[0]["title"]
                        thumbnail = results[0]["thumbnails"][0]
                        duration = results[0]["duration"]
                        views = results[0]["views"]
                        channel_name=results[0]["channel"]
                        publish_time=results[0]["publish_time"]
                        abtvdo="**Title **: __{}__\n**views[‎ ]({}) **: __{}__\n**Duration **: __{}__\n**Channel **: __{}__\n**Published **: __{}__".format(title,thumbnail,views,duration,channel_name,publish_time)
                        about_video.append(abtvdo)
                        await m.edit(abtvdo,
                                     reply_markup=InlineKeyboardMarkup(
                                             [
                                                 [
                            InlineKeyboardButton('Low Quality', callback_data=url_suff+'rizaaah'),
                            InlineKeyboardButton('High  Quality', callback_data=url_suff+'rizaaah')
                                   ]       
                                             ]))
                      except Exception as e:
                        print(e)
                        await m.edit("__Sorry I Can't Find The Song \nTry Again With Correct Spell__")
                        return
              except Exception as e:
                  m.edit("❎ I don't know which song is this.\n\nEg.`/play kyun rabba`")
                  print(str(e))
                  return

def download_youtube_video(url, file_name, format):
    ydl_opts = {
        "format": format,
        "outtmpl": f"{file_name}.%(ext)s"
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{file_name}.mp4"
           
@app.on_message(filters.regex(r"(?i)https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|playlist\?list=|channel/|shorts/)|youtu\.be/)([^\s/?#&]+).*"))
async def handle_message(client, message):
           user_id=str(message.from_user.id)
        
           querry=str(message.text)
           if querry == "/yt":
               await message.reply("Uh!\nSend a Youtube Video Link To Downlod \n**/yt |Youtube Link|**\n\n__Example__ : `/yt https://www.youtube.com/watch?v=cdwal5Kw3Fc`")
           elif querry=="/YT":
               await message.reply("Uh!\nSend a Youtube Video Link To Downlod \n**/yt |Youtube Link|**\n\n__Example__ : `/yt https://www.youtube.com/watch?v=cdwal5Kw3Fc`")
           else:
            try:    
              url = str(message.text)
              ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
              info = ydl.extract_info(url, download=False)
              formats = info.get('formats', [])
              available_formats_fn = []
              available_formats = []
              for f in formats:
                  if f.get('format_note') == '720p':
                      available_formats.append(22)
                  elif f.get('format_note') == '360p':
                      available_formats.append(18)
                  elif f.get('format_note') == '1080p':
                      available_formats.append(137)
              keyboard = []
              for i in available_formats:
                  if i not in available_formats_fn:
                     available_formats_fn.append(i)
              for i in available_formats_fn:
                  x=i
                  if i==18:
                      i="360p Quality"
                  elif i==22:
                       i="720p Quality"
                  elif i==137:
                       i="1080p Quality"
                  button = InlineKeyboardButton(
                      text=i,
                      callback_data=f"youtubevdodl {url} {x}"
                  )
                  keyboard.append([button])
              reply_markup = InlineKeyboardMarkup(keyboard)
              results = YoutubeSearch(url, max_results=1).to_dict()
              try:
                  link = url
                  url_suff=results[0]['url_suffix']
                  title = results[0]["title"]
                  thumbnail = results[0]["thumbnails"][0]
                  duration = results[0]["duration"]
                  views = results[0]["views"]
                  channel_name=results[0]["channel"]
                  publish_time=results[0]["publish_time"]
                  abtvdo="**Title **: __{}__\n**views[‎ ]({}) **: __{}__\n**Duration **: __{}__\n**Channel **: __{}__\n**Published **: __{}__".format(title,thumbnail,views,duration,channel_name,publish_time)
                  
              except:pass
              s=await message.reply_text(
                  abtvdo,
                  reply_markup=reply_markup
              )
            except:pass



@app.on_message(filters.regex(r"(?i)^(https?\:\/\/)?(www\.instagram\.com)\/reel\/.+$"))
async def ig_reel_dl(client,message):
        user_id=str(message.from_user.id)
        try:
            name=str(message.from_user.first_name)
            reel_link=message.text
            try:
               await message.reply_chat_action(action=ChatAction.RECORD_VIDEO)
               m=await message.reply_text('__Downloading Video..__⏳')
               reel_location_dl=download_instagram_video(reel_link)
               await message.reply_chat_action(action=ChatAction.UPLOAD_VIDEO)
               await m.edit('__Uploading Video..__⏳')
               print(reel_location_dl)
               capyn=f"**Original Post : ** [Link 🗞]({reel_link})\n\n**Downloaded From : ** [Siaah🖤](https://github.com/riz4d/Siaah)"
               await m.delete()
               await message.reply_video(reel_location_dl,caption=capyn)
               os.remove(reel_location_dl)
            except Exception as e:
                print(e)
                await message.reply("__❗️ Invalid Instagram Reel Link__")
        except Exception as o:
            print(o)

@app.on_message(filters.regex(r"(?i)^(https?\:\/\/)?(www\.instagram\.com)\/p\/.+$"))
async def ig_post_dl(client,message):
    user_id=str(message.from_user.id)
    try:
        name=str(message.from_user.first_name)
        post_link=message.text
        try:
          await message.reply_chat_action(action=ChatAction.PLAYING)
          m = await message.reply_text('__Downloading Post..__⏳')
          post_location_dl=download_instagram_post(post_link)
          await message.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
          await m.edit('__Uploading Post..__⏳')
          print(post_location_dl)
          capyn=f"**Original Post : ** [Link 🗞]({post_link})\n**Downloaded From : ** [Siaah🖤](https://github.com/riz4d/Siaah)"
          await m.delete()
          await message.reply_photo(post_location_dl,caption=capyn)
          os.remove(post_location_dl)
        except:
            await message.reply("__❗️ Invalid Instagram Post Link__")
    except Exception as o:
        print(o)



@app.on_callback_query()
async def tablequery(client,message):
    response=message.data
    if 'rizaah' in response:
        response=response.replace('rizaah', '')
        await client.send_chat_action(chat_id=message.message.chat.id, action=ChatAction.RECORD_AUDIO)
        await message.edit_message_text('__Downloading Audio..__⏳')

        link = "https://youtube.com"+response
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
             info_dict = ydl.extract_info(link, download=False)
             audio_file = ydl.prepare_filename(info_dict).replace(".m4a", ".mp3")
             ydl.process_info(info_dict)
             await message.edit_message_text('__Uploading Audio..__⏳')
             print(audio_file)
             cap=about_video[0]
             await client.send_chat_action(chat_id=message.message.chat.id, action=ChatAction.UPLOAD_AUDIO)
             await client.send_audio(chat_id=message.message.chat.id, audio=audio_file,caption=cap)
             await message.edit_message_text('__Uploaded Successfully ✅__')
             about_video.clear()
             os.remove(audio_file)
    

    elif 'rizaaah' in response:
        response=response.replace('rizaaah', '')
        await client.send_chat_action(chat_id=message.message.chat.id, action=ChatAction.RECORD_AUDIO)
        await message.edit_message_text('__Downloading Audio..__⏳')

        link = "https://youtube.com"+response
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
             info_dict = ydl.extract_info(link, download=False)
             audio_file = ydl.prepare_filename(info_dict)
             ydl.process_info(info_dict)
             await message.edit_message_text('__Uploading Audio..__⏳')
             print(audio_file)
             cap=about_video[0]
             await client.send_chat_action(chat_id=message.message.chat.id, action=ChatAction.UPLOAD_AUDIO)
             await client.send_audio(chat_id=message.message.chat.id, audio=audio_file,caption=cap)
             await message.edit_message_text('__Uploaded Successfully ✅__')
             about_video.clear()
             os.remove(audio_file)                                
    elif "youtubevdodl " in response:
       callbackdatayt=str(message.data).replace("youtubevdodl ", "")
       url, format_id = callbackdatayt.split()
       print(url,format_id)
       
       try:
           results = YoutubeSearch(url, max_results=1).to_dict()
           link = url
           url_suff=results[0]['url_suffix']
           title = results[0]["title"]
           thumbnail = results[0]["thumbnails"][0]
           duration = results[0]["duration"]
           views = results[0]["views"]
           channel_name=results[0]["channel"]
           publish_time=results[0]["publish_time"]
           abtvdo="**Title **: __{}__\n**views[‎ ]({}) **: __{}__\n**Duration **: __{}__\n**Channel **: __{}__\n**Published **: __{}__".format(title,thumbnail,views,duration,channel_name,publish_time)
           
       except:pass
       await message.edit_message_text('__Downloading Video..__⏳')
       file_name=str(message.message.chat.id)+str(message.message.id)
       file_path = download_youtube_video(url, file_name, format_id)
       await message.edit_message_text('__Uploading Video..__⏳')
       await message.message.reply_video(
               file_path,
               caption=abtvdo
           )
       await message.edit_message_text('__Uploaded Successfully ✅__')
       os.remove(file_path)

app.run()
