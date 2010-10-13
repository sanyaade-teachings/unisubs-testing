"""Functions to take care of business on the universalsubtitles website


"""

from selenium import selenium

import unittest
import time
import re
import codecs
import mslib
import testvars
import widget


#Login as a user

def SiteLogIn(self,sel,user,passw):
    """
    Description: Login to site using the website login button and a site account
    
    Requires: valid site user name and password.
    
    Pre-condition: user is on the site page.


    
    Post-condition: user is still on the site page
    """
    sel.open("/logout/?next=/")
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["Login_Button"])
    sel.click(testvars.WebsiteUI["Login_Button"])
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    sel.type("id_username", user)
    sel.type("id_password", passw)
    sel.click("//button[@value='login']")
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["Logout_Button"])

def SiteLogout(self,sel):
    """
    Description: Logout of site using site Logout button.

    """
    sel.open("/logout/?next=/")
    mslib.wait_for_element_present(self,sel,"css=.login_link")
    if sel.is_element_present(testvars.WebsiteUI["Logout_Button"]):
        sel.click(testvars.WebsiteUI["Logout_Button"])
        mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["Login_Button"])
    

def Login(self,sel,auth_type):
    """
    Description: Log on using website button and select an external login option.
    auth_type can be either 'twitter', 'open-id', or 'google'

    Requires: valid account for selected login.  See testvars for existing accounts.

    Pre-condition: user is on the site page
    
    Post-condition: offsite login form displayed, see offsite
    
    
    """
    # auth_type can be either ".twitter", ".open-id", "google"
    if auth_type == "twitter":
        auth_link = "css=a[href*='twitter']"
    elif auth_type == "open-id":
        auth_link = "css=a[href*='openid']"
    elif auth_type == "google":
        auth_link = "css=a[href*='gmail']"
    else:
        self.fail("unrecognized auth type")
    sel.select_window("null")
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["Login_Button"])
    sel.click(testvars.WebsiteUI["Login_Button"])
    mslib.wait_for_element_present(self,sel,auth_link)
    sel.click(auth_link)
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    #After login, use offsite to do auth

def start_demo(self,sel):
    """
    Description: Starts the demo widget from the site

    Pre-condition: site page is opened

    Post-condition: /demo page is opened, usually next step is start_sub_widget
    """
    sel.open("/demo/")
#    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])

def submit_video(self,sel,url):
    """
    Description: Submit a video using the site button

    Pre-condition: site page is opened

    Post-condition: the widget is launched immediately.
    You'll need to deal with the help video, see widget.close_howto_video
    """
    print "* Submit Video"
    sel.open("/")
    sel.click(testvars.WebsiteUI["Subtitle_Button"])
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    sel.type("video_url", url)
    sel.click(testvars.WebsiteUI["Video_Submit_Button"])
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    widget.close_howto_video(self,sel)
    

def start_sub_widget(self,sel,wig_menu=testvars.WebsiteUI["SubtitleMe_menu"],skip="True",vid_lang="English",sub_lang="English"):
    """Start the Subtitle Widget using the Subtitle Me menu.

    This will handle the language choice for demo or submitted videos.
    skip is set to true by default and gets passed to widget.close_howto_video
    to prevent further how-to video displays.

    Pre-condition: On a page where Subtitle Me menu is present. Video with no subs.

    Post-condition: the widget is launched and you will be on step 1 or Edit step
    """
    
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["SubtitleMe_menu"])
    sel.click(testvars.WebsiteUI["SubtitleMe_menu"])
    time.sleep(5)
    if sel.is_element_present(testvars.WidgetUI["Select_language"]):
        widget.select_video_language(self,sel,vid_lang,sub_lang)
        widget.close_howto_video(self,sel)
    elif sel.is_element_present(testvars.WebsiteUI["AddSubtitles_menuitem"]):
        sel.click(testvars.WebsiteUI["AddSubtitles_menuitem"])
        widget.select_video_language(self,sel,vid_lang,sub_lang)    
        widget.close_howto_video(self,sel)
    else:
        self.fail("wtf - no widget, no sub menu")
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-activestep")

def verify_login(self,sel,username="sub_writer"):
    """
    Description: Verifies user is logged in by finding the logout button on the
    website and then starting the demo and looking for logout menu item on the
    Subtitle Me button.

    Pre-Condition: must be logged into site.

    Post-Condition: will be on the /demo page
    """
    mslib.wait_for_element_present(self,sel,testvars.WebsiteUI["Logout_Button"])
    self.failUnless(sel.is_element_present("css=.user_panel"),\
                    "user not logged in, user_panel not displayed")
    print "logged in as: " + sel.get_text("css=.user_panel a")
    self.failUnless(sel.is_element_present("css=.user_panel a:contains("+username+")"),\
                    "username: "+username+ " not found. Got "+ sel.get_text("css=.user_panel a"))



