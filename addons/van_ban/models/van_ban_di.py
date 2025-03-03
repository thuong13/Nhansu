from odoo import models, fields

class VanBanDi(models.Model):
    _name = "van_ban_di"
    _description = "Quản lý Văn Bản Đi"
    _rec_name = "ten_vb"

    ten_vb = fields.Char(string="Tên Văn Bản", required=True)
    so_hieu_vb = fields.Char(string="Số Hiệu Văn Bản", required=True)
    so_vb = fields.Integer(string="Số Văn Bản")
    noi_nhan = fields.Char(string="Nơi Nhận", required=True)
    ngay_gui = fields.Date(string="Ngày Gửi")

    muc_do = fields.Selection([
        ('hoa_toc', 'Hỏa tốc'),
        ('thuong_khan', 'Thượng khẩn'),
        ('khan', 'Khẩn'),
    ], string="Mức độ khẩn", default="binh_thuong")
    # Quan hệ với Văn Bản Đến (Many2one)
    loai_van_ban_id = fields.Many2one("loai_van_ban", string = "Loại văn bản", required = True)