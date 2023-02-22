from dbservices.project_services import ProjectService


class ProjectManager:

    def __init__(self):
        pass

    def get_project_by_id(self, project_id):
        return ProjectService.get_project_by_projectid(project_id)