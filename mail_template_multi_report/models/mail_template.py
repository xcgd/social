# © 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo import _, api, fields, models, exceptions
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat


class MailTemplate(models.Model):

    _inherit = "mail.template"

    report_line_ids = fields.One2many(
        comodel_name="mail.template.report.line",
        inverse_name="template_id",
        string="Other Reports",
    )

    def _patch_email_values(self, values, res_id, report_line):

        condition = report_line.condition

        if condition and condition.strip():
            condition_result = self.render_template(
                condition, self.model, res_id
            )

            if not condition_result or not safe_eval(condition_result):
                return values

        report_name = self.render_template(
            report_line.report_name, self.model, res_id
        )
        report = report_line.report_template_id
        report_service = report.report_name

        result, fmt = report.render([res_id])
        if result is None:
            raise exceptions.UserError(
                _("Unsupported report type %s found.")
                % report.report_type
            )
        result = base64.b64encode(result)

        if not report_name:
            report_name = "report." + report_service

        ext = "." + fmt
        if not report_name.endswith(ext):
            report_name += ext

        values.setdefault('attachments', [])
        values["attachments"].append((report_name, result))

        return values

    @api.multi
    def generate_email(self, res_ids, fields=None):
        results = super(MailTemplate, self).generate_email(
            res_ids, fields=fields
        )

        multi_mode = True
        if isinstance(res_ids, pycompat.integer_types):
            res_ids = [res_ids]
            multi_mode = False

        if multi_mode:
            for report_line in self.report_line_ids:
                for res_id, values in results.items():
                    results[res_id] = (
                        self._patch_email_values(values, res_id, report_line)
                    )
            return results

        for report_line in self.report_line_ids:
            results.update(
                self._patch_email_values(results, res_ids[0], report_line)
            )
        return results
