# Gym Management System 🏋️‍♂️

Hệ thống quản lý phòng gym hoàn chỉnh được xây dựng bằng Python với giao diện dòng lệnh đơn giản, dễ sử dụng.

## 🚀 Tính năng chính

### 👥 Quản lý theo vai trò
- **Admin**: Quản lý toàn bộ hệ thống
- **Trainer**: Quản lý thành viên được phân công
- **Member**: Xem thông tin cá nhân và cập nhật tiến độ

### 📊 Chức năng chính
- ✅ Quản lý thành viên (thêm, xóa, gia hạn)
- ✅ Quản lý huấn luyện viên và phân công
- ✅ Quản lý thiết bị phòng gym
- ✅ Tạo lịch tập luyện
- ✅ Điểm danh thành viên
- ✅ Theo dõi tiến độ tập luyện
- ✅ Báo cáo doanh thu và thống kê
- ✅ Xuất dữ liệu CSV
- ✅ Hệ thống gói đăng ký linh hoạt

## 📁 Cấu trúc dự án

```
gym-management-system/
├── main.py                 # File chính để chạy ứng dụng
├── models.py              # Các class đối tượng (Member, Trainer, Admin, etc.)
├── gym_system.py          # Logic xử lý chính của hệ thống
├── data_manager.py        # Quản lý dữ liệu và file JSON
├── ui/                    # Thư mục giao diện người dùng
│   ├── __init__.py
│   ├── base_ui.py        # Lớp giao diện cơ bản
│   ├── main_ui.py        # Giao diện chính
│   ├── login_ui.py       # Giao diện đăng nhập
│   ├── admin_ui.py       # Giao diện Admin
│   ├── trainer_ui.py     # Giao diện Trainer
│   ├── member_ui.py      # Giao diện Member
│   └── reports_ui.py     # Giao diện báo cáo
├── gym_data.json         # File dữ liệu (tự động tạo)
├── README.md             # Tài liệu hướng dẫn
└── requirements.txt      # Các thư viện cần thiết
```

## 🔧 Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- Các thư viện: `json`, `csv`, `datetime`, `os` (tích hợp sẵn)


## 🎯 Cách sử dụng

### Đăng nhập
Hệ thống đã có sẵn dữ liệu mẫu:
- **1 Admin**: Nguyễn Văn Quản
- **3 Trainers**: Trần Thị Hương, Lê Văn Mạnh, Phạm Minh Tuấn
- **10 Members**: member001 đến member010

Chỉ cần chọn số thứ tự để đăng nhập!

### Gói đăng ký có sẵn
- **Gói Cơ Bản**: 1 tháng - 500,000 VND
- **Gói Nâng Cao**: 3 tháng - 1,200,000 VND
- **Gói VIP**: 6 tháng - 2,000,000 VND
- **Gói Gia Đình**: 12 tháng - 3,500,000 VND

## 👨‍💼 Chức năng theo vai trò

### Admin
- Quản lý thành viên (thêm, xóa, gia hạn)
- Quản lý huấn luyện viên
- Quản lý thiết bị phòng gym
- Phân công trainer cho thành viên
- Xem báo cáo doanh thu và thống kê
- Xuất dữ liệu CSV

### Trainer
- Xem thành viên được phân công
- Tạo lịch tập cho thành viên
- Điểm danh thành viên
- Cập nhật tiến độ tập luyện
- Cập nhật trạng thái thiết bị
- Xem báo cáo điểm danh

### Member
- Xem thông tin cá nhân
- Xem lịch tập
- Cập nhật tiến độ tập luyện
- Gia hạn đăng ký
- Xem báo cáo điểm danh cá nhân

## 📊 Báo cáo và thống kê

### Báo cáo doanh thu
- Tổng doanh thu
- Doanh thu theo gói đăng ký
- Số lượng thành viên hoạt động/hết hạn

### Báo cáo điểm danh
- Theo khoảng thời gian tùy chọn
- Tỷ lệ điểm danh từng thành viên
- Xếp hạng theo mức độ tích cực

### Thống kê tổng quan
- Tổng số thành viên, trainer, thiết bị
- Thành viên xuất sắc nhất
- Thống kê theo gói đăng ký
- Tình trạng thiết bị

## 💾 Quản lý dữ liệu

### Lưu trữ
- Dữ liệu lưu trong file `gym_data.json`
- Tự động lưu khi thoát ứng dụng
- Backup dữ liệu bằng cách sao chép file JSON

### Xuất dữ liệu
- Xuất CSV với 2 định dạng: Excel/WPS và UTF-8
- Các loại dữ liệu: thành viên, điểm danh, trainer, thiết bị
- Tên file tự động với timestamp

## 🔐 Bảo mật

- Hệ thống phân quyền 3 cấp: Admin > Trainer > Member
- Trainer chỉ thao tác với thành viên được phân công
- Member chỉ xem và cập nhật thông tin cá nhân

## 🛠️ Tùy chỉnh

### Thêm gói đăng ký mới
Chỉnh sửa trong `data_manager.py`:
```python
SubscriptionPlan("plan_id", "Tên gói", duration_months, price, features_list)
```

### Thêm vai trò mới
Mở rộng trong `models.py` và `gym_system.py`:
```python
class NewRole(User):
    def __init__(self, ...):
        super().__init__(..., role="NewRole")
```

## 📝 Changelog

### Version 1.0.0
- Hệ thống quản lý cơ bản
- Giao diện đăng nhập đơn giản
- Báo cáo và thống kê
- Xuất dữ liệu CSV
- Dữ liệu mẫu phong phú

## 🤝 Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

