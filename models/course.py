from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from flectra import api, fields, models, tools, SUPERUSER_ID
from flectra.tools.translate import _
from flectra.tools import email_re, email_split
from flectra.exceptions import UserError, AccessError


class Course(models.Model):
    _inherit = "op.course"

    description = fields.Text(string ='Description' , required=True)