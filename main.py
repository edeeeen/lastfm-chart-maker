import requests, json, os
from slugify import slugify
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#####CHANGE THIS TO YOUR OWN KEY#####
KEY = 'PUT KEY HERE'

##### You might wanna change this, this is just what I used. #####
headers = {
    'user-agent': "pyvin"
}

def getTop(name, limit, timeframe):
    payload = {
        'api_key': KEY,
        'method': 'user.getTopAlbums',
        'period': timeframe,
        'user': name,
        'limit': limit,
        'format': 'json'
    }
    return requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

timeframe = ""
size = ""
playcount = ""

name = input("Lastfm Username: ")
while timeframe == "": 
    x = input("[1] 7 Days  [2] 1 Month  [3] 3 Months  [4]  6 Months  [5] 1 Year  [6] Overall:  ")
    match x:
        case "1":
            timeframe = "7day"
        case "2":
            timeframe = "1month"
        case "3":
            timeframe = "3month"
        case "4":
            timeframe = "6month"
        case "5":
            timeframe = "12month"
        case "6":
            timeframe = "overall"
        case _:
            print("Not an option.  Try again.")
while playcount == "": 
    x = input("Display playcount? [Y/N]:  ").lower()
    match x:
        case "y":
            playcount = True
        case "n":
            playcount = False
        case _:
            print("Not an option.  Try again.")
while size == "":
    size = input("[1] 3x3  [2] 4x4  [3] 5x5  [4] 10x10:  ")

    match size:
        case "1":
            r = getTop(name, '9', timeframe)
            size = 3
        case "2":
            r = getTop(name, '16', timeframe)
            size = 4
        case "3":
            r = getTop(name, '25', timeframe)
            size = 5
        case "4":
            r = getTop(name, '100', timeframe)
            size = 10
        case _:
            size = ""
            print("Not an option.  Try again.")

font1 = ImageFont.truetype('files\\PixelCode.ttf', 30)

list_im = []
#returns the top however many albums
jsonReturn = json.loads(r.text)
#loop through the albums in the json
for x in jsonReturn["topalbums"]["album"]:
    image = x['image'][3]['#text']
    #check if there is an image attatched
    if (image != ""):
        #download img to files/
        r = requests.get(x['image'][3]['#text'], allow_redirects=True)
        #add to list_im
        list_im.append("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
        #if its a png turn it into a jpg if not just save it
        if(x['image'][3]['#text'][-4:] == ".png"):
            open("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.png', 'wb').write(r.content)
            im1 = Image.open('files\\' + slugify(x['artist']['name'] + "---" + x['name']) + '.png')
            im2 = im1.convert('RGB')
            im2.save("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
            im1.close()
            os.remove("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.png')
        else:
            open("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg', 'wb', ).write(r.content)
        img = Image.open("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
        #resize so the text doesnt look rly bad then add the text
        if(size == 10):
            interval = 20
            font1 = ImageFont.truetype('files\\PixelCode.ttf', 16)
            img = img.resize((450, 450))
        else:
            interval = 30
            img = img.resize((900, 900))
        I1 = ImageDraw.Draw(img)
        I1.text((5, 6), x['artist']['name'], fill=(0, 0, 0), font=font1)
        I1.text((5, 5), x['artist']['name'], fill=(255, 255, 255), font=font1)
        I1 = ImageDraw.Draw(img)
        I1.text((5, 6+interval), x['name'], fill=(0, 0, 0), font=font1)
        I1.text((5, 5+interval), x['name'], fill=(255, 255, 255), font=font1)
        if(playcount):
            I1.text((5, 6+interval*2), "Playcount:" + x['playcount'], fill=(0, 0, 0), font=font1)
            I1.text((5, 5+interval*2), "Playcount:" + x['playcount'], fill=(255, 255, 255), font=font1)
        img.save("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
    #if image isnt attatched use emtpy.jpg and add text to it
    else:
        img = Image.open("files\\empty.jpg")
        if(size == 10):
            interval = 20
            font1 = ImageFont.truetype('files\\PixelCode.ttf', 16)
            img = img.resize((450, 450))
        else:
            interval = 30
            img = img.resize((900, 900))
        I1 = ImageDraw.Draw(img)
        I1.text((5, 6), x['artist']['name'], fill=(0, 0, 0), font=font1)
        I1.text((5, 5), x['artist']['name'], fill=(255, 255, 255), font=font1)
        I1 = ImageDraw.Draw(img)
        I1.text((5, 6+interval), x['name'], fill=(0, 0, 0), font=font1)
        I1.text((5, 5+interval), x['name'], fill=(255, 255, 255), font=font1)
        if(playcount):
            I1.text((5, 6+interval*2), "Playcount:" + x['playcount'], fill=(0, 0, 0), font=font1)
            I1.text((5, 5+interval*2), "Playcount:" + x['playcount'], fill=(255, 255, 255), font=font1)
        img.save("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
        list_im.append("files\\" + slugify(x['artist']['name'] + "---" + x['name']) + '.jpg')
    #print what image is being downloaded
    print(x['name'])
#create a list for image types
imgs = [Image.open(i) for i in list_im]
temp = []
tempNames = []
z = 0
for w in range(size):
    #concat $size them all together horizontally.  Create $size of these
    imgs_comb = np.hstack([i for i in imgs[z:z+size]])
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save(str(w) + '.jpg')
    z=z+size
    temp.append(Image.open(str(w) + '.jpg'))
    tempNames.append(str(w) + '.jpg')
#close files
for cover in range(len(imgs)):
    imgs[cover] = None
#delete files
for cover in list_im:
    try:
        os.remove(cover)
    except:
        #if there is a filename that gets repeaded because of lastfm double catagorizing something then this occours.  
        print("Dupe error - ignore.  Files might not get cleaned up properly.")
#take the $size rows and stack them into one img
imgs_comb = np.vstack([i for i in temp])
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( 'Collage.jpg' )
#delete all the rows
for files in range(len(temp)):
    temp[files] = None
for files in tempNames:
    os.remove(files)
