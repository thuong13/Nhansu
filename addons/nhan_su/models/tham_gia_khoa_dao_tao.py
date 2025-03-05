from odoo import models, fields, api

class ThamGiaKhoaDaoTao(models.Model):
    _name = 'tham_gia_khoa_dao_tao'
    _description = 'Danh sách tham gia khóa đào tạo'

    ma_khoa_hoc = fields.Many2one(
        "khoa_hoc",
        string="Khóa học",
        required=True,
        ondelete="cascade"
    )

    nhan_vien_id = fields.Many2one(
        "nhan_vien",
        string="Nhân viên",
        required=True,
        ondelete="cascade"
    )

    vai_tro = fields.Selection(
        [("trainer", "Người đào tạo"), ("student", "Học viên")],
        string="Vai trò",
        required=True
    )

    ngay_tham_gia = fields.Date(
        string="Ngày tham gia",
        default=fields.Date.today
    )

    trang_thai = fields.Selection(
        [
            ("dang_hoc", "Đang học"),
            ("hoan_thanh", "Hoàn thành"),
            ("huy_bo", "Hủy bỏ")
        ],
        string="Trạng thái",
        default="dang_hoc"
    )

    _sql_constraints = [
        ('unique_participation', 'UNIQUE(ma_khoa_hoc, nhan_vien_id)', 
         'Nhân viên đã tham gia khóa học này!')
    ]