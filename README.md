# Mailer
UtilityForHandlingMails

Example

from mailer import mailer

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
                    attachments=attachment, mail_cc=['rabindrasapkota2@gmail.com'],
                    mail_bcc=['testrabindrasapkota@esewa.com'])
