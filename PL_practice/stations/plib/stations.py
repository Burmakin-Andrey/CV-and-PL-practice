import json


class PointError(Exception):
    ...






class Point:

    def __init__(self, x: float, y: float) -> None:
        

        if not isinstance(x, float) or not isinstance(y, float):
            raise PointError("x should be float")

        self.x = x
        self.y = y


    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            if hasattr(other, "__iter__"):
                return self == Point(*other)
            else:
                raise NotImplementedError
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def to_json(self) -> str:
        return json.dumps({"x": self.x, "y": self.y})

    @classmethod
    def from_json(cls, js: dict) -> "Point":
        x = 0.0
        y = 0.0
        if "lat" in js["location"] and "lon" in js["location"]:
            return cls(float(js["location"]["lat"]), float(js["location"]["lon"]))
            
        else:
            if  "lat" not in js["location"] and "lon" in js["location"]:
                return cls(x, float(js["location"]["lon"]))

            elif  "lat" in js["location"] and "lon" not in js["location"]:
                return cls(float(js["location"]["lat"]), y)

            else:
                return cls(0.0, 0.0)
    
    def perimetr(self, other1: "Point", other2: "Point") -> float:
        return (self.distance_to(other1) + self.distance_to(other2) + other1.distance_to(other2)) * 0.5
            
    def find_triangl(self, other1: "Point", other2: "Point") -> float:
        p = self.perimetr(other1, other2)
        return (p * (p - self.distance_to(other1)) * (p - self.distance_to(other2)) * (p - other1.distance_to(other2))) ** 0.5

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y}"

    def is_center(self: "Point") -> bool:
        return self == Point(0, 0)
    

class Stations:
    def __init__(self, file_name):
        self.points = []
        with open(file_name) as f:
            file_content = json.load(f)

            
        for station in file_content:
                self.points.append(Point.from_json(station))        
                        
    def find_min_tri(self):         
        minS = 100000.0
        for i in range(len(self.points) - 2):
            for j in range(i + 1, len(self.points) - 1):
                for k in range(j + 1, len(self.points)):
                    s = self.points[i].find_triangl(self.points[j], self.points[k])
                    if s < minS:
                        minS = s

        return minS
    