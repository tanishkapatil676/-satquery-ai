# Data Contracts: SatQuery AI

## 1. Core schemas

- **RasterMetadataSchema:** Driver, dimensions, band count, CRS, bounds,
  resolution, nodata value, and data types.
- **ProcessingRecord:** Operation name and parameters.
- **AssetManifest:** Asset identifier, source filename, media type,
  lifecycle status, storage key, metadata, and processing history.

## 2. Lifecycle statuses

1. **staged:** Upload has been written to temporary storage.
2. **validated:** Raster structure and metadata have been checked.
3. **prepared:** Pixel data has been read and any requested preprocessing
   has been applied.

## 3. Array conventions

- Pixel arrays use band-first shape: `(bands, height, width)`.
- Invalid or nodata pixels are represented as `NaN` during reading.
