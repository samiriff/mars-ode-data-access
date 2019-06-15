from skdaccess.framework.data_class import DataFetcherCache, ImageWrapper
from skdaccess.utilities.ode_util import get_query_url, get_files_urls


class QueryProcessor:

    def query_files_urls(self, target, mission, instrument, product_type,
                         western_lon, eastern_lon, min_lat, max_lat,
                         min_ob_time, max_ob_time, product_id, file_name,
                         number_product_limit, result_offset_number):
        # Returns a list of products with selected product metadata that meet the query parameters
        query_type = 'product'
        # Controls the return format for product queries or error messages
        output = 'XML'
        # For each product found return the product files and IDS
        results = 'fp'

        query_url = get_query_url(target, mission, instrument, product_type,
                                  western_lon, eastern_lon, min_lat, max_lat,
                                  min_ob_time, max_ob_time, product_id,
                                  query_type, output, results,
                                  number_product_limit, result_offset_number)

        print('Query URL:', query_url)
        print('\nFiles that will be downloaded (if not previously downloaded):')
        file_urls = get_files_urls(query_url, file_name, print_info=False)
        return file_urls
