from ode_data_access.lblreader import  LBLReader
from ode_data_access.chunk_processor import ChunkProcessor
import urllib


class QueryResultProcessor:

    def __init__(self):
        self.required_products = set()
        self.lblReader = LBLReader()
        self.product_image_urls = []

    def get_bin_type(self, binning):
        if binning.startswith('(-9998'):
            return 1
        if binning.startswith('(2'):
            return 2
        if binning.startswith('(4'):
            return 4
        return None

    def download_product_images(self, product_image_urls):
        for product_image_url, product_name in product_image_urls:
            print("Downloading", product_image_url)
            filename = product_image_url.split('/')[-1]
            urllib.request.urlretrieve(product_image_url, filename)

    def download(self, query_results, bin_type):
        self.find_required_products(query_results, bin_type)
        self.find_required_product_image_urls(query_results)
        self.download_product_images(self.product_image_urls)

    def find_required_products(self, query_results, bin_type):
        for query_result in query_results.keys():
            product_name, product_type = query_results[query_result]
            if product_type == 'PRODUCT LABEL FILE':
                filename = query_result.split('/')[-1]
                urllib.request.urlretrieve(query_result, filename)
                self.lblReader.read(filename)
                binning = self.lblReader.get('MRO:BINNING')
                if self.get_bin_type(binning) == bin_type:
                    self.required_products.add(product_name)

    def find_required_product_image_urls(self, query_results):
        for query_result in query_results.keys():
            product_name, product_type = query_results[query_result]
            if product_type == 'PRODUCT DATA FILE' and product_name in self.required_products:
                self.product_image_urls.append((query_result, product_name))

    def process(self, save_dir_prefix, chunk_size, skip_black_images, align_images, save_npz):
        chunk_processor = ChunkProcessor()
        chunk_processor.chunkify_all(save_dir_prefix, chunk_size,
                                     self.product_image_urls, skip_black_images, align_images, save_npz)
