"""
Configuration file for dashboard parameters
Set True to display parameter, False to hide
"""

DASHBOARD_CONFIG = {
    'organization_metrics': {
        'total_projects': True,
        'total_clusters': True,
        'total_users': True,
        'billing_info': False,  # Set to False to hide billing information
    },
    'project_metrics': {
        'database_users': True,
        'database_roles': True,
        'clusters': True,
        'network_access': True,
        'api_keys': False,  # Set to False to hide API keys count
        'alerts': True,
        'project_limits': True,
    },
    'limits': {
        'show_limits': True,
        'show_usage_percentage': True,
        'highlight_near_limit': True,  # Highlight when usage > 80%
        'near_limit_threshold': 0.8,
    },
    'display_options': {
        'show_empty_projects': False,  # Hide projects with no resources
        'items_per_page': 10,
        'refresh_interval': 300,  # seconds
    }
}

# Default limits for MongoDB Atlas (adjust based on your tier)


# convert the below selected  JSON to python dict keep only keys and set the keys values as int without sub-dict
DEFAULT_LIMITS={
    'allowedShardInstanceSizeDifference': 2,
    'awsNumTenantPrivateEndpointServices': 1,
    'awsNumTenantPrivateEndpoints': 3000,
    'azureExportIops': 5000,
    'azureNumTenantPrivateEndpointServices': 8,
    'azureNumTenantPrivateEndpoints': 8000,
    'azurePrivateLinkInboundNATRuleMaximumPort': 2524,
    'azurePrivateLinkInboundNATRuleMinimumPort': 1024,
    'azurePrivateLinkMaxNodesPerPrivateLinkRegion': 150,
    'azureStreamingRestoreIops': 3500,
    'exportIops': 3000,
    'gcpPSCNATSubnetMask': 27,
    'maxActiveOnlineArchivesPerCluster': 20,
    'maxConcurrentPlans': 51,
    'maxCrossRegionNetworkPermissionEntries': 40,
    'maxCustomRolesPerUser': 20,
    'maxCustomShardKeys': 40,
    'maxDataLakeTenants': 25,
    'maxIngestionPipelines': 25,
    'maxManualDownloads': 30,
    'maxNetworkPermissionEntries': 200,
    'maxNodesPerPrivateLinkRegion': 50,
    'maxOnlineArchivesPerCluster': 50,
    'maxValidAtlasGeneratedCerts': 50,
    'maxZonesPerGeoCluster': 9,
    'mongodbUsers': 100,
    'numBackgroundCustomRoles': 100,
    'numClusters': 25,
    'numPrivateServiceConnectionsPerRegionGroup': 50,
    'numSalesSoldM0': 100,
    'numServerlessMTMs': 100,
    'numUserCustomRoles': 100,
    'privateEndpointsPerTenantInstance': 2,
    'streamingRestoreIops': 300,
}


DEFAULT_LIMITS_OLD = {
    'database_users_per_project': 100,
    'database_roles_per_project': 50,
    'clusters_per_project': 25,
    'network_access_entries': 200,
    'api_keys_per_project': 50,
}