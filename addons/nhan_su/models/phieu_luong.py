# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class PhieuLuong(models.Model):
    _name = 'phieu_luong'
    _description = 'Phiếu Lương Nhân Viên'
    _order = "nam desc, ngay_bat_dau desc"

    ten_phieu = fields.Char(string='Mã Phiếu Lương', required=True, copy=False, readonly=True, index=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete="cascade")

    # Thêm trường năm, ngày bắt đầu và ngày kết thúc
    nam = fields.Integer(string="Năm", compute="_compute_nam", store=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu kỳ lương", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc kỳ lương", required=True)
    
    thang = fields.Selection([
        ('01', 'Tháng 01'), ('02', 'Tháng 02'), ('03', 'Tháng 03'),
        ('04', 'Tháng 04'), ('05', 'Tháng 05'), ('06', 'Tháng 06'),
        ('07', 'Tháng 07'), ('08', 'Tháng 08'), ('09', 'Tháng 09'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng hành chính", default='01')

    # Các khoản thu nhập
    luong_co_ban = fields.Float(string="Lương cơ bản", required=True, default=0.0)
    thuong = fields.Float(string="Thưởng", default=0.0)
    phu_cap_xang_xe = fields.Float(string="Phụ cấp xăng xe", default=0.0)
    phu_cap_an_trua = fields.Float(string="Phụ cấp ăn trưa", default=0.0)
    phu_cap_dien_thoai = fields.Float(string="Phụ cấp điện thoại", default=0.0)
    phu_cap_khac = fields.Float(string="Phụ cấp khác", default=0.0)
    phat = fields.Float(string="Phạt", default=0.0)

    # Thông tin công việc
    ngay_nghi = fields.Integer(string="Ngày nghỉ", default=0)
    ngay_cong_thuc_te = fields.Integer(string="Ngày công thực tế", compute="_compute_ngay_cong", store=True)
    gio_lam_them = fields.Float(string="Giờ làm thêm", default=0.0)
    luong_lam_them = fields.Float(string="Lương làm thêm", compute="_compute_luong_lam_them", store=True)

    # Bảo hiểm và thuế
    bhxh = fields.Float(string="BHXH", compute="_compute_bao_hiem", store=True)
    bhyt = fields.Float(string="BHYT", compute="_compute_bao_hiem", store=True)
    bhtn = fields.Float(string="BHTN", compute="_compute_bao_hiem", store=True)
    thue_tncn = fields.Float(string="Thuế TNCN", compute="_compute_thue", store=True)
    khau_tru_khac = fields.Float(string="Khấu trừ khác", default=0.0)

    # Tổng lương thực nhận
    tong_luong = fields.Float(string="Tổng lương", compute="_compute_salary", store=True)

    # Trạng thái phiếu lương
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='cho_duyet', track_visibility='onchange')

    hop_dong_id = fields.Many2one('hr_contract', string="Hợp đồng", compute="_compute_hop_dong", store=True)

    @api.depends("ngay_bat_dau")
    def _compute_nam(self):
        for record in self:
            record.nam = record.ngay_bat_dau.year if record.ngay_bat_dau else date.today().year

    @api.depends("luong_co_ban", "thuong", "phu_cap_xang_xe", "phu_cap_an_trua", "phu_cap_dien_thoai", "phu_cap_khac", "phat", "bhxh", "bhyt", "bhtn", "thue_tncn", "khau_tru_khac", "luong_lam_them")
    def _compute_salary(self):
        for record in self:
            tong_thu_nhap = (
                record.luong_co_ban + record.thuong + record.phu_cap_xang_xe +
                record.phu_cap_an_trua + record.phu_cap_dien_thoai + record.phu_cap_khac +
                record.luong_lam_them
            )
            tong_khau_tru = record.phat + record.bhxh + record.bhyt + record.bhtn + record.thue_tncn + record.khau_tru_khac
            record.tong_luong = max(tong_thu_nhap - tong_khau_tru, 0)

    @api.depends("luong_co_ban")
    def _compute_bao_hiem(self):
        for record in self:
            record.bhxh = record.luong_co_ban * 0.08
            record.bhyt = record.luong_co_ban * 0.015
            record.bhtn = record.luong_co_ban * 0.01

    @api.depends("luong_co_ban")
    def _compute_thue(self):
        for record in self:
            taxable_income = max(record.luong_co_ban - 11000000, 0)
            record.thue_tncn = taxable_income * 0.1 if taxable_income > 0 else 0.0

    @api.constrains("luong_co_ban", "thuong", "gio_lam_them", "ngay_nghi")
    def _check_valid_values(self):
        for record in self:
            if record.luong_co_ban < 0 or record.thuong < 0 or record.gio_lam_them < 0 or record.ngay_nghi < 0:
                raise ValidationError("Giá trị không hợp lệ! Lương, thưởng, giờ làm thêm, và ngày nghỉ không được âm.")

    def action_xac_nhan(self):
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({'trang_thai': 'da_thanh_toan'})

    @api.onchange("nhan_vien_id")
    def _compute_hop_dong(self):
        for record in self:
            hop_dong = self.env['hr_contract'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('status', '=', 'active')
            ], limit=1, order="ngay_bat_dau desc")
            record.hop_dong_id = hop_dong.id if hop_dong else False
            record.luong_co_ban = hop_dong.luong_hop_dong if hop_dong else 0.0

    @api.depends("gio_lam_them")
    def _compute_luong_lam_them(self):
        HE_SO_LAM_THEM = 100000
        for record in self:
            record.luong_lam_them = record.gio_lam_them * HE_SO_LAM_THEM

    @api.depends("ngay_nghi")
    def _compute_ngay_cong(self):
        for record in self:
            record.ngay_cong_thuc_te = max(26 - record.ngay_nghi, 0)
