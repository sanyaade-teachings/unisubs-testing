"""
widget.py
Description: handles actions that are performed within the widget.
"""

from selenium import selenium

import unittest
import time
import re
import codecs
import mslib
import testvars


def Login(self,sel,auth_type):
    """
    Description: Initiates login sequence using the Subtitle Me menu that's attached to
    an embedded vidoe, either onsite or offsite.

    auth_type can be 'log' (for site), 'twitter','openid','gmail'
    Requires valid accounts for chosen login type

    Pre-condition: Subtitle me widget menu should be present on page.

    Post-condition: either site or external login authorization pages are opened.
    For offsite login options see <a href="offsite.html">offsite</a>
    """
    print "logging in using "+auth_type+ " account"
    mslib.wait_for_element_present(self,sel, testvars.WebsiteUI["SubtitleMe_menu"])
    sel.click_at(testvars.WebsiteUI["SubtitleMe_menu"], "")
    sel.click_at(testvars.WebsiteUI["Login_menuitem"], "")
    sel.select_frame("relative=top")
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-"+auth_type)
    sel.click("css=.mirosubs-"+auth_type)

def site_login_from_widget_link(self,sel):
    """
    Description: performs a site login from the Login link on the widget steps.

    Pre-condition: widget is opened and user is not logged in.

    Post-condition: user is returned to starting widget page.
    """

    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Must_Login"])        
    print "loggin in from widget"
    sel.click("link=LOGIN")
    site_login_auth(self,sel)

def site_login_auth(self,sel):
    """
    Description: specifically logs in as the site user defined in <a href="testvars.html">testvars</a>

    Pre-condition: Login link was clicked from widget

    Post-condition: user logged in and returned to widget page.
    """
    auth_type = "log"
    sel.select_frame("relative=top")
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-"+auth_type)
    sel.click("css=.mirosubs-"+auth_type)
    sel.select_pop_up("null")
    mslib.wait_for_element_present(self,sel,"id_username")
    sel.type("id_username", testvars.siteuser)
    sel.type("id_password", testvars.passw)
    sel.click("//button[@value='login']")
    #wait for the login to complete
    time.sleep(10)
    
        
def close_howto_video(self,sel,skip="True"):
    """
    Description: closes the how-to interstitial help video
    Default is set to "True", to skip the video on proceeding steps.

    Pre-condition: widget has been launched.
    
    Post-condition: help video is closed and returned to previous widget page.
    """
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-modal-widget-content")
    if sel.is_element_present("css=.mirosubs-howtopanel"):
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-done:contains('Continue')")
        mslib.wait_for_element_present(self,sel,"css=.goog-checkbox-unchecked")
        if skip=="True":
            sel.click("css=.goog-checkbox-unchecked")
        sel.click("css=.mirosubs-done:contains('Continue')")


def transcribe_video(self,sel,sub_file,mode="Expert",step="Continue", buffer="yes"):
    """
    Description: On widget Step 1, reads in lines of subtitle text and types it.

    Options:
        sub_file - the full path to the text to enter
        mode - sets typing mode {'Beginner' | 'Recommended' | 'Expert (default)'}
        step - {'Stop' | 'Continue' (default)} Continue on to next step.
        buffer {'yes' (default) | 'no'} will buffer the video to 75% before
        proceeding. see wait_for_video_to_buffer
    """
    print "starting to transcribe video"
    # giving the video a chance to load.
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Play_pause"])
    mode_label = sel.get_text("css=.mirosubs-speedmode option:contains("+mode+")")
    sel.select("//select", "label=" +mode_label)
    if buffer != "no":
        mslib.wait_for_video_to_buffer(self,sel)
    else: time.sleep(10)
        
    sel.click(testvars.WidgetUI["Play_pause"])

    for line in codecs.open(sub_file,encoding='utf-8'):
        sel.click("css=.trans")
        sel.type("css=.trans", line)
        sel.type_keys("css=.trans"," ")
        mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Transcribe_current_sub"])
        current_sub = sel.get_text(testvars.WidgetUI["Transcribe_current_sub"])
        if line.rstrip() != current_sub.rstrip():
            mslib.AppendErrorMessage(self,sel,"sub text mismatch")
            print "found: " + current_sub.rstrip()
            print "expected: " +line
        sel.key_press("css=.trans", "\\13")
        time.sleep(2)
    if step == "Continue":
        sel.click(testvars.WidgetUI["Next_step"])


