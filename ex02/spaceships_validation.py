
from typing import List

from pydantic import (
    BaseModel,
    ValidationError,
    model_validator,
)

import spaceships_config


class Spaceship(BaseModel):
    alignment: bool
    name: str
    class_: str
    length: float
    crew_size: int
    armed: bool
    officers: List[dict]

    @model_validator(mode="after")
    def validation_ship_name(self):
        if self.alignment != "Enemy" and self.name == "Unknowm":
            raise ValueError("Ally ships cant be unknown")
        return self

    @model_validator(mode="after")
    def validation_type_ship(self):
        class_data = {
            "Corvette": (80, 250, 4, 10, True, True),
            "Frigate": (300, 600, 10, 15, True, False),
            "Cruiser": (500, 1000, 15, 30, True, True),
            "Destroyer": (800, 2000, 50, 80, True, False),
            "Carrier": (1000, 4000, 120, 250, False, True),
            "Dreadnought": (5000, 20000, 300, 500, True, True),
        }

        min_len, max_len, min_cr, max_cr, need_arm, need_al = class_data[
            self.class_]
        if min_len > self.length or self.length > max_len:
            raise ValueError(
                f"The length is not correct {self.length} for {self.class_}")
        if min_cr > self.crew_size or self.crew_size > max_cr:
            raise ValueError(
                f"crew_size is not correct {self.length} for {self.class_}")
        if self.armed != need_arm:
            raise ValueError(
                f"The armed is not correct {self.length} for {self.class_}")
        if self.alignment != need_al:
            raise ValueError(
                f"The aligment is not correct {self.length} for {self.class_}")
        return self
