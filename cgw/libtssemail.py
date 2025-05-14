# -*- coding: utf-8 -*-

import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders


class Smtp(object):
    def __init__(self, address, user, password, host, port, is_secure=True):
        self.address = address
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.is_secure = is_secure

    def test(self):
        try:
            smtp = smtplib.SMTP(self.host, self.port)
            if self.is_secure:
                smtp.ehlo()
                smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.quit()
            return ''
        except Exception as e:
            return str(e)

    def send(self, from_name, to_addrs, subj, text, html, images, files):
        msg = MIMEMultipart()
        msg['Subject'] = subj
        msg['From'] = '%s <%s>' % (from_name, self.address)
        msg['To'] = ', '.join(to_addrs)

        if len(text) != 0:
            msg.attach(MIMEText(text, _charset='utf-8'))

        if len(html) != 0:
            msg.attach(MIMEText(html, 'html', _charset='utf-8'))

        for fn in images:
            part = MIMEImage(file(fn, 'rb').read())
            part.add_header('Content-ID', '<{0}>'.format(os.path.basename(fn)))
            msg.attach(part)

        for fn in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file(fn, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(fn)))
            msg.attach(part)
        try:
            smtp = smtplib.SMTP(self.host, self.port)
            if self.is_secure:
                smtp.ehlo()
                smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.address, to_addrs, msg.as_string())
            smtp.quit()
            return ''
        except Exception as e:
            return str(e)
