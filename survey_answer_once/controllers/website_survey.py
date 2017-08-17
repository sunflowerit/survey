# -*- coding: utf-8 -*-
# © 2017 Sunflower IT (http://sunflowerweb.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import openerp.addons.survey.controllers.main as main
from openerp.addons.web import http
from openerp.exceptions import ValidationError


class WebsiteSurveyExtension(main.WebsiteSurvey):

    @http.route(['/survey/already.answered', '/survey/already-answered'],
                type='http', auth="public", website=True)
    def already_answered(self, **kwargs):
        return http.request.website.render(
            "survey_answer_once.duplicatesurvey")

    @http.route(['/survey/submit/<model("survey.survey"):survey>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, survey, **post):
        try:
            return super(WebsiteSurveyExtension, self).submit(survey, **post)
        except ValidationError as e:
            if len(e.args) <= 1 or e.args[1] != 'duplicate_answer':
                raise
            return json.dumps(dict(redirect='/survey/already-answered'))
