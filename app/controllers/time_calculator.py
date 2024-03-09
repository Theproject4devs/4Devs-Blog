def calculate_time_since_creation(created_at):
    from datetime import datetime
    created_at_datetime = datetime.strptime(created_at, '%d/%m/%Y %H:%M')
    current_datetime = datetime.now()
    difference = current_datetime - created_at_datetime
    days = difference.days
    hours = difference.seconds // 3600
    minutes = (difference.seconds % 3600) // 60
    return hours, minutes, days
