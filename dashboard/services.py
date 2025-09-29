from .atlas_client import MongoDBAtlasClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from driver_config import DASHBOARD_CONFIG, DEFAULT_LIMITS
from typing import Dict, List, Any
import logging

logger = logging.getLogger('dashboard')

class DashboardService:
    def __init__(self, public_key=None, private_key=None):
        self.atlas_client = MongoDBAtlasClient(public_key, private_key)
        self.config = DASHBOARD_CONFIG
    
    def get_linked_organizations(self, org_id: str) -> List[str]:
        """Get linked organizations for a given organization ID"""
        try:
            logger.info(f"Fetching linked organizations for organization: {org_id}")
            linked_orgs = self.atlas_client.get_linked_organization(org_id)
            if not linked_orgs:
                logger.warning(f"No linked organizations found or API credentials invalid for org: {org_id}")
                return []
            logger.info(f"Linked organizations retrieved: {linked_orgs}")
            return linked_orgs
        except Exception as e:
            logger.error(f"Error getting linked organizations: {e}")
            return []   
        
    def get_organization_data(self, org_id: str) -> Dict[str, Any]:
        """Get comprehensive organization data"""
        try:
            logger.info(f"Fetching data for organization: {org_id}")
            
            # Get organization info
            org_data = self.atlas_client.get_organization(org_id)
            if not org_data:
                return {'error': 'Organization not found or API credentials invalid'}
            
            logger.info(f"Organization data retrieved")

            # Get projects
            projects = self.atlas_client.get_organization_projects(org_id)
            logger.info(f"Found {len(projects)} projects")
            
            logger.info(f"Organization PROJECT data retrieved")

            # Process each project
            processed_projects = []
            total_metrics = {
                'total_projects': len(projects),
                'total_clusters': 0,
                'total_users': 0,
                'total_roles': 0,
                'total_limits': 0,
            }

            for project in projects:
                logger.info(f"Processing project: {project['name']} ({project['id']})")
                project_data = self._get_project_metrics(project['id'], project['name'],clusters=project['numCluster'])
                
                # Update totals
                total_metrics['total_clusters'] += project['numCluster']
                total_metrics['total_users'] += project['users']
                total_metrics['total_roles'] += project_data.get('database_roles_count', 0)
                total_metrics['total_limits'] += project_data.get('project_limits_count', 0)


                # Only include project if it has resources or if config allows empty projects
                if (self.config['display_options']['show_empty_projects'] or 
                    self._project_has_resources(project_data)):
                    processed_projects.append(project_data)

            return {
                'organization': org_data,
                'projects': processed_projects,
                'metrics': self._filter_metrics(total_metrics, 'organization_metrics'),
                'config': self.config
            }

        except Exception as e:
            logger.error(f"Error getting organization data: {e}")
            return {'error': str(e)}

    def _get_project_metrics(self, project_id: str, project_name: str,clusters: int) -> Dict[str, Any]:
        """Get metrics for a single project"""
        metrics = {
            'id': project_id,
            'name': project_name,
            'clusters': clusters,
        }

        try:
            # Get various project resources based on configuration
            ## if self.config['project_metrics']['database_users']:
            ##     users = self.atlas_client.get_project_database_users(project_id)
            ##     metrics['database_users_count'] = len(users)
            ##     metrics['database_users_limit'] = DEFAULT_LIMITS['database_users_per_project']
            ##     metrics['database_users_percentage'] = (
            ##         len(users) / DEFAULT_LIMITS['database_users_per_project'] * 100
            ##     )
                
            ## if self.config['project_metrics']['database_roles']:
            ##     roles = self.atlas_client.get_project_custom_roles(project_id)
            ##     metrics['database_roles_count'] = len(roles)
            ##     metrics['database_roles_limit'] = DEFAULT_LIMITS['database_roles_per_project']
            ##     metrics['database_roles_percentage'] = (
            ##         len(roles) / DEFAULT_LIMITS['database_roles_per_project'] * 100
            ##     )
                
            if self.config['project_metrics']['project_limits']:
                limits = self.atlas_client.get_project_limits(project_id)
                #logger.info(f"Project Limits data: {limits}")

                for key, value in limits.items():
                    if value.get("currentUsage") is not None and value.get("currentUsage") != 0:
                        #logger.info(f"Key: {key}, currentLimit: {value['currentLimit']}, currentUsage: {value['currentUsage']}")
                        metrics[f"{key}_count"] = value.get("currentUsage", 0)
                        metrics[f"{key}_limit"] = value.get("currentLimit", 0)
                        #pick the default limit from DEFAULT_LIMITS if key exists
                        if key in DEFAULT_LIMITS:
                            metrics[f"{key}_default"] = DEFAULT_LIMITS[key]
                        else:
                            metrics[f"{key}_default"] = 000
                        #metrics[f"{key}_default"] = DEFAULT_LIMITS[key]
                        if value.get("currentLimit", 0) > 0:
                            metrics[f"{key}_percentage"] = (
                                value.get("currentUsage", 0) / value.get("currentLimit", 1) * 100
                            )
                        else:
                            metrics[f"{key}_percentage"] = 0 # Avoid division by zero 
        

            if self.config['project_metrics']['clusters']:
                #clusters = self.atlas_client.get_project_clusters(project_id)
                metrics['clusters_count'] = clusters
                metrics['clusters_limit'] = DEFAULT_LIMITS['clusters']
                metrics['clusters_percentage'] = (
                    clusters / DEFAULT_LIMITS['clusters_per_project'] * 100
                )
