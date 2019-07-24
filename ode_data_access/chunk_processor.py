import matplotlib.image as mpimg
import cv2
import rasterio
from ode_data_access.image_utils import view_as_blocks, is_black, align_and_crop
import os
import numpy as np
from tqdm import tqdm


class ChunkProcessor:

    def write_result_blocks(self, result_blocks, window, product_name, chunk_size, save_dir='test', skip_black_images=False,
                            align_and_crop_thresholds=None, vectorized_chunks=None):
        for i in range(result_blocks.shape[0]):
            for j in range(result_blocks.shape[1]):
                img = result_blocks[i][j]
                if not skip_black_images or not is_black(img):
                    filename = f'{product_name}_img_row_{window.row_off}_col_{window.col_off}_w_{window.width}_h_{window.height}_x_{i}_y_{j}.jpg'
                    filepath = './' + save_dir + '/' + filename
                    mpimg.imsave(filepath, img, cmap="gray")
                    img = mpimg.imread(filepath)

                    if align_and_crop_thresholds is not None:
                        img = align_and_crop(img, *align_and_crop_thresholds)
                        img = cv2.resize(img, (chunk_size, chunk_size), cv2.INTER_AREA)
                        mpimg.imsave(filepath, img, cmap='gray')
                        new_filename = f'{product_name}_img_row_{window.row_off}_col_{window.col_off}_w_{img.shape[1]}_h_{img.shape[0]}_x_{i}_y_{j}.jpg'
                        new_filepath = './' + save_dir + '/' + new_filename
                        os.rename(filepath, new_filepath)

                    if vectorized_chunks is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                        vectorized_chunks.append(img.astype(np.uint8))


    # Based on the idea provided here - https://gis.stackexchange.com/questions/158527/reading-raster-files-by-block-with-rasterio
    def chunkify(self, img_file, product_name, chunk_size=256, save_dir='test', skip_black_images=True, align_and_crop_thresholds=None,
                 vectorized_chunks=None):
        with rasterio.open(img_file) as src:
            print('Resolution =', src.width, 'x', src.height)
            print('Estimated number of iterations =', ((src.width * src.height) / (1024 * 1024)) * 1.085)

            for block_index, window in tqdm(src.block_windows(1)):
                block_array = src.read(window=window)
                # print('Block array', block_array.shape)

                block_array = np.moveaxis(block_array, 0, -1)
                # print('Move axis', block_array.shape)

                if block_array.shape[2] != 1:
                    block_array = cv2.cvtColor(block_array, cv2.COLOR_RGB2GRAY)
                else:
                    block_array = np.squeeze(block_array)
                block_array_shape = block_array.shape

                # plt.imshow(block_array, cmap='gray')
                # print('Grayscale Block Shape', block_array_shape)

                if block_array_shape[0] % chunk_size == 0 and block_array_shape[1] % chunk_size == 0:
                    result_blocks = view_as_blocks(block_array, block_shape=(chunk_size, chunk_size))
                    self.write_result_blocks(result_blocks, window, product_name, chunk_size, save_dir, skip_black_images,
                                        align_and_crop_thresholds, vectorized_chunks)


    def chunkify_all(self, save_dir_prefix, chunk_size, product_image_urls, skip_black_images=True, align_and_crop_thresholds=None,
                     vectorized_chunks=None):

        for product_image_url, product_name in product_image_urls:
            filename = product_image_url.split('/')[-1]
            if filename.endswith('JP2') or filename.lower().endswith('jpg'):
                print('Chunkifying', product_name)
                jp2_filename = filename
                chunk_dir = save_dir_prefix + '_' + product_name

                if not os.path.exists(chunk_dir):
                    os.makedirs(chunk_dir)

                self.chunkify(jp2_filename, product_name, chunk_size, chunk_dir, skip_black_images, align_and_crop_thresholds,
                         vectorized_chunks)

                print("Number of chunks found:",
                      len([name for name in os.listdir(chunk_dir) if os.path.isfile(chunk_dir + '/' + name)]))
                print('-----')