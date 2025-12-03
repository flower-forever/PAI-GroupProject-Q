from dataclasses import dataclass


@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    email: str
    password: str
    year: int


    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __post_init__(self):
        # year must be integer
        if not isinstance(self.year, int):
            raise TypeError(f"Year must be an integer, got {type(self.year).__name__}")

        # year must greater than 0
        if self.year < 1:
            raise ValueError(f"Year must be a positive integer, got {self.year}")

        # check email format
        if "@" not in self.email:
            raise ValueError("Invalid email format")