from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KhenThuong(models.Model):
    _name = 'khen_thuong'
    _description = 'Quản lý khen thưởng cho nhân viên'
    _rec_name='ten_khen_thuong'

    ten_khen_thuong = fields.Char("Tên khen thưởng", required=True)  # Tên khen thưởng
    mo_ta = fields.Text("Mô tả khen thưởng")  # Mô tả về khen thưởng
    loai_khen = fields.Selection([
        ('bonus', 'Thưởng tiền'),  # Thưởng tiền
        ('certificate', 'Chứng chỉ'),  # Thưởng chứng chỉ
        ('promotion', 'Thăng chức'),  # Thưởng thăng chức
        ('other', 'Khác')  # Các loại khen thưởng khác
    ], string="Loại khen thưởng", required=True)  # Loại khen thưởng
    so_tien = fields.Float("Số tiền thưởng", default=0.0)  # Số tiền thưởng
    ngay = fields.Date("Ngày khen thưởng", default=fields.Date.today())  # Ngày khen thưởng
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)  # Liên kết với bảng nhân viên
    trang_thai = fields.Boolean("Hoạt động", default=True)  # Trạng thái khen thưởng

    @api.model
    def create_khen_thuong(self, nhan_vien_id, ten_khen_thuong, loai_khen, so_tien):
        """Tạo khen thưởng cho nhân viên"""
        if so_tien <= 0 and loai_khen == 'bonus':
            raise ValidationError("Số tiền thưởng phải lớn hơn 0 nếu loại khen thưởng là 'Thưởng tiền'")
        
        khen_thuong = self.create({
            'ten_khen_thuong': ten_khen_thuong,  # Tên khen thưởng
            'loai_khen': loai_khen,  # Loại khen thưởng
            'so_tien': so_tien,  # Số tiền thưởng
            'nhan_vien_id': nhan_vien_id,  # Nhân viên nhận khen thưởng
            'ngay': fields.Date.today(),  # Ngày khen thưởng
            'trang_thai': True  # Khen thưởng đang hoạt động
        })
        return khen_thuong
