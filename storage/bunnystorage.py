from io import BytesIO
from shutil import copyfileobj
from tempfile import SpooledTemporaryFile

# from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.core.files.storage import Storage
# from django.utils._os import safe_join
from django.utils.deconstruct import deconstructible
from .BunnyCDNStorage import CDNConnector
from .utils import get_available_overwrite_name, setting, safe_join

_DEFAULT_TIMEOUT = 100
_DEFAULT_MODE = 'add'


class BunnyStorageException(Exception):
    pass


class BunnyFile(File):
    def __init__(self, name, storage):
        print(name)
        self.name = name
        self._storage = storage
        self._file = None

    def _get_file(self):
        if self._file is None:
            self._file = SpooledTemporaryFile()
            response = \
                self._storage.client.get_file(self.name)
            if response.status_code == 200:
                with BytesIO(response.content) as file_content:
                    copyfileobj(file_content, self._file)
            else:
                raise BunnyStorageException(
                    "Bunny CDN server returned a {} response when accessing {}"
                    .format(response.status_code, self.name)
                )
            self._file.seek(0)
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)


@deconstructible
class BunnyStorage(Storage):
    """BunnyCDN Storage class for Django pluggable storage system."""
    location = setting('BUNNY_ROOT_PATH', '/')
    timeout = setting('BUNNY_TIMEOUT', _DEFAULT_TIMEOUT)
    write_mode = setting('BUNNY_WRITE_MODE', _DEFAULT_MODE)

    CHUNK_SIZE = 4 * 1024 * 1024

    def __init__(
            self,
            root_path=location,
            timeout=timeout,
            write_mode=write_mode
            ):

        self.root_path = root_path
        self.write_mode = write_mode
        self.client = CDNConnector()

    def _full_path(self, name):
        if name == '/':
            name = ''
        return safe_join(self.root_path, name).replace('\\', '/')

    def delete(self, name):
        self.client.remove(self._full_path(name))

    def exists(self, name):
        return bool(self.client.file_exists(self._full_path(name)))

    def url(self, name):
        return self.client.get_url(self._full_path(name))

    def _open(self, name, mode='rb'):
        remote_file = BunnyFile(self._full_path(name), self)
        return remote_file

    def _save(self, name, content):
        content.open()
        if content.size <= self.CHUNK_SIZE:
            self.client.upload_file(
                '',
                self._full_path(name),
                content.read()
            )
        else:
            pass
            print('File size too large')
            # self._chunked_upload(content, self._full_path(name))
        content.close()
        return name

    def get_available_name(self, name, max_length=None):
        """Overwrite existing file with the same name."""
        name = self._full_path(name)
        if self.write_mode == 'overwrite':
            return get_available_overwrite_name(name, max_length)
        return super().get_available_name(name, max_length)

    # def _chunked_upload(self, content, dest_path):
    #     upload_session = self.client.files_upload_session_start(
    #         content.read(self.CHUNK_SIZE)
    #     )
    #     cursor = UploadSessionCursor(
    #         session_id=upload_session.session_id,
    #         offset=content.tell()
    #     )
    #     commit = CommitInfo(path=dest_path, mode=WriteMode(self.write_mode))

    #     while content.tell() < content.size:
    #         if (content.size - content.tell()) <= self.CHUNK_SIZE:
    #             self.client.files_upload_session_finish(
    #                 content.read(self.CHUNK_SIZE), cursor, commit
    #             )
    #         else:
    #             self.client.files_upload_session_append_v2(
    #                 content.read(self.CHUNK_SIZE), cursor
    #             )
    #             cursor.offset = content.tell()

    # def listdir(self, path):
    #     directories, files = [], []
    #     full_path = self._full_path(path)

    #     if full_path == '/':
    #         full_path = ''

    #     metadata = self.client.files_list_folder(full_path)
    #     for entry in metadata.entries:
    #         if isinstance(entry, FolderMetadata):
    #             directories.append(entry.name)
    #         else:
    #             files.append(entry.name)
    #     return directories, files

    # def size(self, name):
    #     metadata = self.client.files_get_metadata(self._full_path(name))
    #     return metadata.size

    # def modified_time(self, name):
    #     metadata = self.client.files_get_metadata(self._full_path(name))
    #     return metadata.server_modified

    # def accessed_time(self, name):
    #     metadata = self.client.files_get_metadata(self._full_path(name))
    #     return metadata.client_modified
