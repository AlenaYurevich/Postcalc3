notification_costs = {
    1: 0.65,
    2: 2.10,
    3: 0.45,
    4: 0.00,
}


def notification_cost(notification):
    if not isinstance(notification, int) or notification not in notification_costs:
        raise ValueError("Invalid notification type. Must be one of: 1, 2, 3, 4.")
    return notification_costs.get(notification)
