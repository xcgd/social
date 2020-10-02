from odoo import api, models


class MailThread(models.AbstractModel):
    """Override to:
    - Update the cache, after the execution of the modifications in email
    sending and mail thread management added by this module.
    """

    _inherit = "mail.thread"

    @api.multi
    def message_post(
        self,
        body="",
        subject=None,
        message_type="notification",
        subtype=None,
        parent_id=False,
        attachments=None,
        content_subtype="html",
        **kwargs
    ):
        """Override to:
        - Update the cache, after the execution of the modifications in email
        sending and mail thread management added by this module.
        """

        result = super(MailThread, self).message_post(
            body=body,
            subject=subject,
            message_type=message_type,
            subtype=subtype,
            parent_id=parent_id,
            attachments=attachments,
            content_subtype=content_subtype,
            **kwargs
        )

        # Update the cache, after the execution of the modifications in email
        # sending and mail thread management added by this module.
        self.refresh()

        return result
