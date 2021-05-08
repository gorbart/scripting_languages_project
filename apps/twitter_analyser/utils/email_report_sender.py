import datetime

from django.core.mail import EmailMessage
from django.template import loader


class EmailReportSender:
    """
    EmailReportSender is used for sending reports about current webapp state (currently displayed most popular hashtags
    in the world and most popular tweets for given hashtag and profile).
    """

    @staticmethod
    def send_report(context, message_path='twitter_analyser/email.html', subject="Report for {} concerning {}"):
        """
        send_report uses Django SMTP mailing to send email to a given app user containing currently displayed most
        popular hashtags in the world and most popular tweets for given hashtag and profile
        :param context: dictionary containing current webpage context - variables needed to prepare email template for
        sending: user (passed to template but also giving receiver email address), trending hashtags, current date,
        current hashtag, hashtags tweets, current profile and profiles tweets
        :param message_path: path to email HTML template - default is "twitter_analyser/email.html"
        :param subject: subject of email - default is "Report for {} concerning {}" with two empty spaces to format in
        user's username and date, for which the report is generated
        """

        if not context['current_date']:
            context['current_date'] = datetime.datetime.now().date()
        else:
            context['current_date'] = context['current_date'].date()

        subject_final = subject.format(context['user'].username, context['current_date'])
        message_final = loader.render_to_string(message_path, context)

        msg = EmailMessage(subject_final, message_final, to=[context['user'].email])
        msg.content_subtype = 'html'
        msg.send()
