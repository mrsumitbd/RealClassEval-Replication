class StreamManager:

    @staticmethod
    def TotalBuffers():
        """
        Get the total number of buffers stored in the StreamManager.

        Returns:
            int:
        """
        return len(__mstreams__)

    @staticmethod
    def get_stream(data=None):
        """
        Get a MemoryStream instance.

        Args:
            data (bytes, bytearray, BytesIO): (Optional) data to create the stream from.

        Returns:
            MemoryStream: instance.
        """
        if len(__mstreams_available__) == 0:
            if data:
                mstream = MemoryStream(data)
                mstream.seek(0)
            else:
                mstream = MemoryStream()
            __mstreams__.append(mstream)
            return mstream
        mstream = __mstreams_available__.pop()
        if data is not None and len(data):
            mstream.clean_up()
            mstream.write(data)
        mstream.seek(0)
        return mstream

    @staticmethod
    def release_stream(mstream):
        """
        Release the memory stream
        Args:
            mstream (MemoryStream): instance.
        """
        mstream.clean_up()
        __mstreams_available__.append(mstream)