def restart_typing(self,sel):
    """
    Description: Clicks the 'Restart Typing' link, and handle the confirmation dialog.
    """
    if sel.is_element_present("css=.mirosubs-restart"):
    # If it loads the widget automatically
        sel.click("css=.mirosubs-restart")
        self.failUnless(re.search(r"^Are you sure you want to start over[\s\S] All subtitles will be deleted\.$", sel.get_confirmation()))

def back_step(self,sel):
    """
    Description: Clicks the 'Back to' link to go back 1 step.
    """
    while sel.is_text_present("Back to") or sel.is_text_present("Return to"):
        sel.click("css=.mirosubs-backTo")
        time.sleep(3)
        mslib.wait_for_element_present(self,sel,"css=.mirosubs-steps")

def sync_video(self,sel,sub_file,start_delay=2,sub_int=2,step="Continue"):
    """
    Description: Use the defined sync button to sync the subtitles.  Waits for
    text present on the video and prints the subtime.

    Options:
        sub_file - path to file or text lines to enter
        start_delay - time to wait before 1st sync (default = 2 secs)
        sub_int - time to wait before next sub (default = 2 secs
        step - {'Continue' (default) | 'Stop} move on to next step when done.

    Pre-condition - can use this to sync on Step 2, Step 3 or Edit.
    """
    print "starting video / sub syncing"
    sel.select_frame("relative=top")
    #give video a chance to load
    time.sleep(5)
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Play_pause"])
    print "clicking video play button to start playback"
    sel.click(testvars.WidgetUI["Video_playPause"])
       
    time.sleep(start_delay)
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Sync_sub"])
    for line in open(sub_file):
        sel.focus(testvars.WidgetUI["Sync_sub"])
        sel.click_at(testvars.WidgetUI["Sync_sub"],"")
        mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Active_subtime"])
        print sel.get_text(testvars.WidgetUI["Active_subtime"]) +": "+ sel.get_text(testvars.WidgetUI["Active_subtext"])
        time.sleep(sub_int)
    sel.focus(testvars.WidgetUI["Sync_sub"])
    sel.click_at(testvars.WidgetUI["Sync_sub"],"")
    if step == "Continue":
        sel.click(testvars.WidgetUI["Next_step"])
    
                  


def edit_text(self,sel,subtextfile,new_text="my hovercraft is full of eels"):
    """
    Description: Input the same text used in transcribe_video and for each line,
    edit the text with new_text.  Verifies text has been updated.

    Options:
        new_text - text string

    Pre-condition - can use this to sync on Step 2, Step 3 or Edit.
    """
    sel.select_window("null")
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-titlesList")
    sub_li=1
    for line in open(subtextfile):
        sub_cell = "//li["+str(sub_li)+"]/span[2]"
        sel.focus(sub_cell)
        sel.click(sub_cell)
        sel.type("css=textarea", new_text)
        sel.key_press("css=textarea", "\\13")
        sub_cell_text=sel.get_text(sub_cell)
        if sub_cell_text.rstrip() != new_text.rstrip():
            mslib.AppendErrorMessage(self,sel,"text not edited correctly")
            print "expected: " +new_text+ "found: "+ sub_cell_text.rstrip
        sub_li = sub_li + 1
        
