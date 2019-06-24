# Mars Orbital Data Explorer Access
This project aims to provide an easy-to-use interface to access data from the [Mars Orbital Data Explorer (ODE)](https://ode.rsl.wustl.edu/mars/indexProductSearch.aspx), maintained by the Geosciences Node of NASA's **[Planetary Data System](https://pds.nasa.gov/)**(PDS), via the [ODE REST Service](http://oderest.rsl.wustl.edu/)

Since the data return by the ODE usually consists of high-resolution map-projected JP2 images, utility methods have also been provided to slice each image into equal-size chunks with all black-margins cropped out so that they can be processed by appropriate machine learning models.

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

## Acknowledgements
- [scikit-dataaccess](https://github.com/MITHaystack/scikit-dataaccess)
- [Autocroppy](https://github.com/gerwin3/autocroppy)
- [scikit-image](https://scikit-image.org/)
