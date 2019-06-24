# Mars Orbital Data Explorer Access
This project aims to provide an easy-to-use interface to access data from the [Mars Orbital Data Explorer (ODE)](https://ode.rsl.wustl.edu/mars/indexProductSearch.aspx), maintained by the Geosciences Node of NASA's **[Planetary Data System](https://pds.nasa.gov/)**(PDS), via the [ODE REST Service](http://oderest.rsl.wustl.edu/)

Since the data return by the ODE usually consists of high-resolution map-projected JP2 images, utility methods have also been provided to slice each image into equal-size chunks with all black-margins cropped out so that they can be processed by appropriate machine learning models.

```
   _____                                ________  ________  ___________         ________          __                      _____                                    
  /     \ _____ _______  ______         \_____  \ \______ \ \_   _____/         \______ \ _____ _/  |______              /  _  \   ____  ____  ____   ______ ______
 /  \ /  \\__  \\_  __ \/  ___/  ______  /   |   \ |    |  \ |    __)_   ______  |    |  \\__  \\   __\__  \    ______  /  /_\  \_/ ___\/ ___\/ __ \ /  ___//  ___/
/    Y    \/ __ \|  | \/\___ \  /_____/ /    |    \|    `   \|        \ /_____/  |    `   \/ __ \|  |  / __ \_ /_____/ /    |    \  \__\  \__\  ___/ \___ \ \___ \ 
\____|__  (____  /__|  /____  >         \_______  /_______  /_______  /         /_______  (____  /__| (____  /         \____|__  /\___  >___  >___  >____  >____  >
        \/     \/           \/                  \/        \/        \/                  \/     \/          \/                  \/     \/    \/    \/     \/     \/
```

## Project Structure
```
root/
├── ode_data_access/                
│   ├── autocropper.py/                    Aligns, rotates and crops images to remove black margins
│   ├── chunk_processor.py/                Slices a high-resolution (m x n) image into (m / p x n / p) chunks, where each chunk is of size (p x p)
│   ├── image_utils.py/                    Utility methods to process images
│   ├── lblreader.py/                      Reads an LBL file and converts it into a map of key-value pairs
│   ├── query_processor.py/                Constructs a HTTP Request to be sent to the Orbital Data Explorer, using user-defined query parameters 
│   ├── query_result_processor.py/         Processes the results sent by the Orbital Data Explorer in response to a user-defined query
├── LICENSE
├── main.py                                Provides Sample Usage of package
├── README.md
├── setup.cfg
├── setup.py
└── VERSION
```

## Basic Usage

The entire process consists of 3 steps:

### 1. Query Processor
Initialize an instance of the QueryProcessor class to process user-defined query parameters, details of which are given in the upcoming sections:

```
query_processor = QueryProcessor()
query_results = query_processor.query_files_urls(target, mission, instrument, product_type,
                                                 western_lon, eastern_lon, min_lat, max_lat,
                                                 min_ob_time, max_ob_time, product_id, file_name,
                                                 number_product_limit, result_offset_number)
```

#### Supported Query Parameters
The list of supported query parameters is as shown below:
| Parameter | Description |
|--|--|
| target | Aimed planetary body, i.e., Mars, Mercury, Moon, Phobos, or Venus |
| mission | Aimed mission, e.g., MGS or MRO |
| instrument | Aimed instrument from the mission, e.g., HIRISE or CRISM |
| product_type | Type of product to look for, e.g., DTM or RDRV11 |
| western_lon | Western longitude to look for the data, from 0 to 360 |
| eastern_lon | Eastern longitude to look for the data, from 0 to 360 |
| min_lat | Minimal latitude to look for the data, from -90 to 90 |
| max_lat | Maximal latitude to look for the data, from -90 to 90 |
| product_id | PDS Product Id to look for, with wildcards (*) allowed |
| min_ob_time | Minimal observation time in (even partial) UTC format, e.g., '2017-03-01' |
| max_ob_time | Maximal observation time in (even partial) UTC format, e.g., '2017-03-01' |
| file_name | File name to look for, with wildcards (*) allowed |
| number_product_limit | Maximal number of products to return (100 at most) |
| result_offset_number | Offset the return products, to go beyond the limit of 100 returned products |
| remove_ndv | Replace the no-data value as mentionned in the label by np.nan |

### 2. Query Result Processor
Initialize an instance of the QueryResultProcessor class to process the results returned by your QueryProcessor instance. In this step, you will have to specify user-defined parameters for the chunks and bin type (if applicable):
```
query_result_processor = QueryResultProcessor()
should_continue = query_result_processor.download(query_results, bin_type)
if should_continue:
  query_result_processor.process(SAVE_DIR_PREFIX, CHUNK_SIZE, SKIP_BLACK_IMAGES, ALIGN_AND_CROP_THRESHOLDS, None)
```

#### Supported Query Result Parameters
The list of supported query result parameters is as shown below:
| Parameter | Description |
|--|--|
| bin_type | Type of binning used in image - Bin1 = 0.35 cm/pixel, Bin2 = 2xBin1, Bin4 = 2xBin2 |

#### Chunk Parameters
| Parameter | Description |
|--|--|
| save_dir_prefix | Prefix to be used in the name of the directory where the chunks of an image will be saved. For eg., chunks of an image "ESP_123_456.JP2" will be saved in a directory named "save_dir_prefix_ESP_123_456" | 
| chunk_size | Size of each chunk that will be sliced from a high-resolution image. Eg., 1024 |
| vectorized_chunks | List in which all chunks of all JP2 images will be aggregated. If not required, just assign None |  
| skip_black_images | Flag to indicate that all images containing black pixels near the center should be skipped |

#### Chunk Alignment and Cropping Thresholds
| Parameter | Description |
|--|--|
| max_border_size | Border to be checked around the image while aligning and cropping black margins |
| safety_margin | Removes extra pixels from the sides to make sure no black remains while aligning and cropping black margins |
| tolerance | A gray value is more likely to be considered black when you increase the tolerance |

### 3.  Vectorized Chunks (Optional)
If you wish to accumulate all chunks of all images into a python list, then initialize an empty list before step 1, and each time you call the QueryResultProcessor for multiple queries, pass this list as the `vectorized_chunks` parameter:
```
query_result_processor.process(SAVE_DIR_PREFIX, CHUNK_SIZE, SKIP_BLACK_IMAGES, ALIGN_AND_CROP_THRESHOLDS, vectorized_chunks)
```

## Acknowledgements
- [scikit-dataaccess](https://github.com/MITHaystack/scikit-dataaccess)
- [Autocroppy](https://github.com/gerwin3/autocroppy)
- [scikit-image](https://scikit-image.org/)
