# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class Survey(models.Model):
    _inherit = 'survey.survey'

    allow_duplicates = fields.Boolean(
        "Allow users to give multiple Responses",
        default=True
    )


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    @api.multi
    @api.constrains('user_input_id')
    def _check_allow_duplicates(self):
        for record in self:
            if record.survey_id and not record.survey_id.allow_duplicates:
                existing = self.env['survey.user_input_line'].search([
                    ('id', '!=', record.id),
                    ('question_id', '=', record.question_id.id),
                    ('user_input_id.create_uid', '=', self.env.uid)
                ])
                if len(existing) > 0:
                    raise ValidationError(_('duplicate_answer'))
