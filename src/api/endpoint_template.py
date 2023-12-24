
import time

import ast
import traceback


def error_logging_handler(exception):
    try:
        errors = {'errors': [ast.literal_eval(str(exception))]}
    except:
        errors = {'errors': ''.join(traceback.format_tb(exception.__traceback__)) + '' + str(exception)}
    return errors


def endpoint_template(func):

    def wrapper(input_instance, endpoint, file_logger, *args, **kwargs):

        timer = time.time()

        input_dict = {}
        input_dict['endpoint'] = endpoint
        input_dict = {**input_dict, **input_instance.__dict__}
        
        try:
            output = func(input_instance, *args, **kwargs)
            
            runtime = time.time() - timer    
            output['runtime'] = runtime

            request_log = dict(INPUTS = input_dict, OUTPUTS = output)
            file_logger.info(request_log, exc_info=True)
        
        except Exception as e:
            runtime = time.time() - timer
            file_logger.error('Unhandled error %s', e)
            file_logger.debug('', exc_info=True)
            errors = error_logging_handler(e)
            errors['runtime'] = runtime
            request_log = dict(INPUTS = input_dict, ERRORS = errors)
            file_logger.info(request_log, exc_info=True)
            return errors
        
        return output
        
    return wrapper