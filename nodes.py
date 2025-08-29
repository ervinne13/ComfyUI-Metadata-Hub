from dao.exif_data import ExifData
from nodes.metadata_hub import MetadataHub
from nodes.save_image import SaveImage

CUSTOM_TYPE_CLASSES = {
    "EXIFDATA": ExifData,
}

NODE_CLASS_MAPPINGS = {
    "Metadata Hub": MetadataHub,
    "Save Image With Metadata": SaveImage,
}
