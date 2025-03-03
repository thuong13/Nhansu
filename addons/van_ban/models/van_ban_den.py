from odoo import models, fields

class VanBanDen(models.Model):
    _name = "van_ban_den"
    _description = "Quản lý Văn Bản Đến"
    _rec_name = "ten_vb"

    ten_vb = fields.Char(string="Tên Văn Bản", required=True)
    so_vb_den = fields.Char(string="Số Văn Bản Đến", required=True)
    noi_den = fields.Char(string="Nơi Đến", required=True)
    ngay_nhan = fields.Date(string="Ngày Nhận")

    muc_do = fields.Selection([
        ('hoa_toc', 'Hỏa tốc'),
        ('thuong_khan', 'Thượng khẩn'),
        ('khan', 'Khẩn'),
    ], string="Mức độ khẩn", default="binh_thuong")
    # Quan hệ với Văn Bản Đi (One2many)
    loai_van_ban_id = fields.Many2one("loai_van_ban", string = "Loại văn bản", required = True)
    