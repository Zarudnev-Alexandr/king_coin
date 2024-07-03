# import datetime
#
# from pydantic import BaseModel
#
#
# class UserBase(BaseModel):
#     tg_id: int
#     lvl: int
#     is_admin: bool
#     is_banned: bool
#     money: int
#     current_factor: float
#
#
# class UserCreate(UserBase):
#     username: str
#     fio: str
#     last_login_date: datetime.date
#     days_in_row: int

from pydantic import BaseModel
from datetime import datetime, date

class UserBase(BaseModel):
    tg_id: int
    username: str
    fio: str
    lvl: int
    is_admin: bool
    is_banned: bool
    money: int
    current_factor: float
    invited_tg_id: int
    last_login_date: date
    days_in_row: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True

class UpgradeCategoryBase(BaseModel):
    category: str

class UpgradeCategoryCreate(UpgradeCategoryBase):
    pass

class UpgradeCategory(UpgradeCategoryBase):
    id: int

    class Config:
        orm_mode = True

class UpgradeBase(BaseModel):
    name: str
    category_id: int
    image_url: str

class UpgradeCreate(UpgradeBase):
    pass

class Upgrade(UpgradeBase):
    id: int

    class Config:
        orm_mode = True

class UpgradeLevelBase(BaseModel):
    upgrade_id: int
    lvl: int
    factor: float
    price: int

class UpgradeLevelCreate(UpgradeLevelBase):
    pass

class UpgradeLevel(UpgradeLevelBase):
    pass

    class Config:
        orm_mode = True

class UserUpgradeBase(BaseModel):
    user_id: int
    upgrade_id: int
    lvl: int

class UserUpgradeCreate(UserUpgradeBase):
    pass

class UserUpgrade(UserUpgradeBase):
    pass

    class Config:
        orm_mode = True

class DailyRewardBase(BaseModel):
    day: int
    reward: int

class DailyRewardCreate(DailyRewardBase):
    pass

class DailyReward(DailyRewardBase):
    pass

    class Config:
        orm_mode = True

class ClickBase(BaseModel):
    user_id: int

class ClickCreate(ClickBase):
    pass

class Click(ClickBase):
    pass

    class Config:
        orm_mode = True


