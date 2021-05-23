from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from flectra import api, fields, models, tools, SUPERUSER_ID
from flectra.tools.translate import _
from flectra.tools import email_re, email_split
from flectra.exceptions import UserError, AccessError


AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Cold'),
    ('2', 'Medium'),
    ('3', 'Hot'),
]

class Lead(models.Model):
    _inherit = "crm.lead"

    date = fields.Date(string ='Date' , required=True)
    first_name = fields.Char(string ='First Name' , required=True)
    last_name = fields.Char(string ='Surname' , required=True)
    course =fields.Many2many( 'op.course' ,string='Courses')
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Entry Potential',required=True, index=True, default=AVAILABLE_PRIORITIES[0][0])
    programme_type = fields.Many2one(string= 'Interested Programme Type' , required=True)
    programme_name = fields.Many2one('op.course' , string='Specific programme of Interested')
    other_information = fields.Text(string= 'Any Specific Requirements')
    user_id = fields.Many2one(string='Admission Consultant' , required=True)
    medium_id = fields.Many2one(string='Entry Referal' , required=True)
    # medium_id = fields.Many2one(string='Entry Referal')
    # source_id = fields.Many2one(string='Entry Source')



    @api.multi
    def write(self,vals_list):
        if vals_list.get('stage_id'):
            stage = vals_list.get('stage_id')
            stage_name = self.env['crm.stage'].search([('id', '=', stage)]).name
            if stage_name == 'Qualified':
            
                self.ensure_one()
                ir_model_data = self.env['ir.model.data']
                try:
                    template_id = ir_model_data.get_object_reference('ric_crm', 'email_template_qualified_lead')[1]
                except ValueError:
                    template_id = False

                template = self.env['mail.template'].search([('id',  '=', template_id)])

                template.send_mail(self.id, force_send=True)          


        res = super(Lead, self).write(vals_list)    
        return res
    

    def action_email_send_contact(self):
    
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('ric_crm', "email_template_contact_lead")[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
        'default_model': 'crm.lead',
        'default_res_id': self.ids[0],
        'default_use_template': bool(template_id),
        'default_template_id': template_id,
        'default_composition_mode': 'comment',
        'mark_so_as_sent': True,
        'custom_layout': "sale.mail_template_data_notification_email_sale_order",
        'proforma': self.env.context.get('proforma', False),
        'force_email': True
        }
        return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id, 'form')],
        'view_id': compose_form_id,
        'target': 'new',
        'context': ctx,
        }
    
    