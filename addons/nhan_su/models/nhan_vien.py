from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    # _order= 'ten asc, tuoi desc'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_va_ten = fields.Char("Họ và tên", required=True)
    hinh_anh = fields.Binary("Hình ảnh")     #Thêm ảnh cho thông tin nhân viên
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    can_cuoc_cong_dan = fields.Char("CCCD",required=True)

    gioi_tinh = fields.Selection(
        [('nam', 'Nam',), ('nu', 'Nữ'),('chon gioi tinh', 'Chọn giới tính')],
        string="Giới tính",default='chon gioi tinh',
        required=True
    )
    email = fields.Char("Email", required=True)
    dc_tam_tru = fields.Char("Địa chỉ tạm trú", required=True)
    dc_thuong_tru = fields.Char("Địa chỉ thường trú", required=True)
    so_dien_thoai = fields.Char("Số điện thoại",required=True)
    don_vi = fields.Char("Đơn vị", required=True)
    chuc_vu = fields.Char("Chức vụ", required=True)

    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac",  # Model name
        "nhan_vien_id",      # Inverse field name in 'lich_su_cong_tac'
        string="Danh sách lịch sử công tác"
    )
    danh_muc_chung_chi_bang_cap_ids = fields.One2many(
        "danh_muc_chung_chi_bang_cap",  # Model name
        "chung_chi_id",      
        string="Danh mục chứng chỉ bằng cấp"
    )
 # Liên kết phòng ban
    phong_ban_id = fields.One2many(
        'phong_ban', 
        "nhan_vien_id", 
        string="Phòng ban") 
   
    # Liên kết với khóa học
    khoa_hoc_id = fields.Many2one(
        'khoa_hoc', 
        inverse_name = "nhan_vien_id", 
        string="Khóa học") 


    # Khóa học tham gia
    khoa_hoc_tham_gia_ids = fields.One2many("tham_gia_khoa_dao_tao", "nhan_vien_id", string="Khóa học tham gia")
    
    phieu_luong_ids = fields.One2many(
        'phieu_luong', 
        'nhan_vien_id',  
        string="Bảng lương"
    )

    hop_dong_ids = fields.One2many(
        'hr_contract', 
        'nhan_vien_id',  
        string="Bảng lương"
    )

    ky_luat_ids = fields.One2many(
        'ky_luat',  # Model name
        'nhan_vien_id',  # Inverse field in the 'ky_luat' model
        string="Kỷ luật"
    )

    khen_thuong_ids = fields.One2many(
        'khen_thuong',  
        'nhan_vien_id', 
        string="Khen thưởng"
    )

    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)

    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                today = date.today()
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0
    
    @api.constrains('ngay_sinh', 'tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")
    