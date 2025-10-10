
from sqlalchemy.orm import Session
from db.database import engine, Base, User, Income, Expense
from db.test_data import USERS_DATA, INCOMES_DATA, EXPENSES_DATA
from passlib.context import CryptContext
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    # Создание таблиц в PostgreSQL
    Base.metadata.create_all(bind=engine)

    # Инициализация сессии для PostgreSQL
    db = Session(bind=engine)

    try:
        # Stop if the database has already been seeded
        if db.query(User).count() > 0:
            logger.info("Database has already been seeded.")
            return

        logger.info("Seeding new users...")
        # --- Create Users ---
        user_objects = []
        for user_data in USERS_DATA:
            user_obj = User(
                username=user_data["username"],
                login=user_data["login"],
                password=pwd_context.hash(user_data["password"]),
                role=user_data["role"]
            )
            user_objects.append(user_obj)
        db.add_all(user_objects)
        db.flush()

        login_to_user_id = {user.login: user.id for user in user_objects}

        logger.info("Seeding new incomes...")
        income_objects = []
        for income_data in INCOMES_DATA:
            user_id = login_to_user_id.get(income_data["user_login"])
            if user_id:
                new_income = Income(
                    amount=income_data["amount"],
                    description=income_data["description"],
                    user_id=user_id  # Use the correct foreign key
                )
                income_objects.append(new_income)
        db.add_all(income_objects)

        logger.info("Seeding new expenses...")
        expense_objects = []
        for expense_data in EXPENSES_DATA:
            user_id = login_to_user_id.get(expense_data["user_login"])
            if user_id:
                new_expense = Expense(
                    amount=expense_data["amount"],
                    description=expense_data["description"],
                    user_id=user_id  # Use the correct foreign key
                )
                expense_objects.append(new_expense)
        db.add_all(expense_objects)

        db.commit()
        logger.info("Database seeding complete.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing the database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()