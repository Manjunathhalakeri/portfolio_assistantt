# This is what you feed to the SQL agent so it knows the DB structure
# Think of it as the agent's "map" of your database

SCHEMA_DESCRIPTION = """
PostgreSQL Database Schema for Investment Portfolio System:

Table: investors
- id: primary key
- name: investor full name
- pan: PAN card number
- risk_profile: 'conservative', 'moderate', or 'aggressive'

Table: portfolios
- id: primary key
- investor_id: foreign key to investors
- fund_name: mutual fund name e.g. 'HDFC Flexicap Fund'
- fund_type: 'equity', 'debt', 'hybrid'
- category: 'largecap', 'midcap', 'smallcap', 'flexicap', 'elss'
- invested_amount: total amount invested in INR
- current_value: current market value in INR
- start_date: when investment started
- sip_amount: monthly SIP amount (0 if lump sum)
- is_sip: true if SIP, false if lump sum

Table: transactions
- id: primary key
- portfolio_id: foreign key to portfolios
- txn_date: date of transaction
- txn_type: 'buy', 'sell', 'dividend'
- amount: transaction amount in INR
- units: number of units
- nav: NAV at time of transaction

To calculate returns (%):
  ((current_value - invested_amount) / invested_amount) * 100
"""