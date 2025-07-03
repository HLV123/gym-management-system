# ==================== UI/LOGIN_UI.PY ====================
# Giao diện đăng nhập đơn giản - chỉ cần chọn số

from .base_ui import BaseUI

class LoginUI(BaseUI):
    """Giao diện đăng nhập đơn giản"""
    
    def show_login_menu(self):
        """Menu đăng nhập đơn giản với số thứ tự"""
        self.print_section("ĐĂNG NHẬP - CHỌN SỐ ĐỂ VÀO")
        users = self.gym_system.get_users_for_login()
        
        user_mapping = {}
        count = 1
        
        # Hiển thị tất cả users với số thứ tự liên tục
        print("Chọn số để đăng nhập:")
        print("-" * 50)
        
        # Admin
        if users["Admins"]:
            for uid, name, role in users["Admins"]:
                print(f"{count:2d}. {name} (Admin)")
                user_mapping[count] = uid
                count += 1
        
        # Trainer  
        if users["Trainers"]:
            for uid, name, role in users["Trainers"]:
                print(f"{count:2d}. {name} (Trainer)")
                user_mapping[count] = uid
                count += 1
        
        # Members
        if users["Members"]:
            for uid, name, role in users["Members"]:
                print(f"{count:2d}. {name} (Member)")
                user_mapping[count] = uid
                count += 1
        
        print("-" * 50)
        print(f"{count:2d}. Thoát")
        
        return user_mapping, count
    
    def handle_login(self):
        """Xử lý đăng nhập đơn giản"""
        while True:
            user_mapping, max_choice = self.show_login_menu()
            
            try:
                choice = input(f"\nNhập số (1-{max_choice}): ").strip()
                
                # Thoát
                if choice == str(max_choice):
                    return False
                
                choice_num = int(choice)
                
                # Kiểm tra choice hợp lệ
                if choice_num in user_mapping:
                    user_id = user_mapping[choice_num]
                    
                    # Đăng nhập
                    if self.gym_system.login(user_id):
                        user = self.gym_system.current_user
                        print(f"\nĐăng nhập thành công!")
                        print(f"Chào {user.name} ({user.role})")
                        input("Nhấn Enter để vào hệ thống...")
                        return True
                    else:
                        self.show_error("Đăng nhập thất bại!")
                else:
                    self.show_error(f"Vui lòng chọn từ 1 đến {max_choice}!")
                    
            except ValueError:
                self.show_error("Vui lòng nhập số!")
            except KeyboardInterrupt:
                print("\nTạm biệt!")
                return False
            
            # Chờ một chút trước khi hiển thị lại menu
            input("Nhấn Enter để thử lại...")
            self.clear_screen()