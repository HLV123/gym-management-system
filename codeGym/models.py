# ==================== MODELS.PY ====================
# Các lớp đối tượng cơ bản

from datetime import datetime, timedelta
from typing import List

class User:
    """Lớp người dùng cơ bản"""
    def __init__(self, user_id: str, name: str, email: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

class Member(User):
    """Lớp thành viên phòng gym"""
    def __init__(self, user_id: str, name: str, email: str, phone: str, 
                 subscription_plan: str, subscription_start: str, subscription_end: str,
                 gender: str = "", age: int = 0):
        super().__init__(user_id, name, email, "Member")
        self.phone = phone
        self.gender = gender
        self.age = age
        self.subscription_plan = subscription_plan
        self.subscription_start = subscription_start
        self.subscription_end = subscription_end
        self.workout_progress = {}
        self.attendance_records = []
        self.training_progress_status = "Chưa đánh giá"
    
    def is_membership_active(self) -> bool:
        """Kiểm tra thành viên còn trong thời gian đăng ký không"""
        end_date = datetime.strptime(self.subscription_end, "%Y-%m-%d")
        return datetime.now() <= end_date
    
    def get_membership_status(self) -> str:
        """Lấy trạng thái đăng ký"""
        if not self.is_membership_active():
            return "Hết hạn"
        
        end_date = datetime.strptime(self.subscription_end, "%Y-%m-%d")
        days_remaining = (end_date - datetime.now()).days
        
        if days_remaining <= 7:
            return "Sắp hết hạn"
        elif days_remaining <= 30:
            return "Bình thường"
        else:
            return "Mới đăng ký"
    
    def get_remaining_days(self) -> int:
        """Lấy số ngày còn lại"""
        end_date = datetime.strptime(self.subscription_end, "%Y-%m-%d")
        remaining = (end_date - datetime.now()).days
        return max(0, remaining)
    
    def add_attendance_record(self, date: str, time: str):
        """Thêm ngày điểm danh"""
        attendance_entry = f"{date} {time}"
        if date not in [record.split()[0] for record in self.attendance_records]:
            self.attendance_records.append(attendance_entry)
    
    def update_workout_progress(self, exercise: str, progress: str):
        """Cập nhật tiến độ tập luyện"""
        self.workout_progress[exercise] = progress

class Trainer(User):
    """Lớp huấn luyện viên"""
    def __init__(self, user_id: str, name: str, email: str, specialization: str):
        super().__init__(user_id, name, email, "Trainer")
        self.specialization = specialization
        self.assigned_members = []
    
    def assign_member(self, member_id: str):
        """Phân công thành viên"""
        if member_id not in self.assigned_members:
            self.assigned_members.append(member_id)
    
    def remove_member(self, member_id: str):
        """Xóa thành viên khỏi danh sách"""
        if member_id in self.assigned_members:
            self.assigned_members.remove(member_id)

class Admin(User):
    """Lớp quản trị viên"""
    def __init__(self, user_id: str, name: str, email: str):
        super().__init__(user_id, name, email, "Admin")

class GymEquipment:
    """Lớp thiết bị phòng gym"""
    def __init__(self, equipment_id: str, name: str, quantity: int, 
                 status: str = "Mới", maintenance_schedule: str = ""):
        self.equipment_id = equipment_id
        self.name = name
        self.quantity = quantity
        self.status = status
        self.maintenance_schedule = maintenance_schedule

class WorkoutSchedule:
    """Lớp lịch tập luyện"""
    def __init__(self, schedule_id: str, member_id: str, trainer_id: str, 
                 date: str, time: str, exercises: List[str]):
        self.schedule_id = schedule_id
        self.member_id = member_id
        self.trainer_id = trainer_id
        self.date = date
        self.time = time
        self.exercises = exercises
        self.completed = False

class SubscriptionPlan:
    """Lớp gói đăng ký"""
    def __init__(self, plan_id: str, name: str, duration_months: int, 
                 price: float, features: List[str]):
        self.plan_id = plan_id
        self.name = name
        self.duration_months = duration_months
        self.price = price
        self.features = features