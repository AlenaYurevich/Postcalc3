"""
Плата за внутренние уведомления, руб. без НДС
"""
notification_costs = {
    1: 0.70,
    2: 2.20,
    3: 0.45,
    4: 0.00,
}


def notification_cost(notification):
    if not isinstance(notification, int) or notification not in notification_costs:
        raise ValueError("Invalid notification type. Must be one of: 1, 2, 3, 4.")
    return notification_costs.get(notification)


"""
Плата за отслеживание и дополнительную обработку международных писем, мелких пакетов, посылок руб.без НДС
"""
TRACKED_RATE = 5.05
REGISTERED_RATE = 9.65
VALUE_RATE = 11.45
PARCEL_VALUE_RATE = 6.15
