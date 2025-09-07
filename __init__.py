from metadata_hub.dao.exif_data import ExifData
from metadata_hub.nodes.metadata_hub import MetadataHub
from metadata_hub.nodes.save_image import SaveImage

CUSTOM_TYPE_CLASSES = {
    "EXIFDATA": ExifData,
}

NODE_CLASS_MAPPINGS = {
    "Metadata Hub": MetadataHub,
    "Save Image With Metadata": SaveImage,
}
