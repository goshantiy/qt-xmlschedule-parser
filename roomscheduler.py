from datetime import datetime, timedelta

class RoomScheduler:
    def __init__(self, room_data):
        self.room_data = room_data
        self.schedule = self.create_schedule()

    def create_schedule(self):
        schedule = {}
        for room_id, room_data_list in self.room_data.items():
            # Предполагаем, что в списке всегда есть хотя бы один элемент
            room_data = room_data_list[0]
            work_hours = room_data['work_hours']

            # Создаем пустой словарь для расписания данной аудитории
            room_schedule = {}

            # Проходимся по всем неделям
            for week in work_hours:
                # Создаем пустой список для хранения рабочих часов текущей недели
                week_schedule = []

                # Проходимся по всем дням в текущей неделе
                for day_schedule in work_hours[week].values():
                    # Преобразуем строку в число для удобства обработки
                    day_schedule_int = int(day_schedule)
                    
                    # Проверяем каждый бит в числе и добавляем часы работы в список, если бит равен 1
                    for i in range(7):  # Предполагаем, что всегда 7 дней в неделе
                        if day_schedule_int & (1 << i):
                            # Если i-й бит равен 1, это рабочий час
                            week_schedule.append(i + 1)  # Добавляем номер рабочего дня в список

                # Добавляем список рабочих часов текущей недели в общее расписание аудитории
                room_schedule[week] = week_schedule

            # Добавляем расписание текущей аудитории в общее расписание
            schedule[room_id] = room_schedule

        return schedule


    def get_date_from_week_and_day(self, week_number, day_of_week):
        start_date = datetime(2024, 2, 1)  # Начальная дата
        week_delta = timedelta(weeks=week_number)  # Дельта для номера недели
        day_delta = timedelta(days=day_of_week)  # Дельта для дня недели
        target_date = start_date + week_delta + day_delta
        return target_date.strftime('%d.%m.%Y')