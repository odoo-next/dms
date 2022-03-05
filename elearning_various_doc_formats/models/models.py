# -*- coding: utf-8 -*-


import base64
import datetime
import io
import re
import requests
import PyPDF2
import os
from PIL import Image
from werkzeug import urls
from pathlib import Path
from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import Warning, UserError, AccessError
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for

class SlideInherit(models.Model):
    _inherit = 'slide.slide'

    various_doc_formats = fields.Boolean(
        string='Various Doc Formats',
        required=False, default=False)

    datas = fields.Binary('Content', attachment=True)
    filename = fields.Char("Image Filename")

    @api.onchange('datas')
    def _on_change_datas(self):
        if self.datas:
            data = base64.b64decode(self.datas)
            if data.startswith(b'%PDF-'):
                pdf = PyPDF2.PdfFileReader(io.BytesIO(data), overwriteWarnings=False, strict=False)
                try:
                    pdf.getNumPages()
                except PyPDF2.utils.PdfReadError:
                    return
                self.completion_time = (5 * len(pdf.pages)) / 60



    @api.depends('document_id', 'slide_type', 'mime_type')
    def _compute_embed_code(self):
        base_url = request and request.httprequest.url_root
        for record in self:
            if not base_url:
                base_url = record.get_base_url()
            if base_url[-1] == '/':
                base_url = base_url[:-1]
            if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
                if not record.various_doc_formats:
                    slide_url = base_url + url_for('/slides/embed/%s?page=1' % record.id)
                    record.embed_code = '<iframe src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (slide_url, 315, 420)
                else:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    access_url = base_url +"/my/elearning/file/download/%s/%s" % (record.id,record.filename)
                    record.embed_code = '<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                        access_url, 315, 420)

            elif record.slide_type == 'video' and record.document_id:
                if not record.mime_type:
                    # embed youtube video
                    query = urls.url_parse(record.url).query
                    query = query + '&theme=light' if query else 'theme=light'
                    record.embed_code = '<iframe src="//www.youtube-nocookie.com/embed/%s?%s" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id, query)
                else:
                    # embed google doc video
                    record.embed_code = '<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id)
            else:
                record.embed_code = False