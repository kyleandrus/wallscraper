'''
Created on Aug 1, 2012

@author: kandrus
'''

import os 
import re 
import sys 
import urllib 
import urllib2
import cookielib



#    Create cookie file, bind variables to openeners and requesters
#    This simplifies the typing and makes it easier to make the script
#    cross platform
COOKIEFILE = 'cookies.lwp'
urlopen = urllib2.urlopen
Request = urllib2.Request
cj = cookielib.LWPCookieJar()
cj.save(COOKIEFILE)


#    Installing the CookieJar - This will make the urlopener bound to the CookieJar.
#    This way, any urls that are opened will handle cookies appropratiely
if cj is not None:
    if os.path.isfile(COOKIEFILE):
    #If there is already a cookoie file, load from it
        cj.load(COOKIEFILE)
        
    if cookielib is not None:
    #This installs the cookie Jar into the opener for fetching URLs
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        
        
#Values used to login and create requests for urls etc...

#login_vals = {'usrname': username, 'pass': password, 'nopass_email': 'TypeInYourEmailAndPressEnter', 'nopass': '0', '1': '1'}
#login_url = 'http://wallbase.cc/user/login'
#login_data = urllib.urlencode(login_vals)




#method for opening the wallbase url and parsing the html code
#need to add arguments and search options. Will do later
def Wallbase_Search(url):
    """
    This Method open the wallbase main search page, scrape them from the host server
    and downloads them to the directory of your choice '''
    """
    login_vals = {'usrname': 'andrusk', 'pass': 'p0w3rus3r', 'nopass_email': 'TypeInYourEmailAndPressEnter', 'nopass': '0', '1': '1'}
    login_data = urllib.urlencode(login_vals)
    http_headers =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'referer': 'wallbase.cc http://wallbase.cc/user/adult_confirm/1'} 
    search_headers = {}
    
#    Lists that will contain all of the urls found in the main search page 
#    as well as the associated filename of the source image
    img_src_name = []
    img_src_url = []
    
#   Instantiate an object to hold the html text from the webpage
#    search_url = urllib.urlopen(url)
    req = Request(url, login_data, http_headers)
    search_url = urlopen(req)

    
#    Populate an object with the source html
    url_html = search_url.read()
    #This code will output the html for each match to a file
    filename = 'page.html'
    FILE = open(filename, "w")
    FILE.writelines(url_html)
    FILE.close()
    
#    Regular expression used to find valid wallpaper urls and append them to the url list
    matchs = re.findall(r'http://wallbase.cc/wallpaper/\d+', url_html)
    
#    Code for clearing the terminal, not really necessary
#    if sys.platform == 'linux2' or sys.platform == 'cygwin':
#        os.system('clear')
#    elif sys.platform == 'win32':
#        os.system('cls')

    print "\nPress enter to begin searching for matches\nWe are looking for wallpapers in the url:",  url
    raw_input()
    print '\nCurrently processing matches'

    for match in matchs:
        #img_src_open = urllib.urlopen(match)
        #img_src_html = img_src_open.read()
        ##The following is test code delete if it doesn't work, and uncomment above 2 lines
        img_src_req = Request(match, login_data, http_headers)
        img_src_open = urlopen(img_src_req)
        img_src_html = img_src_open.read()
        img_match_src = re.search(r'http://[^www]\S+(wallpaper-*\d+\S+\w+)', img_src_html)
        #img_match_src = re.search(r'http://[^www]\S+(wallpaper-\d+\S\w+)', img_src_html)
        #img_match_src_imgshack = re.search(r'http://[^www]\S+(wallpaper\d+\S+\w+)', img_src_html)
        #if not img_match_src:
        #img_match_src = re.search(r'http://[^www]\w+', img_src_html)
        #print img_match_src.group()
        #End of the test code
        if img_match_src:
            img_src_name.append(img_match_src.group(1))
            img_src_url.append(img_match_src.group(0))
            #Verbose output, uncomment if you want to see the source urls of the imgs
            print img_src_url[-1]
            #Completion percentage, usefl to see where you are in the matching process
            print 'wb ', 100 * float(matchs.index(match) +1)/float(len(matchs)), '% complete'
        else:
            #If no <img src> is found in the file, print error. Probably a login issue.
            print 'Error: No img_src\'s found'
            
    print '\n', len(img_src_name), " Wallpapers successfully found."
    raw_input("\n\nPress enter to download your wallpapers!")
    print "\nDeploying ninjas to steal wallpapers"
    
    count = 0
    for img in img_src_name:
        #    Humoreous retreival string
        print 'Stealing wallpaper', img_src_name.index(img) + 1
        get_img(img, img_src_url[count])
        count += 1
    print "Wallpapers successfully stolen. Enjoy!"


