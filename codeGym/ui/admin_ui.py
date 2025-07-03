# ==================== UI/ADMIN_UI.PY ====================
# Giao diện Admin

from .base_ui import BaseUI

class AdminUI(BaseUI):
    """Giao diện Admin"""
    
    def show_menu(self):
        """Menu Admin"""
        self.print_section("MENU QUẢN TRỊ VIÊN")
        print("1. Quản lý thành viên")
        print("2. Quản lý huấn luyện viên") 
        print("3. Quản lý thiết bị")
        print("4. Phân công trainer")
        print("5. Báo cáo doanh thu")
        print("6. Báo cáo điểm danh")
        print("7. Thống kê tổng quan")
        print("8. Xuất dữ liệu CSV")
        print("9. Đăng xuất")
    
    def manage_members(self):
        """Quản lý thành viên"""
        self.print_section("QUẢN LÝ THÀNH VIÊN")
        print("1. Thêm thành viên mới")
        print("2. Xóa thành viên")
        print("3. Danh sách thành viên")
        print("4. Gia hạn cho thành viên")
        
        choice = self.get_choice(4)
        
        if choice == 1:
            self.add_member()
        elif choice == 2:
            self.remove_member()
        elif choice == 3:
            self.list_members()
        elif choice == 4:
            self.renew_membership()
    
    def add_member(self):
        """Thêm thành viên"""
        self.print_section("THÊM THÀNH VIÊN MỚI")
        
        try:
            user_id = input("ID thành viên: ").strip()
            name = input("Họ tên: ").strip()
            email = input("Email: ").strip()
            phone = input("Điện thoại: ").strip()
            gender = input("Giới tính (Nam/Nữ): ").strip()
            age_input = input("Tuổi: ").strip()
            age = int(age_input) if age_input.isdigit() else 0
            
            self.print_section("GÓI ĐĂNG KÝ CÓ SẴN")
            plans = list(self.gym_system.data["subscription_plans"].values())
            for i, plan in enumerate(plans, 1):
                features_str = ", ".join(plan.features[:2])
                print(f"{i}. {plan.name} - {plan.duration_months} tháng - {plan.price:,} VND")
                print(f"   {features_str}...")
            
            plan_choice = self.get_choice(len(plans), "Chọn gói")
            
            if plan_choice > 0:
                selected_plan = plans[plan_choice - 1]
                self.gym_system.add_member(user_id, name, email, phone, selected_plan.plan_id, gender, age)
                
        except Exception as e:
            self.show_error(f"Lỗi: {e}")
    
    def remove_member(self):
        """Xóa thành viên với menu chọn"""
        self.print_section("XÓA THÀNH VIÊN")
        
        if not self.gym_system.data["members"]:
            self.show_info("Không có thành viên nào!")
            return
        
        members = list(self.gym_system.data["members"].values())
        print("Chọn thành viên để xóa:")
        self.show_members_list(members)
        
        choice = self.get_choice(len(members), "Chọn thành viên")
        
        if choice > 0:
            selected_member = members[choice - 1]
            if self.confirm_action(f"Xác nhận xóa {selected_member.name}?"):
                self.gym_system.remove_member(selected_member.user_id)
            else:
                self.show_info("Đã hủy thao tác")
    
    def list_members(self):
        """Danh sách thành viên"""
        self.print_section("DANH SÁCH THÀNH VIÊN")
        
        if not self.gym_system.data["members"]:
            self.show_info("Không có thành viên nào!")
            return
        
        # Phân loại theo trạng thái
        active_members = []
        expiring_members = []
        expired_members = []
        
        for member in self.gym_system.data["members"].values():
            status = member.get_membership_status()
            if status == "Hết hạn":
                expired_members.append(member)
            elif status == "Sắp hết hạn":
                expiring_members.append(member)
            else:
                active_members.append(member)
        
        # Hiển thị từng nhóm
        if active_members:
            print(f"\nTHÀNH VIÊN ĐANG HOẠT ĐỘNG ({len(active_members)}):")
            for member in active_members:
                print(f"   {member.name} ({member.user_id})")
                print(f"      Gói: {member.subscription_plan} | còn {member.get_remaining_days()} ngày")
                print(f"      Điểm danh: {len(member.attendance_records)} lần | Tiến độ: {member.training_progress_status}")
                print()
        
        if expiring_members:
            print(f"\nTHÀNH VIÊN SẮP HẾT HẠN ({len(expiring_members)}):")
            for member in expiring_members:
                print(f"   {member.name} ({member.user_id}) - còn {member.get_remaining_days()} ngày")
        
        if expired_members:
            print(f"\nTHÀNH VIÊN HẾT HẠN ({len(expired_members)}):")
            for member in expired_members:
                print(f"   {member.name} ({member.user_id}) - hết hạn từ {member.subscription_end}")
    
    def renew_membership(self):
        """Admin gia hạn cho thành viên"""
        self.print_section("GIA HẠN CHO THÀNH VIÊN")
        
        if not self.gym_system.data["members"]:
            self.show_info("Không có thành viên nào!")
            return
        
        members = list(self.gym_system.data["members"].values())
        print("Chọn thành viên để gia hạn:")
        
        for i, member in enumerate(members, 1):
            days_left = member.get_remaining_days()
            status = "[Hoạt động]" if member.is_membership_active() else "[Hết hạn]"
            print(f"{i}. {status} {member.name} ({member.user_id}) - còn {days_left} ngày")
        
        choice = self.get_choice(len(members), "Chọn thành viên")
        
        if choice > 0:
            selected_member = members[choice - 1]
            
            # Chọn gói mới
            plans = list(self.gym_system.data["subscription_plans"].values())
            print(f"\nGói hiện tại: {selected_member.subscription_plan}")
            print("Chọn gói mới:")
            
            for i, plan in enumerate(plans, 1):
                print(f"{i}. {plan.name} - {plan.duration_months} tháng - {plan.price:,} VND")
            
            plan_choice = self.get_choice(len(plans), "Chọn gói mới")
            
            if plan_choice > 0:
                selected_plan = plans[plan_choice - 1]
                self.gym_system.renew_membership(selected_member.user_id, selected_plan.plan_id)
    
    def manage_trainers(self):
        """Quản lý trainer"""
        self.print_section("QUẢN LÝ HUẤN LUYỆN VIÊN")
        print("1. Thêm trainer mới")
        print("2. Danh sách trainer")
        
        choice = self.get_choice(2)
        
        if choice == 1:
            self.add_trainer()
        elif choice == 2:
            self.list_trainers()
    
    def add_trainer(self):
        """Thêm trainer"""
        self.print_section("THÊM HUẤN LUYỆN VIÊN MỚI")
        
        user_id = input("ID trainer: ").strip()
        name = input("Họ tên: ").strip()
        email = input("Email: ").strip()
        specialization = input("Chuyên môn: ").strip()
        
        self.gym_system.add_trainer(user_id, name, email, specialization)
    
    def list_trainers(self):
        """Danh sách trainer"""
        self.print_section("DANH SÁCH HUẤN LUYỆN VIÊN")
        
        if not self.gym_system.data["trainers"]:
            self.show_info("Không có trainer nào!")
            return
        
        for trainer in self.gym_system.data["trainers"].values():
            print(f"{trainer.name} ({trainer.user_id})")
            print(f"   Chuyên môn: {trainer.specialization}")
            print(f"   Số thành viên: {len(trainer.assigned_members)}")
            if trainer.assigned_members:
                member_names = []
                for mid in trainer.assigned_members:
                    if mid in self.gym_system.data["members"]:
                        member_names.append(self.gym_system.data["members"][mid].name)
                print(f"   Phụ trách: {', '.join(member_names)}")
            print()
    
    def manage_equipment(self):
        """Quản lý thiết bị"""
        self.print_section("QUẢN LÝ THIẾT BỊ")
        print("1. Thêm thiết bị mới")
        print("2. Danh sách thiết bị")
        
        choice = self.get_choice(2)
        
        if choice == 1:
            self.add_equipment()
        elif choice == 2:
            self.list_equipment()
    
    def add_equipment(self):
        """Thêm thiết bị"""
        self.print_section("THÊM THIẾT BỊ MỚI")
        
        equipment_id = input("ID thiết bị: ").strip()
        name = input("Tên thiết bị: ").strip()
        
        try:
            quantity = int(input("Số lượng: ").strip())
        except ValueError:
            self.show_error("Số lượng phải là số!")
            return
        
        print("\nTrạng thái:")
        print("1. Mới")
        print("2. Đang sử dụng")
        print("3. Cần bảo trì")
        print("4. Hỏng")
        
        status_choice = self.get_choice(4, "Chọn trạng thái")
        status_map = {1: "Mới", 2: "Đang sử dụng", 3: "Cần bảo trì", 4: "Hỏng"}
        status = status_map.get(status_choice, "Mới")
        
        self.gym_system.add_equipment(equipment_id, name, quantity, status)
    
    def list_equipment(self):
        """Danh sách thiết bị"""
        self.print_section("DANH SÁCH THIẾT BỊ")
        
        if not self.gym_system.data["gym_equipments"]:
            self.show_info("Không có thiết bị nào!")
            return
        
        # Phân loại theo trạng thái
        status_groups = {}
        for equipment in self.gym_system.data["gym_equipments"].values():
            status = equipment.status
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(equipment)
        
        # Hiển thị theo từng nhóm trạng thái
        for status, equipments in status_groups.items():
            print(f"\n{status.upper()} ({len(equipments)}):")
            for eq in equipments:
                print(f"   {eq.name} ({eq.equipment_id}) - SL: {eq.quantity}")
                if eq.maintenance_schedule:
                    print(f"      Bảo trì: {eq.maintenance_schedule}")
    
    def assign_trainer(self):
        """Phân công trainer"""
        self.print_section("PHÂN CÔNG TRAINER")
        
        if not self.gym_system.data["trainers"]:
            self.show_info("Không có trainer nào!")
            return
        
        if not self.gym_system.data["members"]:
            self.show_info("Không có thành viên nào!")
            return
        
        # Chọn trainer
        trainers = list(self.gym_system.data["trainers"].values())
        print("Chọn trainer:")
        
        for i, trainer in enumerate(trainers, 1):
            print(f"{i}. {trainer.name} ({trainer.specialization}) - {len(trainer.assigned_members)} thành viên")
        
        trainer_choice = self.get_choice(len(trainers), "Chọn trainer")
        
        if trainer_choice > 0:
            selected_trainer = trainers[trainer_choice - 1]
            
            # Chọn member
            members = list(self.gym_system.data["members"].values())
            print(f"\nChọn thành viên để phân công cho {selected_trainer.name}:")
            
            for i, member in enumerate(members, 1):
                assigned = "[Đã phân công]" if member.user_id in selected_trainer.assigned_members else "[Chưa phân công]"
                print(f"{i}. {assigned} {member.name} ({member.user_id}) - {member.subscription_plan}")
            
            member_choice = self.get_choice(len(members), "Chọn thành viên")
            
            if member_choice > 0:
                selected_member = members[member_choice - 1]
                self.gym_system.assign_member_to_trainer(selected_trainer.user_id, selected_member.user_id)