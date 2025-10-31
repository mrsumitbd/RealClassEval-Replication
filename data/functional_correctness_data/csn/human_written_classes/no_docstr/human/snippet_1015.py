import logging
import os

class Options:
    collect_methods = ('mv', 'cp', 'plotdata', 'image', 'custom')

    def __init__(self, args):
        self._valid = True
        self.particle_no = args.particle_no
        if self.particle_no < 1:
            logger.error('Number of particles should be positive integer (got ' + str(self.particle_no) + ' instead')
            self._valid = False
        self.jobs_no = args.jobs_no
        if self.jobs_no < 1:
            logger.error('Number of jobs should be positive integer (got ' + str(self.jobs_no) + ' instead')
            self._valid = False
        self.input_path = args.input
        if not os.path.exists(self.input_path):
            logger.error('Input path ' + str(self.input_path) + " doesn't exists")
            self._valid = False
        self.input_path = os.path.abspath(self.input_path)
        if args.workspace is not None:
            if not os.path.exists(args.workspace):
                logger.warning('Workspace dir ' + args.workspace + " doesn't exists, will be created.")
            self.root_dir = args.workspace
        elif os.path.isdir(self.input_path):
            self.root_dir = self.input_path
        else:
            self.root_dir = os.path.dirname(self.input_path)
        logger.debug('Root directory: ' + str(self.root_dir))
        self.mc_run_template = args.mc_run_template
        if self.mc_run_template is not None and (not os.path.exists(self.mc_run_template)):
            logging.error('MC run template ' + self.mc_run_template + " doesn't exists")
            self._valid = False
        else:
            logger.debug('MC run template: ' + str(self.mc_run_template))
        self.scheduler_options = args.scheduler_options
        if self.scheduler_options is not None:
            if not os.path.exists(self.scheduler_options):
                if not (self.scheduler_options[0] == '[' and self.scheduler_options[-1] == ']'):
                    logger.error('-s should be followed by a path or text enclosed in square brackets, i.e. [--help]')
                    self._valid = False
                else:
                    logger.debug('scheduler options: ' + str(self.scheduler_options))
            else:
                logger.debug('scheduler options header file: ' + str(self.scheduler_options))
        self.mc_engine_options = args.mc_engine_options
        if self.mc_engine_options is not None:
            if not os.path.exists(self.mc_engine_options):
                if not (self.mc_engine_options[0] == '[' and self.mc_engine_options[-1] == ']'):
                    logger.error('-e should be followed by a path or text enclosed in square brackets, i.e. [--help]')
                    self._valid = False
                else:
                    logger.debug('MC engine options: ' + str(self.mc_engine_options))
            else:
                logger.debug('MC engine options header file: ' + str(self.mc_engine_options))
        self.external_files = args.external_files
        if self.external_files is not None:
            logger.info('Files : {}'.format(self.external_files))
            for file_path in self.external_files:
                if not os.path.exists(file_path):
                    logger.error("External file {:s} doesn't exists".format(file_path))
                    self._valid = False
        self.collect = args.collect
        self.batch = args.batch

    @property
    def valid(self):
        return self._valid