# handing missing data
# outlier treatment
# convert categorical data to numerical data
# handle imabalanced dataset


from dataclasses import dataclass
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.exceptions import CustomException
from src.logger import logging
import numpy as np
import os, sys
from src.utils import save_object

@dataclass
class DataTransformConfig:
    data_transform_obj_file_path = os.path.join("data/transformations", 'preprocessor.pkl')        


class Datatransform:
    def __init__(self):
        self.data_transformation_config = DataTransformConfig()
    
    def get_transformations(self):
        try:
            logging.info("Data Transformation Started....")



            # I have already converted categorial data to numerical data
            numeric_features = ['step', 'type', 'amount', 'newbalanceOrig', 'newbalanceDest']
            
            # numerical feature pipeline ---> missing data handle and then scale the data
            numerical_pipeline = Pipeline(
                steps = [ ('impute',SimpleImputer(strategy='median')),
                        ('scaler', StandardScaler())
            ])

            preprocessor = ColumnTransformer([('numerical_pipeline', numerical_pipeline, numeric_features)])

            return preprocessor
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def remove_outlier(self, df, col):
        '''removing outlier using IQR method'''

        try:
            logging.info("Removing outliers using IQR method")
        
            q1 = df[col].quantile(q = 0.25)
            
            q3 = df[col].quantile(q = 0.75)

            iqr = q3-q1

            upper_l = q3+1.5*iqr
            lower_l = q1-1.5*iqr

            df.loc[(df[col]>upper_l), col] = upper_l
            df.loc[(df[col]<lower_l), col] = lower_l

            logging.info("Outliers Removed.")

            return df
        
        except Exception as e:
            logging.info("Problem in outlier handling function")
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            numeric_features = ['step', 'type', 'amount', 'newbalanceOrig', 'newbalanceDest',
       ]
            
            # handle outliers
            # train data
            logging.info("Removing outliers from training data")
            for col in numeric_features:
                self.remove_outlier(train_data, col = col)
            
            logging.info("Removing Done from training data")

            # test data
            logging.info("Removing outliers from test data")
            for col in numeric_features:
                self.remove_outlier(test_data, col = col)
            
            logging.info("Removing Done from test data")

            preprocessor = self.get_transformations()
            target_col = 'isFraud'
            drop_col = [target_col]

            logging.info("Splitting into dependent and independent variables")
            X_train = train_data.drop(columns=drop_col)
            X_test = test_data.drop(columns=drop_col)

            y_train = train_data[drop_col]
            y_test = test_data[drop_col]

            # Apply transformations
            X_train_arr = preprocessor.fit_transform(X_train)
            X_test_arr = preprocessor.transform(X_test)

            # concat the target values as arrays
            train_array = np.c_[X_train_arr, np.array(y_train)]
            test_array = np.c_[X_test_arr, np.array(y_test)]


            save_object(file_path=self.data_transformation_config.data_transform_obj_file_path,
                        obj = preprocessor)
            logging.info("Data transformation done and .pkl file saved")
            return (train_array, test_array, self.data_transformation_config.data_transform_obj_file_path)

        
        except Exception as e:
            logging.info("Problem in initiating data transform")
            raise CustomException(e, sys)
        

# if __name__== "__main__":

#     train_path, test_path = "data/data_injestion/test.csv", "data/data_injestion/test.csv"
#     transformation = Datatransform()
#     transformation.initiate_data_transformation(train_path=train_path, test_path=test_path)

