from flask import Flask,request,Response,make_response
import hashlib
import xml.etree.cElementTree as ET
import time
import logging
from DBModel import make_session
from DBModel.InputMessage import InputMessage
from ES import query_es

app = Flask(__name__)


@app.route('/',methods = ['GET'])
def echo():
    data = request.args
    sig = data.get('signature')
    timestamp = data['timestamp']
    nonce = data['nonce']
    echostr = data['echostr']
    token = 'humantragedy'
    li = [token,timestamp,nonce]
    li.sort()
    temp = ''.join(list(li))

    hashcode = hashlib.sha1(temp.encode('utf-8')).hexdigest()
    if hashcode == sig:
        return make_response(echostr)
    else:
        return ''

@app.route('/',methods = ['POST'])
def accept_info():
    data = request.data
    xml = ET.fromstring(data)
    to_user = xml.find('ToUserName').text
    from_user = xml.find('FromUserName').text
    msg_type = xml.find('MsgType').text
    msg_id = xml.find('MsgId').text
    now = time.time()

    if msg_type == 'text':
        content = xml.find('Content').text
        query=''
        if content.startswith('诗：'):
            query = content.split('：',1)[1]
            resp = query_es(query)
            if not resp:
                resp = content
        else:
            resp = content

        msg_type = 0
    else:
        content = msg_type
    with make_session() as sess:
        sess.add(InputMessage(
            from_user = from_user,
            to_user = to_user,
            msg_type = msg_type,
            msg_id = msg_id,
            text_content = content            
        ))
    res = r'''
         <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml>
            '''
    response = make_response(res % (from_user, to_user, str(now), resp))
    response.headers['content-type'] = 'application/xml'
    return response
    

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

