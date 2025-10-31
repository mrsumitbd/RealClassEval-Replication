import time
from http import HTTPStatus
import dashscope
from dashscope.common.constants import DeploymentStatus, FilePurpose, TaskStatus

class Deployments:

    @classmethod
    def call(cls, args):
        rsp = dashscope.Deployments.call(model=args.model, capacity=args.capacity, suffix=args.suffix)
        if rsp.status_code == HTTPStatus.OK:
            deployed_model = rsp.output['deployed_model']
            print('Create model: %s deployment' % deployed_model)
            try:
                while True:
                    status = dashscope.Deployments.get(deployed_model)
                    if status.status_code == HTTPStatus.OK:
                        if status.output['status'] in [DeploymentStatus.PENDING, DeploymentStatus.DEPLOYING]:
                            time.sleep(30)
                            print('Deployment %s is %s' % (deployed_model, status.output['status']))
                        else:
                            print('Deployment: %s status: %s' % (deployed_model, status.output['status']))
                            break
                    else:
                        print_failed_message(rsp)
            except Exception:
                print('You can get deployment status via:                         dashscope deployments.get -d %s' % deployed_model)
        else:
            print_failed_message(rsp)

    @classmethod
    def get(cls, args):
        rsp = dashscope.Deployments.get(args.deploy)
        if rsp.status_code == HTTPStatus.OK:
            print('Deployed model: %s capacity: %s status: %s' % (rsp.output['deployed_model'], rsp.output['capacity'], rsp.output['status']))
        else:
            print_failed_message(rsp)

    @classmethod
    def list(cls, args):
        rsp = dashscope.Deployments.list(page_no=args.start_page, page_size=args.page_size)
        if rsp.status_code == HTTPStatus.OK:
            if rsp.output is not None:
                if 'deployments' not in rsp.output or len(rsp.output['deployments']) == 0:
                    print('There is no deployed model!')
                    return
                for deployment in rsp.output['deployments']:
                    print('Deployed_model: %s, model: %s, status: %s' % (deployment['deployed_model'], deployment['model_name'], deployment['status']))
            else:
                print('There is no deployed model.')
        else:
            print_failed_message(rsp)

    @classmethod
    def update(cls, args):
        rsp = dashscope.Deployments.update(args.deployed_model, args.version)
        if rsp.status_code == HTTPStatus.OK:
            if rsp.output is not None:
                if 'deployments' not in rsp.output:
                    print('There is no deployed model!')
                    return
                for deployment in rsp.output['deployments']:
                    print('Deployed_model: %s, model: %s, status: %s' % (deployment['deployed_model'], deployment['model_name'], deployment['status']))
            else:
                print('There is no deployed model.')
        else:
            print_failed_message(rsp)

    @classmethod
    def scale(cls, args):
        rsp = dashscope.Deployments.scale(args.deployed_model, args.capacity)
        if rsp.status_code == HTTPStatus.OK:
            if rsp.output is not None:
                print('Deployed_model: %s, model: %s, status: %s' % (rsp.output['deployed_model'], rsp.output['model_name'], rsp.output['status']))
            else:
                print('There is no deployed model.')
        else:
            print_failed_message(rsp)

    @classmethod
    def delete(cls, args):
        rsp = dashscope.Deployments.delete(args.deploy)
        if rsp.status_code == HTTPStatus.OK:
            print('Deployed model: %s delete success' % args.deploy)
        else:
            print_failed_message(rsp)