def verify_submitted_video(self,sel,vid_url,embed_type="html5"):
    """
    Description: Verifies the contents of the main video page of a submitted video.
    Require's the original url and expected type of embed.  Assumes html5 video if not specified.

    embed_type one of 'youtube', 'flow' 'html5' (default)

    Returns: url of the video on the universalsubtitles site.
    """
    print " * verify submitted video, embed type"
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
   
    if embed_type == "flow":
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-videoDiv object")
        self.assertTrue(sel.is_element_present("css=.mirosubs-videoDiv object[data*='flowplayer']"),\
                        "can't verify video embedded with flowplayer")
    elif embed_type == "youtube":
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-videoDiv object[data]")
        self.assertTrue(sel.is_element_present("css=.mirosubs-videoDiv object[data*='youtube.com']"),\
                        "can't verify video embed is youtube native")
    elif embed_type == 'vimeo':
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-videoDiv object")
        self.assertTrue(sel.is_element_present("css=.mirosubs-videoDiv object[data*='moogaloop.swf']"),\
                        "can't verify video embed is vimeo native")
    elif embed_type == 'dailymotion':
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-videoDiv object")
        self.assertTrue(sel.is_element_present("css=.mirosubs-videoDiv object[id$='_dailymotionplayer']"),\
                        "can't verify video embed is dailymotion native")
    else:
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-videoDiv")
        self.assertTrue(sel.is_element_present("css=.mirosubs-videoDiv video"),\
                        "can't verify video embed is html5 native")
        
   
    self.assertTrue(sel.is_element_present("css=.mirosubs-embed"),\
                    "no embed code present")
    unisubs_link = sel.get_text("css=.mirosubs-permalink[href]")
    print sel.get_text("css=.mirosubs-embed")
    return unisubs_link

def get_video_with_translations(self,sel):
    """Get the url of the video page for a video that has translations.

    Returns: video_url
    """
    sel.open("videos/")
    sort_videos_table(self,sel,"Translations","desc") 
    row_no = 3
    local_url = "none"
    
    subtitled_cell="css=tr:nth-child("+str(row_no)+") > "+testvars.videos_subtitled_td
    while sel.is_element_present(subtitled_cell):
        subtitled_cell=("css=tr:nth-child("+str(row_no)+") > "+testvars.videos_subtitled_td)
        if sel.get_text(subtitled_cell) == 'yes':
            local_url = sel.get_attribute("css=tr:nth-child("+str(row_no)+ ") > "+testvars.videos_url_td+" > a@href")
            break
        row_no = row_no + 1
        
    if int(sel.get_text("css=tr:nth-child("+str(row_no)+ " ) > "+testvars.videos_trans_td)) == 0:
        print "no translations - have to add one"
        get_video_no_translations(self,sel)
        translate_video(self,sel)
       
        
    return local_url
def get_video_no_translations(self,sel):
    """Get the url of the video page for a video that has translations.

    Returns: video_url
    """
    sel.open("videos/")
    sort_videos_table(self,sel,"Translations","asc") 
    row_no = 3
    local_url = "none"
    
    subtitled_cell="css=tr:nth-child("+str(row_no)+") > "+testvars.videos_trans_td
    while sel.is_element_present(subtitled_cell):
        subtitled_cell=("css=tr:nth-child("+str(row_no)+") > "+testvars.videos_trans_td)
        if int(sel.get_text(subtitled_cell)) == 0:
            local_url = sel.get_attribute("css=tr:nth-child("+str(row_no)+ ") > "+testvars.videos_url_td+" > a@href")
            break
        row_no = row_no + 1
        
    if local_url == "none":
        print "no untranslated vidoes - must add one."
        vid_url = offsite.get_youtube_video_url(self)
        submit_video(self,sel,vid_url)
        widget.select_video_language(self,sel)
        widget.close_howto_video(self,sel)
        widget.close_widget(self,sel)
        local_url = sel.get_eval("window.location")
        
    return local_url

def get_translated_lang(self,sel):
    """Locate a language (not metadata or original) tab for a video.

    Need to exclude Original, Video Info, and Metadata
    """
    #get the original language
    original_lang = sel.get_text(testvars.video_original)
    tab_no = 1
    tab_li = "css=ul.left_nav li:nth-child("+str(tab_no)+")"
    skip_list = [original_lang, "Video Info", "Metadata: Twitter", "Metadata: Geo", "Metadata: Wikipedia"]
    while sel.is_element_present(tab_li):
        tab_li = "css=ul.left_nav li:nth-child("+str(tab_no)+")"
        if sel.get_text(tab_li) not in skip_list:
            test_lang = sel.get_text(tab_li)
            break
        tab_no = tab_no + 1
    print test_lang
    return test_lang

