import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.utils import make_msgid, formatdate


class Mailer:

    def __init__(self, mail_host, mail_port, mail_address, mail_password):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_address = mail_address
        self.mail_password = mail_password
        self.msg = MIMEMultipart()
        self.msg['Message-Id'] = make_msgid()
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['From'] = self.mail_address

    def send_mail(self, to_address, subject, mail_body, mail_body_args=None, mail_cc=None, mail_bcc=None, attachments=None,
                  file_as_html=None, compression=None, password=None):

        if mail_cc is None:
            mail_cc = []
        else:
            self.msg['cc'] = ', '.join(mail_cc)

        if mail_bcc is None:
            mail_bcc = []

        receiver_address = to_address + mail_cc + mail_bcc
        self.__data_assertion(to_address, mail_cc, mail_bcc, mail_body_args, subject, attachments)
        self.msg['To'] = ', '.join(to_address)
        self.msg['Subject'] = subject

        if body_args is None:
            self.msg.attach(MIMEText(mail_body, 'plain'))
        else:
            self.__compose_body(mail_body, mail_body_args)

        if attachments is not None:
            self.__attach_files(attachments)

        self.__deliver_mail(receiver_address)
        return

    def __data_assertion(self, to_address, mail_cc, mail_bcc, mail_body_args, subject, attachments):
        if not isinstance(to_address, list):
            raise TypeError('to_address should be of type list')
        if not isinstance(mail_cc, list):
            raise TypeError('mail_cc should be of type list')
        if not isinstance(mail_bcc, list):
            raise TypeError('mail_cc should be of type list')
        if not isinstance(mail_body_args, dict):
            raise TypeError('mail_body_args should be of type dictionary')
        if not isinstance(subject,str):
            raise TypeError('subject should be of type string')
        if attachments is not None and not isinstance(attachments, list):
            raise TypeError('attachments should be as type list of attachment file')

    def __compose_body(self, mail_body, mail_body_args):
        try:
            self.msg.attach(MIMEText(mail_body.format(**mail_body_args), 'plain'))
        except KeyError as e:
            raise ValueError('Parameter of mail_body not found in mail_body_args')
        return

    def __attach_files(self, attachments):
        def extract_file_name(path_of_file):
            regex_pattern = "[ \w-]+?(?=\.).*$"
            name_of_file = re.findall(regex_pattern, path_of_file)
            if len(name_of_file) != 1:
                raise ValueError('Invalid file_attachment')
            return ''.join(name_of_file)

        attachment_names = list(map(extract_file_name, attachments))
        for attachment_name, attachment_path in zip(attachment_names, attachments):
            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(open(attachment_path, "rb").read())
            encode_base64(payload)
            payload.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)
            self.msg.attach(payload)
        return

    def __deliver_mail(self, receiver_address):
        mail_session = smtplib.SMTP(self.mail_host, self.mail_port)
        mail_session.starttls()
        mail_session.login(self.mail_address, self.mail_password)
        mail_as_string = self.msg.as_string()
        mail_session.sendmail(self.mail_address, receiver_address, mail_as_string)
        mail_session.quit()
        print("Delivered")
        return

my_mailer = Mailer('smtp.gmail.com', '587', 'testrabindrasapkota@gmail.com', 'test@1234567890')
body = '''
Dear {RECEIVER},

How are you? I Hope you are fine.

With Regards,
{SENDER}
'''
body_args = {'RECEIVER': 'RabindraR', 'SENDER': 'RabindraS'}
attachment = ['C:/Users/rabindra/Desktop/image.jpg', 'C:/Users/rabindra/Desktop/SnapShotTestOnCluster.pdf']
my_mailer.send_mail(['071bex429@ioe.edu.np'], 'TestUltimate', body, mail_body_args=body_args,
                    attachments=attachment, mail_cc=['rabindrasapkota2@gmail.com'], mail_bcc=['rabindra.sapkota@esewa.com.np'])