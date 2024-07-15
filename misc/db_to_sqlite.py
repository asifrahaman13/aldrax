"""
This python file is a separate entity. It only helps to create sqlite database from the csv files.
This does no have direct relationship with the server.
"""

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_logo_url = Column(Text)
    company_logo_text = Column(Text)
    company_name = Column(Text)
    relation_to_event = Column(Text)
    event_url = Column(Text)
    company_revenue = Column(Text)
    n_employees = Column(Text)
    company_phone = Column(Text)
    company_founding_year = Column(Text)
    company_address = Column(Text)
    company_industry = Column(Text)
    company_overview = Column(Text)
    homepage_url = Column(Text)
    linkedin_company_url = Column(Text)
    homepage_base_url = Column(Text)
    company_logo_url_on_event_page = Column(Text)
    company_logo_match_flag = Column(Text)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_logo_url = Column(Text)
    event_name = Column(Text)
    event_start_date = Column(Text)
    event_end_date = Column(Text)
    event_venue = Column(Text)
    event_country = Column(Text)
    event_description = Column(Text)
    event_url = Column(Text)

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    job_title = Column(Text)
    person_city = Column(Text)
    person_state = Column(Text)
    person_country = Column(Text)
    email_pattern = Column(Text)
    homepage_base_url = Column(Text)
    duration_in_current_job = Column(Text)
    duration_in_current_company = Column(Text)

def company():
    engine = create_engine('sqlite:///databases/company.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv('databases/company_info.csv')
    for _, row in df.iterrows():
        company = Company(
            company_logo_url=row['company_logo_url'],
            company_logo_text=row['company_logo_text'],
            company_name=row['company_name'],
            relation_to_event=row['relation_to_event'],
            event_url=row['event_url'],
            company_revenue=row['company_revenue'],
            n_employees=row['n_employees'],
            company_phone=row['company_phone'],
            company_founding_year=row['company_founding_year'],
            company_address=row['company_address'],
            company_industry=row['company_industry'],
            company_overview=row['company_overview'],
            homepage_url=row['homepage_url'],
            linkedin_company_url=row['linkedin_company_url'],
            homepage_base_url=row['homepage_base_url'],
            company_logo_url_on_event_page=row['company_logo_url_on_event_page'],
            company_logo_match_flag=row['company_logo_match_flag']
        )
        session.add(company)
    
    session.commit()
    session.close()
    print("Company CSV data has been successfully inserted into the SQLite table.")


def event():
    engine = create_engine('sqlite:///databases/company.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv('databases/event_info.csv')
    for _, row in df.iterrows():
        event = Event(
            event_logo_url=row['event_logo_url'],
            event_name=row['event_name'],
            event_start_date=row['event_start_date'],
            event_end_date=row['event_end_date'],
            event_venue=row['event_venue'],
            event_country=row['event_country'],
            event_description=row['event_description'],
            event_url=row['event_url']
        )
        session.add(event)
    
    session.commit()
    session.close()
    print("Event CSV data has been successfully inserted into the SQLite table.")


def people():
    engine = create_engine('sqlite:///databases/company.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv('databases/people_info.csv')
    for _, row in df.iterrows():
        person = Person(
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            job_title=row['job_title'],
            person_city=row['person_city'],
            person_state=row['person_state'],
            person_country=row['person_country'],
            email_pattern=row['email_pattern'],
            homepage_base_url=row['homepage_base_url'],
            duration_in_current_job=row['duration_in_current_job'],
            duration_in_current_company=row['duration_in_current_company']
        )
        session.add(person)
    
    session.commit()
    session.close()
    print("Person CSV data has been successfully inserted into the SQLite table.")


def main():
    company()
    event()
    people()
    
if __name__ == '__main__':
    main()
