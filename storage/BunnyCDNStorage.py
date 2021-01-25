import requests
from django.conf import settings


class CDNConnector():

    def __init__(
            self,
            api_key=settings.BUNNY_API_KEY,
            storage_zone=settings.BUNNY_STORAGE_ZONE,
            storage_zone_region=settings.BUNNY_STORAGE_ZONE_REGION):
        """

        Creates an object for using bunnyCDN
        api_key=Your Bunny Storage ApiKey/FTP key
        storage_zone=Name of your storage zone

        """
        self.headers = {
           'AccessKey': settings.BUNNY_API_KEY
        }

        if(storage_zone_region == 'de' or storage_zone_region == ''):
            self.base_url = 'https://storage.bunnycdn.com/'+storage_zone+'/'

        else:
            self.base_url = 'https://' + storage_zone_region \
                + '.storage.bunnycdn.com/' + storage_zone+'/'

    def get_storaged_objects(self, cdn_path):

        """

        Returns files and folders stored information stored
        in CDN (json data) path=folder path in cdn

        """

        request_url = self.base_url + cdn_path

        if(cdn_path[-1] != '/'):
            request_url = request_url+'/'

        response = requests.request('GET', request_url, headers=self.headers)
        return(response.json())

    def get_file(self, cdn_path, download_path=None):
        """

        Download file from your cdn storage
        cdn_path storage path for the file, (including file name),
        in cdn, use / as seperator eg, 'images/logo.png'
        download_path (default=None, stores in your present working directory)
        pass your desired download path with file name, will rewrite already
        existing files, if do not exists create them.

        Note, directory will not be created

        """
        # print('cdn_path', cdn_path)
        # if(cdn_path[-1] == '/'):
        #     cdn_path = cdn_path[:-1]

        # filename = cdn_path.split('/')[-1]

        request_url = self.base_url + cdn_path
        response = requests.request("GET", request_url, headers=self.headers)
        if(response.status_code == 404):
            raise ValueError('No such file exists')

        if(response.status_code != 200):
            raise Exception(
                'Some error, please check all settings once and retry')

        return response.text

    def upload_file(self, cdn_path, file_name, file_data):
        """

        Uploads your files to cdn server
        cdn_path - directory to save in CDN
        filename - name to save with cdn
        file_path - locally stored file path,
        if none it will look for file in present working directory

        """

        request_url = self.base_url+cdn_path+'/'+file_name

        response = requests.request(
            "PUT", request_url, data=file_data, headers=self.headers
        )

        return(response.json())

    def remove(self, cdn_dir):
        """

        Deletes a directory or file from cdn \n
        cdn_dir=complete path including file on CDN \n
        for directory make sure that path ends with /

        """
        request_url = self.base_url+cdn_dir
        response = requests.request(
            'DELETE', request_url, headers=self.headers)

        return(response.json())

    def file_exists(self, cdn_path, download_path=None):
        # Check if file exists
        request_url = self.base_url + cdn_path
        response = requests.request("GET", request_url, headers=self.headers)
        if(response.status_code != 200):
            return False
        return True

    def get_url(self, cdn_path, download_path=None):
        request_url = self.base_url + cdn_path
        return request_url
