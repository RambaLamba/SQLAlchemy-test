import json
import sqlalchemy as sq
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from datetime import datetime


DSN = '!!!введите свой DSN!!!'
engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_sales_by_publisher():
    """Запрос информации о продажах книг конкретного издателя."""
    try:
        publisher_input = input("Введите имя или ID издателя: ").strip()

        if publisher_input.isdigit():
            publisher = session.query(Publisher).get(int(publisher_input))
        else:
            publisher = session.query(Publisher).filter(
                Publisher.name.ilike(f"%{publisher_input}%")
            ).first()

        if not publisher:
            print("Издатель не найден!")
            return

        query = (
            session.query(
                Book.title.label("book_title"),
                Shop.name.label("shop_name"),
                Sale.price,
                Sale.date_sale
            )
            .select_from(Book)
            .join(Stock, Book.id == Stock.id_book)
            .join(Shop, Shop.id == Stock.id_shop)
            .join(Sale, Sale.id_stock == Stock.id)
            .filter(Book.id_publisher == publisher.id)
            .order_by(Sale.date_sale.desc())
        )

        sales = query.all()

        if not sales:
            print("Нет данных о продажах книг этого издателя")
            return

        print("\nРезультаты:")
        print("-" * 60)
        print(f"{'Книга'.ljust(30)} | {'Магазин'.ljust(15)} | Цена | Дата")
        print("-" * 60)

        for sale in sales:
            date_str = sale.date_sale.strftime("%d-%m-%Y") if isinstance(sale.date_sale, datetime) else sale.date_sale
            print(f"{sale.book_title.ljust(30)} | {sale.shop_name.ljust(15)} | {sale.price} | {date_str}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        session.close()

def fill_data(session, json_file_path="fixtures/test_data.json"):
    """Заполнение базы данных из JSON-файла."""
    try:
        with open(json_file_path, "r", encoding="utf-8") as fd:
            data = json.load(fd)

        model = {"publisher": Publisher,
                "book": Book,
                "shop": Shop,
                "stock": Stock,
                "sale": Sale
        }

        for record in data:
            model_name = record.get('model')
            if model_name not in model:
                print(f"Неизвестная модель '{model_name}' пропущена")
                continue

            model_class = model[model_name]
            try:
                session.add(model_class(id=record.get('pk'), **record.get('fields', {})))
            except TypeError as e:
                print(f"Ошибка при создании модели {model_name}: {e}")
                continue

        session.commit()
        print("Данные успешно загружены!")

    except FileNotFoundError:
        print(f"Файл {json_file_path} не найден")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга в файле{json_file_path}")
    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка целостности данных: {e}")
    except Exception as e:
        session.rollback()
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    fill_data(session)
    get_sales_by_publisher()
