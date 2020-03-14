from .__init__ import String,Base,Integer,Column

class InputMessage(Base):
    __tablename__ = 'INMSG'

    id = Column(Integer,autoincrement=True,primary_key = True)
    from_user = Column(String(64),comment='用户名')
    to_user = Column(String(64),comment='公众号')
    msg_type = Column(Integer,comment = '消息类型')
    msg_id = Column(String(64),comment = '消息id')
    text_content = Column(String(256),comment = '文本内容')




