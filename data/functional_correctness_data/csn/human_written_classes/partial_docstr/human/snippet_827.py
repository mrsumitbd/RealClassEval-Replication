class HistoryEntity:
    """
    HistoryEntity model
    """
    endpoint = 'history'

    def __init__(self, requester):
        self.requester = requester

    def get(self, resource_id):
        """
        Get a history element

        :param resource_id: id of the resource object (resource type is defined by the HistoryEntity subclass used)
        """
        response = self.requester.get('/{endpoint}/{entity}/{id}', endpoint=self.endpoint, entity=self.entity, id=resource_id, paginate=False)
        return response.json()

    def delete_comment(self, resource_id, comment_id):
        """
        Delete a comment

        :param resource_id: id of the resource object (resource type is defined by the HistoryEntity subclass used)
        :param comment_id: id of the comment to delete
        """
        self.requester.post('/{endpoint}/{entity}/{id}/delete_comment?id={comment_id}', endpoint=self.endpoint, entity=self.entity, id=resource_id, comment_id=comment_id)

    def undelete_comment(self, resource_id, comment_id):
        """
        Undelete a comment

        :param resource_id: id of the resource object (resource type is defined by the HistoryEntity subclass used)
        :param comment_id: id of the comment to undelete
        """
        self.requester.post('/{endpoint}/{entity}/{id}/undelete_comment?id={comment_id}', endpoint=self.endpoint, entity=self.entity, id=resource_id, comment_id=comment_id)