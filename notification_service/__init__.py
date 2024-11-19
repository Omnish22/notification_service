from dotenv import load_dotenv
import os
load_dotenv()

print(str(os.getenv('POSTGRESDB')), os.getenv('POSTGRESUSER'), os.getenv('POSTGRESPASSWORD'), os.getenv('POSTGRESHOST'), os.getenv('POSTGRESPORT'))