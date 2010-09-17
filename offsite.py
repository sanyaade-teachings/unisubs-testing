"""
offsite.py
    Defines actions that don't take place directly on the universalsubtitles website or widget
"""
from selenium import selenium
import unittest
import time
import urllib
import mslib
import testvars
import widget
import selvars


def TwitterAuth(self,sel,user,passw):
    """
    Description: Perform twitter account sign-in once window
                 has been launced via website or widget.
    Requires: valid username and password
    """
    print "twitter auth: "+ user+":"
    sel.select_pop_up("null")
    mslib.wait_for_element_present(self,sel,"username_or_email")
    sel.type("username_or_email", user)
    sel.type("session[password]", passw)
    sel.click("allow")



def OpenIdAuth(self,sel,user,passw):
    """
    Description: Perform open id [from http://myopenid.com ]account sign-in once window
                 has been launced via website or widget.
    Requires: valid username and password
    """
    print "open id auth: "+ user
    sel.select_pop_up("null")
    mslib.wait_for_element_present(self,sel,"openid_url")
    sel.type("css=.openid", testvars.openiduser)
    sel.click("css=.open-id")
    mslib.wait_for_element_present(self,sel,"signin_button")
    sel.type("password", testvars.passw)
    sel.click("signin_button")
    

def GmailAuth(self,sel,user,passw):
    """
    Description: Perform gmail account sign-in once window
                 has been launced via website or widget.
    Requires: valid username and password
    """
    sel.select_pop_up("null")
    print "gmail auth: "+ user
    mslib.wait_for_element_present(self,sel,"signIn")
    sel.type("Email", user)
    sel.type("Passwd", passw)
    sel.click("signIn")

def start_youtube_widget_null(self,sel):
    """
    Description: Opens the widet for subtitling a YouTube video against
                 dev.universalsubtitles.org in the null sandbox.

                 Test site http://pculture.org/mirosubs_tests/dev-widget-null.html, has
                 multiple embedded widgets.

                 After running this, user should be in step 1 or edit dialog of widget.
                 
                 See http://s3.staging.universalsubtitles.org/embed00081.js for embed
                 code documentation.
            
    """
    sel.open("http://pculture.org/mirosubs_tests/dev-widget-null.html")
    #left column is the youtube video
    mslib.wait_for_element_present(self,sel,"css=.left_column span.mirosubs-tabTextchoose")
    sel.click("css=.left_column span.mirosubs-tabTextchoose")
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["AddSubtitles_menuitem"])
    sel.click(testvars.WebsiteUI["AddSubtitles_menuitem"])
    widget.close_howto_video(self,sel)
        
def start_ogg_widget_null(self,sel):
    """
    Description: Opens the widet for subtitling an ogg video against
                 dev.universalsubtitles.org in the null sandbox.

                 Test site http://pculture.org/mirosubs_tests/dev-widget-null.html, has
                 multiple embedded widgets.
                 
                 After running this, user should be in step 1 or edit dialog of widget.
                 
                 See http://s3.staging.universalsubtitles.org/embed00081.js for embed
                 code documentation.
    """
    sel.open("http://pculture.org/mirosubs_tests/dev-widget-null.html")
    #right column is the .ogg video
    mslib.wait_for_element_present(self,sel,"css=.right_column span.mirosubs-tabTextchoose")
    sel.click("css=.right_column span.mirosubs-tabTextchoose")
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["AddSubtitles_menuitem"])
    sel.click(testvars.WebsiteUI["AddSubtitles_menuitem"])
    widget.close_howto_video(self,sel)

def handle_warning_popup(self,sel):
    """
    Description: Closes the warning pop-up for offsite widgets

    """
    sel.select_pop_up("null")
    if sel.is_element_present("css=.mirosubs-warning"):
        sel.click("link=Continue")
        for i in range(60):
            try:
                if not sel.is_element_present("css=.mirosubs-warning"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
    sel.select_window("null")

def get_blip_video_url(self,file_type="flv"):
    try:
        self.selenium = (selenium(selvars.set_localhost(), selvars.set_port(), selvars.set_browser("blip",": get video url"), "http://blip.tv/"))
        self.selenium.start()
        bsel= self.selenium
        bsel.set_timeout(testvars.MSTestVariables["TimeOut"])
        random_url = "posts?sort=random&file_type="+file_type+"&page=1&view=list"
        bsel.open(random_url)
        print "opening: "+random_url
        mslib.wait_for_element_present(self,bsel,"css=.EpisodeListThumb img")
        bsel.click("css=.EpisodeListThumb img")
        bsel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
        blipURL = bsel.get_eval("window.location")
    finally:
        bsel.close()
        bsel.stop()
    print blipURL
    return blipURL


def get_vimeo_video_url(self):
    try:
        self.selenium = (selenium(selvars.set_localhost(), selvars.set_port(), selvars.set_browser("vimeo",": get video url"), "http://vimeo.com/"))
        self.selenium.start()
        vsel= self.selenium
        vsel.set_timeout(testvars.MSTestVariables["TimeOut"])
        vsel.open("groups/all/sort:recent")
        vsel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
        vsel.click("css=.detail_format a.thumbnail")
        mslib.wait_for_element_present(self,vsel,"css=div.tabmain a:contains('Videos')")
        vsel.click("css=div.tabmain a:contains('Videos')")
        mslib.wait_for_element_present(self,vsel,"css=div#vimeo_dropdown_2")
        vsel.click_at("css=div#vimeo_dropdown_2", "")
        vsel.click_at("css=li#detail", "")
        mslib.wait_for_element_present(self,vsel,"css=.thumbnail_box a.thumbnail")
        vsel.click("css=.thumbnail_box a.thumbnail")
        mslib.wait_for_element_present(self, vsel,"css=input#clip_id")
        urlid = vsel.get_value("css=input#clip_id")
        vimeoURL = "http://vimeo.com/"+urlid
        print vimeoURL
        return vimeoURL

    finally:
        vsel.close()
        vsel.stop()
    return vimeoURL

        
    
