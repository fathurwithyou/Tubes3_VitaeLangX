import time

class Utils:
    """
    A utility class for various helpful functions.
    """
    @staticmethod
    def time_function(func, *args, **kwargs):
        """
        Measures the execution time of a given function.
        Returns a tuple of (result, execution_time_ms).
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        return result, execution_time_ms