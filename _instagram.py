import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from _instagramform import Ui_MainWindow
import instaloader


class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set combobox
        self.combo = self.ui.cboption
        self.combo.addItems(["Followees Doesnt Follow Back","Followers I Dont Follow Back"])

        # Initialize the Instaloader
        self.L = instaloader.Instaloader()

        # info confirm button initialize
        self.ui.btnconfirm.clicked.connect(self.confirmInfo)

        # confirm combobox
        self.ui.btnconfirmcombo.clicked.connect(self.comboBox)

        # clear the widget
        self.ui.btbclear.clicked.connect(self.removelist)

    def confirmInfo(self):
        # Get username and password from the GUI
        username = self.ui.lnname.text()
        password = self.ui.lnpassword.text()

        try:
            self.L.login(username,password)
        except instaloader.exceptions.BadCredentialsException:
            # If the username and password are incorrect, show an error message
            QMessageBox.critical(self, "Error", "Incorrect username or password.")
        else:
            # If the login session file exists and is valid, show a success message
            QMessageBox.information(self, "Success", "You are now logged in to Instagram.")

        # get the profile of the logged-in user
        self.profile = instaloader.Profile.from_username(self.L.context, username)
        # profile info
        self.followers_count = self.profile.followers
        self.followings_count = self.profile.followees
        # show count
        self.ui.lblnumfollowers.setText(str(self.followers_count))
        self.ui.lblnumfollowing.setText(str(self.followings_count))
        print(username,password)

    # Set combobox
    def comboBox(self):
        print(self.combo.currentText())
        if self.combo.currentText() == "Followees Doesnt Follow Back":
            self.findunfollowers()
        elif self.combo.currentText() == "Followers I Dont Follow Back":
            self.findIdontfollow()

    # find unfollowers
    def findunfollowers(self):
        # get the set of followers and followees
        followers = set(self.profile.get_followers())
        followees = set(self.profile.get_followees())

        # find the set of users who are followed but not following back
        unfollowers = followees - followers  

        # add the unfollowers to the userlist widget
        for user in unfollowers:
            self.ui.userlist.addItem(user.username)

        self.ui.lbllistcount.setText(str(len(unfollowers)))
    
    def findIdontfollow(self):
        # get the set of followers and followees
        followers = set(self.profile.get_followers())
        followees = set(self.profile.get_followees())

        # find the set of users who follow me but I don't follow back
        dont_follow_back = followers - followees 

        # add the users who don't follow back to the userlist widget
        for user in dont_follow_back:
            self.ui.userlist.addItem(user.username)
        
        self.ui.lbllistcount.setText(str(len(dont_follow_back)))

    def removelist(self):
        # clear the userlist widget
        self.ui.userlist.clear()



def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app() 
