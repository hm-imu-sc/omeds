from my_modules import database_populator

print("[+] Genrating Data ...")
database_populator.populate_patient(100)
database_populator.populate_doctor(100)
print("[+] Data generated successfully.")
