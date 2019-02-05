#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import re

import requests


class AutoDiscuz:
    LOGIN_URL = "/member.php?mod=logging&action=login&loginsubmit=yes"
    LOGIN_POST = {"username": "", "password": ""}

    def __init__(self, forum_url, user_name, password):
        """初始化论坛 url、用户名、密码和代理服务器."""
        self.forum_url = forum_url
        self.user_name = user_name
        self.password = password
        self.formhash = None
        self.is_login = False
        self.session = requests.Session()
        logging.basicConfig(level=logging.INFO,
                            format="[%(levelname)1.1s %(asctime)s] %(message)s")

    def login(self):
        """登录论坛."""
        url = self.forum_url + AutoDiscuz.LOGIN_URL
        AutoDiscuz.LOGIN_POST["username"] = self.user_name
        AutoDiscuz.LOGIN_POST["password"] = self.password
        req = self.session.post(url, data=AutoDiscuz.LOGIN_POST)
        if self.user_name in req.text:
            self.is_login = True
            if self.get_formhash():
                logging.info("Login success!")
                return
        logging.error("Login faild!")

    def get_formhash(self):
        """获取 formhash."""
        req = self.session.get(self.forum_url)
        rows = re.findall(
            r"<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />", req.text)
        if len(rows) != 0:
            self.formhash = rows[0]
            logging.info("Formhash is: " + self.formhash)
            return True
        else:
            logging.error("None formhash!")
            return False

    def reply(self, tid, subject="", msg="6666666666666666666"):
        """回帖."""
        url = self.forum_url + \
            "/forum.php?mod=post&action=reply&replysubmit=yes&inajax=1&tid=" + \
            str(tid)
        post_data = {"formhash": self.formhash,
                     "message": msg, "subject": subject}
        content = self.session.post(url, post_data).text
        if "发布成功" in content:
            logging.info("Tid: " + str(tid) + " reply success!")
            return True
        else:
            logging.error("Tid: " + str(tid) + " reply faild!")
            return False


def main():
    auto_discuz = AutoDiscuz("http://url", "account", "password")
    auto_discuz.login()
    if auto_discuz.is_login:
        auto_discuz.reply(tid=1000)


if __name__ == "__main__":
    main()
