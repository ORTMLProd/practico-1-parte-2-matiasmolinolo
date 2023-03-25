import os

from azure.storage.blob import BlobServiceClient
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.spiders import Spider
from scrapy.utils.misc import md5sum


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider: Spider) -> dict:
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item


class AzureImagesPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        self.container_name = os.getenv("AZURE_CONTAINER_NAME")

    def image_downloaded(self, response, request, info, *, item=None):
        # TODO: puede ser una buena idea implementarlo de manera tal que quede la label
        # y el id o algún otro dato en el path de la imagen en el blob
        checksum = None
        for path, _, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=path
            )
            blob_client.upload_blob(buf.getvalue(), blob_type="BlockBlob")
        return checksum
