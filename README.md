# Shifting Bloom filter implementation in python3.

## Brief description
Bloom filter is a probabilistic test data structure that returns False if an object is not part of a set. When bloom filter returns True an object might or might not be part of a set. Shifting Bloom filter is an extension on  Bloom fliter that allows for multiple set or multiset usecases.

## Library description
This library is made up of 4 submodules, namely the `ShiftingBloomFilter` which contains the Shifting Bloom filter it self, `utils` which contains a set of utilities that are useful while using the set, `exceptions` which contain the exceptions associated with the bloom filter and visualiser which contains a graphic tool that can be used to inspect the filter.

## API description

### `ShiftingBloomFilter`
The filter supports following built-in methods: `len()`, `bool()` (True if not empty), `str()`, `repr()`, `obj[index]` 
|name|type|arguments|description|
|---------|---------|---------|---------|
|`MULTISET`|constant|N/A|constant value for initialising the filter to be used with multiset|
|`MULTIPLE`|constant|N/A|constant value for initialising the filter to be used with multiple sets|
|`ShiftingBloomFilter(length)`|class|length, hash_count, hash_source, mode, set_count| bloom filter with support for handling multisets or multiplesets|
| | |`length`| the size of the underlying bytearrray which is used to represent the filter|
| | |`hash_count=len(algorithms_guaranteed)`| amount of hashing functions to use. NOTE!: cannot be greater than the length of hash source|
| | |`hash_source=algorithms_guaranteed`| a list of hashing functions to use.|
| | |`length_as_power=True`|is length of filter expressed as power of 2 (`True`) or is it literal (`False`)|
| | |`mode=MULTIPLE`|`MULTIPLE` if there are multiple sets or `MULTISET` if its one set but supporting multiple elements|
| | |`set_count=0`| how many sets is this filter suppoused to support|
|`obj.insert(item)`|method|`item`, `set_no=0`|insert item into the filter with set_no (applicable for multiple sets only)|
|`obj.check(item)`|method|`item`| check if item is in the filter|
|`obj.save2file()`|method|`filename=sbf.bin`|save filter to file (binary)|
|`obj.get_fpr()`|method||get false postitive rate for current state of the filter|
|`ShiftingBloomFilter.load_from_file()`|static method|`filename=sbf.bin`|load filter from binary file|


### `utils`
|name|type|arguments|description|
|---------|---------|---------|---------|
|`CSVDataSet(filename)`|class|filename, separator=','|Iterative reader for csv data sets|
||built-ins||`repr()`, `next()`|
|`RandomStringGenerator()`|class|`string_length=4`, `ascii_start=32`, `ascii_end=126`, `stream_length=...`| a stream of random strings of given length|
||built-ins||`repr()`, `len()`, `next()`|
|`HashFunction(hash_base, salt)`|class|`hash_base`, `salt`| wrapper around salted hashing function|
||built-ins||`repr()`, `obj()`|
|`HashFactory(hash_family, hash_count)`|class|`hash_family`, `hash_count`|Produces a list of salted hash functions. `hash_family` is a base hash function from hashlib. hash_count is number of hash functions to create|
|`obj.save2file()`|method|`filename=hashdata.bin`| save `HashFactory` object to file.|
|`HashFactory.load_from_file()`|static method| `filename=hashdata.bin`| load `HashFactory` object from file|
||built-ins||`len()`, `repr()`, `next()`, `obj[index]`|


### `exceptions`
|name|type|arguments|description|
|---------|---------|---------|---------|
|`SBFException()`|Exception class||Top-level module excpetion|
|`HashesUnavailableError(message)`|Exception class|message| Exception raised when there is error related to hashing functions|


### `ShiftingBloomFilter.visualiser`
Tool for presenting how shifting bloom filter works. Can be used as debugger if needed.

|name|type|arguments|description|
|---------|---------|---------|---------|
|`Main()`|class|`title=ShiftingBloomFilter Visualiser`, `length=25`, `hash_count=None`, `hash_source=None`, `bloom=None`, `deepcopy=True`, `mode=MULTIPLE`, `no_sets=1`| Main window of Visualiser.|
|||title| title for the visualiser window|
|||length | length of the filter|
|||hash_count| number of hashing functions to use|
|||hash_source| source of hash functions|
|||bloom| use existing bloom filter instead of creating new one (useful for debugging)
|||deepcopy| work on copy of a given bloom filter|
|`Main.run()`|static method|`title=ShiftingBloomFilter Visualiser`, `length=25`, `mode=MULTIPLE`|Starts the visualiser|
