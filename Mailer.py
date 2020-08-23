import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64


class Mailer:

    def __init__(self, mail_host, mail_port, mail_address, mail_password):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_address = mail_address
        self.mail_password = mail_password
        self.msg = MIMEMultipart()

    def send_mail(self, to_address, subject, mail_body, mail_body_args=None, mail_cc=None, mail_bcc=None, attachments=None,
                  file_as_html=None, compression=None, password=None):
        self.msg['From'] = self.mail_address
        self.msg['To'] = ', '.join(to_address)
        self.msg['Subject'] = subject

        if mail_cc is not None:
            self.msg['cc'] = ', '.join(mail_cc)

        if attachments is not None:
            self.__attach_files(attachments)

        if body_args is None:
            self.msg.attach(MIMEText(mail_body, 'plain'))
        else:
            self.__compose_body(mail_body, mail_body_args)

        self.__deliver_mail(to_address, mail_cc, mail_bcc)
        return

    def __compose_body(self, mail_body, mail_body_args):
        # Template key should be on dictionary key so handle exception here
        self.msg.attach(MIMEText(mail_body.format(**mail_body_args), 'plain'))
        return

    def __attach_files(self, attachments):
        # Handle for file not found
        # Attachment has to be as string or list of string
        def extract_file_name(path_of_file):
            regex_pattern = "[ \w-]+?(?=\.).*$"
            name_of_file = re.findall(regex_pattern, path_of_file)
            # Assert only one file name is matched in path_of_file
            return ''.join(name_of_file)

        attachment_names = list(map(extract_file_name, attachments))
        for attachment_name, attachment_path in zip(attachment_names, attachments):
            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(open(attachment_path, "rb").read())
            encode_base64(payload)
            payload.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)
            self.msg.attach(payload)
        return

    def __deliver_mail(self, to_address, mail_cc, mail_bcc):
        mail_session = smtplib.SMTP(self.mail_host, self.mail_port)
        mail_session.starttls()
        mail_session.login(self.mail_address, self.mail_password)
        mail_as_string = self.msg.as_string()

        if mail_cc is None:
            mail_cc = []

        if mail_bcc is None:
            mail_bcc = []

        mail_session.sendmail(self.mail_address, to_address + mail_cc + mail_bcc, mail_as_string)
        # Put in try except and close the session even if exception arise
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
my_mailer.send_mail(['rabindrasapkota2@gmail.com'], 'BCC Test', body, mail_body_args=body_args,
                    attachments=attachment, mail_cc=['071bex429@ioe.edu.np'], mail_bcc=['rabindra.sapkota@esewa.com.np'])