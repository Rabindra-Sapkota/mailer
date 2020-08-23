import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class Mailer:

    def __init__(self,mail_host, mail_port, mail_address, mail_password):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_address = mail_address
        self.mail_password = mail_password

    def send_mail(self, to_address, subject, body, body_args=None, cc=None, bcc=None, attachment=None, file_as_html=None, compression=None, password=None):
        self.msg = MIMEMultipart()
        self.msg['From'] = self.mail_address
        self.msg['To'] = to_address
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body, 'plain'))
        self.__compose_mail(to_address, subject, body)
        self.__deliver_mail(to_address)
        pass

    def __compose_mail(self, to, subject, body):
        pass

    def __deliver_mail(self,to_address):
        mail_session = smtplib.SMTP(self.mail_host, self.mail_port)
        mail_session.starttls()
        mail_session.login(self.mail_address, self.mail_password)
        mail_as_string = self.msg.as_string()
        mail_session.sendmail(self.mail_address, to_address, mail_as_string)
        # Put in try except and close the session even if exception arise
        mail_session.quit()
        print("Delivered")
        pass

my_mailer = Mailer('smtp.gmail.com','587','testrabindrasapkota@gmail.com','test@1234567890')
my_mailer.send_mail('rabindrasapkota2@gmail.com','Test Mail','Hello there')