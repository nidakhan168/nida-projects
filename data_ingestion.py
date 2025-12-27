import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionconfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str  = os.path.join('artifacts', "test.csv")
    raw_data_path: str   = os.path.join('artifacts', "StudentsPerformance.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

    def initiate_data_ingestion(self):
        print("CWD inside script:", os.getcwd())

        df = pd.read_csv('/Users/siddiqkhan/Downloads/StudentsPerformance.csv')
        print("Read dataset, shape:", df.shape)

        # Create artifacts dir
        artifacts_dir = os.path.dirname(self.ingestion_config.train_data_path)
        print("Artifacts dir (relative):", artifacts_dir)
        print("Artifacts dir (absolute):", os.path.abspath(artifacts_dir))
        os.makedirs(artifacts_dir, exist_ok=True)

        # Save raw
        print("Saving raw data to:", os.path.abspath(self.ingestion_config.raw_data_path))
        df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

        # Train/test split
        from sklearn.model_selection import train_test_split
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

        print("Saving train to:", os.path.abspath(self.ingestion_config.train_data_path))
        train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

        print("Saving test to:", os.path.abspath(self.ingestion_config.test_data_path))
        test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

        return (
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path,
        )


if __name__ == "__main__":
    obj = DataIngestion()
    paths = obj.initiate_data_ingestion()
    print("Returned paths (absolute):", [os.path.abspath(p) for p in paths])
