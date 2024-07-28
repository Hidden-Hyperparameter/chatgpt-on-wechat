# encoding:utf-8

import requests
import json
from common import const
from bot.bot import Bot
from bot.session_manager import SessionManager
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
from .cphos_wenxin_session import CPHOSWechatSession

class CPHOSBot(Bot):

    def __init__(self):
        super().__init__()
        wenxin_model = conf().get("baidu_wenxin_model")
        if wenxin_model is not None:
            wenxin_model = conf().get("baidu_wenxin_model") or "eb-instant"
        else:
            if conf().get("model") and conf().get("model") == const.WEN_XIN:
                wenxin_model = "completions"
            elif conf().get("model") and conf().get("model") == const.WEN_XIN_4:
                wenxin_model = "completions_pro"

        self.sessions = SessionManager(CPHOSWechatSession)

    def reply(self, query, context=None):
        print('-'*20,'\n','[CPHOSBot] query={}'.format(query),'\n','-'*20)
        # acquire reply content
        if context and context.type:
            if context.type == ContextType.TEXT:
                logger.info("[CPHOSBot] query={}".format(query))
                session_id = context["session_id"]
                reply = None
                if query == "#清除记忆":
                    self.sessions.clear_session(session_id)
                    reply = Reply(ReplyType.INFO, "记忆已清除")
                elif query == "#清除所有":
                    self.sessions.clear_all_session()
                    reply = Reply(ReplyType.INFO, "所有人记忆已清除")
                else:
                    session = self.sessions.session_query(query, session_id)
                    result = self.reply_text(session)
                    successful, reply_content = (
                        result['status'],
                        result['content']
                    )
                    logger.debug(
                        "[CPHOSBot] new_query={}, session_id={}, reply_cont={}".format(session.messages, session_id, reply_content)
                    )

                    if not successful:
                        reply = Reply(ReplyType.ERROR, reply_content)
                    else:
                        self.sessions.session_reply(reply_content, session_id)
                        reply = Reply(ReplyType.TEXT, reply_content)
                return reply
            elif context.type == ContextType.IMAGE_CREATE:
                ok, retstring = self.create_img(query, 0)
                reply = None
                if ok:
                    reply = Reply(ReplyType.IMAGE_URL, retstring)
                else:
                    reply = Reply(ReplyType.ERROR, retstring)
                return reply

    def reply_text(self, session, retry_count=0):
        try:
            return {'status': True, "content": "Hello, World!"}
        except Exception as e:
            need_retry = retry_count < 2
            logger.warn("[CPHOSBot] Generation Exception: {}".format(e))
            need_retry = False
            self.sessions.clear_session(session.session_id)
            result = {'status':False, "content": "出错了: {}".format(e)}
            return result
        
    def create_img(self, query, retry_count=0):
        raise NotImplementedError