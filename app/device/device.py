from app.device.meter import Meter, MeterData


class Device:

    def __init__(self, year):
        self.meters: list[Meter] = list()
        for i in range(1, 3):
            self.meters.append(Meter(year, i))


if __name__ == "__main__":
    device = Device(2016)
