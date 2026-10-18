# Ingestion Policy: SatQuery AI

## 1. Limits

- Allowed raster extensions: `.tif` and `.tiff`.
- Maximum upload size is configured through `satquery_max_upload_bytes`.
- Maximum raster pixel count is configured through
  `satquery_max_raster_pixels`.

## 2. File handling

- Uploaded files receive UUID-based staged filenames.
- Public manifests should use relative storage keys rather than exposing
  internal absolute paths.
- Failed uploads should remove partial files.

## 3. Paired raster inputs

- Bi-temporal inputs are checked for matching CRS, dimensions, and bounds.
- Distinct timestamps are required for a confirmed temporal comparison.
- Optical and SAR inputs may differ in modality and radiometry; grid
  compatibility alone does not make their measurements equivalent.
- Reprojection, resampling, or cropping must be explicit operations.
