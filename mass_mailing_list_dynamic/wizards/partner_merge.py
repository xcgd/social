# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    @api.model
    def _merge_mass_mailing_contacts(self, src_partners, dst_partner):

        src_contacts = self.env["mail.mass_mailing.contact"].search(
            [("partner_id", "in", src_partners.ids)]
        )
        dst_contact = dst_partner.mass_mailing_contact_ids.with_context(
            bypass_dynamic_list_check=True
        )

        dst_contact.list_ids = [
            (4, mailing_list.id) for mailing_list in src_contacts.list_ids
        ]
        src_contacts.unlink()

        return True

    @api.model
    def _update_foreign_keys(self, src_partners, dst_partner):

        self._merge_mass_mailing_contacts(src_partners, dst_partner)

        return super(
            BasePartnerMergeAutomaticWizard, self
        )._update_foreign_keys(src_partners, dst_partner)

    def _merge(self, partner_ids, dst_partner=None):
        return super(
            BasePartnerMergeAutomaticWizard,
            self.with_context(bypass_dynamic_list_check=True),
        )._merge(partner_ids=partner_ids, dst_partner=dst_partner)
