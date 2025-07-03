# ==================== UI/BASE_UI.PY ====================
# Lớp giao diện cơ bản

import os

class BaseUI:
    """Lớp giao diện cơ bản với các phương thức chung"""
    
    def __init__(self, gym_system):
        self.gym_system = gym_system
    
    def clear_screen(self):
        """Xóa màn hình"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """In header đẹp"""
        print("\n" + "="*60)
        print(f"  {title.center(56)}  ")
        print("="*60)
    
    def print_section(self, title: str):
        """In section header"""
        print(f"\n{title}")
        print("-" * len(title))
    
    def get_choice(self, max_choice: int, prompt: str = "Chọn") -> int:
        """Lấy lựa chọn từ người dùng"""
        try:
            choice = int(input(f"{prompt} (1-{max_choice}): ").strip())
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"Vui lòng chọn từ 1 đến {max_choice}!")
                return 0
        except ValueError:
            print("Vui lòng nhập số!")
            return 0
    
    def confirm_action(self, message: str) -> bool:
        """Xác nhận hành động"""
        response = input(f"{message} (y/N): ").strip().lower()
        return response == 'y'
    
    def show_members_list(self, members: list, show_status: bool = True):
        """Hiển thị danh sách members"""
        for i, member in enumerate(members, 1):
            if show_status:
                status = "Hoạt động" if member.is_membership_active() else "Hết hạn"
                print(f"{i}. [{status}] {member.name} ({member.user_id}) - {member.subscription_plan}")
            else:
                print(f"{i}. {member.name} ({member.user_id})")
    
    def show_trainers_list(self, trainers: list):
        """Hiển thị danh sách trainers"""
        for i, trainer in enumerate(trainers, 1):
            print(f"{i}. {trainer.name} ({trainer.user_id}) - {trainer.specialization}")
    
    def show_equipment_list(self, equipments: list):
        """Hiển thị danh sách thiết bị"""
        for i, equipment in enumerate(equipments, 1):
            print(f"{i}. [{equipment.status}] {equipment.name} ({equipment.equipment_id})")
    
    def wait_for_enter(self, message: str = "Nhấn Enter để tiếp tục..."):
        """Chờ người dùng nhấn Enter"""
        input(f"\n{message}")
    
    def show_error(self, message: str):
        """Hiển thị lỗi"""
        print(f"LỖI: {message}")
    
    def show_success(self, message: str):
        """Hiển thị thành công"""
        print(f"THÀNH CÔNG: {message}")
    
    def show_info(self, message: str):
        """Hiển thị thông tin"""
        print(f"THÔNG TIN: {message}")
    
    def show_warning(self, message: str):
        """Hiển thị cảnh báo"""
        print(f"CẢNH BÁO: {message}")