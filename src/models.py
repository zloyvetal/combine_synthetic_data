from datetime import datetime
from typing import Any

import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Column, String, BigInteger, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base
import os

XLSX_FILE = "test_data.xlsx"

engine = create_engine("postgresql://postgres:123@localhost/task1", echo=False)
Session = sessionmaker(bind=engine)

BaseModel = declarative_base()


class Accounts(BaseModel):
    __tablename__ = "accounts"

    acc_id = Column(Integer, primary_key=True)
    company_name = Column(String, unique=True)

    def __init__(self, acc_id, company_name):
        self.acc_id = acc_id
        self.company_name = company_name

    def __repr__(self) -> str:
        return f"Company (id={self.acc_id}, name={self.company_name})"


class Opportunities(BaseModel):
    __tablename__ = "opportunities"

    opportunity_id = Column(Integer, primary_key=True)

    stage = Column(String)
    closing_date = Column(Date)
    account_id = Column(Integer, ForeignKey('accounts.acc_id'))

    def __init__(self, opportunity_id, stage, closing_date, account_id):
        self.opportunity_id = opportunity_id
        self.stage = stage
        self.closing_date = closing_date
        self.account_id = account_id

    def __repr__(self) -> str:
        return f"Opportunity_id(id={self.opportunity_id!r}, closing date={self.closing_date!r})"


class Revenue(BaseModel):
    __tablename__ = "revenue"
    id = Column(Integer, primary_key=True)

    opportunity_id = Column(Integer, ForeignKey("opportunities.opportunity_id"))

    date = Column(Date)
    value = Column(Integer, ForeignKey("opportunities.opportunity_id"))

    def __init__(self, opportunity_id, date, value):
        self.opportunity_id = opportunity_id
        self.date = date
        self.value = value

    def __repr__(self) -> str:
        return f"Opportunity_id(id={self.opportunity_id!r}, date={self.date!r}, value = {self.value!r})"


class SegmentCodes(BaseModel):
    __tablename__ = "segment_codes"
    id = Column(Integer, primary_key=True)

    segment_label = Column(String)
    recency_score = Column(String)
    frequency_score = Column(String)
    monetary_score = Column(String)

    def __init__(self, segment_label, recency_score, frequency_score, monetary_score):
        self.segment_label = segment_label
        self.recency_score = recency_score
        self.frequency_score = frequency_score
        self.monetary_score = monetary_score

    def __repr__(self) -> str:
        return f"segment_label(id={self.segment_label!r}, recency_score={self.recency_score!r}, " \
               f"frequency_score = {self.frequency_score!r}, monetary_score = {self.monetary_score!r})"


def xlsx_to_dict(xlsx_file, sheet_number) -> list[dict[str: Any]]:
    df = pd.read_excel(xlsx_file, sheet_name=sheet_number)
    dict_data = df.to_dict(orient="records")

    return dict_data


with Session() as session, session.begin():
    accounts_data = xlsx_to_dict(XLSX_FILE, 0)
    for i in accounts_data:
        session.add(Accounts(
            acc_id=i['Acc Id'],
            company_name=i['Company Name']
        ))

    opportunities_data = xlsx_to_dict(XLSX_FILE, 1)
    for i in opportunities_data:
        session.add(Opportunities(
            opportunity_id=i['Opportunity Id'],
            stage=i['Stage'],
            closing_date=i['Closing Date'],
            account_id=i['Account Id']
        ))

    # revenue_data = xlsx_to_dict(XLSX_FILE, 2)
    # for i in revenue_data:
    #     session.add(Revenue(
    #
    #     opportunity_id=i['Opportunity Id'],
    #     date="",
    #     value=""
    #     ))

    segment_codes_date = xlsx_to_dict(XLSX_FILE, 3)
    for i in segment_codes_date:
        session.add(SegmentCodes(
            segment_label=i["Segment label"],
            recency_score=i["Recency Score"],
            frequency_score=i["Frequency Score"],
            monetary_score=i["Monetary Score"]
        ))
