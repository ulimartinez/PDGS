import os


# Class Workspace collaborates with GUI
# Displays project name and its specific protocol.
# Projects can be imported and exported from the workspace
# @param (name, path, protocol, layout)


class Workspace:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.listProjects = []

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_path(self):
        return self.path

    def set_path(self, value):
        self.path = value

    def get_list(self):
        return self.listProjects

    def addProjectToList(self,project):
        self.listProjects.append(project)
        self.listProjects.sort()


# creates new workspace directory with description
# @\requires (name != null or contain illegal characters) && (save_path exists)
# @\ensures project exists at save_path with description text file
def new_workspace(name, save_path):
    # Check if path exists
    if verify_path(save_path):
        # Set directory at save_path
        os.chdir(save_path)
        try:
            # If workspace name doesn't exists create new workspace
            os.makedirs(name, 1)
            created_workspace = Workspace(name, save_path)
            c_workspace = created_workspace.get_name()

        except OSError as e:
            print('Workspace name already exists: Workspace not created.')


# verify directory path
def verify_path(path):
    if os.path.exists(path):
        return 1
