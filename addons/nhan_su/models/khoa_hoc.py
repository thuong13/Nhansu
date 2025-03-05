from odoo import models, fields, api

class KhoaHoc(models.Model):
    _name = 'khoa_hoc'
    _description = 'Bảng chứa danh sách các khóa học'
    _rec_name = 'ten_khoa_hoc'

    ma_khoa_hoc = fields.Char("Mã khóa học", required=True)
    ten_khoa_hoc = fields.Char("Tên khóa học", required=True)
    mo_ta_khoa_hoc = fields.Text("Mô tả khóa học", required=True)
    ke_hoach_giang_day = fields.Text("Kế hoạch giảng dạy", required=True)
    
    loai_khoa_hoc = fields.Selection(
        [
            ("Chuyenmon", "Kỹ năng chuyên môn"),
            ("mem", "Kỹ năng mềm"),
            ("Noibo&Hoinhap", "Đào tạo nội bộ & Hội nhập"),
            ("Lanhdao&Quanly", "Đào tạo lãnh đạo và quản lý")
        ],
        string="Loại khóa học",
        default="Chuyenmon"
    )

    # Người đào tạo (Tính toán từ danh sách tham gia)
    nguoi_dao_tao = fields.Many2one(
        'nhan_vien', 
        string="Người đào tạo",
        compute="_compute_nguoi_dao_tao",
        store=True
    )

    # Danh sách nhân viên tham gia khóa học (One2many)
    tham_gia_ids = fields.One2many(
        "tham_gia_khoa_dao_tao",
        "ma_khoa_hoc",
        string="Danh sách tham gia"
    )

    # Số lượng nhân viên (Chỉ đếm học viên)
    so_luong_nhan_vien = fields.Integer(
        string="Số lượng học viên",
        compute="_compute_so_luong_nhan_vien",
        store=True
    )

    @api.depends('tham_gia_ids.vai_tro')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = sum(1 for t in record.tham_gia_ids if t.vai_tro == 'student')

    @api.depends('tham_gia_ids')
    def _compute_nguoi_dao_tao(self):
        for record in self:
            trainer = next((t.nhan_vien_id for t in record.tham_gia_ids if t.vai_tro == 'trainer'), False)
            record.nguoi_dao_tao = trainer
