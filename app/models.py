import enum
from sqlalchemy import DateTime, func, BigInteger, Integer, String, Float, Date, ForeignKey, Boolean, Text, Enum, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class TaskType(enum.Enum):
    INVITE = "invite"
    SUBSCRIBE_TELEGRAM = "subscribe_telegram"
    GENERIC = "generic"


class UpgradeConditionType(enum.Enum):
    INVITE = "invite_friends"
    REACH_UPGRADE_LEVEL = "reach_upgrade_level"
    SUBSCRIBE_TELEGRAM = "subscribe_channel"


class User(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    username: Mapped[str] = mapped_column(String)
    fio: Mapped[str] = mapped_column(String)
    lvl: Mapped[int] = mapped_column(Integer, default=1)
    taps_for_level: Mapped[int] = mapped_column(Integer, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    money: Mapped[float] = mapped_column(Float, default=0)
    current_factor: Mapped[float] = mapped_column(Float, default=0)
    invited_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), nullable=True)
    last_login: Mapped[DateTime] = mapped_column(DateTime)
    received_last_daily_reward: Mapped[DateTime] = mapped_column(DateTime)
    days_in_row: Mapped[int] = mapped_column(Integer, default=0)
    number_of_columns_passed = mapped_column(BigInteger, default=0, nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=True)

    invited_by: Mapped["User"] = relationship("User", remote_side=[tg_id], lazy='selectin')
    upgrades: Mapped[list["UserUpgrades"]] = relationship("UserUpgrades", back_populates="user",
                                                          cascade="all, delete-orphan", lazy='selectin')
    combo_progress: Mapped[list["UserDailyComboProgress"]] = relationship("UserDailyComboProgress",
                                                                          back_populates="user",
                                                                          cascade="all, delete-orphan", lazy='selectin')
    boost: Mapped[list["UserBoost"]] = relationship("UserBoost", back_populates="user", cascade="all, delete-orphan",
                                                    lazy='selectin')
    tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan", lazy='selectin')


class Level(Base):
    __tablename__ = 'level'

    lvl: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    taps_for_level: Mapped[int] = mapped_column(Integer)
    required_money: Mapped[int] = mapped_column(BigInteger, unique=True)


class UpgradeCategory(Base):
    __tablename__ = 'upgrade_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    category: Mapped[str] = mapped_column(String, unique=True, index=True)

    upgrades: Mapped[list["Upgrades"]] = relationship("Upgrades", back_populates="category", lazy='selectin')





class UpgradeLevel(Base):
    __tablename__ = 'upgrade_lvl'

    upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), primary_key=True, index=True)
    lvl: Mapped[int] = mapped_column(Integer, primary_key=True)
    factor: Mapped[float] = mapped_column(Float)
    price: Mapped[int] = mapped_column(BigInteger)

    upgrade: Mapped["Upgrades"] = relationship("Upgrades", back_populates="levels", lazy='selectin')


class UpgradeConditions(Base):
    __tablename__ = 'upgrade_conditions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), index=True)
    condition_type: Mapped[TaskType] = mapped_column(Enum(UpgradeConditionType))  # Тип условия, например "invite_friends", "reach_upgrade_level", "subscribe_channel"
    condition_value: Mapped[int] = mapped_column(Integer,
                                                 nullable=True)  # Значение условия (например, количество друзей, уровень)
    related_upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'),
                                                    nullable=True)  # Связанный апгрейд (если условие связано с другим апгрейдом)
    channel_url: Mapped[str] = mapped_column(String, nullable=True)  # URL канала, если нужно подписаться на канал
    description: Mapped[str] = mapped_column(Text, nullable=True)
    name_of_condition_upgrade: Mapped[str] = mapped_column(String, nullable=True)

    upgrade: Mapped["Upgrades"] = relationship("Upgrades", foreign_keys=[upgrade_id], back_populates="conditions",
                                               lazy='selectin')
    related_upgrade: Mapped["Upgrades"] = relationship("Upgrades", foreign_keys=[related_upgrade_id], lazy='selectin')


