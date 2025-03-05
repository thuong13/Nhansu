from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KyLuat(models.Model):
    _name = 'ky_luat'
    _description = 'Quản lý kỷ luật cho nhân viên'
    _rec_name='ten_vi_pham'

    ten_vi_pham = fields.Char("Tên vi phạm", required=True)  # Tên vi phạm kỷ luật
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    mo_ta = fields.Text("Mô tả vi phạm")  # Mô tả về vi phạm
    loai_vi_pham = fields.Selection([
        ('đi trễ', 'Đi trễ'),  # Đi trễ
        ('Lơ là công việc', 'Lơ là công việc'),  # Lơ là công việc
        ('Quấy rối', 'Quấy rối'),  # Quấy rối
        ('khác', 'Khác')  # Các loại vi phạm khác
    ], string="Loại vi phạm", required=True)  # Loại vi phạm kỷ luật
    phat_tien = fields.Float("Số tiền phạt", default=0.0)  # Số tiền phạt (nếu có)
    ngay_vi_pham = fields.Date("Ngày vi phạm", default=fields.Date.today())  # Ngày vi phạm
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)  # Liên kết với bảng nhân viên
    trang_thai = fields.Selection([
        ('chờ xử lý', 'Chờ xử lý'),  # Chờ xử lý
        ('đã xử lý', 'Đã xử lý'),  # Đã xử lý
        ('hủy bỏ', 'Hủy bỏ')  # Hủy bỏ
    ], string="Trạng thái", default='chờ xử lý', required=True)  # Trạng thái kỷ luật
    note = fields.Text("Ghi chú")  # Ghi chú về quyết định xử lý kỷ luật

    @api.model
    def create_ky_luat(self, nhan_vien_id, ten_vi_pham, loai_vi_pham, phat_tien, note=''):
        """Tạo kỷ luật cho nhân viên"""
        ky_luat = self.create({
            'ten_vi_pham': ten_vi_pham,  # Tên vi phạm
            'loai_vi_pham': loai_vi_pham,  # Loại vi phạm
            'phat_tien': phat_tien,  # Số tiền phạt
            'nhan_vien_id': nhan_vien_id,  # Nhân viên vi phạm
            'ngay_vi_pham': fields.Date.today(),  # Ngày vi phạm
            'trang_thai': 'chờ xử lý',  # Kỷ luật đang chờ xử lý
            'note': note  # Ghi chú (nếu có)
        })
        return ky_luat

    def xu_ly_ky_luat(self, trang_thai, note=''):
        """Cập nhật trạng thái xử lý kỷ luật"""
        if trang_thai == 'đã xử lý' and not note:
            raise ValidationError("Cần ghi chú lý do xử lý kỷ luật.")
        self.write({
            'trang_thai': trang_thai,
            'note': note
        })

    @api.constrains('phat_tien')
    def _check_phat_tien(self):
        """Kiểm tra số tiền phạt phải hợp lý"""
        for record in self:
            if record.phat_tien < 0:
                raise ValidationError("Số tiền phạt không thể nhỏ hơn 0.")
