
import io


class MultiprocessingStringIO(io.StringIO):

    def getvalue(self):
        return self.getvalue()

    def writelines(self, content_list):
        '''
        Shadow the StringIO.writelines method. Ingests a list and
        translates that to a string
        '''
        content = ''.join(content_list)
        super().writelines(content)

    def writelines(self, content_list):
        self.writelines(content_list)
