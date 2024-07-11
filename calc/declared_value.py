def cost_for_declared_value(declared_value):
    if not declared_value or declared_value in ("нет", "", 0, "0"):
        return 0
    res = round(float(declared_value) * 3 / 100, 4)
    return res
