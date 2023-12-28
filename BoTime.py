class BoTime:
    def __init__(self, minutes, seconds):
        self.__minutes = minutes
        self.__seconds = seconds

    def parse(self, data):
        spliter = data.split(":")

        self.__seconds = int(spliter[0])
        self.__minutes = int(spliter[1])

    def encode(self):
        flux = ""

        if self.__minutes < 10:
            flux += "0"
        flux += str(self.__minutes) + ":"

        if self.__seconds < 10:
            flux += "0"
        flux += str(self.__seconds)

        return flux

    def getTime(self):
        return (self.__minutes, self.__seconds)

    def getTimeSeconds(self):
        return self.__minutes*60 + self.__seconds

def diffBoTime(t1, t2):
    m1, s1 = t1.getTime()
    m2, s2 = t2.getTime()

    total1 = m1*60 + s1
    total2 = m2*60 + s2

    return total2 - total1
