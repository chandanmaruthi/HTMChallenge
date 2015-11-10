from slacker import Slacker
from integration_omdb import *

a= OMDBServiceIntegration()
Help_File_Path ='/home/chandan/chandan/code/brainscience/curious/curiousWorkbench/slackClient_Help.txt'


slack = Slacker('xoxb-11405793909-rR17V7X3V0iJ2Lv5uJbvoIei')

# Send a message to #general channel
slack.chat.post_message('#general', 'Hello fellow slackers!')

# Get users list
response = slack.users.list()
users = response.body['members']

# Upload a file
#slack.files.upload(Help_File_Path)

print a.FindMovie('100')
