# ==================== UI/MEMBER_UI.PY ====================
# Giao diện Member

from .base_ui import BaseUI

class MemberUI(BaseUI):
    """Giao diện Member"""
    
    def show_menu(self):
        """Menu Member"""
        member = self.gym_system.current_user
        days_left = member.get_remaining_days()
        status = member.get_membership_status()
        
        self.print_section(f"MENU THÀNH VIÊN - {member.subscription_plan.upper()}")
        
        # Hiển thị thông tin nhanh
        if status == "Hết hạn":
            self.show_warning("Gói tập của bạn đã hết hạn!")
        elif status == "Sắp hết hạn":
            self.show_warning(f"Gói tập còn {days_left} ngày (sắp hết hạn)")
        else:
            print(f"Gói tập còn {days_left} ngày")
        
        print()
        print("1. Xem thông tin cá nhân")
        print("2. Xem lịch tập")
        print("3. Cập nhật tiến độ cá nhân")
        print("4. Gia hạn đăng ký")
        print("5. Báo cáo điểm danh cá nhân")
        print("6. Đăng xuất")
    
    def show_member_info(self):
        """Hiển thị thông tin thành viên"""
        self.print_section("THÔNG TIN CÁ NHÂN")
        member = self.gym_system.current_user
        
        print(f"ID: {member.user_id}")
        print(f"Tên: {member.name}")
        print(f"Email: {member.email}")
        print(f"Điện thoại: {member.phone}")
        if member.gender:
            print(f"Giới tính: {member.gender}")
        if member.age:
            print(f"Tuổi: {member.age}")
        
        print(f"\nGói đăng ký: {member.subscription_plan}")
        print(f"Ngày bắt đầu: {member.subscription_start}")
        print(f"Ngày hết hạn: {member.subscription_end}")
        print(f"Trạng thái: {member.get_membership_status()}")
        print(f"Số ngày còn lại: {member.get_remaining_days()}")
        
        print(f"\nTiến độ tập luyện: {member.training_progress_status}")
        print(f"Số lần điểm danh: {len(member.attendance_records)}")
        print(f"Số bài tập: {len(member.workout_progress)}")
        
        if member.workout_progress:
            print("\nChi tiết tiến độ:")
            for exercise, progress in member.workout_progress.items():
                print(f"   {exercise}: {progress}")
    
    def show_member_schedule(self):
        """Hiển thị lịch tập"""
        self.print_section("LỊCH TẬP CỦA TÔI")
        member_id = self.gym_system.current_user.user_id
        
        schedules = [s for s in self.gym_system.data["workout_schedules"].values() 
                    if s.member_id == member_id]
        
        if not schedules:
            self.show_info("Chưa có lịch tập nào!")
            return
        
        # Sắp xếp theo ngày
        schedules.sort(key=lambda x: x.date)
        
        for schedule in schedules:
            trainer_name = "Không rõ"
            if schedule.trainer_id in self.gym_system.data["trainers"]:
                trainer_name = self.gym_system.data["trainers"][schedule.trainer_id].name
            
            status = "[Hoàn thành]" if schedule.completed else "[Chưa hoàn thành]"
            
            print(f"{status} {schedule.date} {schedule.time}")
            print(f"   Trainer: {trainer_name}")
            print(f"   Bài tập: {', '.join(schedule.exercises)}")
            print(f"   Trạng thái: {'Hoàn thành' if schedule.completed else 'Chưa hoàn thành'}")
            print()
    
    def update_own_progress(self):
        """Cập nhật tiến độ cá nhân"""
        self.print_section("CẬP NHẬT TIẾN ĐỘ CÁ NHÂN")
        member = self.gym_system.current_user
        
        if member.workout_progress:
            print("Tiến độ hiện tại:")
            for exercise, progress in member.workout_progress.items():
                print(f"   {exercise}: {progress}")
        
        print("\nThêm/cập nhật tiến độ mới:")
        exercise = input("Bài tập: ").strip()
        progress = input("Tiến độ: ").strip()
        
        member_id = self.gym_system.current_user.user_id
        self.gym_system.update_progress(member_id, exercise, progress)
    
    def renew_membership(self):
        """Gia hạn đăng ký"""
        self.print_section("GIA HẠN ĐĂNG KÝ")
        member = self.gym_system.current_user
        
        print(f"Gói hiện tại: {member.subscription_plan}")
        print(f"Ngày hết hạn: {member.subscription_end}")
        print(f"Số ngày còn lại: {member.get_remaining_days()}")
        
        print("\nGói đăng ký có sẵn:")
        plans = list(self.gym_system.data["subscription_plans"].values())
        
        for i, plan in enumerate(plans, 1):
            features_str = ", ".join(plan.features[:2])
            print(f"{i}. {plan.name} - {plan.duration_months} tháng - {plan.price:,} VND")
            print(f"   {features_str}...")
        
        choice = self.get_choice(len(plans), "Chọn gói mới")
        
        if choice > 0:
            selected_plan = plans[choice - 1]
            if self.confirm_action(f"Xác nhận gia hạn gói {selected_plan.name}?"):
                self.gym_system.renew_membership(member.user_id, selected_plan.plan_id)
            else:
                self.show_info("Đã hủy gia hạn")