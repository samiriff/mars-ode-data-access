from ode_data_access.query_processor import QueryProcessor
from ode_data_access.query_result_processor import QueryResultProcessor
import numpy as np


if __name__ == '__main__':
    vectorized_chunks = []

    target = 'mars'  # Aimed planetary body, i.e., Mars, Mercury, Moon, Phobos, or Venus
    mission = 'MRO'  # Aimed mission, e.g., MGS or MRO
    instrument = 'HIRISE'  # Aimed instrument from the mission, e.g., HIRISE or CRISM
    product_type = 'RDRV11'  # Type of product to look for, e.g., DTM or RDRV11
    western_lon = 55.18  # Western longitude to look for the data, from 0 to 360
    eastern_lon = 55.31  # Eastern longitude to look for the data, from 0 to 360
    min_lat = -26.9  # Minimal latitude to look for the data, from -90 to 90
    max_lat = -26.66  # Maximal latitude to look for the data, from -90 to 90
    product_id = '*1530*RED*'  # PDS Product Id to look for, with wildcards (*) allowed
    min_ob_time = ''  # Minimal observation time in (even partial) UTC format, e.g., '2017-03-01'
    max_ob_time = ''  # Maximal observation time in (even partial) UTC format, e.g., '2017-03-01'
    file_name = '*.(JP2|LBL)'  # File name to look for, with wildcards (*) allowed
    number_product_limit = 10  # Maximal number of products to return (100 at most)
    result_offset_number = 0  # Offset the return products, to go beyond the limit of 100 returned products
    remove_ndv = True  # Replace the no-data value as mentionned in the label by np.nan
    bin_type = 1 # Type of binning used in image - Bin1 = 0.35 cm/pixel, Bin2 = 2xBin1, Bin4 = 2xBin2

    query_processor = QueryProcessor()
    query_results = query_processor.query_files_urls(target, mission, instrument, product_type,
                                                     western_lon, eastern_lon, min_lat, max_lat,
                                                     min_ob_time, max_ob_time, product_id, file_name,
                                                     number_product_limit, result_offset_number)
    print("Total Number of Files of all bin types =", len(query_results.keys()))

    SAVE_DIR_PREFIX = 'chunks'
    CHUNK_SIZE = 1024
    SAVE_NPZ = True

    # Default Settings to Skip all black images
    SKIP_BLACK_IMAGES = True  # Set to False to retain all images that contain black pixels

    # Default Settings to Align and Crop images with black margins
    MAX_BORDER_SIZE = 200   # Border to be checked around the image
    SAFETY_MARGIN = 0       # Removes extra pixels from the sides to make sure no black remains
    TOLERANCE = 10          # A gray value is more likely to be considered black when you increase the tolerance
    ALIGN_AND_CROP_THRESHOLDS = (MAX_BORDER_SIZE, SAFETY_MARGIN, TOLERANCE) # Set to None to prevent alignment and cropping

    # Uncomment the following lines to Keep black images and use Sebastien's rotation logic to align images
    # SKIP_BLACK_IMAGES = False
    # ALIGN_IMAGES = True

    query_result_processor = QueryResultProcessor()
    should_continue = query_result_processor.download(query_results, bin_type)
    if should_continue:
        query_result_processor.process(SAVE_DIR_PREFIX, CHUNK_SIZE, SKIP_BLACK_IMAGES, ALIGN_AND_CROP_THRESHOLDS, vectorized_chunks)

    np.savez_compressed('all_chunks.npz', np.array(vectorized_chunks))