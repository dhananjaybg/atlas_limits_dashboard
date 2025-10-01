import json
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from atlas_sdk.client.api import AtlasUIApiClient

if __name__ == "__main__":
    atlas = AtlasUIApiClient(cookiejar_path="mdbcookie.pickle")
    #atlas.save_cookiejar("mdbcookie.pickle")
    result = atlas.get(f"https://cloud.mongodb.com/orgs/64ca747b952bcb462e491b03/groups").json()
    print("Done retrieving projects: ")

    print("Cookie jar saved to atlas_dashboard/mdbcookie.pickle")
