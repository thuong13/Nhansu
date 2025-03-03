from odoo import models, fields, api

class DonVi(models.Model):
    _name = 'don_vi'
    _description = 'Quản lý đơn vị'
    _rec_name= 'ten_don_vi'
    ten_don_vi = fields.Char("Tên đơn vị")
    ma_don_vi = fields.Char("Mã đơn vị", required=True)
    
