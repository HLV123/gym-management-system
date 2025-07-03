# ==================== UI/REPORTS_UI.PY ====================
# Giao diện báo cáo và thống kê

from datetime import datetime, timedelta
from .base_ui import BaseUI

class ReportsUI(BaseUI):
    """Giao diện báo cáo và thống kê"""
    
    def show_revenue_report(self):
        """Báo cáo doanh thu"""
        self.print_section("BÁO CÁO DOANH THU")
        report = self.gym_system.get_revenue_report()
        
        if not report:
            return
        
        print(f"Tổng doanh thu: {report['total_revenue']:,} VND")
        print(f"Tổng thành viên: {report['total_members']}")
        print(f"Thành viên hoạt động: {report['active_members']}")
        print(f"Thành viên hết hạn: {report['expired_members']}")
        
        if 'revenue_by_plan' in report:
            print("\nDoanh thu theo gói:")
            for plan_name, data in report['revenue_by_plan'].items():
                percentage = (data['revenue'] / report['total_revenue'] * 100) if report['total_revenue'] > 0 else 0
                print(f"   {plan_name}: {data['count']} người - {data['revenue']:,} VND ({percentage:.1f}%)")
    
    def show_attendance_report(self):
        """Báo cáo điểm danh"""
        self.print_section("BÁO CÁO ĐIỂM DANH")
        
        # Tùy chọn khoảng thời gian
        print("Chọn khoảng thời gian:")
        print("1. 7 ngày qua")
        print("2. 30 ngày qua")
        print("3. Tùy chỉnh")
        
        choice = self.get_choice(3)
        
        start_date = None
        end_date = None
        
        if choice == 1:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        elif choice == 2:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        elif choice == 3:
            start_date = input("Ngày bắt đầu (YYYY-MM-DD): ").strip()
            end_date = input("Ngày kết thúc (YYYY-MM-DD): ").strip()
        
        if choice == 0:
            return
        
        report = self.gym_system.get_attendance_report(start_date, end_date)
        
        if not report:
            self.show_info("Không có dữ liệu!")
            return
        
        # Sắp xếp theo tỷ lệ điểm danh
        sorted_report = sorted(report.items(), key=lambda x: x[1]['attendance_percentage'], reverse=True)
        
        print(f"\nBáo cáo từ {start_date or '30 ngày trước'} đến {end_date or 'hôm nay'}:")
        print("="*70)
        
        for member_id, data in sorted_report:
            percentage = data['attendance_percentage']
            
            if percentage >= 70:
                rank = "[Xuất sắc]"
            elif percentage >= 50:
                rank = "[Tốt]"
            elif percentage >= 30:
                rank = "[Khá]"
            else:
                rank = "[Cần cải thiện]"
            
            print(f"{rank} {data['name']:20} | {data['attendance_days']:2d}/{data['total_days']:2d} ngày | {percentage:5.1f}% | {data['subscription_plan']}")
    
    def show_statistics(self):
        """Thống kê tổng quan"""
        self.print_section("THỐNG KÊ TỔNG QUAN")
        stats = self.gym_system.calculate_statistics()
        
        if not stats:
            return
        
        print(f"Tổng thành viên: {stats['total_members']}")
        print(f"Thành viên hoạt động: {stats['active_members']}")
        print(f"Thành viên hết hạn: {stats['expired_members']}")
        print(f"Tổng trainer: {stats['total_trainers']}")
        print(f"Tổng lịch tập: {stats['total_schedules']}")
        print(f"Điểm danh trung bình: {stats['average_attendance']} lần/người")
        
        if stats['best_performance_member']:
            print(f"Thành viên xuất sắc: {stats['best_performance_member']}")
        
        # Thống kê theo gói
        if 'plan_statistics' in stats:
            print("\nThống kê theo gói đăng ký:")
            for plan, data in stats['plan_statistics'].items():
                total = data['active'] + data['expired']
                print(f"   {plan}: {total} người (Hoạt động: {data['active']} | Hết hạn: {data['expired']})")
        
        # Thống kê thiết bị
        if 'equipment_statistics' in stats:
            print("\nThống kê thiết bị:")
            for status, count in stats['equipment_statistics'].items():
                print(f"   {status}: {count} thiết bị")
    
    def export_data_menu(self):
        """Menu xuất dữ liệu"""
        self.print_section("XUẤT DỮ LIỆU CSV")
        
        print("Chọn loại dữ liệu:")
        print("1. Danh sách thành viên")
        print("2. Dữ liệu điểm danh")
        print("3. Danh sách trainer")
        print("4. Danh sách thiết bị")
        print("5. Báo cáo doanh thu")
        
        data_choice = self.get_choice(5, "Chọn dữ liệu")
        
        data_map = {
            1: "members",
            2: "attendance", 
            3: "trainers",
            4: "equipment",
            5: "revenue"
        }
        
        if data_choice not in data_map:
            return
        
        data_type = data_map[data_choice]
        
        # Chọn định dạng
        print("\nChọn định dạng file:")
        print("1. Excel/WPS (UTF-8 với BOM)")
        print("2. UTF-8 thường")
        
        format_choice = self.get_choice(2, "Chọn định dạng")
        if format_choice == 0:
            return
            
        format_type = "excel" if format_choice == 1 else "utf-8"
        
        # Tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_type}_{timestamp}.csv"
        
        custom_name = input(f"Tên file ({filename}): ").strip()
        if custom_name:
            if not custom_name.endswith('.csv'):
                custom_name += '.csv'
            filename = custom_name
        
        # Xuất file
        if self.gym_system.export_to_csv(data_type, filename, format_type):
            self.show_success(f"File đã được lưu: {filename}")
        else:
            self.show_error("Có lỗi xảy ra khi xuất file!")