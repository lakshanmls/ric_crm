{
    'name': 'RIC CRM',
    'version': '1.0.0',
    'author' : 'Lakshan Eranga,Thisura Weerakkody',
    'category': 'Extra tools',
    'sequence': '38',
    'summary': 'FOR CRM of Royal Institute College Lead Process',
    'description': 'System for Customer Management',
    'depends': [ 'base','crm'],
                 
    'data': [ 
        'data/mail_template.xml',

        'views/lead.xml',
        'views/course.xml',                  
    ],
    'demo': [],

'installable': True,
'application': True,
'auto_install': False,
}