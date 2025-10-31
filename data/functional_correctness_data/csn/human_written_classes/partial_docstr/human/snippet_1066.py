class Constraints:

    def __init__(self, args, conduct_dispatch_disaggregation, apply_on='grid_model'):
        self.args = args
        self.conduct_dispatch_disaggregation = conduct_dispatch_disaggregation
        self.apply_on = apply_on

    def functionality(self, network, snapshots):
        """Add constraints to pypsa-model using extra-functionality.
        Serveral constraints can be choosen at once. Possible constraints are
        set and described in the above functions.

        Parameters
        ----------
        network : :class:`pypsa.Network`
            Overall container of PyPSA
        snapshots : pandas.DatetimeIndex
            List of timesteps considered in the optimization

        """
        if 'CH4' in network.buses.carrier.values:
            if self.args['method']['formulation'] == 'pyomo':
                if self.args['scn_name'] in ['eGon100RE', 'powerd2025', 'powerd2030', 'powerd2035']:
                    add_electrolysis_coupling_constraints(network, snapshots)
                    add_chp_constraints_simplyfied(network, snapshots)
                else:
                    add_chp_constraints(network, snapshots)
                if (self.args['scn_name'] != 'status2019') & (len(snapshots) > 1500):
                    add_ch4_constraints(self, network, snapshots)
                    add_biomass_constraint(self, network, snapshots)
            elif self.args['method']['formulation'] == 'linopy':
                if (self.args['scn_name'] != 'status2019') & (len(snapshots) > 1500):
                    add_ch4_constraints_linopy(self, network, snapshots)
                    add_biomass_constraint_linopy(self, network, snapshots)
                if self.apply_on == 'last_market_model':
                    fixed_storage_unit_soc_at_the_end(network, snapshots)
                elif self.apply_on == 'market_model':
                    fixed_storage_unit_soc_at_horizon_end(self, network, snapshots)
                add_chp_constraints_linopy(network, snapshots)
            else:
                add_chp_constraints_nmp(network)
                if self.args['scn_name'] != 'status2019':
                    add_ch4_constraints_nmp(self, network, snapshots)
        for constraint in self.args['extra_functionality'].keys():
            if self.args['method']['formulation'] == 'pyomo':
                try:
                    eval('_' + constraint + '(self, network, snapshots)')
                    logger.info('Added extra_functionality {}'.format(constraint))
                except:
                    logger.warning('Constraint {} not defined'.format(constraint) + '. New constraints can be defined in' + ' etrago/tools/constraint.py.')
            elif self.args['method']['formulation'] == 'linopy':
                try:
                    eval('_' + constraint + '_linopy(self, network, snapshots)')
                    logger.info('Added extra_functionality {}'.format(constraint))
                except:
                    logger.warning('Constraint {} not defined for linopy formulation'.format(constraint) + '. New constraints can be defined in' + ' etrago/tools/constraint.py.')
            else:
                try:
                    eval('_' + constraint + '_nmp(self, network, snapshots)')
                    logger.info('Added extra_functionality {} without pyomo'.format(constraint))
                except:
                    logger.warning('Constraint {} not defined'.format(constraint))
        if self.args['snapshot_clustering']['active'] and self.args['snapshot_clustering']['method'] == 'typical_periods':
            if self.args['snapshot_clustering']['storage_constraints'] == 'daily_bounds':
                if self.args['method']['pyomo']:
                    snapshot_clustering_daily_bounds(self, network, snapshots)
                else:
                    snapshot_clustering_daily_bounds_nmp(self, network, snapshots)
            elif self.args['snapshot_clustering']['storage_constraints'] == 'soc_constraints':
                if self.args['snapshot_clustering']['how'] == 'hourly':
                    if self.args['method']['pyomo']:
                        snapshot_clustering_seasonal_storage_hourly(self, network, snapshots)
                    else:
                        snapshot_clustering_seasonal_storage_hourly_nmp(self, network, snapshots)
                elif self.args['method']['pyomo']:
                    snapshot_clustering_seasonal_storage(self, network, snapshots)
                else:
                    snapshot_clustering_seasonal_storage_nmp(self, network, snapshots)
            elif self.args['snapshot_clustering']['storage_constraints'] == 'soc_constraints_simplified':
                if self.args['snapshot_clustering']['how'] == 'hourly':
                    logger.info('soc_constraints_simplified not possible while hourly\n                        clustering -> changed to soc_constraints')
                    if self.args['method']['pyomo']:
                        snapshot_clustering_seasonal_storage_hourly(self, network, snapshots)
                    else:
                        snapshot_clustering_seasonal_storage_hourly_nmp(self, network, snapshots)
                if self.args['method']['pyomo']:
                    snapshot_clustering_seasonal_storage(self, network, snapshots, simplified=True)
                else:
                    snapshot_clustering_seasonal_storage_nmp(self, network, snapshots, simplified=True)
            else:
                logger.error('If you want to use constraints considering the storage\n                    behaviour, snapshot clustering constraints must be in\n                    [daily_bounds, soc_constraints,\n                     soc_constraints_simplified]')
        if self.conduct_dispatch_disaggregation is not False:
            if self.args['method']['formulation'] == 'pyomo':
                split_dispatch_disaggregation_constraints(self, network, snapshots)
            else:
                split_dispatch_disaggregation_constraints_nmp(self, network, snapshots)