def drag_time_bubbles(self,sel,subtextfile):
    """
    Description: For each line, initially used in transcribe_video, grab
    the left and right sides of the timeline bubbles and edit the time.
    Verifies the time stamp has been modified.
    
    Options:
        new_text - text string

    Pre-condition - use must be on Step 3 or Review with known text data.
    """

    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Sync_sub"])
    sub_li = 1
    for line in open(subtextfile):
        
        sub_cell_start_time = "//li["+str(sub_li)+"]/span[1]/span/span[1]"
        
        sub_cell_end_time = "//span["+str(sub_li)+"]/span/span[2]"
    
        # drag start time to the left and verify time change
        start_time = sel.get_text(sub_cell_start_time)
        print start_time
        drag_it(self,sel,line.rstrip(),"left","-60")
        new_start_time = sel.get_text(sub_cell_start_time)
        self.failUnless(int(start_time) > int(new_start_time))

        # drag start time to the right and verify time change
        start_time = sel.get_text(sub_cell_start_time)
        print start_time
        drag_it(self,sel,line.rstrip(),"left","+60")
        new_start_time = sel.get_text(sub_cell_start_time)
        self.failUnless(int(start_time) < int(new_start_time))
           
        # drag end time to the left and verify time change
        end_time = sel.get_text(sub_cell_end_time)
        print end_time
        drag_it(self,sel,line.rstrip(),"right","-60")
        new_end_time = sel.get_text(sub_cell_end_time)
        self.failUnless(int(end_time) > int(new_end_time))

        # drag end time to the right and verify time change
        end_time = sel.get_text(sub_cell_end_time)
        print end_time
        drag_it(self,sel,line.rstrip(),"right","+60")
        new_end_time = sel.get_text(sub_cell_end_time)
        self.failUnless(int(end_time) < int(new_end_time))

  
def drag_it(self,sel,sub_text,side,move_pixels):
    """
    Description: actually grabs the timeline bubbles and moves them

    Options:
        sub_text - text used to locate correct bubble
        side - {'left' | 'right'}
        move_pixels - number of pixels to move bubble { + | - }
    """
    if "left" in side:
        sel.drag_and_drop("css=.mirosubs-subtext:contains(" + sub_text + ") + span", move_pixels+",0")
    if "right" in side:
        sel.drag_and_drop("css=.mirosubs-subtext:contains(" + sub_text + ") +span + span", move_pixels+",0")


                

def click_time_shift_arrows(self,sel,subtextfile):
    """
    Description: clicks the left and right arrows on subtitle text box.
    Verifies that the time has been changed by .05 seconds.

    Options:
        subtextfile - text used in transcribe step.
        
    """
    
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Sync_sub"])
    sub_li = 1
    for line in open(subtextfile):
        sub_cell_start_time = "//li["+str(sub_li)+"]/span[1]/span/span[1]"
        up_arrow = "//li["+str(sub_li)+"]/span[1]/span/span[2]/a[1]"
        down_arrow = "//li["+str(sub_li)+"]/span[1]/span/span[2]/a[2]"
        for x in range(0,5):  
            #Click up (right) and verify time jump of .05 seconds
            start_time = sel.get_text(sub_cell_start_time)
            sel.focus(up_arrow)
            sel.click_at(up_arrow,"")
            new_start_time = sel.get_text(sub_cell_start_time)
            self.failUnless(float(new_start_time) - float(start_time)) == .05
            #maybe verify the pixel change on the timeline
        for x in range(0,5):
            #Click text-arrow right and verify time jump
            start_time = sel.get_text(sub_cell_start_time)
            sel.click_at(down_arrow,"")
            new_start_time = sel.get_text(sub_cell_start_time)
            self.failUnless(float(start_time) - float(new_start_time)) == .05
            #maybe verify the pixel change on the timeline

    
def hold_down_delay_sub(self,sel,sub_file,delay_time=4,hold_time=2, sync_time=2):
    """
    Description: tests the time shift of subs when holding then releasing the down key.
    Verifies that the time has been shifted.

    Options:
        delay_time - amount of time to wait before jumping back with ctrl key (default=4)
        hold_time - amount of time to hold down the key (default=2) 
        sync_time - amount of time wait before starting next subtitle (default=2)

    Pre-conditions: must coordinate this with the times used in sync_video or the time shift
    comparision may fail.

    Post-condition - still on same step in widget, with new times.
    """
    print "down key time shift"
    sel.select_frame("relative=top")
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Play_pause"])
    sel.click(testvars.WidgetUI["Video_playPause"])
    time.sleep(delay_time)
    sel.click(testvars.WidgetUI["Skip_back"])
    sub_li = 1
    for line in open(sub_file):
        sub_cell_start_time = "//li["+str(sub_li)+"]/span[1]/span/span[1]"
        old_time = sel.get_text(sub_cell_start_time)
        # 40 is the native key code for down arrow key
        sel.key_down_native("40")
        time.sleep(hold_time)
        sel.key_up_native("40")
        new_time = sel.get_text(sub_cell_start_time)
        print old_time + " ==> " + new_time
        if old_time == new_time:
            mslib.AppendErrorMessage(self,sel,"time's not shifted")
        time.sleep(sync_time)
        sub_li = sub_li + 1

