from typing import List

from jira import JIRA
from ftea import models


class Jira_connector:
    def get_connection_data(self, request):
        connection_data = models.Jira_projects.objects.filter(jira_project_user=request.user)
        connection_data_set: List[str] = [connection_data[0].jira_project_server, connection_data[0].jira_project_login,
                               connection_data[0].jira_project_api_key]
        return connection_data_set

    def connect(self, connection_data_set: object) -> object:
        jira_server = connection_data_set[0]
        jira_user_id = connection_data_set[1]
        jira_api_key = connection_data_set[2]
        jira = JIRA(jira_server, basic_auth = (jira_user_id, jira_api_key))
        return jira