def get_img(filename, url):
    """This method is used to retrieve a specific url in the form of 'http://valid-path.jpg'
    FUTURE: feed a list of urls into this method instead of one url at a time """
#    Verbose file retrieval string
#    print 'Retrieving ' + filename +' from the URL @' +  url
    urllib.urlretrieve(url, filename)
    
def wallbase_auth(username, password):
    '''The following code takes user variables and logs you into wallbase.
    this allows you to download images from favorites, and NSFW images. 
    This method needs to be run every time you attempt to run a match against
    restricted pages on wallbase'''
    
    #    Variables for the wallbase login page from the bash script
    #    usrname=$USER&pass=$PASS&nopass_email=Type+in+your+e-mail+and+press+enter&nopass=0&1=1
    login_vals = {'usrname': username, 'pass': password, 'nopass_email': 'TypeInYourEmailAndPressEnter', 'nopass': '0', '1': '1'}
    login_url = 'http://wallbase.cc/user/login'
    login_data = urllib.urlencode(login_vals)
    #    Used to fool the website into this it's a browser, and a fake referer for login
    http_headers =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'referer': 'http://wallbase.cc/start/'} 
    #    Request built to actually log the user into the server        
    req = Request(login_url, login_data, http_headers)
    resp = urlopen(req)
    cj.save(COOKIEFILE)
    #print resp.read()
    #print 'Successfully authed'

def list_favorites():
    '''Calls to this method returns a dictionary of the users favorites
    This will allow to select which favorites they would like to download'''
    
    #Code to set variables for login and search functions
    login_vals = {'usrname': 'andrusk', 'pass': 'p0w3rus3r', 'nopass_email': 'TypeInYourEmailAndPressEnter', 'nopass': '0', '1': '1'}
    login_data = urllib.urlencode(login_vals)
    http_headers =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'referer': 'wallbase.cc http://wallbase.cc/user/adult_confirm/1 '} 
    favorites_url = 'http://wallbase.cc/user/favorites'
    fav_req = Request(favorites_url, login_data, http_headers)
    fav_resp = urlopen(fav_req)
    fav_list_html = fav_resp.read()
    cj.save(COOKIEFILE)
    
    #Begin matching the favorites urls and their names
    fav_src_dict ={}
    fav_src_url = re.findall(r'(http://wallbase.cc/user/favorites/\d+)" class="collink"><span class="counter">\d+</span>\s\w+\s*\w*', fav_list_html)
    fav_src_name = re.findall(r'</span>\s(\w+\s*\w*)', fav_list_html)
    count = 0
    while count < len(fav_src_name):
        fav_src_dict [fav_src_name[count]] = fav_src_url[count]
        count +=1
    return fav_src_dict
    
    
def logout():
    '''This sub-method when invoked will clear all cookies
        stored by this method and effectively log the user out.
        Run this method when you're down downloading if you want to 
        clear your cookies'''
    cj.clear_session_cookies()
    print 'You have been logged out'



wallbase_auth('andrusk', 'p0w3rus3r')
#print list_favorites()


Wallbase_Search('http://wallbase.cc/user/favorites/24355')
#Wallbase_Search('http://wallbase.cc/user/favorites/6066')
#Wallbase_Search('http://wallbase.cc/search')