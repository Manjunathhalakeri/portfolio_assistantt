import asyncio
from sqlalchemy import text
from db.connection import AsyncSessionLocal

async def seed():
    async with AsyncSessionLocal() as session:
        await session.execute(text("""
            INSERT INTO investors (name, pan, risk_profile) VALUES
            ('Manjunath H', 'ABCDE1234F', 'moderate'),
            ('Rahul Sharma', 'PQRST5678G', 'aggressive'),
            ('Priya Nair',   'XYZAB9012H', 'conservative')
            ON CONFLICT DO NOTHING;
        """))

        await session.execute(text("""
            INSERT INTO portfolios 
            (investor_id, fund_name, fund_type, category, 
             invested_amount, current_value, start_date, sip_amount, is_sip)
            VALUES
            (1, 'HDFC Flexicap Fund',        'equity', 'flexicap',  120000, 158000, '2021-06-01', 5000,  true),
            (1, 'Parag Parikh Flexicap Fund', 'equity', 'flexicap',  80000,  112000, '2021-09-01', 3000,  true),
            (1, 'Axis Bluechip Fund',         'equity', 'largecap',  50000,  54000,  '2022-01-01', 2000,  true),
            (1, 'SBI Small Cap Fund',         'equity', 'smallcap',  40000,  67000,  '2020-11-01', 2000,  true),
            (1, 'ICICI Pru Liquid Fund',      'debt',   'liquid',    100000, 106000, '2023-01-01', 0,     false),
            (1, 'Mirae Asset ELSS Fund',      'equity', 'elss',      30000,  41000,  '2021-03-01', 1500,  true),
            (2, 'Nippon Small Cap Fund',      'equity', 'smallcap',  200000, 310000, '2020-01-01', 10000, true),
            (3, 'HDFC Short Term Debt Fund',  'debt',   'short_term',150000, 162000, '2022-06-01', 0,     false)
            ON CONFLICT DO NOTHING;
        """))

        await session.execute(text("""
            INSERT INTO transactions
            (portfolio_id, txn_date, txn_type, amount, units, nav)
            VALUES
            (1, '2021-06-01', 'buy', 5000,  120.5, 41.49),
            (1, '2021-07-01', 'buy', 5000,  118.2, 42.30),
            (1, '2021-08-01', 'buy', 5000,  122.1, 40.95),
            (2, '2021-09-01', 'buy', 3000,  68.4,  43.85),
            (2, '2021-10-01', 'buy', 3000,  65.1,  46.08),
            (4, '2020-11-01', 'buy', 2000,  45.3,  44.15),
            (4, '2021-11-01', 'buy', 2000,  41.8,  47.85),
            (6, '2021-03-01', 'buy', 1500,  38.2,  39.27)
            ON CONFLICT DO NOTHING;
        """))

        await session.commit()
        print("Seed data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(seed())