import time

from db_operations.db_schema import Session, Employee
from db_operations import db
from sqlalchemy.orm import sessionmaker
import json
from scraper_instance import emp_information_scraper as scrapper
import threading

new_employees_dict = scrapper.ScrapeFormulaChampions(
    "https://en.wikipedia.org/wiki/List_of_Formula_One_World_Drivers%27_Champions"
).return_values_to_save_to_database()
Session = sessionmaker(bind=db.postgres_engine)

#print(new_employees_dict)
# Open a file for writing
with open('new_employees.json', 'w') as fp:
    # Serialize new_employees_dict to the file with pretty printing
    json.dump(new_employees_dict, fp, indent=4)


def process_employee(attributes):
    session = Session()  # Create a new session inside each thread
    try:
        new_employee = Employee(name=attributes[0], surname=attributes[1], zaradenie=attributes[2])
        session.add(new_employee)
        session.commit()
        #print("committed")
    except Exception as e:
        session.rollback()
        #print(f"Error: {e}")
    finally:
        session.close()


threads = []
for attributes in new_employees_dict.values():
    time0 = time.time()
    thread = threading.Thread(target=process_employee, args=(attributes,))
    thread.start()
    threads.append(thread)
    print(time.time() - time0)

# Wait for all threads to complete
for thread in threads:
    thread.join()



"""# Assuming postgres_engine is already defined and configured
with Session(db.postgres_engine) as session:
    for new_employee,attributes in new_employees_dict.items():
        attributes = Employee(name=attributes[0],surname=attributes[1],zaradenie=attributes[2])
        session.add(attributes)
        session.commit()
        print("commited")"""

#SELECT STATEMENT WITH JOIN
"""stmt = select(Employee).join(Employee.contracts)
    result = session.execute(stmt)
    for employee in result.scalars():
        for contract in employee.contracts:
            print(f"{contract.id} {contract.mzda_fix} {employee.id} {employee.name}")"""
