# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Training(models.Model):
    _name = "hr.training"
    _description = "Training"

    name = fields.Char(string="Name")
    from_date = fields.Date(string="From Date")
    course_subject = fields.Char(string="Course Subject")
    to_date = fields.Date(string="To Date")
    status = fields.Selection([('start', 'To Start'),
                               ('running', 'Running'),
                               ('hold', 'Hold'),
                               ('cancel', 'Cancel'),
                               ('Done', 'Done')], default='start',
                              string="Status")
    employee_ids = fields.One2many('employee.training','hr_training_id', string="Employee")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)



class EmployeeTraining(models.Model):
    _name = "employee.training"
    _description = "Employee Training"

    name = fields.Char(string=" Course Name")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    hr_training_id = fields.Many2one("hr.training", string="Training Program")
    result = fields.Char(string='Result')
    from_date = fields.Date(string="From Date")
    course_subject = fields.Char(string="Course Subject", related='hr_training_id.course_subject')
    to_date = fields.Date(string="To Date")
    status = fields.Selection([('start', 'To Start'),
                               ('running', 'Running'),
                               ('hold', 'Hold'),
                               ('cancel', 'Cancel'),
                               ('Done', 'Done')], default='start',
                              string="Status")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)


class HREmployee(models.Model):
    _inherit = 'hr.employee'


    punish_ids = fields.One2many("employee.punish", "employee_id", string="????????????????")
    reward_ids = fields.One2many("employee.reward", "employee_id", string="????????????????")
    training_ids = fields.One2many("employee.training", "employee_id", string="Training")
    zmm_ids = fields.One2many("hr.zmm", "employee_id", string="Training")
    debit_account_id = fields.Many2one('account.account', string="Depit Account", required=True, )

    credit_account_id = fields.Many2one('account.account', string="Credit Account", required=True,)
    zmm_entry = fields.Many2one('account.move', string="?????? ??????????", readonly=True, copy=False, )
    def create_zmm_entry(self):
        summ = 0
        for zmm in self.zmm_ids:
            summ += zmm.amount

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'date':datetime.today().date(),
            'ref': '??????',
            'line_ids': [
                (0, 0, {
                    'account_id': self.debit_account_id.id,
                    #'currency_id': self.currency_data['currency'].id,
                    'debit': summ,
                    'credit': 0.0,
#                    'partner_id': self.partner_id.id,

                }),
                (0, 0, {
                    'account_id': self.credit_account_id.id,
                    # 'currency_id': self.currency_data['currency'].id,
                    'debit': 0.0,
                    'credit': summ,
                    #'partner_id': self.partner_id.id,
                }),

            ],
        })
        if move:
            self.zmm_entry = move.id

    latee = fields.Float(string="??????????????",  required=False, )
    early_leave = fields.Float(string="???????????? ???????????? ",  required=False, )
    days_latee = fields.Float(string="???????? ????????????",  required=False, )
    pre_job = fields.Char(string="Previous Job ", required=False, )



class HrZmm(models.Model):
    _name = 'hr.zmm'
    name = fields.Char("??????????")
    note = fields.Char("??????????????????")
    date = fields.Date(string="?????????? ??????????????????", required=False, )
    date_tasleem = fields.Date(string="?????????? ????????????????", required=False, )
    amount = fields.Float(string=" ????????????",  required=False, )
    employee_id = fields.Many2one("hr.employee", string="Employee")
