import pandas as pd
import os, sys

from src.logger import logging
from src.exceptions import CustomException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.components.data_transformer import Datatransform

@dataclass
class DataInjestionConfig:
    train_data_path = os.path.join("data/data_injestion", "train.csv")
    test_data_path = os.path.join("data/data_injestion", "test.csv")
    raw_data_path = os.path.join("data/data_injestion", "raw.csv")

class DataInjestion:
    def __init__(self) -> None:
        self.data_injestion_config = DataInjestionConfig()
    
    def initiate_data_injestion(self, data_path):
        
        # try loading data and saving it in /data folder 
        # This code works with .csv files, I will have to change this to include other extensions as well.

        # Change here for getting the data from online sources.
        logging.info("Data Injestion Started")
        try:
            data = pd.read_csv(data_path)

            os.makedirs(os.path.dirname(self.data_injestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.data_injestion_config.raw_data_path, index=False )

            
            # split into train and test
            train_data, test_data = train_test_split(data, test_size=0.33, random_state=42)
            logging.info("Data Splitting Done...")

            train_data.to_csv(self.data_injestion_config.train_data_path, index = False, header = True)
            test_data.to_csv(self.data_injestion_config.test_data_path, index = False, header = True)
            logging.info("Data Injestion Done...")

            # return the train and test data file path
            return (self.data_injestion_config.train_data_path, self.data_injestion_config.test_data_path)
        
        except Exception as e:
            logging.info("Error Occured in Data Injestion")
            raise CustomException(e, sys)
        

if __name__== "__main__":

    injestion = DataInjestion()
    train_path, test_path = injestion.initiate_data_injestion("./data/cleandata.csv")

    transformation = Datatransform()
    transformation.initiate_data_transformation(train_path=train_path, test_path=test_path)
# src/components/data_injestion.py