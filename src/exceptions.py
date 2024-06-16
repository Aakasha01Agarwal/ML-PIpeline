import os, sys
from src.logger import logging

# return details of the error input

def error_details(error, error_detail:sys):

    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured in file {}, at line number: {}, error message: {} \n".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message

class CustomException(Exception):
    
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_details(error_message, error_detail=error_detail)
    
    def __str__(self) -> str:
        return self.error_message
    

    