def upload_subtitles(self,sel,sub_file,lang=None):
    """Uploads subtitles for the specified language."

    """
    sel.click(testvars.video_upload_subtitles)
    if lang == None:
        sel.select("id_language", "label=English")
    else:
        sel.select("id_language", "label="+lang)
    sel.type("subtitles-file-field",sub_file)
    sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])

def verify_sub_upload(self,sel,sub_file,lang=""):
    sub_td = 1
    for line in codecs.open(sub_file,encoding='utf-8'):
        subline = line.split(',')
        sub = subline[0].rstrip()
        self.assertTrue(sel.get_text("css=tr:nth-child("+str(sub_td)+") > td.last:contains('"+sub+"')"))
        sub_td = sub_td + 1
    if lang == "":
        self.assertEqual(sel.get_text("css=.active a"),"English")
    else:
        self.assertEqual(sel.get_text("css=.active a"),lang)

def translate_video(self,sel,url=None,lang=None):
    """Given the local url of a video, adds a translation.
        
    """
    if url == None:
        print "adding translation from current page"
    else:
        print "opening video page to translate"
        sel.open(url)
    self.assertTrue(sel.is_element_present("css=a#add_translation"),"add translation button not found")
    sel.click(testvars.add_translation_button)       

def sort_videos_table(self,sel,column,order):
    """Sort the videos table by the specified heading in the specified order

    Current column headings are: URL, Pageloads, Subtitles Fetched, Translations, Subtitled?
    Order can be 'asc' or 'desc'

    """

    if sel.is_element_present("css=a."+order+":contains("+column+")"):
        sel.click("link="+column)
        sel.wait_for_page_to_load(testvars.MSTestVariables["TimeOut"])
    if order == "asc":
        self.assertTrue(sel.is_element_present("css=a.desc:contains("+column+")"),"sort not correct")
    if order == "desc":
        self.assertTrue(sel.is_element_present("css=a.asc:contains("+column+")"),"sorted by desc")


def enter_comment_text(self,sel,comment):
    """Enter text in the Comments box and submit

    Assumes user is on the comments tab
    """
    self.assertTrue(sel.is_element_present("css=li.active span:contains(\"Comments\")"),"comments tab not found")
    sel.type("css=textarea#id_comment_form_content", comment)
    sel.click("css=button:contains('Comment')")

def verify_comment_text(self,sel,comment,result="posted",reply_text=None):
    """After comment text is entered in enter_comment_text, verify correct post behavior

    Result options: 'posted' comment is posted
                    'stripped' commented is posted and html stripped
                    'too long' > 3000 char length warning
                    'login' user must be logged into post
                    'reply' reply post contains original and new comment
    
    """
    #give it 3 seconds to post
    print "* Verify Comment"
    time.sleep(5)
    if result == "posted":
        posted_text = sel.get_text("css=ul.comments.big_list li:nth-child(1) > div.info p")
        self.assertEqual(posted_text.strip(),comment.strip(),"posted text doesn't match expected text")
    elif result == "too long":
        self.assertTrue(sel.is_element_present("css=p.error_list:contains('Ensure this value has at most 3000 characters')"), \
                        "too long message not found")
    elif result == "login":
        self.assertTrue(sel.is_element_present("css=.login-for-comment:contains('Login to post a comment')"), \
                        "login message not present")
        if sel.is_element_present("css=ul.comments.big_list li:nth-child(1) > div.info p"):
            self.assertNotEqual(sel.get_text("css=ul.comments.big_list li:nth-child(1) > div.info p"),"comment", \
                                "comment posted without login")  
   


def handle_error_page(self,sel,test_id):
    if sel.is_element_present("css=form h2:contains('Error')"):
        print sel.get_attribute("css=h2 + input@value")
        print sel.get_attribute("css=h2 + input@name")
        sel.type("feedback_email", testvars.gmail)
        feedback_math = sel.get_text("css=form#feedback_form p + p label")
        s = feeback_math[20:25]
        sel.type("feedback_math_captcha_field", eval(s))
        sel.type("feedback_message", "test_id: "+test_id+" sel-rc automated test encountered an error")
        sel.click("css=button[type='submit']")
        print "submitted error to feedback form"
    else:
        pass



