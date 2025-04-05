"""insert_data

Revision ID: 4b4d2ed54889
Revises: 62100b163c82
Create Date: 2025-04-05 15:24:31.265699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pandas as pd
import logging

alembic_logger = logging.getLogger("alembic_logger")


# revision identifiers, used by Alembic.
revision: str = '4b4d2ed54889'
down_revision: Union[str, None] = '62100b163c82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    df = pd.read_csv('pedant_killer/data/device_service.csv')
    df = df.dropna()
    df['Устройство'] = df['Устройство'].str.strip()
    df_manufacturer = df['Производитель']
    df_manufacturer = df_manufacturer.drop_duplicates()
    df_device_type = df['Тип девайса']
    df_device_type = df_device_type.drop_duplicates()
    df_device = df[['Устройство', 'Тип девайса', 'Производитель']]
    df_device = df_device.drop_duplicates()
    df_service = df['Услуга'].drop_duplicates()
    df_device_service = df[['Устройство', 'Услуга', 'Цена', 'Гарантия']]
    df_breaking = pd.read_csv('pedant_killer/data/breaking.csv')
    df_breaking = df_breaking['Поломка']

    for row in df_manufacturer.tolist():

        conn.execute(
            sa.text("""
                    INSERT INTO manufacturer (name)
                    VALUES (:manufacturer)
                    """),
            {'manufacturer': row}
        )

    for row in df_device_type.tolist():
        conn.execute(
            sa.text("""
                    INSERT INTO device_type (name)
                    VALUES (:device_type)
                """),
            {'device_type': row}
        )

    for row_manufacturer in df_manufacturer.tolist():
        for row_device_type in df_device_type.tolist():
            conn.execute(
                sa.text("""
                    INSERT INTO manufacturer_device_type (manufacturer_id, device_type_id) 
                        VALUES (
                            (SELECT id FROM manufacturer
                            WHERE name = :manufacturer),
                            (SELECT id FROM device_type
                            WHERE name = :device_type)
                        )
                    """),
                {'manufacturer': row_manufacturer, 'device_type': row_device_type}
            )

    for _, row in df_device.iterrows():
        manufacturer = row['Производитель']
        device_type = row['Тип девайса']
        model = row['Устройство']

        conn.execute(
            sa.text("""
                    INSERT INTO device (manufacturer_device_type_id, name_model)
                    VALUES (
                        (SELECT id FROM manufacturer_device_type
                         WHERE manufacturer_id = (SELECT id FROM manufacturer WHERE name = :manufacturer)
                         AND device_type_id = (SELECT id FROM device_type WHERE name = :device_type)),
                        :name_model
                    )
                """),
            {'manufacturer': manufacturer, 'device_type': device_type, 'name_model': model}
       )

    for row in df_service.tolist():
        conn.execute(
            sa.text("""
                INSERT INTO service (name) 
                VALUES (:service)
            """),
            {'service': row}
        )

    for _, row in df_device_service.iterrows():
        device_model = row['Устройство']
        service = row['Услуга']
        price = row['Цена']
        warranty = row['Гарантия']

        conn.execute(
            sa.text("""
            INSERT INTO device_service (device_id, service_id, price, work_duration, warranty)
            VALUES (
                (SELECT id FROM device
                WHERE name_model = :device_model),
                (SELECT id FROM service
                WHERE name = :service),
                :price,
                :work_duration,
                :warranty
                )
            """),
            {'device_model': device_model,
             'service': service,
             'price': price,
             'work_duration': 1,
             'warranty': warranty}
        )

    conn.execute(
        sa.text("""
        INSERT INTO access_level (name, importance) VALUES
        ('Пользователь', 10),
        ('Администратор', 20), 
        ('Мастер', 30)
        """)
    )

    conn.execute(
        sa.text("""
        INSERT INTO order_status(name, description) VALUES
        ('Новый', 'Заказ создан'),
        ('Ждет запчасть', 'Заказ ждет запчасть'),
        ('На диагностике', 'Проводится Диагностика'),
        ('Отложен без ремонта', 'Заказ отложен без ремонта'),
        ('В работе', 'Заказ находится в работе'),
        ('Аутсорсер в работе', 'Заказ находится в работе'),
        ('Готов', 'Заказ готов к выдаче'),
        ('Закрыт', 'Заказ выполнен'),
        ('Выдан клиенту без ремонта', 'Заказ выполнен'),
        ('На согласовании', 'Заказ в процессе согласования работ'),
        ('Доставка', 'Производится доставка заказа')
        """)
    )
    alembic_logger.info('Статичные данные добавлены в таблицы')

    for row in df_breaking.tolist():
        conn.execute(
            sa.text("""
            INSERT INTO breaking(name) VALUES
            (:breaking)
            """),
            {'breaking': row}
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("""
        TRUNCATE TABLE manufacturer, device_type, manufacturer_device_type, device, access_level, order_status CASCADE
        """)
    )
    alembic_logger.info('Статичные данные удалены из таблиц')

    # ### end Alembic commands ###
