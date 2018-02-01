#!/usr/bin/env python2

# found on <http://files.majorsilence.com/rubbish/pygtk-book/pygtk-notebook-html/pygtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGTK

import gtk
import subprocess

def get_status():
    retval = subprocess.check_output(
        "systemctl status openvpn@client | grep active | awk '{print $2}'",
        shell=True
    )
    retval = retval[0:-1]
    return retval

def message(data=None):
  "Function to display messages to the user."

  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()



def start_openvpn(data=None):
    subprocess.call( "systemctl restart openvpn@client", shell=True)

def stop_openvpn(data=None):
    subprocess.call( "systemctl stop openvpn@client", shell=True)



def close_app(data=None):
#  message(data)
  gtk.main_quit()


def make_menu(event_button, event_time, data=None):
    menu = gtk.Menu()

  #------
    close_item = gtk.MenuItem("Close App")
    status_item = gtk.MenuItem("Status:"+get_status() )
    startvpn_item = gtk.MenuItem("StartVPN")
    stopvpn_item = gtk.MenuItem("StopVPN")

  #Append the menu items
    menu.append(status_item)
    menu.append(startvpn_item)
    menu.append(stopvpn_item)
    menu.append(close_item)

  #add callbacks
    close_item.connect_object("activate", close_app, "Close App")
    startvpn_item.connect_object("activate",start_openvpn,"StartVPN" )
    stopvpn_item.connect_object("activate",stop_openvpn,"StopVPN" )


  #Show the menu items

    status_item.show()
    close_item.show()
    startvpn_item.show()
    stopvpn_item.show()

  #Popup the menu
    menu.popup(None, None, None, event_button, event_time)

def on_right_click(data, event_button, event_time):
    make_menu(event_button, event_time)

#def on_left_click(event):

if __name__ == '__main__':
    icon = gtk.status_icon_new_from_file("/usr/share/icons/hicolor/48x48/ovpntech_key_green.png")
    icon.connect('popup-menu', on_right_click)
    gtk.main()