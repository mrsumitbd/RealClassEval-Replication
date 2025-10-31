from pyicloud.exceptions import PyiCloudServiceNotActivatedException
from urllib.parse import urlencode
import base64

class PhotosService:
    """The 'Photos' iCloud service."""
    SMART_FOLDERS = {'All Photos': {'obj_type': 'CPLAssetByAddedDate', 'list_type': 'CPLAssetAndMasterByAddedDate', 'direction': 'ASCENDING', 'query_filter': None}, 'Time-lapse': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Timelapse', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'TIMELAPSE'}}]}, 'Videos': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Video', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'VIDEO'}}]}, 'Slo-mo': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Slomo', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'SLOMO'}}]}, 'Bursts': {'obj_type': 'CPLAssetBurstStackAssetByAssetDate', 'list_type': 'CPLBurstStackAssetAndMasterByAssetDate', 'direction': 'ASCENDING', 'query_filter': None}, 'Favorites': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Favorite', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'FAVORITE'}}]}, 'Panoramas': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Panorama', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'PANORAMA'}}]}, 'Screenshots': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Screenshot', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'SCREENSHOT'}}]}, 'Live': {'obj_type': 'CPLAssetInSmartAlbumByAssetDate:Live', 'list_type': 'CPLAssetAndMasterInSmartAlbumByAssetDate', 'direction': 'ASCENDING', 'query_filter': [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'LIVE'}}]}, 'Recently Deleted': {'obj_type': 'CPLAssetDeletedByExpungedDate', 'list_type': 'CPLAssetAndMasterDeletedByExpungedDate', 'direction': 'ASCENDING', 'query_filter': None}, 'Hidden': {'obj_type': 'CPLAssetHiddenByAssetDate', 'list_type': 'CPLAssetAndMasterHiddenByAssetDate', 'direction': 'ASCENDING', 'query_filter': None}}

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = dict(params)
        self._service_root = service_root
        self.service_endpoint = '%s/database/1/com.apple.photos.cloud/production/private' % self._service_root
        self._albums = None
        self.params.update({'remapEnums': True, 'getCurrentSyncToken': True})
        url = f'{self.service_endpoint}/records/query?{urlencode(self.params)}'
        json_data = '{"query":{"recordType":"CheckIndexingState"},"zoneID":{"zoneName":"PrimarySync"}}'
        request = self.session.post(url, data=json_data, headers={'Content-type': 'text/plain'})
        response = request.json()
        indexing_state = response['records'][0]['fields']['state']['value']
        if indexing_state != 'FINISHED':
            raise PyiCloudServiceNotActivatedException('iCloud Photo Library not finished indexing. Please try again in a few minutes.')
        self._photo_assets = {}

    @property
    def albums(self):
        """Returns photo albums."""
        if not self._albums:
            self._albums = {name: PhotoAlbum(self, name, **props) for name, props in self.SMART_FOLDERS.items()}
            for folder in self._fetch_folders():
                if 'albumNameEnc' not in folder['fields']:
                    continue
                if folder['recordName'] == '----Root-Folder----' or (folder['fields'].get('isDeleted') and folder['fields']['isDeleted']['value']):
                    continue
                folder_id = folder['recordName']
                folder_obj_type = 'CPLContainerRelationNotDeletedByAssetDate:%s' % folder_id
                folder_name = base64.b64decode(folder['fields']['albumNameEnc']['value']).decode('utf-8')
                query_filter = [{'fieldName': 'parentId', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': folder_id}}]
                album = PhotoAlbum(self, folder_name, 'CPLContainerRelationLiveByAssetDate', folder_obj_type, 'ASCENDING', query_filter)
                self._albums[folder_name] = album
        return self._albums

    def _fetch_folders(self):
        url = f'{self.service_endpoint}/records/query?{urlencode(self.params)}'
        json_data = '{"query":{"recordType":"CPLAlbumByPositionLive"},"zoneID":{"zoneName":"PrimarySync"}}'
        request = self.session.post(url, data=json_data, headers={'Content-type': 'text/plain'})
        response = request.json()
        return response['records']

    @property
    def all(self):
        """Returns all photos."""
        return self.albums['All Photos']