# Flickr stuff #

A set of scripts and libraries for working with Flickr on a Macintosh. They all require [Sybren Stüvel’s FlickrAPI library][2].

This is based on [Dr. Drang's original version](https://github.com/drdrang/flickr-stuff), this adds the ability to get Markdown or HTML linked images via the `currentFlickrURL()` function, and adds a few more TextExpander snippets that use this ability.

## getFlickrToken ##



getFlickrToken authorizes any program you've registered with Flickr (http://www.flickr.com/services/apps/create/) and puts its "token" in your `~/.flickr` directory. It's a command line program that your run with three arguments:

    1. The program's api key, which you get from Flickr.
    2. The program's api secret, which you get from Flickr.
    3. The program's permissions (read, write, or delete), which you determine.


## snapflickr ##

snapflickr takes a snapshot of your screen (similar to the builtin ⇧⌘4), saves a copy to your ~/Pictures/Screenshots folder (which you must create first), and uploads a copy to your Flickr account.

When snapflickr is run, it turns the cursor into a camera, ready to take a snapshot of any window (you can change it to take a snapshot of an arbitrary rectangle by pressing the spacebar). After the snapshot is taken, a window appears in which you provide a file name and (optionally) a description.

![snapflickr dialog box](https://farm3.staticflickr.com/2936/14551651529_ed08dd5631_o.png)

By default, the snapshot is uploaded to your Flickr account, but if you click the "Local file only" checkbox, there's no upload. If the image is uploaded to Flickr, its page is opened in the default browser and an `<img>` tag for the chosen size is put on the clipboard.

It requires [Carsten Blüm's Pashua application][1] and its accompanying Python library. The use is described in more detail [here][3]. It also requires the [Python Imaging Library][5] to add border around window screenshots. The border is set to 16 pixels and the standard Solid Aqua Dark Blue color from the Desktop system preference. These can be changed in the local parameters section at the top of the file.

Also near the top of snapflickr is a section of Flickr parameters:

    # Flickr parameters
    fuser = 'your Flickr username'
    key = 'get your key from Flickr'
    secret = 'get your secret from Flickr'
    screenshotsID = 'the ID of the Flickr set'

These must be customized with the appropriate username, API info, and Flickr set ID.

## currentflickr.py ##

This is a Python library for getting the name or certain types of URL for the Flickr image currently showing in your browser (works only for Safari). In addition to the FlickrAPI library, it also requires the `applescript.py` file to be somewhere that your Python installation can locate it. `applescript.py` uses OSAScript to run AppleScripts within Python.

The currentFlickrURL function can return the URLs for various sizes of an image, or return an image's short Flickr URL (http://flic.kr/p/xxxxx). Additionally, if `'md'` is supplied as the optional second parameter, the function returns a Markdown image reference within a link to the image's Flickr page, or if `'html'` is sent as the second parameter, it returns an HTML `\<img\>` tag surrounded by an `\<a\>` tag linking to the image's Flickr page.
Eg. `currentFlickrURL('Medium','md')` returns something like:

	[![Image Title](https://farmn.staticflickr.com/xxxxx.jpg)](https://www.flickr.com/photos/user/nnnnn/)

and  `currentFlickrURL('Medium 800','html')` returns something like: 

	<a href='https://www.flickr.com/photos/user/nnnnn/' title='Image Title'><img src='https://farmn.staticflickr.com/xxxxx.jpg' width='800' height='600'></a>`

A couple of locations within `currentflickr.py` have sections of Flickr parameters:

    # Flickr parameters
    fuser = 'Flickr username'
    key = 'Get key from Flickr'
    secret = 'Get secret from Flickr'

These must be customized with the appropriate username and API info and you should run the `getFlickrToken` script so that Python running on your system has the correct permissions to access your Flickr library.

In order to use this in the TextExpander snippets described below, both `currentflickr.py` and `applescript.py` must be located somewhere that your Python installation can find it. I don't know much about Python, but putting the files into the `/Library/Python/2.7/site-packages` directory does the trick.

## Flickr.textexpander ##

This is a plist of TextExpander shell snippets for getting various Flickr URLs of the image shown in the frontmost tab of the browser. The snippets use the currentflickr.py library, so it must be customized with the user's name and API credentials and installed where Python can find it. 

## download-flickr-image ##

A script that downloads the large version of the Flickr image currently showing in the browser window and saves it to the Desktop. The filename is the Flickr image title, with ".jpg" appended if necessary. This is intended to be called via FastScripts or a similar utility. It dings using the Glass sound if it succeeds and burps with the Basso sound if it fails.

To play the sounds, the script requires the free [Play Sound utility][4] from Microcosm Software.

## up2flickr ##

A script that uploads a list of images to Flickr. The title on Flickr is the file name minus the extension. The images are private by default but can be made public through a command line option.

Near the top of up2flickr is a section of Flickr parameters:

    # Flickr parameters
    fuser = 'Flickr username'
    key = 'Get key from Flickr'
    secret = 'Get secret from Flickr'

These must be customized with the appropriate username and API info.



[1]: http://www.bluem.net/en/mac/pashua/
[2]: http://stuvel.eu/flickrapi
[3]: http://www.leancrew.com/all-this/2012/02/snapflickr-update/
[4]: http://microcosmsoftware.com/playsound/
[5]: http://www.pythonware.com/products/pil/
