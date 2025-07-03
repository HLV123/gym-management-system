# ==================== UI/TRAINER_UI.PY ====================
# Giao diện Trainer

from .base_ui import BaseUI

class TrainerUI(BaseUI):
    """Giao diện Trainer"""
    
    def show_menu(self):
        """Menu Trainer"""
        trainer = self.gym_system.data["trainers"][self.gym_system.current_user.user_id]
        self.print_section(f"MENU HUẤN LUYỆN VIÊN - {trainer.specialization}")
        print(f"Bạn đang phụ trách {len(trainer.assigned_members)} thành viên")
        print()
        print("1. Xem thành viên được phân công")
        print("2. Tạo lịch tập")
        print("3. Điểm danh")
        print("4. Cập nhật tiến độ thành viên")
        print("5. Cập nhật thiết bị")
        print("6. Báo cáo điểm danh")
        print("7. Xuất dữ liệu CSV")
        print("8. Đăng xuất")
    
    def show_assigned_members(self):
        """Hiển thị thành viên được phân công"""
        self.print_section("THÀNH VIÊN ĐƯỢC PHÂN CÔNG")
        trainer = self.gym_system.data["trainers"][self.gym_system.current_user.user_id]
        
        if not trainer.assigned_members:
            self.show_info("Chưa có thành viên nào được phân công!")
            return
        
        for member_id in trainer.assigned_members:
            if member_id in self.gym_system.data["members"]:
                member = self.gym_system.data["members"][member_id]
                status = "[Hoạt động]" if member.is_membership_active() else "[Hết hạn]"
                
                print(f"{status} {member.name} ({member.user_id})")
                print(f"   Gói: {member.subscription_plan}")
                print(f"   Còn {member.get_remaining_days()} ngày")
                print(f"   Điểm danh: {len(member.attendance_records)} lần")
                print(f"   Tiến độ: {member.training_progress_status}")
                print(f"   Bài tập: {len(member.workout_progress)} bài")
                print()
    
    def create_schedule(self):
        """Tạo lịch tập"""
        self.print_section("TẠO LỊCH TẬP")
        trainer = self.gym_system.data["trainers"][self.gym_system.current_user.user_id]
        
        if not trainer.assigned_members:
            self.show_info("Chưa có thành viên nào được phân công!")
            return
        
        # Chọn member
        print("Chọn thành viên:")
        assigned_members = []
        for i, member_id in enumerate(trainer.assigned_members, 1):
            if member_id in self.gym_system.data["members"]:
                member = self.gym_system.data["members"][member_id]
                print(f"{i}. {member.name} ({member.user_id})")
                assigned_members.append(member)
        
        if not assigned_members:
            self.show_info("Không có thành viên hợp lệ!")
            return
        
        choice = self.get_choice(len(assigned_members), "Chọn thành viên")
        
        if choice > 0:
            selected_member = assigned_members[choice - 1]
            
            # Nhập thông tin lịch tập
            date = input("Ngày (YYYY-MM-DD): ").strip()
            time = input("Giờ (HH:MM): ").strip()
            exercises_input = input("Bài tập (cách nhau bởi dấu phẩy): ").strip()
            exercises = [ex.strip() for ex in exercises_input.split(",")]
            
            self.gym_system.create_schedule(
                selected_member.user_id, 
                self.gym_system.current_user.user_id, 
                date, time, exercises
            )
    
    def mark_attendance(self):
        """Điểm danh"""
        self.print_section("ĐIỂM DANH THÀNH VIÊN")
        trainer = self.gym_system.data["trainers"][self.gym_system.current_user.user_id]
        
        if not trainer.assigned_members:
            self.show_info("Chưa có thành viên nào được phân công!")
            return
        
        # Chọn member
        print("Chọn thành viên để điểm danh:")
        assigned_members = []
        for i, member_id in enumerate(trainer.assigned_members, 1):
            if member_id in self.gym_system.data["members"]:
                member = self.gym_system.data["members"][member_id]
                last_attendance = member.attendance_records[-1].split()[0] if member.attendance_records else "Chưa có"
                print(f"{i}. {member.name} ({member.user_id}) - Lần cuối: {last_attendance}")
                assigned_members.append(member)
        
        if not assigned_members:
            self.show_info("Không có thành viên hợp lệ!")
            return
        
        choice = self.get_choice(len(assigned_members), "Chọn thành viên")
        
        if choice > 0:
            selected_member = assigned_members[choice - 1]
            
            # Tùy chọn ngày giờ
            use_current = input("Sử dụng ngày giờ hiện tại? (Y/n): ").strip().lower()
            
            if use_current == 'n':
                date = input("Ngày (YYYY-MM-DD): ").strip()
                time = input("Giờ (HH:MM): ").strip()
                self.gym_system.mark_attendance(selected_member.user_id, date, time)
            else:
                self.gym_system.mark_attendance(selected_member.user_id)
    
    def update_member_progress(self):
        """Cập nhật tiến độ thành viên"""
        self.print_section("CẬP NHẬT TIẾN ĐỘ THÀNH VIÊN")
        trainer = self.gym_system.data["trainers"][self.gym_system.current_user.user_id]
        
        if not trainer.assigned_members:
            self.show_info("Chưa có thành viên nào được phân công!")
            return
        
        # Chọn member
        print("Chọn thành viên:")
        assigned_members = []
        for i, member_id in enumerate(trainer.assigned_members, 1):
            if member_id in self.gym_system.data["members"]:
                member = self.gym_system.data["members"][member_id]
                print(f"{i}. {member.name} ({member.user_id}) - {member.training_progress_status}")
                assigned_members.append(member)
        
        if not assigned_members:
            self.show_info("Không có thành viên hợp lệ!")
            return
        
        choice = self.get_choice(len(assigned_members), "Chọn thành viên")
        
        if choice > 0:
            selected_member = assigned_members[choice - 1]
            
            # Hiển thị tiến độ hiện tại
            if selected_member.workout_progress:
                print(f"\nTiến độ hiện tại của {selected_member.name}:")
                for exercise, progress in selected_member.workout_progress.items():
                    print(f"   {exercise}: {progress}")
            
            # Thêm/cập nhật tiến độ
            exercise = input("\nBài tập: ").strip()
            progress = input("Tiến độ: ").strip()
            
            self.gym_system.update_progress(selected_member.user_id, exercise, progress)
            
            # Cập nhật trạng thái tổng thể
            print("\nCập nhật trạng thái tiến độ tổng thể:")
            print("1. Xuất sắc")
            print("2. Tốt")
            print("3. Bình thường")
            print("4. Chưa tốt")
            print("5. Cần quan tâm nhiều hơn")
            
            status_choice = self.get_choice(5, "Chọn (Enter để bỏ qua)")
            status_map = {
                1: "Xuất sắc",
                2: "Tốt", 
                3: "Bình thường",
                4: "Chưa tốt", 
                5: "Cần quan tâm nhiều hơn"
            }
            
            if status_choice in status_map:
                self.gym_system.update_training_status(selected_member.user_id, status_map[status_choice])
    
    def update_equipment(self):
        """Cập nhật thiết bị"""
        self.print_section("CẬP NHẬT TRẠNG THÁI THIẾT BỊ")
        
        if not self.gym_system.data["gym_equipments"]:
            self.show_info("Không có thiết bị nào!")
            return
        
        equipments = list(self.gym_system.data["gym_equipments"].values())
        print("Chọn thiết bị để cập nhật:")
        self.show_equipment_list(equipments)
        
        choice = self.get_choice(len(equipments), "Chọn thiết bị")
        
        if choice > 0:
            selected_equipment = equipments[choice - 1]
            
            print(f"\nCập nhật trạng thái cho: {selected_equipment.name}")
            print("1. Đang sử dụng")
            print("2. Cần bảo trì")
            print("3. Hỏng")
            
            status_choice = self.get_choice(3, "Chọn trạng thái mới")
            status_map = {1: "Đang sử dụng", 2: "Cần bảo trì", 3: "Hỏng"}
            
            if status_choice in status_map:
                new_status = status_map[status_choice]
                self.gym_system.update_equipment_status(selected_equipment.equipment_id, new_status)
                
                # Nếu chọn "Cần bảo trì", hỏi ngày bảo trì
                if status_choice == 2:
                    date = input("Ngày bảo trì (YYYY-MM-DD): ").strip()
                    if date:
                        self.gym_system.schedule_maintenance(selected_equipment.equipment_id, date)