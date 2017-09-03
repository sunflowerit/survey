# -*- coding: utf-8 -*-
import logging

from openerp import SUPERUSER_ID, fields, models, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


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
            partner_id = self.env.user.partner_id.id
            question_id = record.question_id.id
            _logger.info(
                _("User '%s' (%d, partner %d) filled survey %d question %d"),
                self.env.user.name,
                self.env.uid,
                partner_id,
                record.survey_id.id,
                question_id
            )
            if record.survey_id.allow_duplicates:
                _logger.info(
                    _('Allowing, because survey allows duplicate answers'))
            else:
                if self.env.uid == SUPERUSER_ID:
                    alt_partner_id = record.user_input_id.partner_id.id
                    if alt_partner_id and alt_partner_id != partner_id:
                        partner_id = alt_partner_id
                        _logger.info(
                            _("User input object says this is user with partner id %d"),
                            partner_id
                        )
                    else:
                        _logger.info(
                            _('Disallowing, because we cannot check duplicates.'))
                        raise ValidationError(_('disallow_invite'))
                existing = self.env['survey.user_input_line'].search([
                    ('id', '!=', record.id),
                    ('question_id', '=', question_id),
                    ('user_input_id.partner_id', '=', partner_id)
                ])
                if not existing:
                    _logger.info(
                        _('Allowing, because we found no existing answers.'))
                else:
                    _logger.info(
                        _('Disallowing, because we found existing answers.'))
                    raise ValidationError(_('duplicate_answer'))
