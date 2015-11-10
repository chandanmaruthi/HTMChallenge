# import time
# from slackclient import SlackClient
#
# token = "xoxb-11405793909-rR17V7X3V0iJ2Lv5uJbvoIei"      # found at https://api.slack.com/#auth)
# sc = SlackClient(token)
# print sc.api_call("api.test")
# print sc.api_call("channels.list")
# print sc.api_call("channels.info", channel="C0ATCSFNY")
# print sc.api_call("chat.postMessage", channel="C0ATCSFNY", text="Hello botty bot")
#


import time
import json
from slackclient import SlackClient
from slacker import Slacker
from integration_omdb import OMDBServiceIntegration

Help_File_Path ='/home/chandan/chandan/code/brainscience/curious/curiousWorkbench/slackClient_Help.txt'
absFileLocation = '/home/chandan/chandan/code/brainscience/curious/curiousWorkbench/static/curiousWorkbench/images' +'/predictionGraph.png'


token = "xoxb-11405793909-rR17V7X3V0iJ2Lv5uJbvoIei"# found at https://api.slack.com/#auth)
#token = 'xoxp-10930857875-10930857891-10931049571-57b02068c8'
inputMsg='no value'
channel_general = 'C0ATCSFNY'
#token = "xoxb-11419374998-BlgFgJxlJWTi7b9zDH2e1tkp"
omdb = OMDBServiceIntegration()

msg='{"ok":true,"channel":"C0ATCSFNY","ts":"1446956286.000011","message":{"type":"message","user":"U0ATCR7S7","text":"ddd","attachments":[{"image_url":"http:\/\/usercontent2.hubimg.com\/9081995.jpg","image_width":1024,"image_height":768,"image_bytes":34245,"text":"Optionaltextthatappearswithintheattachment","color":"36a64f","fields":[{"title":"Priority","value":"High","short":false}]}],"ts":"1446956286.000011"}}'

def handle_help():
    a = open(Help_File_Path, 'rb')
    b=a.read()
    return str(b)

def handle_AllServices():
    b= 'handle_AllServices'
    return b

def handle_StateServices():
    b= 'handle_StateServices'
    return b
def handle_Message( inputMessage):
    print inputMessage
    b = omdb.FindMovie(str(inputMessage))
    return b
def eventHandler():
    sc = SlackClient(token)
    slack = Slacker(token)
    #print sc.api_call("channels.list")
    inputMsg='no value'
    try:
        if sc.rtm_connect():
            while True:
                inputList = sc.rtm_read()
                print inputList
                if len(inputList) >0:
                    try:
                        eventType = inputList[0]['type']
                        if eventType == 'message':
                            inputMsg=str(inputList[0]['text']).lower()

                        if eventType == 'message':
                            if inputMsg.find('#help') >-1:
                                sc.rtm_send_message(channel_general, handle_help() )
                            elif inputMsg.find('#allservices') >-1:
                                sc.rtm_send_message(channel_general, handle_AllServices())
                            elif inputMsg.find('#state000') >-1:
                                sc.rtm_send_message(channel_general, handle_StateServices())
                            elif inputMsg.lower().find('#hollybot') >-1:
                                strMsg=handle_Message(inputMsg.replace('#hollybot ',''))
                                #sc.rtm_send_message(channel_general,strMsg )
                                print '--------------------------------'

                                #dictAttachment ={}
                                #dictAttachment[fallback] = 'Required plain-text summary of the attachment.'
                                #dictAttachment[color] = '#36a64f'
                                #dictAttachment[pretext] ='Knowledge graph'
                                #dictAttachment[text] = 'Optional text that appears within the attachment'
                                #dictAttachment[image_url] ='http://cdn.akc.org/akcdoglovers/GoldenRetriever_cutout.png'
                                #jsonAttachments = json.dumps(dictAttachment)
                                #print jsonAttachments
                                strlink='http://walnutai.com/static/curiousWorkbench/images/predictionGraph.png'
                                strAttachments = '[{"fallback": "Required plain-text summary of the attachment.","color": "#36a64f","pretext": "Knowledge graph","text": "Optional text that appears within the attachment","image_url": "'+strlink+'"}]'
                                #slack.files.upload(Help_File_Path)
                                slack.chat.post_message('#general', strMsg, attachments=strAttachments)
                                #self, channel, text, username=None, as_user=None,
                                #parse=None, link_names=None, attachments=None,
                                #unfurl_links=None, unfurl_media=None, icon_url=None,
                                #icon_emoji=None
                                #slack.files.upload(Help_File_Path)
                    except:
                        eventType =''
                        print ''


                time.sleep(1)
        else:
            print "Connection Failed, invalid token?"
    except:
        raise 'error'
    return True



eventHandler()
