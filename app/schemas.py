from typing import Optional, List

from pydantic import BaseModel, validator
from datetime import datetime, timedelta


# Создаем буст
from app.models import TaskType


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
    invited_tg_id: Optional[int] = None


class UserBase(UserCreate):
    lvl: int
    taps_for_level: int
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


class UpgradeInfoSchema(BaseModel):
    is_bought: bool
    image_url: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class UserDailyComboSchema(BaseModel):
    user_id: int
    combo_id: int
    upgrade_1: UpgradeInfoSchema
    upgrade_2: UpgradeInfoSchema
    upgrade_3: UpgradeInfoSchema
    reward_claimed: bool

    combo: DailyComboSchema


class CreateDailyRewardSchema(BaseModel):
    day: int
    reward: int


class DailyRewardResponse(CreateDailyRewardSchema):
    total_money: int

    class Config:
        orm_mode = True


class ImageUploadResponse(BaseModel):
    image_url: str


class InitDataSchema(BaseModel):
    allows_write_to_pm: bool
    first_name: str
    id: int
    language_code: str
    last_name: str
    username: str


class TaskBaseSchema(BaseModel):
    name: str
    description: str
    type: TaskType
    reward: int
    requirement: Optional[int] = None
    link: Optional[str] = None
    end_time: Optional[datetime] = None


class TaskCreateSchema(TaskBaseSchema):
    user_creator_id: int
    days_active: int = None

    @validator('days_active')
    def check_days_active(cls, v):
        if v is not None and v < 0:
            raise ValueError('days_active must be a non-negative integer')
        return v


class TaskResponseSchema(TaskBaseSchema):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class GameResultsSchema(BaseModel):
    encrypted_information: str


class Message(BaseModel):
    message: str
