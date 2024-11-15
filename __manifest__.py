# maintenance_approval_workflow/__manifest__.py
{
    'name': 'Maintenance Approval Workflow',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': 'Your Name',
    'description': 'A multi-level approval workflow for maintenance requests.',
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',
    ],
    'application': True,
}
