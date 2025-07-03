# ==================== DATA_MANAGER.PY ====================
# Quản lý dữ liệu và tạo dữ liệu mẫu

import json
import csv
import random
from datetime import datetime, timedelta
from models import Member, Trainer, Admin, WorkoutSchedule, SubscriptionPlan, GymEquipment

class DataManager:
    """Quản lý dữ liệu và tạo dữ liệu mẫu"""
    
    def create_sample_data(self):
        """Tạo dữ liệu mẫu phong phú"""
        data = {
            "members": {},
            "trainers": {},
            "admins": {},
            "workout_schedules": {},
            "subscription_plans": {},
            "gym_equipments": {}
        }
        
        # 1 Admin
        admin = Admin("admin01", "Nguyễn Văn Quản", "admin@fitnesszone.com")
        data["admins"][admin.user_id] = admin
        
        # 3 Trainers
        trainers_data = [
            ("trainer01", "Trần Thị Hương", "huong@fitnesszone.com", "Yoga & Pilates"),
            ("trainer02", "Lê Văn Mạnh", "manh@fitnesszone.com", "Gym & Strength Training"),
            ("trainer03", "Phạm Minh Tuấn", "tuan@fitnesszone.com", "Cardio & Aerobic")
        ]
        
        for trainer_data in trainers_data:
            trainer = Trainer(*trainer_data)
            data["trainers"][trainer.user_id] = trainer
        
        # Gói đăng ký
        plans = [
            SubscriptionPlan("normal", "Gói Cơ Bản", 1, 500000, 
                           ["Sử dụng thiết bị cơ bản", "Phòng tập chung"]),
            SubscriptionPlan("big", "Gói Nâng Cao", 3, 1200000, 
                           ["Sử dụng tất cả thiết bị", "Hướng dẫn cơ bản", "Phòng xông hơi"]),
            SubscriptionPlan("vip", "Gói VIP", 6, 2000000, 
                           ["Tất cả thiết bị", "Huấn luyện 1:1", "Tư vấn dinh dưỡng", "Massage"]),
            SubscriptionPlan("family", "Gói Gia Đình", 12, 3500000, 
                           ["Tất cả dịch vụ", "Cho 2-4 người", "Ưu tiên booking"])
        ]
        for plan in plans:
            data["subscription_plans"][plan.plan_id] = plan
        
        # 10 Members
        members_data = [
            ("member001", "Nguyễn Thị Lan", "lan.nguyen@email.com", "0901234567", "normal", "Nữ", 25),
            ("member002", "Trần Văn Nam", "nam.tran@email.com", "0901234568", "big", "Nam", 30),
            ("member003", "Lê Thị Mai", "mai.le@email.com", "0901234569", "vip", "Nữ", 28),
            ("member004", "Phạm Văn Hùng", "hung.pham@email.com", "0901234570", "family", "Nam", 35),
            ("member005", "Hoàng Thị Linh", "linh.hoang@email.com", "0901234571", "normal", "Nữ", 22),
            ("member006", "Đặng Văn Tùng", "tung.dang@email.com", "0901234572", "big", "Nam", 27),
            ("member007", "Vũ Thị Hoa", "hoa.vu@email.com", "0901234573", "vip", "Nữ", 32),
            ("member008", "Bùi Văn Thắng", "thang.bui@email.com", "0901234574", "normal", "Nam", 29),
            ("member009", "Đinh Thị Thu", "thu.dinh@email.com", "0901234575", "big", "Nữ", 26),
            ("member010", "Ngô Văn Đức", "duc.ngo@email.com", "0901234576", "family", "Nam", 33)
        ]
        
        # Tạo members với dữ liệu ngẫu nhiên
        for i, member_data in enumerate(members_data):
            user_id, name, email, phone, subscription_plan, gender, age = member_data
            plan = data["subscription_plans"][subscription_plan]
            
            # Ngày bắt đầu ngẫu nhiên trong 6 tháng qua
            days_ago = random.randint(0, 180)
            start_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            end_date = (datetime.now() - timedelta(days=days_ago) + 
                       timedelta(days=plan.duration_months * 30)).strftime("%Y-%m-%d")
            
            member = Member(user_id, name, email, phone, subscription_plan, start_date, end_date, gender, age)
            
            # Thêm dữ liệu điểm danh và tiến độ ngẫu nhiên
            self._add_random_data(member, days_ago)
            
            data["members"][user_id] = member
        
        # Phân công members cho trainers
        member_ids = list(data["members"].keys())
        trainer_ids = list(data["trainers"].keys())
        
        for i, member_id in enumerate(member_ids):
            trainer_id = trainer_ids[i % len(trainer_ids)]
            data["trainers"][trainer_id].assign_member(member_id)
        
        # Thiết bị phòng gym
        equipments = [
            GymEquipment("eq001", "Máy chạy bộ Life Fitness", 8, "Đang sử dụng"),
            GymEquipment("eq002", "Máy duỗi chân Technogym", 5, "Đang sử dụng"),
            GymEquipment("eq003", "Tạ đòn Olympic", 15, "Đang sử dụng"),
            GymEquipment("eq004", "Máy đấm bao cát", 3, "Cần bảo trì", "2025-07-15"),
            GymEquipment("eq005", "Xe đạp tập Matrix", 10, "Đang sử dụng"),
            GymEquipment("eq006", "Máy kéo xô Hammer Strength", 4, "Đang sử dụng"),
            GymEquipment("eq007", "Thảm Yoga", 20, "Đang sử dụng"),
            GymEquipment("eq008", "Máy cáp đa năng", 6, "Đang sử dụng"),
            GymEquipment("eq009", "Ghế tập ngực", 8, "Đang sử dụng"),
            GymEquipment("eq010", "Máy Smith", 2, "Cần bảo trì", "2025-07-20")
        ]
        for equipment in equipments:
            data["gym_equipments"][equipment.equipment_id] = equipment
        
        # Tạo lịch tập mẫu
        data["workout_schedules"] = self._create_sample_schedules(
            list(data["members"].keys()), 
            list(data["trainers"].keys())
        )
        
        return data
    
    def _add_random_data(self, member: Member, days_since_start: int):
        """Thêm dữ liệu điểm danh và tiến độ ngẫu nhiên"""
        # Tần suất điểm danh theo gói
        frequency_map = {
            "normal": 0.3, "big": 0.5, "vip": 0.7, "family": 0.6
        }
        frequency = frequency_map.get(member.subscription_plan, 0.3)
        
        # Tạo điểm danh ngẫu nhiên
        for i in range(min(days_since_start, 90)):
            if random.random() < frequency:
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                time = f"{random.randint(6, 21):02d}:{random.randint(0, 59):02d}"
                member.add_attendance_record(date, time)
        
        # Tạo tiến độ tập luyện
        exercises = ["Bench Press", "Squat", "Deadlift", "Pull-up", "Push-up", "Plank", "Running"]
        member_exercises = random.sample(exercises, random.randint(3, 5))
        
        for exercise in member_exercises:
            if exercise in ["Bench Press", "Squat", "Deadlift"]:
                progress = f"{random.randint(40, 120)}kg x {random.randint(5, 12)} reps"
            elif exercise in ["Pull-up", "Push-up"]:
                progress = f"{random.randint(5, 30)} reps"
            elif exercise == "Plank":
                progress = f"{random.randint(30, 180)} seconds"
            elif exercise == "Running":
                progress = f"{random.randint(3, 10)}km in {random.randint(15, 60)} mins"
            
            member.update_workout_progress(exercise, progress)
        
        # Random training status
        statuses = ["Tốt", "Chưa tốt", "Cần quan tâm nhiều hơn", "Xuất sắc"]
        member.training_progress_status = random.choice(statuses)
    
    def _create_sample_schedules(self, member_ids: list, trainer_ids: list) -> dict:
        """Tạo lịch tập mẫu"""
        schedules = {}
        
        exercises_by_trainer = {
            "trainer01": ["Yoga Flow", "Pilates Core", "Stretching", "Meditation"],
            "trainer02": ["Strength Training", "Weight Lifting", "Muscle Building", "Powerlifting"],
            "trainer03": ["Cardio Blast", "HIIT", "Aerobic Dance", "Fat Burning"]
        }
        
        for i in range(15):
            schedule_id = f"schedule_{i+1:04d}"
            member_id = random.choice(member_ids)
            trainer_id = random.choice(trainer_ids)
            
            future_date = (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
            time = f"{random.randint(6, 20):02d}:{random.choice(['00', '30'])}"
            
            available_exercises = exercises_by_trainer.get(trainer_id, ["General Training"])
            exercises = random.sample(available_exercises, random.randint(1, 3))
            
            schedule = WorkoutSchedule(schedule_id, member_id, trainer_id, future_date, time, exercises)
            schedules[schedule_id] = schedule
        
        return schedules
    
    def save_data(self, data: dict, filename: str = "gym_data.json"):
        """Lưu dữ liệu ra file JSON"""
        serializable_data = {
            "members": {mid: {
                "user_id": m.user_id, "name": m.name, "email": m.email, "phone": m.phone,
                "gender": m.gender, "age": m.age, "subscription_plan": m.subscription_plan,
                "subscription_start": m.subscription_start, "subscription_end": m.subscription_end,
                "workout_progress": m.workout_progress, "attendance_records": m.attendance_records,
                "training_progress_status": m.training_progress_status
            } for mid, m in data["members"].items()},
            
            "trainers": {tid: {
                "user_id": t.user_id, "name": t.name, "email": t.email,
                "specialization": t.specialization, "assigned_members": t.assigned_members
            } for tid, t in data["trainers"].items()},
            
            "admins": {aid: {
                "user_id": a.user_id, "name": a.name, "email": a.email
            } for aid, a in data["admins"].items()},
            
            "gym_equipments": {eid: {
                "equipment_id": e.equipment_id, "name": e.name, "quantity": e.quantity,
                "status": e.status, "maintenance_schedule": e.maintenance_schedule
            } for eid, e in data["gym_equipments"].items()},
            
            "workout_schedules": {sid: {
                "schedule_id": s.schedule_id, "member_id": s.member_id, "trainer_id": s.trainer_id,
                "date": s.date, "time": s.time, "exercises": s.exercises, "completed": s.completed
            } for sid, s in data["workout_schedules"].items()},
            
            "subscription_plans": {pid: {
                "plan_id": p.plan_id, "name": p.name, "duration_months": p.duration_months,
                "price": p.price, "features": p.features
            } for pid, p in data["subscription_plans"].items()}
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
            print("Đã lưu dữ liệu thành công!")
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
            return False
    
    def load_data(self, filename: str = "gym_data.json") -> dict:
        """Tải dữ liệu từ file JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            data = {
                "members": {},
                "trainers": {},
                "admins": {},
                "workout_schedules": {},
                "subscription_plans": {},
                "gym_equipments": {}
            }
            
            # Load subscription plans first
            for pid, p_data in json_data.get("subscription_plans", {}).items():
                plan = SubscriptionPlan(
                    p_data["plan_id"], p_data["name"], p_data["duration_months"],
                    p_data["price"], p_data["features"]
                )
                data["subscription_plans"][pid] = plan
            
            # Load members
            for mid, m_data in json_data.get("members", {}).items():
                member = Member(
                    m_data["user_id"], m_data["name"], m_data["email"], m_data["phone"],
                    m_data["subscription_plan"], m_data["subscription_start"], m_data["subscription_end"],
                    m_data.get("gender", ""), m_data.get("age", 0)
                )
                member.workout_progress = m_data.get("workout_progress", {})
                member.attendance_records = m_data.get("attendance_records", [])
                member.training_progress_status = m_data.get("training_progress_status", "Chưa đánh giá")
                data["members"][mid] = member
            
            # Load trainers
            for tid, t_data in json_data.get("trainers", {}).items():
                trainer = Trainer(t_data["user_id"], t_data["name"], t_data["email"], t_data["specialization"])
                trainer.assigned_members = t_data.get("assigned_members", [])
                data["trainers"][tid] = trainer
            
            # Load admins
            for aid, a_data in json_data.get("admins", {}).items():
                admin = Admin(a_data["user_id"], a_data["name"], a_data["email"])
                data["admins"][aid] = admin
            
            # Load equipment
            for eid, e_data in json_data.get("gym_equipments", {}).items():
                equipment = GymEquipment(
                    e_data["equipment_id"], e_data["name"], e_data["quantity"],
                    e_data.get("status", "Mới"), e_data.get("maintenance_schedule", "")
                )
                data["gym_equipments"][eid] = equipment
            
            # Load schedules
            for sid, s_data in json_data.get("workout_schedules", {}).items():
                schedule = WorkoutSchedule(
                    s_data["schedule_id"], s_data["member_id"], s_data["trainer_id"],
                    s_data["date"], s_data["time"], s_data["exercises"]
                )
                schedule.completed = s_data.get("completed", False)
                data["workout_schedules"][sid] = schedule
            
            print("Đã tải dữ liệu từ file thành công!")
            return data
            
        except FileNotFoundError:
            print("Không tìm thấy file dữ liệu, tạo dữ liệu mẫu mới")
            return self.create_sample_data()
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            return self.create_sample_data()
    
    def export_to_csv(self, data: dict, data_type: str, filename: str, format_type: str = "utf-8"):
        """Xuất dữ liệu ra CSV"""
        encoding = "utf-8-sig" if format_type == "excel" else "utf-8"
        
        try:
            if data_type == "members":
                with open(filename, 'w', newline='', encoding=encoding) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "ID", "Tên", "Email", "Điện thoại", "Giới tính", "Tuổi",
                        "Gói đăng ký", "Ngày bắt đầu", "Ngày kết thúc", "Trạng thái",
                        "Số ngày còn lại", "Tiến độ", "Số lần điểm danh"
                    ])
                    for member in data["members"].values():
                        writer.writerow([
                            member.user_id, member.name, member.email, member.phone,
                            member.gender, member.age, member.subscription_plan,
                            member.subscription_start, member.subscription_end,
                            member.get_membership_status(), member.get_remaining_days(),
                            member.training_progress_status, len(member.attendance_records)
                        ])
            
            elif data_type == "attendance":
                with open(filename, 'w', newline='', encoding=encoding) as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID thành viên", "Tên", "Ngày", "Giờ", "Gói đăng ký"])
                    for member in data["members"].values():
                        for record in member.attendance_records:
                            parts = record.split()
                            date = parts[0] if len(parts) > 0 else ""
                            time = parts[1] if len(parts) > 1 else ""
                            writer.writerow([
                                member.user_id, member.name, date, time, member.subscription_plan
                            ])
            
            elif data_type == "trainers":
                with open(filename, 'w', newline='', encoding=encoding) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "ID", "Tên", "Email", "Chuyên môn", "Số thành viên được phân công"
                    ])
                    for trainer in data["trainers"].values():
                        writer.writerow([
                            trainer.user_id, trainer.name, trainer.email,
                            trainer.specialization, len(trainer.assigned_members)
                        ])
            
            elif data_type == "equipment":
                with open(filename, 'w', newline='', encoding=encoding) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "ID thiết bị", "Tên", "Số lượng", "Trạng thái", "Lịch bảo trì"
                    ])
                    for equipment in data["gym_equipments"].values():
                        writer.writerow([
                            equipment.equipment_id, equipment.name, equipment.quantity,
                            equipment.status, equipment.maintenance_schedule or "Không có"
                        ])
            
            format_name = "Excel/WPS" if format_type == "excel" else "UTF-8"
            print(f"Đã xuất {data_type} ra file {filename} (định dạng {format_name}) thành công!")
            return True
            
        except Exception as e:
            print(f"Lỗi khi xuất file: {e}")
            return False