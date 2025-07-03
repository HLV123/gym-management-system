# ==================== UI/MAIN_UI.PY ====================
# Giao diện chính đơn giản với flow cải thiện

from .base_ui import BaseUI
from .login_ui import LoginUI
from .admin_ui import AdminUI
from .trainer_ui import TrainerUI
from .member_ui import MemberUI
from .reports_ui import ReportsUI

class MainUI(BaseUI):
    """Giao diện chính đơn giản"""
    
    def __init__(self, gym_system):
        super().__init__(gym_system)
        self.login_ui = LoginUI(gym_system)
        self.admin_ui = AdminUI(gym_system)
        self.trainer_ui = TrainerUI(gym_system)
        self.member_ui = MemberUI(gym_system)
        self.reports_ui = ReportsUI(gym_system)
    
    def run(self):
        """Chạy ứng dụng với flow đơn giản"""
        
        # Đăng nhập
        if not self.login_ui.handle_login():
            return
        
        # Vào hệ thống chính
        while True:
            try:
                self.show_main_menu()
                choice = input("\nChọn: ").strip()
                
                if not self.handle_choice(choice):
                    break
                    
                input("\nNhấn Enter để tiếp tục...")
                
            except KeyboardInterrupt:
                print("\nĐăng xuất...")
                break
            except Exception as e:
                self.show_error(f"Lỗi: {e}")
                input("Nhấn Enter để tiếp tục...")
        
        # Lưu dữ liệu khi thoát
        print("Đang lưu dữ liệu...")
        self.gym_system.save_data()
        print("Đã lưu! Tạm biệt!")
    
    def show_main_menu(self):
        """Menu chính theo role"""
        self.clear_screen()
        user = self.gym_system.current_user
        
        # Header đẹp
        print("="*60)
        print(f"   GYM FITNESS ZONE - {user.name} ({user.role})")
        print("="*60)
        
        # Menu theo role
        if user.role == "Admin":
            self.admin_ui.show_menu()
        elif user.role == "Trainer":
            self.trainer_ui.show_menu()
        else:  # Member
            self.member_ui.show_menu()
    
    def handle_choice(self, choice: str) -> bool:
        """Xử lý lựa chọn"""
        user_role = self.gym_system.current_user.role
        
        # Xử lý đăng xuất cho tất cả roles
        logout_choices = {"9": "Admin", "8": "Trainer", "6": "Member"}
        
        if choice in logout_choices and logout_choices[choice] == user_role:
            return self.logout()
        
        # Xử lý theo role
        if user_role == "Admin":
            return self.handle_admin_choice(choice)
        elif user_role == "Trainer":
            return self.handle_trainer_choice(choice)
        else:  # Member
            return self.handle_member_choice(choice)
    
    def handle_admin_choice(self, choice: str) -> bool:
        """Menu Admin với số đơn giản"""
        choices = {
            "1": self.admin_ui.manage_members,
            "2": self.admin_ui.manage_trainers,
            "3": self.admin_ui.manage_equipment,
            "4": self.admin_ui.assign_trainer,
            "5": self.reports_ui.show_revenue_report,
            "6": self.reports_ui.show_attendance_report,
            "7": self.reports_ui.show_statistics,
            "8": self.reports_ui.export_data_menu,
        }
        
        if choice in choices:
            choices[choice]()
        else:
            self.show_error("Chọn từ 1-9!")
        return True
    
    def handle_trainer_choice(self, choice: str) -> bool:
        """Menu Trainer với số đơn giản"""
        choices = {
            "1": self.trainer_ui.show_assigned_members,
            "2": self.trainer_ui.create_schedule,
            "3": self.trainer_ui.mark_attendance,
            "4": self.trainer_ui.update_member_progress,
            "5": self.trainer_ui.update_equipment,
            "6": self.reports_ui.show_attendance_report,
            "7": self.reports_ui.export_data_menu,
        }
        
        if choice in choices:
            choices[choice]()
        else:
            self.show_error("Chọn từ 1-8!")
        return True
    
    def handle_member_choice(self, choice: str) -> bool:
        """Menu Member với số đơn giản"""
        choices = {
            "1": self.member_ui.show_member_info,
            "2": self.member_ui.show_member_schedule,
            "3": self.member_ui.update_own_progress,
            "4": self.member_ui.renew_membership,
            "5": self.reports_ui.show_attendance_report,
        }
        
        if choice in choices:
            choices[choice]()
        else:
            self.show_error("Chọn từ 1-6!")
        return True
    
    def logout(self) -> bool:
        """Đăng xuất"""
        user_name = self.gym_system.current_user.name
        self.gym_system.logout()
        print(f"Tạm biệt {user_name}!")
        return False