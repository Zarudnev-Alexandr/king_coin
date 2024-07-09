import datetime
from typing import Optional, List

from pydantic import BaseModel


class UserCreate(BaseModel):
    tg_id: int
    username: str
    fio: str
    invited_tg_id: Optional[int]


class UserBase(UserCreate):

    lvl: int
    is_admin: bool
    is_banned: bool
    money: int
    current_factor: float
    days_in_row: int

    class Config:
        orm_mode = True
        from_attributes = True


class UpgradeLevelSchema(BaseModel):
    upgrade_id: int
    lvl: int
    factor: float
    price: int


class CreateUpgradeSchema(BaseModel):
    name: str
    category_id: int
    image_url: str
    is_in_shop: bool


#Улучшение (карточка) без уровней
class UpgradeSchema(CreateUpgradeSchema):
    id: int


#Улучшение (карточка) со всеми уровнями внутри
class UpgradeWithLevelsSchema(CreateUpgradeSchema):
    id: int

    levels: List[UpgradeLevelSchema]


class UpgradeWithoutLevelsSchema(CreateUpgradeSchema):
    id: int
    lvl: int
    is_bought: bool
    factor: float
    price_of_next_lvl: Optional[int]

    # levels: List[UpgradeLevelSchema]


# class UpgradeCategoryCreateSchema(BaseModel):
#     category: str
#
#     upgrades: List[UpgradeWithLevelsSchema]


class UpgradeCategoryCreateSchema(BaseModel):
    category: str

    upgrades: List[UpgradeWithoutLevelsSchema]


class UpgradeCategorySchema(UpgradeCategoryCreateSchema):
    id: int


#Покупка улушение (апгрейд с 0 до 1 уровня)
class UserUpgradeCreateSchema(BaseModel):
    user_id: int
    upgrade_id: int


#Купленные пользователем карты
class UserUpgradeSchema(UserUpgradeCreateSchema):
    lvl: int

    user: UserBase
    upgrade: UpgradeSchema



# class UserBase(BaseModel):
#     tg_id: int
#     username: str
#     fio: str
#     lvl: int
#     is_admin: bool
#     is_banned: bool
#     money: int
#     current_factor: float
#     invited_tg_id: int
#     last_login_date: date
#     days_in_row: int
#     created: datetime
#     updated: datetime
#
# class UserCreate(UserBase):
#     pass

# class User(UserBase):
#     created: datetime
#     updated: datetime
#
#     class Config:
#         orm_mode = True
#
# class UpgradeCategoryBase(BaseModel):
#     category: str
#
# class UpgradeCategoryCreate(UpgradeCategoryBase):
#     pass
#
# class UpgradeCategory(UpgradeCategoryBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
# class UpgradeBase(BaseModel):
#     name: str
#     category_id: int
#     image_url: str
#
# class UpgradeCreate(UpgradeBase):
#     pass
#
# class Upgrade(UpgradeBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
# class UpgradeLevelBase(BaseModel):
#     upgrade_id: int
#     lvl: int
#     factor: float
#     price: int
#
# class UpgradeLevelCreate(UpgradeLevelBase):
#     pass
#
# class UpgradeLevel(UpgradeLevelBase):
#     pass
#
#     class Config:
#         orm_mode = True
#
# class UserUpgradeBase(BaseModel):
#     user_id: int
#     upgrade_id: int
#     lvl: int
#
# class UserUpgradeCreate(UserUpgradeBase):
#     pass
#
# class UserUpgrade(UserUpgradeBase):
#     pass
#
#     class Config:
#         orm_mode = True
#
# class DailyRewardBase(BaseModel):
#     day: int
#     reward: int
#
# class DailyRewardCreate(DailyRewardBase):
#     pass
#
# class DailyReward(DailyRewardBase):
#     pass
#
#     class Config:
#         orm_mode = True
#
# class ClickBase(BaseModel):
#     user_id: int
#
# class ClickCreate(ClickBase):
#     pass
#
# class Click(ClickBase):
#     pass
#
#     class Config:
#         orm_mode = True


class Message(BaseModel):
    message: str
