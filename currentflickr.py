#!/usr/bin/python

from flickrapi import FlickrAPI, shorturl
from applescript import asrun
import re

def currentFlickrID():
  '''Return the ID for the Flickr image currently showing in the browser.

  The function works through Apple Events and supports only the Safari
  browser. It will generate an IndexError if the frontmost tab of the
  browser isn't showing a Flickr image.'''

  # The regex for extracting user and photo info.
  infoRE = r'flickr\.com/photos/(.*)/(\d+)/?'

  # Get the URL of the current page in either Safari.
  thisURL = asrun('tell application "Safari" to get the URL of the front document')

  # Extract the user and photo info from the URL.
  info = re.findall(infoRE, thisURL)
  return info[0][1]

def currentFlickrTitle():
  '''Return the title of the Flickr image currently showing in the browser.

  The function works through Apple Events and supports only the Safari
  browser.'''

  # Flickr parameters
  fuser = 'Flickr username'
  key = 'Get key from Flickr'
  secret = 'Get secret from Flickr'

  # Get the image ID.
  try:
    imageID = currentFlickrID()
  except IndexError:
    return "Not a Flickr image"

  # Establish the connection with Flickr.
  flickr = FlickrAPI(api_key=key, secret=secret)

  # Get the title.
  etree = flickr.photos_getInfo(photo_id = imageID, format = 'etree')
  for i in etree[0]:
   if i.tag == 'title':
     return i.text
     break

  # If the size wasn't found.
  return "Title not found"


def currentFlickrURL(kind, linkformat = ""):
  '''Return a URL for the Flickr image currently showing in the browser.

  The string parameter "kind" can be either "Short" or one of the
  standard Flickr image sizes: "Original", "Large", "Medium 800",
  "Medium 640", "Medium", "Small 320", "Small", "Thumbnail", "Large
  Square", or "Square". If it's Short, the function will return a
  flic.kr URL for the image page. If it's one of the others, the
  function will return the URL of the image of that size, if
  available.
  
  The "linkformat" parameter can be omitted, or can be supplied as
  either "md" or "html" as long as "kind" is not "Short".
  Pass "md" to create a Markdown image reference where the image is linked
  back to its Flickr page, or provide "html" to create an HTML
  img tag surrounded by an a tag linking to the image's Flickr page.

  The function works through Apple Events and supports only the Safari
  browser.'''


  # Flickr parameters
  fuser = 'Flickr username'
  key = 'Get key from Flickr'
  secret = 'Get secret from Flickr'

  # Make sure we're asking for a legitimate kind.
  kind = ' '.join([x.capitalize() for x in kind.split()])
  kinds = ["Short", "Original", "Large", "Medium 800", "Medium 640",
           "Medium", "Small 320", "Small",  "Thumbnail",
           "Large Square", "Square"]
  if kind not in kinds:
    return "Not a legitimate kind of URL"

  # Get the image ID.
  try:
    imageID = currentFlickrID()
  except IndexError:
    return "Not a Flickr image"

  # Establish the connection with Flickr.
  flickr = FlickrAPI(api_key=key, secret=secret)

  # Get the URL.
  if kind == "Short":
    return shorturl.url(photo_id = imageID)
  else:
    etree = flickr.photos_getSizes(photo_id = imageID, format = 'etree')
    if linkformat == '':
      for i in etree[0]:
        if i.attrib['label'] == kind:
          return i.attrib['source']
          break

      # If the size wasn't found.
      return "Size not found"

    elif linkformat == 'md':
      einfo = flickr.photos_getInfo(photo_id = imageID, format = 'etree')
      photourl = einfo.find('photo/urls/url').text
      phototitle = einfo.find('photo/title').text
      if not phototitle:
        phototitle = "Untitled"
      for i in etree[0]:
        if i.attrib['label'] == kind:
          jpgurl = i.attrib['source']
          return "[![" + phototitle + "](" + jpgurl + ")](" + photourl + ")"
          break
      # If the size wasn't found.
      return "Size not found"

    elif linkformat == 'html':
      einfo = flickr.photos_getInfo(photo_id = imageID, format = 'etree')
      photourl = einfo.find('photo/urls/url').text
      phototitle = einfo.find('photo/title').text
      if not phototitle:
        phototitle = "Untitled"
      for i in etree[0]:
        if i.attrib['label'] == kind:
          jpgurl = i.attrib['source']
          photowidth = i.attrib['width']
          photoheight = i.attrib['height']          
          return "<a href='" + photourl + "' title='" + phototitle + "'><img src='" + jpgurl + "' width='" + photowidth + "' height='" + photoheight + "'></a>"
          break
      # If the size wasn't found.
      return "Size not found"
     
    else:
      return "Invalid link format requested"


if __name__ == '__main__':
  print currentFlickrURL('Short')
