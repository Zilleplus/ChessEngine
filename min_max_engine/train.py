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

    print("Training model...")
    TrainModel(model, data, log_dir_board=Path("./tensorboard_log"))
    

if __name__ == "__main__":
    main()
