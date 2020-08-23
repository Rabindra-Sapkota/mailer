# Mailer
Utility For Handling Mails

It can be send simple plain mail, send mail accroding to body template, mail with attachments.

We can include cc and bcc email addresses to the mail

Can be installed fro pypi with pip install mailerpy

# Example

from mailerpy import Mailer

my_mailer = Mailer('smtp.gmail.com', '587', 'testrabindrasapkota@gmail.com', 'test@1234567890')

body = '''

Dear {RECEIVER},

How are you? I Hope you are fine.

With Regards,

{SENDER}

'''

body_args = {'RECEIVER': 'Sir', 'SENDER': 'Rabindra Sapkota'}

attachment = ['C:/Users/rabindra/Desktop/image.jpg', 'C:/Users/rabindra/Desktop/SnapShotTestOnCluster.pdf']

my_mailer.send_mail(['071bex429@ioe.edu.np'], 'Test Mail', body, mail_body_args=body_args,
                    attachments=attachment, mail_cc=['rabindrasapkota2@gmail.com'],
                    mail_bcc=['testrabindrasapkota@esewa.com'])
