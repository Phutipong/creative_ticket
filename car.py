# -*- coding: utf-8 -*-
from odoo import models, api, fields, osv
from datetime import datetime


class Car(models.Model):
    _name = 'creative.car'
    _rec_name = 'name'
    _order = 'name'
    image = fields.Binary("Image", attachment=True)
    name = fields.Char(string='Name', required=True, help="Enter a car name")
    model = fields.Char(string='Model')
    reg_id = fields.Char(string='Reg ID')
    driver_name = fields.Char(string='Driver Name')
    type = fields.Selection([('S', 'รถเก๋ง'), ('T', 'รถบรรทุก')], string='Type', default='S')
    year = fields.Char(string='Year')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    total_day = fields.Integer(string='Total Days', readonly=True, compute="get_total_days")

    @api.depends('start_time', 'end_time')
    def get_total_days(self):
        if self.start_time and self.end_time:
            start_time = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(self.end_time, '%Y-%m-%d %H:%M:%S')
            self.total_day = (end_time - start_time).days

            # start_time = fields.Datetime.from_string(self.start_time)
            # end_time = fields.Datetime.from_string(self.end_time)
            # self.total_day = (end_time - start_time).seconds / 3600
