"""seed categories

Revision ID: 52fc5fe036a4
Revises: 596a050ae659
Create Date: 2026-05-05 00:21:48.356503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52fc5fe036a4'
down_revision: Union[str, Sequence[str], None] = '596a050ae659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    categories_table = sa.table('categories',
        sa.column('name', sa.String),
        sa.column('tags', sa.Text)
    )
    op.bulk_insert(categories_table, [
        {"name": "food, product & groceries", "tags": "еда, продукты, супермаркет, вкусвилл, пятерочка, перекресток, магнит, булочная, макдоналдс, бургер кинг, ужин, обед, завтрак"},
        {"name": "school & education", "tags": "школа, обучение, курсы, репетитор, учебники, тетради, университет, английский, кружок, канцтовары"},
        {"name": "health & medicine", "tags": "аптека, лекарства, врач, стоматолог, анализы, больница, витамины, терапевт, оптика, зрение"},
        {"name": "car spendings", "tags": "машина, авто, бензин, заправка, шиномонтаж, мойка, техосмотр, запчасти, страховка, парковка"},
        {"name": "household spendings", "tags": "дом, мебель, посуда, декор, икеа, ремонт, стройматериалы, хозтовары, уют, шторы"},
        {"name": "utilities & fees", "tags": "жкх, свет, вода, газ, квартплата, отопление, налоги, штраф, госзакупки, госпошлина"},
        {"name": "cat spendings", "tags": "кот, кошка, корм, ветеринар, лоток, наполнитель, игрушки для кота, зоомагазин"},
        {"name": "communication spendings", "tags": "телефон, интернет, связь, билайн, мтс, мегафон, пополнение счета, подписка, облако"},
        {"name": "kids allowance", "tags": "карманные деньги, детям, сыну, дочке, на мороженое, подарок ребенку, выдано детям"},
        {"name": "beauty spendings", "tags": "косметика, парикмахер, стрижка, маникюр, салон красоты, золотое яблоко, парфюм, уход"},
        {"name": "transportation spendings", "tags": "такси, метро, автобус, тройка, электричка, самокат, каршеринг, проездной"},
        {"name": "gifts", "tags": "подарок, цветы, день рождения, праздник, юбилей, сувенир, открытка"},
        {"name": "babysitting", "tags": "няня, присмотр, сиделка, бэбиситтер, услуги няни"},
        {"name": "cleaning", "tags": "уборка, клининг, мытье окон, пылесос, бытовая химия, стирка"},
        {"name": "apartment loan payment", "tags": "ипотека, кредит за квартиру, платеж по ипотеке, банк, проценты, основной долг"},
        {"name": "sports", "tags": "спорт, фитнес, зал, абонемент, тренер, бассейн, кроссовки, спорттовары, йога"},
        {"name": "baby spendings", "tags": "памперсы, подгузники, смесь, детское питание, коляска, игрушки для малыша, погремушка"},
        {"name": "other spendings", "tags": "разное, прочее, непонятное, неучтенное, комиссия"}
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM categories WHERE name IN ("
        "'food, product & groceries', 'school & education', 'health & medicine', "
        "'car spendings', 'household spendings', 'utilities & fees', "
        "'cat spendings', 'communication spendings', 'kids allowance', "
        "'beauty spendings', 'transportation spendings', 'gifts', "
        "'babysitting', 'cleaning', 'apartment loan payment', "
        "'sports', 'baby spendings', 'other spendings'"
        ")"
    )
