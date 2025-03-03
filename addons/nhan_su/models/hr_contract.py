from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrContract(models.Model):
    _name = "hr_contract"
    _description = "Hợp đồng nhân viên"
    _order = "ngay_bat_dau desc"

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete="cascade")
    loai_hop_dong = fields.Selection([
        ('full_time', 'Toàn thời gian'),
        ('internship', 'Thực tập'),
        ('freelance', 'Hợp đồng thời vụ')
    ], string="Loại hợp đồng", required=True)

    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, default=fields.Date.context_today)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=False)
    luong_hop_dong = fields.Float(string="Lương hợp đồng", required=True)

    status = fields.Selection([
        ('active', 'Đang hiệu lực'),
        ('expired', 'Hết hạn'),
        ('terminated', 'Đã chấm dứt')
    ], string="Trạng thái", default='active')

    note = fields.Text(string="Ghi chú")

    # Trường cho phép nhập ngày gia hạn mới
    ngay_gia_han_moi = fields.Date(string="Ngày gia hạn mới")

    def action_terminate(self):
        """ Chấm dứt hợp đồng """
        self.write({'status': 'terminated'})

    def action_renew(self):
        """ Gia hạn hợp đồng """
        # Lấy giá trị ngày gia hạn từ trường nhập liệu
        new_date_end = self.ngay_gia_han_moi or self.ngay_ket_thuc

        if not new_date_end:
            raise ValidationError("Vui lòng chọn ngày gia hạn mới.")

        if new_date_end < fields.Date.today():
            raise ValidationError("Ngày gia hạn phải lớn hơn ngày hiện tại.")

        # Cập nhật ngày kết thúc hợp đồng và trạng thái
        self.write({'ngay_ket_thuc': new_date_end, 'status': 'active'})
