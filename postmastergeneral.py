#*************************#
#   Post Master General   #
#*************************#

from postslave import PostSlave

class PostMasterGeneral:

    def __init__(self):
        self.posty = PostSlave()

    def sendRegistrationEmail(self, toAddress, regURL):
        email = self.posty.create_message(toAddress + '@pitt.edu', 'Academic Committee Registration', '127.0.0.1:5000/register/' + regURL)
        self.posty.send_message(email)


