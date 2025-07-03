# ==================== MAIN.PY ====================
# File chính với giao diện đăng nhập đơn giản

from gym_system import GymManagementSystem
from ui.main_ui import MainUI

def main():
    """Hàm chính với giao diện đơn giản"""
    try:
        print("CHÀO MỪNG ĐẾN VỚI GYM FITNESS ZONE!")
        print()
        print("Hệ thống có sẵn:")
        print("   - 1 Admin: Nguyễn Văn Quản")
        print("   - 3 Trainers: Trần Thị Hương, Lê Văn Mạnh, Phạm Minh Tuấn") 
        print("   - 10 Members: member001 đến member010")
        print("   - Dữ liệu mẫu phong phú với lịch sử điểm danh & tiến độ")
        print()
        print("Đang khởi tạo hệ thống...")
        
        # Khởi tạo hệ thống
        gym_system = GymManagementSystem()
        main_ui = MainUI(gym_system)
        
        # Chạy ứng dụng
        main_ui.run()
        
    except KeyboardInterrupt:
        print("\nTạm biệt! Dữ liệu đã được lưu.")
    except Exception as e:
        print(f"Lỗi: {e}")
        print("Vui lòng kiểm tra lại các file cần thiết:")
        print("   - models.py")
        print("   - data_manager.py") 
        print("   - gym_system.py")
        print("   - ui/ (folder chứa các UI components)")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()