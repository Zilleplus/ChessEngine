from mmEngine import database
from mmEngine.database import load_database, get_database_dir
import numpy as np
from pathlib import Path

database_dir = get_database_dir()

processed_data = load_database(1000000)
if processed_data is not None:
    (X, Y) = processed_data
    print(f"Saving array of shape {X.shape}")
    np.savez(Path(database_dir, "database_processed.npz"), X=X, Y=Y)
