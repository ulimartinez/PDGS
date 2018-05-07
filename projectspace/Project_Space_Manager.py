import os
from Project import *
from Workspace import *


def project_manager(action,workspace,project):
    if (action == "getProjectName"):
        return get_name(project)

    elif (action == "getProjectLayout"):
        return get_layout(project)

    elif (action == "getListOfProjects"):
        return get_list(workspace)
