import os
import pandas as pd
from sqlalchemy.orm import Session
from table_structure import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_CSV_PATH = os.path.join(BASE_DIR, "data", "seed_clients.csv")

def seed_clients_if_empty(db: Session):
    
    if db.query(Client).first() is not None:
        return

    if not os.path.exists(SEED_CSV_PATH):
      
        print(f"[SEED] CSV introuvable: {SEED_CSV_PATH}")
        return

    df = pd.read_csv(SEED_CSV_PATH)

    objs = [Client(**row) for row in df.to_dict(orient="records")]
    db.bulk_save_objects(objs)
    db.commit()
    print(f"[SEED] {len(objs)} clients insérés.")
