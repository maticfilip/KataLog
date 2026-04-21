from datetime import datetime, date, timedelta

today = datetime.now()

start_of_week = today.replace(hour=0, minute=0, second=0, microsecond=0) \
                    - timedelta(days=today.weekday())

end_of_week = start_of_week + timedelta(days=6)

print(start_of_week, end_of_week)