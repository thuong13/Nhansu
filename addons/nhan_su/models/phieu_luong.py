# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class PhieuLuong(models.Model):
    _name = 'phieu_luong'
    _description = 'Phiếu Lương Nhân Viên'
    _order = "ngay desc"

    ten_phieu = fields.Char(string='Mã Phiếu Lương', required=True, copy=False, readonly=True, index=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete="cascade")
    ngay = fields.Date(string="Ngày kỳ lương", required=True, default=fields.Date.context_today)
    
    # Các khoản thu nhập
    luong_co_ban = fields.Float(string="Lương cơ bản", required=True, default=0.0)
    thuong = fields.Float(string="Thưởng", default=0.0)
    phu_cap_xang_xe = fields.Float(string="Phụ cấp xăng xe", default=0.0)
    phu_cap_an_trua = fields.Float(string="Phụ cấp ăn trưa", default=0.0)
    phu_cap_dien_thoai = fields.Float(string="Phụ cấp điện thoại", default=0.0)
    phat = fields.Float(string="Phạt", default=0.0)

    # Bảo hiểm và thuế
    bhxh = fields.Float(string="BHXH", compute="_compute_bao_hiem", store=True)
    bhyt = fields.Float(string="BHYT", compute="_compute_bao_hiem", store=True)
    bhtn = fields.Float(string="BHTN", compute="_compute_bao_hiem", store=True)
    thue_tncn = fields.Float(string="Thuế TNCN", compute="_compute_thue", store=True)

    # Tổng lương thực nhận
    tong_luong = fields.Float(string="Tổng lương", compute="_compute_salary", store=True)

    # Trạng thái phiếu lương
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='cho_duyet', track_visibility='onchange')

    hop_dong_id = fields.Many2one('hr_contract', string="Hợp đồng", compute="_compute_hop_dong", store=True)
    
    # loai_hop_dong = fields.Selection(
        # related='hop_dong_id.loai_hop_dong',  
        # store=True,  
        # string="Loại hợp đồng",
        # readonly=True
    # )

    @api.depends("luong_co_ban", "thuong", "phu_cap_xang_xe", "phu_cap_an_trua", "phu_cap_dien_thoai", "phat", "bhxh", "bhyt", "bhtn", "thue_tncn")
    def _compute_salary(self):
        for record in self:
            tong_thu_nhap = record.luong_co_ban + record.thuong + record.phu_cap_xang_xe + record.phu_cap_an_trua + record.phu_cap_dien_thoai
            tong_khau_tru = record.phat + record.bhxh + record.bhyt + record.bhtn + record.thue_tncn
            record.tong_luong = tong_thu_nhap - tong_khau_tru

    @api.depends("luong_co_ban")
    def _compute_bao_hiem(self):
        for record in self:
            record.bhxh = record.luong_co_ban * 0.08  # 8% BHXH
            record.bhyt = record.luong_co_ban * 0.015 # 1.5% BHYT
            record.bhtn = record.luong_co_ban * 0.01  # 1% BHTN

    @api.depends("luong_co_ban")
    def _compute_thue(self):
        for record in self:
            if record.luong_co_ban > 11000000:  # Mức miễn thuế
                taxable_income = record.luong_co_ban - 11000000
                record.thue_tncn = taxable_income * 0.1  # Thuế 10%
            else:
                record.thue_tncn = 0.0

    @api.constrains("luong_co_ban")
    def _check_luong_co_ban(self):
        for record in self:
            if record.luong_co_ban < 0:
                raise ValidationError("Lương cơ bản không thể nhỏ hơn 0.")

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
            ], limit=1, order="ngay_bat_dau desc")  # Lấy hợp đồng mới nhất

            record.hop_dong_id = hop_dong.id if hop_dong else False
            record.luong_co_ban = hop_dong.luong_hop_dong if hop_dong else 0.0