#
            #if self.config['project_metrics']['network_access']:
            #    network_entries = self.atlas_client.get_project_network_access(project_id)
            #    metrics['network_access_count'] = len(network_entries)
            #    metrics['network_access_limit'] = DEFAULT_LIMITS['network_access_entries']
            #    metrics['network_access_percentage'] = (
            #        len(network_entries) / DEFAULT_LIMITS['network_access_entries'] * 100
            #    )
#
            #if self.config['project_metrics']['api_keys']:
            #    api_keys = self.atlas_client.get_project_api_keys(project_id)
            #    metrics['api_keys_count'] = len(api_keys)
            #    metrics['api_keys_limit'] = DEFAULT_LIMITS['api_keys_per_project']
            #    metrics['api_keys_percentage'] = (
            #        len(api_keys) / DEFAULT_LIMITS['api_keys_per_project'] * 100
            #    )
#
            #if self.config['project_metrics']['alerts']:
            #    alerts = self.atlas_client.get_project_alerts(project_id)
            #    metrics['alerts_count'] = len(alerts)

            # Add status indicators
            metrics['status_indicators'] = self._get_status_indicators(metrics)

        except Exception as e:
            logger.error(f"Error getting metrics for project {project_id}: {e}")
            metrics['error'] = str(e)

        return metrics

    def _project_has_resources(self, project_data: Dict) -> bool:
        """Check if project has any resources"""
        resource_counts = [
            project_data.get('database_users_count', 0),
            project_data.get('database_roles_count', 0),
            project_data.get('clusters_count', 0),
            project_data.get('network_access_count', 0),
            project_data.get('api_keys_count', 0),
        ]
        return sum(resource_counts) > 0

    def _get_status_indicators(self, metrics: Dict) -> Dict[str, str]:
        """Get status indicators for metrics"""
        indicators = {}
        threshold = self.config['limits']['near_limit_threshold']

        for key, value in metrics.items():
            if key.endswith('_percentage'):
                metric_name = key.replace('_percentage', '')
                if value >= threshold * 100:
                    indicators[metric_name] = 'warning'
                elif value >= 90:
                    indicators[metric_name] = 'danger'
                else:
                    indicators[metric_name] = 'success'

        return indicators

    def _filter_metrics(self, metrics: Dict, config_key: str) -> Dict:
        """Filter metrics based on configuration"""
        if config_key not in self.config:
            return metrics

        filtered = {}
        for key, value in metrics.items():
            if key in self.config[config_key] and self.config[config_key][key]:
                filtered[key] = value

        return filtered
