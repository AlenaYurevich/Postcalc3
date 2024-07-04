class DeclaredValue:
    def __init__(self, value):
        self.value = value

    def cost_for_declared_value(self):
        if not self.value or self.value in ("нет", "", 0, "0"):
            return 0
        res = round(float(self.value) * 3 / 100, 4)
        return res


item_declared_value = DeclaredValue(5.85)
print(item_declared_value.cost_for_declared_value())
