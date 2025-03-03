from odoo import models, fields, api
class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Quản lý chức vụ'
    _rec_name = 'ten_chuc_vu'
    ten_chuc_vu = fields.Char("Tên chức vụ")
    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    
