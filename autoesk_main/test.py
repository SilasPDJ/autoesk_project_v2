import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infternal.settings")
import django
django.setup()
from django.conf import settings
import dateutil.parser
import re
import requests
import json
from O365 import *
from sites.models import SiteData
from sites.models import Circuits, CircuitMaintenance
from home.models import MailTemplate, MailImages
from jinja2 import Template, Environment
from django.db.models import Q
from datetime import datetime, timedelta
from django.conf import settings
from StringIO import StringIO
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

env = Environment(autoescape=False, optimized=False)
template_data = MailTemplate.objects.get(pk=1)
mail_template = env.from_string(template_data.template)

template_file = StringIO()
mail_template.stream(
    StartDate   = '17/02/17 Midnight',
    EndDate     = '17/02/17 6 AM',
    Details     = 'Circuit maintenace on the cirasodasd asdas da a dskdka aks ada',
).dump(template_file)

content = template_file.getvalue()

# Define these once; use them twice!
strFrom = 'helpdesk@xxxxx.com'
strTo = 'alex@xxxx.com'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText(content, 'html')
msgAlternative.attach(msgText)
