# -*- coding: utf-8 -*-
{
    'name': "eLearning Office Doc Formats",

    'summary': """eLearning Office Doc Formats""",

    'description': """
       eLearning Various Doc Format
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Blog',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_slides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

       'views/slide_slide.xml',

    ],
    # only loaded in demonstration mode

}