from odoo import models, fields, api

class DanhMucChungChiBangCap(models.Model):
    _name = "danh_muc_chung_chi_bang_cap"
    _description = 'Danh mục chứng chỉ bằng cấp'
    _rec_name = 'ten_chung_chi'

    ten_chung_chi = fields.Char("Tên chứng chỉ",required=True)
    loai_bang = fields.Char ("Loại",required=True)
    ngay_cap = fields.Date("Ngày cấp",required=True)
    noi_cap = fields.Char("Nơi cấp",required=True)
    loai_bang_cap = fields.Selection(
        [
            ("dai_hoc", "Bằng đại học"),
            ("cao_dang", "Bằng cao đẳng"),
            ("trung_cap", "Bằng trung cấp"),
            ("chung_chi", "Chứng chỉ")
        ],
        string="Loại Bằng Cấp",default="Bằng đại học"
    )
    chung_chi_id = fields.Many2one("nhan_vien", string="Nhân viên")
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")
    ma_dinh_danh=fields.Char("Mã định danh",related='chung_chi_id.ma_dinh_danh')
    tuoi=fields.Integer("Tuổi",related='nhan_vien_id.tuoi')