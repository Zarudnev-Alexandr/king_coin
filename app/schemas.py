import datetime
from typing import Optional, List

from pydantic import BaseModel


# Создаем буст
class BoostCreateSchema(BaseModel):
    name: str
    price: int
    lvl: int
    tap_boost: int
    one_tap: int
    pillars_10: int
    pillars_30: int
    pillars_100: int


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
    # boost: ReturnUserBoostSchema

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
    description: Optional[str]


# Улучшение (карточка) без уровней
class UpgradeSchema(CreateUpgradeSchema):
    id: int


# Улучшение (карточка) со всеми уровнями внутри
class UpgradeWithLevelsSchema(CreateUpgradeSchema):
    id: int

    levels: List[UpgradeLevelSchema]


class UpgradeWithoutLevelsSchema(CreateUpgradeSchema):
    id: int
    lvl: int
    is_bought: bool
    factor: Optional[float]
    factor_at_new_lvl: Optional[float]
    price_of_next_lvl: Optional[int]

    # levels: List[UpgradeLevelSchema]


class UpgradeCategoryBaseSchema(BaseModel):
    category: str


class UpgradeCategoryCreateSchema(BaseModel):
    category: str

    upgrades: List[UpgradeWithoutLevelsSchema]


class UpgradeCategorySchema(UpgradeCategoryCreateSchema):
    id: int


class UpgradeCategoryBaseSchemaWithId(UpgradeCategoryBaseSchema):
    id: int


class UpgradeCategoryClassicSchema(BaseModel):
    category: str

    upgrades: List[UpgradeSchema]


# Покупка улушение (апгрейд с 0 до 1 уровня)
class UserUpgradeCreateSchema(BaseModel):
    user_id: int
    upgrade_id: int


# Купленные пользователем карты
class UserUpgradeSchema(UserUpgradeCreateSchema):
    lvl: int

    user: UserBase
    upgrade: UpgradeSchema


class CreateDailyComboSchema(BaseModel):
    upgrade_1_id: int
    upgrade_2_id: int
    upgrade_3_id: int
    reward: int


class DailyComboSchema(CreateDailyComboSchema):
    id: int


class UserDailyComboSchema(BaseModel):
    user_id: int
    combo_id: int
    upgrade_1_bought: bool
    upgrade_2_bought: bool
    upgrade_3_bought: bool
    reward_claimed: bool

    combo: DailyComboSchema


class CreateDailyRewardSchema(BaseModel):
    day: int
    reward: int


class DailyRewardResponse(CreateDailyRewardSchema):
    total_money: int

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str
