# ==================== GYM_SYSTEM.PY ====================
# Hệ thống quản lý phòng gym chính

from datetime import datetime, timedelta
from typing import Dict, List
from models import Member, Trainer, Admin, WorkoutSchedule, SubscriptionPlan, GymEquipment
from data_manager import DataManager

class GymManagementSystem:
    """Hệ thống quản lý phòng gym"""
    
    def __init__(self):
        self.data = {
            "members": {},
            "trainers": {},
            "admins": {},
            "workout_schedules": {},
            "subscription_plans": {},
            "gym_equipments": {}
        }
        self.current_user = None
        self.data_manager = DataManager()
        self.load_data()
    
    def load_data(self):
        """Tải dữ liệu"""
        self.data = self.data_manager.load_data()
    
    def save_data(self):
        """Lưu dữ liệu"""
        return self.data_manager.save_data(self.data)
    
    def get_users_for_login(self) -> Dict[str, List]:
        """Lấy danh sách users để hiển thị menu đăng nhập"""
        return {
            "Admins": [(uid, user.name, user.role) for uid, user in self.data["admins"].items()],
            "Trainers": [(uid, user.name, user.role) for uid, user in self.data["trainers"].items()],
            "Members": [(uid, user.name, user.role) for uid, user in self.data["members"].items()]
        }
    
    def check_permission(self, required_role: str) -> bool:
        """Kiểm tra quyền truy cập"""
        if not self.current_user:
            return False
        
        role_hierarchy = {
            "Admin": ["Admin"],
            "Trainer": ["Admin", "Trainer"], 
            "Member": ["Admin", "Trainer", "Member"]
        }
        
        return self.current_user.role in role_hierarchy.get(required_role, [])
    
    def login(self, user_id: str) -> bool:
        """Đăng nhập"""
        if user_id in self.data["members"]:
            self.current_user = self.data["members"][user_id]
            return True
        elif user_id in self.data["trainers"]:
            self.current_user = self.data["trainers"][user_id]
            return True
        elif user_id in self.data["admins"]:
            self.current_user = self.data["admins"][user_id]
            return True
        return False
    
    def logout(self):
        """Đăng xuất"""
        self.current_user = None
    
    # ==================== QUẢN LÝ THÀNH VIÊN ====================
    
    def add_member(self, user_id: str, name: str, email: str, phone: str, 
                   subscription_plan: str, gender: str = "", age: int = 0) -> bool:
        """Thêm thành viên mới"""
        if not self.check_permission("Admin"):
            print("Không có quyền thực hiện!")
            return False
        
        if user_id in self.data["members"]:
            print("ID đã tồn tại!")
            return False
            
        if subscription_plan not in self.data["subscription_plans"]:
            print("Gói đăng ký không tồn tại!")
            return False
        
        plan = self.data["subscription_plans"][subscription_plan]
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=plan.duration_months * 30)).strftime("%Y-%m-%d")
        
        member = Member(user_id, name, email, phone, subscription_plan, start_date, end_date, gender, age)
        self.data["members"][user_id] = member
        print(f"Đã thêm thành viên {name} thành công!")
        return True
    
    def remove_member(self, user_id: str) -> bool:
        """Xóa thành viên"""
        if not self.check_permission("Admin"):
            print("Không có quyền thực hiện!")
            return False
            
        if user_id not in self.data["members"]:
            print("Không tìm thấy thành viên!")
            return False
        
        # Xóa khỏi danh sách phân công của trainers
        for trainer in self.data["trainers"].values():
            if user_id in trainer.assigned_members:
                trainer.remove_member(user_id)
        
        del self.data["members"][user_id]
        print("Đã xóa thành viên thành công!")
        return True
    
    def renew_membership(self, user_id: str, new_plan: str) -> bool:
        """Gia hạn đăng ký"""
        if not (self.check_permission("Admin") or 
                (self.current_user and self.current_user.user_id == user_id)):
            print("Không có quyền thực hiện!")
            return False
            
        if user_id not in self.data["members"]:
            print("Không tìm thấy thành viên!")
            return False
            
        if new_plan not in self.data["subscription_plans"]:
            print("Gói đăng ký không tồn tại!")
            return False
        
        member = self.data["members"][user_id]
        plan = self.data["subscription_plans"][new_plan]
        
        current_end = datetime.strptime(member.subscription_end, "%Y-%m-%d")
        if current_end > datetime.now():
            new_end = current_end + timedelta(days=plan.duration_months * 30)
        else:
            new_end = datetime.now() + timedelta(days=plan.duration_months * 30)
        
        member.subscription_plan = new_plan
        member.subscription_end = new_end.strftime("%Y-%m-%d")
        print(f"Đã gia hạn đến {member.subscription_end} thành công!")
        return True
    
    # ==================== QUẢN LÝ TRAINER ====================
    
    def add_trainer(self, user_id: str, name: str, email: str, specialization: str) -> bool:
        """Thêm trainer"""
        if not self.check_permission("Admin"):
            print("Không có quyền thực hiện!")
            return False
        
        if user_id in self.data["trainers"]:
            print("ID đã tồn tại!")
            return False
        
        trainer = Trainer(user_id, name, email, specialization)
        self.data["trainers"][user_id] = trainer
        print(f"Đã thêm trainer {name} thành công!")
        return True
    
    def assign_member_to_trainer(self, trainer_id: str, member_id: str) -> bool:
        """Phân công thành viên cho trainer"""
        if not self.check_permission("Admin"):
            print("Không có quyền thực hiện!")
            return False
        
        if trainer_id not in self.data["trainers"] or member_id not in self.data["members"]:
            print("Không tìm thấy trainer hoặc member!")
            return False
        
        trainer = self.data["trainers"][trainer_id]
        trainer.assign_member(member_id)
        print("Đã phân công thành công!")
        return True
    
    # ==================== QUẢN LÝ THIẾT BỊ ====================
    
    def add_equipment(self, equipment_id: str, name: str, quantity: int, status: str = "Mới") -> bool:
        """Thêm thiết bị"""
        if not self.check_permission("Admin"):
            print("Không có quyền thực hiện!")
            return False
        
        if equipment_id in self.data["gym_equipments"]:
            print("ID thiết bị đã tồn tại!")
            return False
        
        equipment = GymEquipment(equipment_id, name, quantity, status)
        self.data["gym_equipments"][equipment_id] = equipment
        print(f"Đã thêm thiết bị {name} thành công!")
        return True
    
    def update_equipment_status(self, equipment_id: str, status: str) -> bool:
        """Cập nhật trạng thái thiết bị"""
        if not self.check_permission("Trainer"):
            print("Không có quyền thực hiện!")
            return False
        
        if equipment_id not in self.data["gym_equipments"]:
            print("Không tìm thấy thiết bị!")
            return False
        
        equipment = self.data["gym_equipments"][equipment_id]
        equipment.status = status
        print("Đã cập nhật trạng thái thiết bị thành công!")
        return True
    
    def schedule_maintenance(self, equipment_id: str, date: str) -> bool:
        """Lên lịch bảo trì"""
        if not self.check_permission("Trainer"):
            print("Không có quyền thực hiện!")
            return False
        
        if equipment_id not in self.data["gym_equipments"]:
            print("Không tìm thấy thiết bị!")
            return False
        
        equipment = self.data["gym_equipments"][equipment_id]
        equipment.maintenance_schedule = date
        equipment.status = "Cần bảo trì"
        print("Đã lên lịch bảo trì thành công!")
        return True
    
    # ==================== QUẢN LÝ LỊCH TẬP ====================
    
    def create_schedule(self, member_id: str, trainer_id: str, 
                       date: str, time: str, exercises: List[str]) -> bool:
        """Tạo lịch tập"""
        if not self.check_permission("Trainer"):
            print("Không có quyền thực hiện!")
            return False
        
        # Trainer chỉ tạo lịch cho thành viên được phân công
        if (self.current_user.role == "Trainer" and 
            member_id not in self.data["trainers"][self.current_user.user_id].assigned_members):
            print("Chỉ tạo lịch cho thành viên được phân công!")
            return False
        
        schedule_id = f"schedule_{len(self.data['workout_schedules']) + 1:04d}"
        schedule = WorkoutSchedule(schedule_id, member_id, trainer_id, date, time, exercises)
        self.data["workout_schedules"][schedule_id] = schedule
        print(f"Đã tạo lịch tập {schedule_id} thành công!")
        return True
    
    # ==================== ĐIỂM DANH ====================
    
    def mark_attendance(self, member_id: str, date: str = None, time: str = None) -> bool:
        """Điểm danh"""
        if not self.check_permission("Trainer"):
            print("Không có quyền thực hiện!")
            return False
            
        if member_id not in self.data["members"]:
            print("Không tìm thấy thành viên!")
            return False
        
        # Trainer chỉ điểm danh cho thành viên được phân công
        if (self.current_user.role == "Trainer" and 
            member_id not in self.data["trainers"][self.current_user.user_id].assigned_members):
            print("Chỉ điểm danh cho thành viên được phân công!")
            return False
            
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if time is None:
            time = datetime.now().strftime("%H:%M")
        
        member = self.data["members"][member_id]
        member.add_attendance_record(date, time)
        print(f"Đã điểm danh cho {member.name} thành công!")
        return True
    
    # ==================== TIẾN ĐỘ TẬP LUYỆN ====================
    
    def update_progress(self, member_id: str, exercise: str, progress: str) -> bool:
        """Cập nhật tiến độ"""
        if not (self.check_permission("Trainer") or 
                (self.current_user and self.current_user.user_id == member_id)):
            print("Không có quyền thực hiện!")
            return False
        
        if self.current_user.role == "Member":
            member_id = self.current_user.user_id
        
        if (self.current_user.role == "Trainer" and 
            member_id not in self.data["trainers"][self.current_user.user_id].assigned_members):
            print("Chỉ cập nhật cho thành viên được phân công!")
            return False
        
        if member_id not in self.data["members"]:
            print("Không tìm thấy thành viên!")
            return False
        
        member = self.data["members"][member_id]
        member.update_workout_progress(exercise, progress)
        print("Đã cập nhật tiến độ thành công!")
        return True
    
    def update_training_status(self, member_id: str, status: str) -> bool:
        """Cập nhật trạng thái tiến độ"""
        if not self.check_permission("Trainer"):
            print("Không có quyền thực hiện!")
            return False
        
        if (self.current_user.role == "Trainer" and 
            member_id not in self.data["trainers"][self.current_user.user_id].assigned_members):
            print("Chỉ cập nhật cho thành viên được phân công!")
            return False
        
        if member_id not in self.data["members"]:
            print("Không tìm thấy thành viên!")
            return False
        
        member = self.data["members"][member_id]
        member.training_progress_status = status
        print("Đã cập nhật trạng thái tiến độ thành công!")
        return True
    
    # ==================== BÁO CÁO ====================
    
    def get_revenue_report(self) -> dict:
        """Báo cáo doanh thu"""
        if not self.check_permission("Trainer"):
            print("Không có quyền xem báo cáo!")
            return {}
        
        total_revenue = 0
        active_members = 0
        expired_members = 0
        revenue_by_plan = {}
        
        for member in self.data["members"].values():
            plan = self.data["subscription_plans"].get(member.subscription_plan)
            if plan:
                total_revenue += plan.price
                
                if plan.name not in revenue_by_plan:
                    revenue_by_plan[plan.name] = {"count": 0, "revenue": 0}
                revenue_by_plan[plan.name]["count"] += 1
                revenue_by_plan[plan.name]["revenue"] += plan.price
            
            if member.is_membership_active():
                active_members += 1
            else:
                expired_members += 1
        
        return {
            "total_revenue": total_revenue,
            "total_members": len(self.data["members"]),
            "active_members": active_members,
            "expired_members": expired_members,
            "revenue_by_plan": revenue_by_plan
        }
    
    def get_attendance_report(self, start_date: str = None, end_date: str = None) -> dict:
        """Báo cáo điểm danh"""
        if self.current_user.role == "Member":
            member_id = self.current_user.user_id
            members_to_check = {member_id: self.data["members"][member_id]}
        elif self.current_user.role == "Trainer":
            trainer = self.data["trainers"][self.current_user.user_id]
            members_to_check = {mid: self.data["members"][mid] for mid in trainer.assigned_members if mid in self.data["members"]}
        else:  # Admin
            members_to_check = self.data["members"]
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        report = {}
        for member_id, member in members_to_check.items():
            attendance_in_period = []
            for record in member.attendance_records:
                date = record.split()[0]
                if start_date <= date <= end_date:
                    attendance_in_period.append(date)
            
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            total_days = (end_datetime - start_datetime).days + 1
            
            attendance_percentage = (len(attendance_in_period) / total_days) * 100 if total_days > 0 else 0
            
            report[member_id] = {
                "name": member.name,
                "attendance_days": len(attendance_in_period),
                "total_days": total_days,
                "attendance_percentage": round(attendance_percentage, 2),
                "subscription_plan": member.subscription_plan,
                "status": member.get_membership_status()
            }
        
        return report
    
    def calculate_statistics(self) -> dict:
        """Tính toán thống kê"""
        if not self.check_permission("Trainer"):
            print("Không có quyền xem thống kê!")
            return {}
        
        active_members = sum(1 for member in self.data["members"].values() if member.is_membership_active())
        expired_members = len(self.data["members"]) - active_members
        
        # Tỷ lệ điểm danh trung bình
        total_attendance = sum(len(member.attendance_records) for member in self.data["members"].values())
        avg_attendance = total_attendance / len(self.data["members"]) if self.data["members"] else 0
        
        # Thành viên xuất sắc nhất
        best_member = None
        best_score = 0
        for member in self.data["members"].values():
            score = len(member.workout_progress) * 2 + len(member.attendance_records)
            if score > best_score:
                best_score = score
                best_member = member.name
        
        # Thống kê theo gói đăng ký
        plan_stats = {}
        for member in self.data["members"].values():
            plan = member.subscription_plan
            if plan not in plan_stats:
                plan_stats[plan] = {"active": 0, "expired": 0}
            
            if member.is_membership_active():
                plan_stats[plan]["active"] += 1
            else:
                plan_stats[plan]["expired"] += 1
        
        # Thống kê thiết bị
        equipment_stats = {}
        for eq in self.data["gym_equipments"].values():
            status = eq.status
            if status not in equipment_stats:
                equipment_stats[status] = 0
            equipment_stats[status] += eq.quantity
        
        return {
            "active_members": active_members,
            "expired_members": expired_members,
            "total_members": len(self.data["members"]),
            "average_attendance": round(avg_attendance, 2),
            "best_performance_member": best_member,
            "plan_statistics": plan_stats,
            "equipment_statistics": equipment_stats,
            "total_trainers": len(self.data["trainers"]),
            "total_schedules": len(self.data["workout_schedules"])
        }
    
    # ==================== XUẤT DỮ LIỆU ====================
    
    def export_to_csv(self, data_type: str, filename: str, format_type: str = "utf-8"):
        """Xuất dữ liệu ra CSV"""
        if not self.check_permission("Trainer"):
            print("Không có quyền xuất dữ liệu!")
            return False
        
        return self.data_manager.export_to_csv(self.data, data_type, filename, format_type)