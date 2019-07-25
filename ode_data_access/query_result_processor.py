from ode_data_access.lblreader import  LBLReader
from ode_data_access.chunk_processor import ChunkProcessor
from ode_data_access.image_utils import query_yes_no
import urllib
import time
import sys
import os


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

    def download_progress_callback(self, count, block_size, total_size):
        global start_time
        if count == 0:
            start_time = time.time()
            return
        duration = time.time() - start_time
        progress_size = int(count * block_size)
        speed = int(progress_size / (1024 * duration))
        percent = min(int(count * block_size * 100 / total_size), 100)
        sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                         (percent, progress_size / (1024 * 1024), speed, duration))
        sys.stdout.flush()

    def download_product_images(self, product_image_urls):
        for product_image_url, product_name in product_image_urls:
            print("Downloading", product_image_url)
            filename = product_image_url.split('/')[-1]
            if os.path.exists(filename):
                print(f'{filename} has already been downloaded')
            else:
                urllib.request.urlretrieve(product_image_url, filename, reporthook=self.download_progress_callback)
            print()

    def download(self, query_results, bin_types=None, product_types=None):
        self.find_required_products(query_results, bin_types)
        self.find_required_product_image_urls(query_results, product_types)
        print('Required Product Names matching the given bin type =', self.required_products)
        print('Total number of images to be downloaded =', len(self.product_image_urls))
        should_continue = query_yes_no('\nDo you wish to proceed?')
        if should_continue == "no":
            print('Terminating Process...')
            return False
        self.download_product_images(self.product_image_urls)
        print('----')
        return True

    def find_required_products(self, query_results, bin_types=None):
        for query_result in query_results.keys():
            product_name, product_type = query_results[query_result]
            if product_type == 'PRODUCT LABEL FILE':
                filename = query_result.split('/')[-1]
                if os.path.exists(filename):
                    print(f'{filename} has already been downloaded')
                else:
                    urllib.request.urlretrieve(query_result, filename)
                self.lblReader.read(filename)
                binning = self.lblReader.get('MRO:BINNING')
                if bin_types is None or self.get_bin_type(binning) in bin_types:
                    self.required_products.add(product_name)

    def find_required_product_image_urls(self, query_results, product_types):
        if product_types is None:
            product_types = set(['PRODUCT DATA FILE'])
        for query_result in query_results.keys():
            product_name, product_type = query_results[query_result]
            if (product_type in product_types) and product_name in self.required_products:
                self.product_image_urls.append((query_result, product_name))

    def process(self, save_dir_prefix, chunk_size, skip_black_images, align_and_crop_thresholds, vectorized_chunks=None):
        print('Beginning Chunking Process')
        chunk_processor = ChunkProcessor()
        chunk_processor.chunkify_all(save_dir_prefix, chunk_size,
                                     self.product_image_urls, skip_black_images, align_and_crop_thresholds, vectorized_chunks)
        print('Completed Chunking Process')
