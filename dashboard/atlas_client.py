import os
import requests
from requests.auth import HTTPDigestAuth
from django.conf import settings
from typing import Dict, List, Optional
import logging

# from functools import partial
# from concurrent.futures import ThreadPoolExecutor
# from atlas_sdk.client.api import AtlasUIApiClient
from atlas_sdk.auth.atlas_cookie_auth import AtlasCookieAuth, EmployeeAtlasCookieAuth
from atlas_sdk.auth.profile import Profile


logger = logging.getLogger("dashboard")


class MongoDBAtlasClient:
    def __init__(self, public_key=None, private_key=None):
        # Use provided credentials or fall back to settings
        self.public_key = public_key or settings.MONGODB_ATLAS_CONFIG["PUBLIC_KEY"]
        self.private_key = private_key or settings.MONGODB_ATLAS_CONFIG["PRIVATE_KEY"]
        self.base_url = settings.MONGODB_ATLAS_CONFIG["BASE_URL"]
        # self.auth = None
        # self.profile
        if self.public_key and self.private_key:
            self.auth = HTTPDigestAuth(self.public_key, self.private_key)

        else:
            logger.error(
                " Authentication keys not provided, attempting cookie-based auth"
            )
            # Cache the cookie in the user's home directory
            cookie_path = os.path.join(
                os.path.expanduser("~"), "dashboardcookie.pickle"
            )
            profile = Profile(
                name="myprofile",
                cookiejar_path=cookie_path,
            )
            self.auth = EmployeeAtlasCookieAuth(profile)
            # self.auth = AtlasCookieAuth(profile)
            self.profile = profile

            ## https://cloud.mongodb.com/billing/payingOrg/linkableOrgs/6178074db1f2d87e98836e74
            ## org/6178074db1f2d87e98836e74/billing/linkOrgs
            ## https://cloud.mongodb.com/billing/payingOrg/6178074db1f2d87e98836e74/linked

            ## if not self.auth:
            ##     logger.error("Dhananjy _INIT_ Auth failed")
            ##     self.auth = None
            ## else:
            ##     logger.error("Dhananjy _INIT_ Auth Success")
            ##     # Test the authentication by making a simple request

            test_response = requests.get(
                "https://cloud.mongodb.com/admin/nds/orgs/64ca747b952bcb462e491b03/limits",
                auth=self.auth,
            )

            test_response = requests.get(
                "https://cloud.mongodb.com/orgs/64ca747b952bcb462e491b03",
                auth=self.auth,
            )
            ## test_response = requests.get("https://cloud.mongodb.com/billing/payingOrg/6178074db1f2d87e98836e74/linked", auth=self.auth)
            if test_response.status_code != 200:
                logger.error("MongoDB Atlas API authentication failed")
                self.auth = None
            else:
                logger.info(
                    "\n\n -->> MongoDB Atlas API authentication mmeded  succeeded"
                )
                logger.info(f"Test Response: {test_response.json()}")
                # iterate thru all the json sub documents and  extract the org ids
                ## org_ids = []
                ## for org in test_response.json():
                ##     org_ids.append(org['orgId'])
                ## logger.info(f"Collected Org IDs: {org_ids}")

    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make authenticated request to MongoDB Atlas API"""
        if not self.auth:
            logger.error("MongoDB Atlas API credentials not configured")
            return None

        try:
            url = f"{self.base_url}/{endpoint}"
            logger.info(f"Making request to: {url}")
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Atlas API request failed for {endpoint}: {e}")
            return None

    def get_linked_organization(self, org_id: str) -> Optional[Dict]:
        """Get organization details"""
        data = self._make_request(f"billing/payingOrg/{org_id}/linked")
        org_ids = []
        for org in data.json():
            org_ids.append(org["orgId"])
        return org_ids

    def get_organization(self, org_id: str) -> Optional[Dict]:
        """Get organization details"""
        return self._make_request(f"orgs/{org_id}")

    def get_organization_projects(self, org_id: str) -> List[Dict]:
        """Get all projects in an organization"""
        data = self._make_request(f"orgs/{org_id}/groups")
        # logger.info(f"get_organization_projects Projects data: {data}")
        return data if data else []  # data.get('results', []) if data else []

    def get_project_database_users(self, project_id: str) -> List[Dict]:
        """Get database users for a project"""
        # data = self._make_request(f"groups/{project_id}/databaseUsers")
        data = self._make_request(f"admin/nds/groups/{project_id}")
        # logger.info(f"get_project_database_users Users data: {data["users"]}")
        return data["users"] if data else []  # data.get('results', []) if data else []

    def get_project_custom_roles(self, project_id: str) -> List[Dict]:
        """Get custom database roles for a project"""
        # data = self._make_request(f"groups/{project_id}/customDBRoles/roles")
        data = self._make_request(f"admin/nds/groups/{project_id}")
        # logger.info(f"get_project_custom_roles Roles data: {data['customDBRoles']}")
        return (
            data["customDBRoles"] if data else []
        )  # data.get('results', []) if data else []

    def get_project_limits(self, project_id: str) -> List[Dict]:
        """Get limits for a project"""
        # data = self._make_request(f"groups/{project_id}/customDBRoles/roles")
        data = self._make_request(f"admin/nds/groups/{project_id}/limits")
        # logger.info(f"get_project_limits data: {data}")
        return data if data else []  # data.get('results', []) if data else []

    def get_project_clusters(self, project_id: str) -> List[Dict]:
        """Get clusters in a project"""
        # data = self._make_request(f"groups/{project_id}/clusters")
        data = self._make_request(f"orgs/{project_id}/groups")
        logger.info(f"get_project_clusters Clusters data: {data}")
        return data if data else []  # data.get('results', []) if data else []

    def get_project_network_access(self, project_id: str) -> List[Dict]:
        """Get network access whitelist for a project"""
        data = self._make_request(f"groups/{project_id}/accessList")
        logger.info(f"get_project_network_access Network Access data: {data}")
        return data if data else []  # data.get('results', []) if data else []

    def get_project_api_keys(self, project_id: str) -> List[Dict]:
        """Get API keys for a project"""
        data = self._make_request(f"groups/{project_id}/apiKeys")
        logger.info(f"get_project_api_keys API Keys data: {data}")
        return data if data else []  # data.get('results', []) if data else []

    def get_project_alerts(self, project_id: str) -> List[Dict]:
        """Get alerts for a project"""
        data = self._make_request(f"groups/{project_id}/alerts?status=OPEN")
        logger.info(f"get_project_alerts Alerts data: {data}")
        return data if data else []  # data.get('results', []) if data else []
