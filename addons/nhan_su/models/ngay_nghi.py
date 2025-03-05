from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NgayNghi(models.Model):
    _name = 'ngay_nghi'
    _description = 'Quản lý ngày nghỉ của công ty và nhân viên'

    ten = fields.Char("Tên ngày nghỉ", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", help="Bỏ trống nếu là ngày nghỉ chung của công ty")
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc", required=True)
    
    loai_nghi = fields.Selection([
        ('le', 'Nghỉ lễ công ty'),
        ('phep', 'Nghỉ phép cá nhân'),
        ('om', 'Nghỉ ốm'),
        ('khac', 'Khác')
    ], string="Loại nghỉ", required=True)
    
    ly_do = fields.Text("Lý do")
    
    trang_thai = fields.Selection([
        ('tu_dong', 'Ngày nghỉ chung'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái", default='tu_dong', required=True)

    so_ngay = fields.Integer("Số ngày nghỉ", compute="_compute_so_ngay", store=True)


    @api.depends('ngay_bat_dau', 'ngay_ket_thuc', 'trang_thai')
    def _compute_so_ngay(self):
        for record in self:
            if record.trang_thai == 'da_duyet':  # Chỉ tính nếu đã duyệt
                if record.ngay_bat_dau and record.ngay_ket_thuc:
                    record.so_ngay = (record.ngay_ket_thuc - record.ngay_bat_dau).days + 1
                else:
                    record.so_ngay = 0
            else:
                record.so_ngay = 0  # Không tính nếu chưa duyệt hoặc bị từ chối


    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _kiem_tra_ngay_nghi(self):
        for record in self:
            if record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError("Ngày bắt đầu không được lớn hơn ngày kết thúc!")