class Upgrades(Base):
    __tablename__ = 'upgrades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrade_category.id'), index=True)
    image_url: Mapped[str] = mapped_column(String)
    is_in_shop: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    category: Mapped["UpgradeCategory"] = relationship("UpgradeCategory", back_populates="upgrades", lazy='selectin')
    levels: Mapped[list["UpgradeLevel"]] = relationship("UpgradeLevel", back_populates="upgrade", lazy='selectin')
    user_upgrades: Mapped[list["UserUpgrades"]] = relationship("UserUpgrades", back_populates="upgrade",
                                                               lazy='selectin')

    # Исправление: указываем foreign_keys явно
    conditions: Mapped[list["UpgradeConditions"]] = relationship(
        "UpgradeConditions",
        foreign_keys=[UpgradeConditions.upgrade_id],  # Добавлено
        back_populates="upgrade",
        lazy='selectin'
    )


class UserUpgrades(Base):
    __tablename__ = 'user_upgrades'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), primary_key=True, index=True)
    upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), primary_key=True, index=True)
    lvl: Mapped[int] = mapped_column(Integer, default=1)

    user: Mapped["User"] = relationship("User", back_populates="upgrades", lazy='selectin')
    upgrade: Mapped["Upgrades"] = relationship("Upgrades", back_populates="user_upgrades", lazy='selectin')


class DailyReward(Base):
    __tablename__ = 'daily_reward'

    day: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    reward: Mapped[int] = mapped_column(Integer)


class UserAdWatch(Base):
    __tablename__ = 'user_ad_watch'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id'), nullable=False)
    watched_date: Mapped[DateTime] = mapped_column(DateTime)
    ads_watched: Mapped[int] = mapped_column(Integer, default=0)
    is_collected: Mapped[bool] = mapped_column(Boolean, default=False)


class DailyCombo(Base):
    __tablename__ = 'daily_combo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    upgrade_1_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), index=True)
    upgrade_2_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), index=True)
    upgrade_3_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), index=True)
    reward: Mapped[int] = mapped_column(Integer)

    upgrade_1: Mapped["Upgrades"] = relationship("Upgrades", foreign_keys=[upgrade_1_id], lazy='selectin')
    upgrade_2: Mapped["Upgrades"] = relationship("Upgrades", foreign_keys=[upgrade_2_id], lazy='selectin')
    upgrade_3: Mapped["Upgrades"] = relationship("Upgrades", foreign_keys=[upgrade_3_id], lazy='selectin')


class UserDailyComboProgress(Base):
    __tablename__ = 'user_daily_combo_progress'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), primary_key=True, index=True)
    combo_id: Mapped[int] = mapped_column(Integer, ForeignKey('daily_combo.id'), primary_key=True, index=True)
    upgrade_1_bought: Mapped[bool] = mapped_column(Boolean, default=False)
    upgrade_2_bought: Mapped[bool] = mapped_column(Boolean, default=False)
    upgrade_3_bought: Mapped[bool] = mapped_column(Boolean, default=False)
    reward_claimed: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="combo_progress", lazy='selectin')
    combo: Mapped["DailyCombo"] = relationship("DailyCombo", lazy='selectin')


class Boost(Base):
    __tablename__ = 'boost'

    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    lvl: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tap_boost: Mapped[int] = mapped_column(Integer)
    one_tap: Mapped[int] = mapped_column(Integer)
    pillars_10: Mapped[int] = mapped_column(Integer)
    pillars_30: Mapped[int] = mapped_column(Integer)
    pillars_100: Mapped[int] = mapped_column(Integer)

    user_boost: Mapped[list["UserBoost"]] = relationship("UserBoost", back_populates="boost", lazy='selectin')


class UserBoost(Base):
    __tablename__ = 'user_boost'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), primary_key=True, index=True)
    boost_id: Mapped[int] = mapped_column(Integer, ForeignKey('boost.lvl'), primary_key=True, index=True)

    user: Mapped["User"] = relationship("User", back_populates="boost", lazy='selectin')
    boost: Mapped["Boost"] = relationship("Boost", back_populates="user_boost", lazy='selectin')


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    type: Mapped[TaskType] = mapped_column(Enum(TaskType))
    reward: Mapped[int] = mapped_column(Integer)
    requirement: Mapped[int] = mapped_column(BigInteger, nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "reward": self.reward,
            "link": self.link,
            "requirement": self.requirement,
            "end_time": self.end_time,
        }


class UserTask(Base):
    __tablename__ = 'user_task'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('task.id'), primary_key=True, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completion_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="tasks", lazy='selectin')
    task: Mapped["Task"] = relationship("Task", lazy='selectin')



