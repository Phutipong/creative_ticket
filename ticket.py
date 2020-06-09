# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Ticket(models.Model):
    _name = 'creative.ticket'
    _rec_name = 'ticket_no'
    ticket_no = fields.Char(string='Ticket No')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="ผู้จองรถ", required=True)
    sale_id = fields.Many2one('sale.order', ondelete='set null', string="Sale Order")
    sale_line_ids = fields.One2many('sale.order.line', string="SO Lines", related="sale_id.order_line")

    car_id = fields.Many2one('creative.car', ondelete='set null', string="รถที่ต้องการจอง", required=True)
    ticket_items = fields.One2many('creative.ticket_item', 'ticket_id', string="Ticket Items")
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approve'), ('complete', 'Complete')], default='draft')
    total_qty = fields.Integer("Total Qty", compute="get_sum_qty")
    total_amount = fields.Float("Total Amount", digits=(6, 2), compute="get_total_amount")
    total_discount = fields.Integer("Total Discount")
    job_no = fields.Char(string='JOB NO')

    _sql_constraints = [
        ('code_uniq', 'unique (job_no)', 'หมายเลข SO นี้มีการนำไปใช้งานแล้ว')
    ]

    purpose = fields.Boolean(string='รับ file งาน')
    send_job = fields.Boolean(string='ส่งงาน')
    send_proof = fields.Boolean(string='ส่ง Proof')
    receipt_cheques = fields.Boolean(string='การจองรถเพื่อรับเช็ค')
    bill_bill = fields.Boolean(string='วางบิล')
    purpose_other = fields.Char(string='อื่นๆ')
    car_other = fields.Char(string='รถรับจ้างภายนอก(ระบุประเภท)')
    customer_company = fields.Char(string='ลูกค้าบริษัท')
    contact_name = fields.Char(string='ชื่อผู้ติดต่อ')
    department = fields.Char(string='แผนก/ฝ่าย')
    tel = fields.Char(string='เบอร์ติดต่อ')
    location = fields.Char(string='สถานที่')
    date_time_delivery = fields.Datetime(string='เวลาที่จัดส่ง')
    note = fields.Text(string='หมายเหตุ')
    approver = fields.Char(string='ผู้อนุมัติ')

    @api.onchange('sale_id')
    def onchange_sale_id(self):
        self.job_no = self.sale_id.proj_id
        self.ticket_no = self.sale_id.name

    @api.onchange('ticket_items')
    def get_sum_qty(self):
        total_qty = 0
        for r in self:
            for item in r.ticket_items:
                total_qty += item.qty
        self.total_qty = total_qty

    @api.onchange('ticket_items')
    def get_total_amount(self):
        total_amount = 0
        for r in self:
            for item in r.ticket_items:
                total_amount += item.amount
        self.total_amount = total_amount - self.total_discount

    @api.one
    def do_ticket_draft(self):
        self.write({'state': 'draft'})

    @api.one
    def do_ticket_completed(self):
        self.write({'state': 'complete'})

    @api.onchange('total_discount')
    def update_discount(self):
        total_amount = 0
        for item in self.ticket_items:
            total_amount = total_amount + item.amount
            self.total_amount = total_amount - self.total_discount

    @api.multi
    def button_open_creative_ticket(self, context):
        external_web = self.env['invoice.external_web'].search([('active', '=', 1)])
        hostname = external_web.external_hostname
        refer_id = self.job_no

        url = "%sreport/sale/report_sale/rep_creative_ticket.jsp?prm_so=%s" % (hostname, refer_id)
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % (url),
            'target': 'new',
            # 'res_id': self.id,
        }

    @api.multi
    def button_open_head_delivery_form_one(self, context):
        external_web = self.env['invoice.external_web'].search([('active', '=', 1)])
        hostname = external_web.external_hostname
        refer_id = self.ticket_no

        url = "%sreport/sale/report_sale/rep_head_delivery_form_one.jsp?prm_so=%s" % (hostname, refer_id)
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % (url),
            'target': 'new',
            # 'res_id': self.id,
        }

    @api.multi
    def button_open_head_delivery_form_two(self, context):
        external_web = self.env['invoice.external_web'].search([('active', '=', 1)])
        hostname = external_web.external_hostname
        refer_id = self.ticket_no

        url = "%sreport/sale/report_sale/rep_head_delivery_form_two.jsp?prm_so=%s" % (hostname, refer_id)
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % (url),
            'target': 'new',
            # 'res_id': self.id,
        }

    @api.multi
    def button_open_delivery_form_one(self, context):
        external_web = self.env['invoice.external_web'].search([('active', '=', 1)])
        hostname = external_web.external_hostname
        refer_id = self.ticket_no

        url = "%sreport/sale/report_sale/rep_delivery_form_one.jsp?prm_so=%s" % (hostname, refer_id)
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % (url),
            'target': 'new',
            # 'res_id': self.id,
        }

    @api.multi
    def button_open_delivery_form_two(self, context):
        external_web = self.env['invoice.external_web'].search([('active', '=', 1)])
        hostname = external_web.external_hostname
        refer_id = self.ticket_no

        url = "%sreport/sale/report_sale/rep_delivery_form_two.jsp?prm_so=%s" % (hostname, refer_id)
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % (url),
            'target': 'new',
            # 'res_id': self.id,
        }

    # def sales_number_update(self):
    #     print ('reset_sale_order_number_successful')
    #     sequences = self.env['ir.sequence'].search([('code', '=', 'sale.order')])
    #     sequences.write({'number_next_actual': 1})


class TicketItem(models.Model):
    _name = 'creative.ticket_item'
    ticket_id = fields.Many2one('creative.ticket', ondelete='cascade', string="Ticket", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    ref_doc = fields.Char(string='Ref Doc')
    price = fields.Float(string='Price', digits=(6, 2))
    qty = fields.Integer(string='Qty')
    amount = fields.Float(string='Amount', digits=(6, 2))
    line_amount = fields.Float(string='Amount', readonly=True, stored=False)
    remark = fields.Text()

    @api.onchange('product_id')
    def get_product_price(self):
        self.price = self.product_id.lst_price
        # if self != null
        if not self.qty:
            self.qty = 1
        self.amount = self.price * self.qty

    # @api.multi
    @api.onchange('price', 'qty')
    def _price_changed(self):
        self.amount = self.price * self.qty
