from skdaccess.framework.data_class import DataFetcherCache, ImageWrapper
from skdaccess.utilities.ode_util import get_query_url, get_files_urls
from six.moves.urllib.request import urlopen
from xml.dom import minidom
from collections import OrderedDict
import re


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
        file_urls = self.get_files_urls(query_url, file_name, print_info=False, limit_file_types='')
        print('File URLs:', file_urls)
        return file_urls

    def get_files_urls(self, query_url, file_name='*', print_info=False, limit_file_types='Product'):
        '''
        Retrieve the files' URLs based on a query from ODE REST interface
        Adapted from the Orbital Data Explorer (ODE) REST Interface Manual

        @param query_url: URL resulting from the query of ODE
        @param file_name: File name to look for, with wildcards (*) allowed
        @param print_info: Print the files that will be downloaded

        @return List of URLs
        '''

        url = urlopen(query_url)
        query_results = url.read()
        xml_results = minidom.parseString(query_results)
        url.close()

        error = xml_results.getElementsByTagName('Error')
        if len(error) > 0:
            print('\nError:', error[0].firstChild.data)
            return None

        file_name = file_name.replace('*', '.')

        products = xml_results.getElementsByTagName('Product')
        file_urls = OrderedDict()
        for product in products:
            product_files = product.getElementsByTagName('Product_file')
            product_id = product.getElementsByTagName('pdsid')[0]
            if print_info == True:
                print('\nProduct ID:', product_id.firstChild.data)
            for product_file in product_files:
                file_type = product_file.getElementsByTagName('Type')[0]
                file_url = product_file.getElementsByTagName('URL')[0]
                file_description = product_file.getElementsByTagName('Description')[0]
                local_filename = file_url.firstChild.data.split('/')[-1]
                local_file_extension = local_filename.split('.')[-1]
                if re.search(file_name, local_filename) is not None:
                    # Restriction on the file type to download
                    if len(limit_file_types) > 0:
                        # If match, get the URL
                        if file_type.firstChild.data == limit_file_types:
                            file_urls[file_url.firstChild.data] = (product_id.firstChild.data,
                                                                   file_description.firstChild.data)
                            if print_info == True:
                                print('File name:', file_url.firstChild.data.split('/')[-1])
                                print('Description:', file_description.firstChild.data)
                    # No restriction on the file type to download
                    else:
                        file_urls[file_url.firstChild.data] = (product_id.firstChild.data,
                                                               file_description.firstChild.data)
                        if print_info == True:
                            print('File name:', file_url.firstChild.data.split('/')[-1])
                            print('Description:', file_description.firstChild.data)

        return file_urls