def resync_video (self,sel,subtextfile,start_delay=1,sub_int=1, step="Stop"):
    """
    Description: tests the time shift of subs when using down key to resyncronize.
    Verifies time stamp has changed.

    Options:
        start_delay - amount of time to wait before jumping back with ctrl key (default=4)
        sub_int - amount of before next sub sync
        step - {'Stop' (default) | 'Continue'}

    Pre-conditions: must coordinate this with the times used in sync_video or the time shift
    comparision may fail.
    """
    print "starting sub resync"
    sel.select_frame("relative=top")
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Play_pause"])
    sel.click(testvars.WidgetUI["Video_playPause"])
       
    time.sleep(start_delay)
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Sync_sub"])
    sub_li = 1
    for line in open(subtextfile):
        #Fix Me - find correct xpath for the sub start time in a cell
        sub_cell_start_time = "//span["+str(sub_li)+"]/span/span[1]"
        start_time=sel.get_text(sub_cell_start_time)
        sel.focus(testvars.WidgetUI["Sync_sub"])
        sel.click_at(testvars.WidgetUI["Sync_sub"],"")
        mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Active_subtime"])
        new_start_time = sel.get_text(testvars.WidgetUI["Active_subtime"])
        self.failUnless(float(start_time) < float(new_start_time))
        time.sleep(sub_int)
    sel.focus(testvars.WidgetUI["Sync_sub"])
    sel.click_at(testvars.WidgetUI["Sync_sub"],"")
    if step == "Continue":
        sel.click(testvars.WidgetUI["Next_step"])


def verify_login_message(self,sel):
    """
    Description: verifies must login message is displayed.
    """
    mslib.wait_for_element_present(self,sel,testvars.WidgetUI["Must_Login"])
    self.failUnless(sel.get_text(testvars.WidgetUI['Must_Login'] +":contains('To save your subtitling work')"))

def steps_display(self,sel,step_num):
    """
    Description: verifies text contents of Steps.  
    """
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-activestep:contains('"+str(step_num)+")")
    self.failUnless("Typing" == sel.get_text("css=h2"))
    self.failUnless(str(step_num) == sel.get_text("css=.mirosubs-activestep"))
    self.failUnless("tab" == sel.get_text("css=.mirosubs-tab"))
    if step == "1":
        self.assertEqual("Play next 8 seconds", sel.get_text("css=.mirosubs-tab + span"))
    else:
        self.assertEqual("Play/Pause", sel.get_text("css=.mirosubs-tab + span"))
    self.assertEqual("ctrl", sel.get_text("css=.mirosubs-control"))
    self.assertEqual("Re-play last 8 seconds", sel.get_text("css=.mirosubs-control + span"))
    self.assertEqual("Speed Mode", sel.get_text("css=.mirosubs-speedmode h4"))

def verify_sub_text(self,sel,subtextfile):
    """
    Description: Compares the current text in the text box with the text in the input subtextfile.

    Pre-condition: User in widget, steps 1,2,3 or Edit.

    """
    print "verifying sub text"
    sel.select_window("null")
    mslib.wait_for_element_present(self,sel,"css=.mirosubs-titlesList")
    sub_li=1
    for line in codecs.open(subtextfile,encoding='utf-8'):
        sub_cell_text = "//li["+str(sub_li)+"]/span[2]"
        self.assertEqual(line.rstrip(), sel.get_text(sub_cell_text).rstrip())
        sub_li = sub_li + 1
        