from sqlalchemy import DateTime, func, BigInteger, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String)
    fio: Mapped[str] = mapped_column(String)
    lvl: Mapped[int] = mapped_column(Integer, default=1)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    money: Mapped[int] = mapped_column(BigInteger, default=0)
    current_factor: Mapped[float] = mapped_column(Float, default=0)
    invited_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), nullable=True)
    last_login_date: Mapped[Date] = mapped_column(Date)
    days_in_row: Mapped[int] = mapped_column(Integer, default=0)

    # invited_by: Mapped["User"] = relationship("User", remote_side=[tg_id], lazy='selectin')
    # upgrades: Mapped[list["UserUpgrades"]] = relationship("UserUpgrades", back_populates="user", lazy='selectin')


class UpgradeCategory(Base):
    __tablename__ = 'upgrade_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    category: Mapped[str] = mapped_column(String, unique=True)

    # upgrades: Mapped[list["Upgrades"]] = relationship("Upgrades", back_populates="category", lazy='selectin')


class Upgrades(Base):
    __tablename__ = 'upgrades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrade_category.id'))
    image_url: Mapped[str] = mapped_column(String)

    # category: Mapped["UpgradeCategory"] = relationship("UpgradeCategory", back_populates="upgrades", lazy='selectin')
    # levels: Mapped[list["UpgradeLevel"]] = relationship("UpgradeLevel", back_populates="upgrade", lazy='selectin')
    # user_upgrades: Mapped[list["UserUpgrades"]] = relationship("UserUpgrades", back_populates="upgrade", lazy='selectin')


class UpgradeLevel(Base):
    __tablename__ = 'upgrade_lvl'

    upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), primary_key=True)
    lvl: Mapped[int] = mapped_column(Integer, primary_key=True)
    factor: Mapped[float] = mapped_column(Float)
    price: Mapped[int] = mapped_column(Integer)

    # upgrade: Mapped["Upgrades"] = relationship("Upgrades", back_populates="levels", lazy='selectin')


class UserUpgrades(Base):
    __tablename__ = 'user_upgrades'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.tg_id'), primary_key=True)
    upgrade_id: Mapped[int] = mapped_column(Integer, ForeignKey('upgrades.id'), primary_key=True)
    lvl: Mapped[int] = mapped_column(Integer, default=1)

    # user: Mapped["User"] = relationship("User", back_populates="upgrades", lazy='selectin')
    # upgrade: Mapped["Upgrades"] = relationship("Upgrades", back_populates="user_upgrades", lazy='selectin')


class DailyReward(Base):
    __tablename__ = 'daily_reward'

    day: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    reward: Mapped[int] = mapped_column(Integer)
