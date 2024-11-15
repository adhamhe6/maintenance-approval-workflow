# maintenance_approval_workflow/models/maintenance_request.py
from odoo import models, fields, api, exceptions

class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Request Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    request_date = fields.Datetime(string="Request Date", default=fields.Datetime.now, required=True)
    requested_by = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user, required=True)
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting for Approval'),
        ('approved_level_1', 'Approved Level 1'),
        ('approved_level_2', 'Approved Level 2'),
        ('approved', 'Fully Approved'),
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('rejected', 'Rejected')
    ], default='draft', string="Status", tracking=True)
    approval_level_1_user = fields.Many2one('res.users', string="Level 1 Approver")
    approval_level_2_user = fields.Many2one('res.users', string="Level 2 Approver")

    @api.model
    def create(self, vals):
        record = super(MaintenanceRequest, self).create(vals)
        record.message_subscribe(partner_ids=[record.requested_by.partner_id.id])
        return record

    def action_submit(self):
        self.state = 'waiting_approval'

    def action_approve_level_1(self):
        if self.env.user != self.approval_level_1_user:
            raise exceptions.UserError("Only Level 1 Approver can approve this request.")
        self.state = 'approved_level_1'

    def action_approve_level_2(self):
        if self.env.user != self.approval_level_2_user:
            raise exceptions.UserError("Only Level 2 Approver can approve this request.")
        self.state = 'approved_level_2'

    def action_fully_approve(self):
        self.state = 'approved'

    def action_schedule(self):
        self.state = 'scheduled'

    def action_done(self):
        self.state = 'done'

    def action_reject(self):
        self.state = 'rejected'
