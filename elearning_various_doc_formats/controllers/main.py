# Copyright 2017-2019 MuK IT GmbH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import OR

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.main import content_disposition, ensure_db

class ContentController(http.Controller):

    @http.route(
        ["/my/elearning/file/download/<string:id>/<string:name>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_elearning_file_download(self,id, name,  **kw):
        """Process user's consent acceptance or rejection."""
        ensure_db()
        # operations
        res = request.env["dms.file"].sudo().search([('id','=',int(id)),('name','=',name)], limit = 1)


        dms_file_sudo = res
        # It's necessary to prevent AccessError in ir_attachment .check() function
        if dms_file_sudo.attachment_id and request.env.user.has_group(
                "base.group_portal"
        ):
            dms_file_sudo = dms_file_sudo.sudo()
        filecontent = base64.b64decode(dms_file_sudo.content)
        content_type = ["Content-Type", "application/octet-stream"]
        disposition_content = [
            "Content-Disposition",
            content_disposition(dms_file_sudo.name),
        ]
        return request.make_response(filecontent, [content_type, disposition_content])
