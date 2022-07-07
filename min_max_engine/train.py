from mmEngine.value_funtions import CreateModel, TrainModel
from mmEngine.database import get_database_dir
from pathlib import Path
import numpy as np

def main():
    database_dir = get_database_dir()
    processed_database_path = Path(database_dir, "database_processed.npz")
    data = np.load(processed_database_path)

    print("Creating model...")
    model = CreateModel()

    print("Traning model...")
    TrainModel(model, data)
    

if __name__ == "__main__":
    main()