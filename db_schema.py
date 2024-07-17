from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Session
import db


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column("id",Integer,primary_key=True)
    name = Column("name", Text, nullable=False)
    surname = Column("surname", Text,nullable=False)
    zaradenie = Column("zaradenie", Text, nullable=False)

    contracts = relationship("Contract", back_populates="employees")


class Contract(Base):
    __tablename__ = "contracts"
    id = Column("id", Integer, primary_key=True)
    od = Column("od", Date, nullable=False)
    do = Column("do", Date, nullable=False)
    mzda_fix = Column("mzda_fix", Integer, nullable=False)
    mzda_var = Column("mzda_variable", Integer, nullable=True)
    employee_id = Column("employee_id", Text, ForeignKey('employees.id'), nullable=False)

    employees = relationship("Employee", back_populates="contracts")

# Assuming postgres_engine is already defined and configured
with Session(db.postgres_engine) as session:
    new_employee = Employee(name="Jan", surname="Trusina",zaradenie="výkon")
    session.add(new_employee)
    session.commit()

    #SELECT STATEMENT WITH JOIN
    """stmt = select(Employee).join(Employee.contracts)
    result = session.execute(stmt)
    for employee in result.scalars():
        for contract in employee.contracts:
            print(f"{contract.id} {contract.mzda_fix} {employee.id} {employee.name}")"""
