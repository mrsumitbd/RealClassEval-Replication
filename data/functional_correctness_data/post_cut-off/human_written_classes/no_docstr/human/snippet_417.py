from http import HTTPStatus
import dashscope
import json

class Files:

    @classmethod
    def upload(cls, args):
        rsp = dashscope.Files.upload(file_path=args.file, purpose=args.purpose, description=args.description, base_address=args.base_url)
        print(rsp)
        if rsp.status_code == HTTPStatus.OK:
            print('Upload success, file id: %s' % rsp.output['uploaded_files'][0]['file_id'])
        else:
            print_failed_message(rsp)

    @classmethod
    def get(cls, args):
        rsp = dashscope.Files.get(file_id=args.id, base_address=args.base_url)
        if rsp.status_code == HTTPStatus.OK:
            if rsp.output:
                print('file info:\n%s' % json.dumps(rsp.output, ensure_ascii=False, indent=4))
            else:
                print('There is no uploaded file.')
        else:
            print_failed_message(rsp)

    @classmethod
    def list(cls, args):
        rsp = dashscope.Files.list(page=args.start_page, page_size=args.page_size, base_address=args.base_url)
        if rsp.status_code == HTTPStatus.OK:
            if rsp.output:
                print('file list info:\n%s' % json.dumps(rsp.output, ensure_ascii=False, indent=4))
            else:
                print('There is no uploaded files.')
        else:
            print_failed_message(rsp)

    @classmethod
    def delete(cls, args):
        rsp = dashscope.Files.delete(args.id, base_address=args.base_url)
        if rsp.status_code == HTTPStatus.OK:
            print('Delete success')
        else:
            print_failed_message(rsp)