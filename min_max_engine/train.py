from ast import Load
from mmEngine.value_funtions import CreateModel, TrainModel, LoadModel
from mmEngine.database import get_database_dir
from pathlib import Path
import numpy as np

def main():
    database_dir = get_database_dir()
    processed_database_path = Path(database_dir, "database_processed.npz")
    data = np.load(processed_database_path)

    network_file_path=Path("./trial_network.keras")

    print("Creating model...")
    model = CreateModel()

    # print("Loading model...")
    # model = LoadModel(network_file_path)


    print("Training model...")
    TrainModel(model, data,save_path=network_file_path)
    

if __name__ == "__main__":
    main()
