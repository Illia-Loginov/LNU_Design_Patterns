class Employee:
    def __init__(self, employee_id, name, address, phone_number, email, salary):
        self.id = employee_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.salary = salary


class Developer(Employee):
    def __init__(self, employee_id, name, address, phone_number, email, salary, position, rank):
        super().__init__(employee_id, name, address, phone_number, email, salary)
        self.position = position
        self.rank = rank
        self.assignments = []

    def assign_possibility(self, project):
        if project in self.assigned_projects():
            return False
        else:
            return True

    def assigned_projects(self):
        projects = []

        for assignment in self.assignments:
            projects.append(assignment.project)

        return projects

    def assign(self, project):
        if not self.assign_possibility(project):
            return

        project.add_developer(self)
        self.assignments.append(Assignment(project))

    def unassign(self, project):
        for i in range(len(self.assignments)):
            if self.assignments[i].project == project:
                project.remove_developer(self)
                del self.assignments[i]
                return


class Assignment:
    def __init__(self, project):
        self.project = project
        self.received_tasks = {}

    def get_tasks_to_date(self, date):
        return self.received_tasks.get(date)


class Project:
    def __init__(self, title, start_date):
        self.title = title
        self.start_date = start_date
        self.task_list = []
        self.developers = []

    def add_developer(self, developer):
        if developer not in self.developers:
            self.developers.append(developer)

    def remove_developer(self, developer):
        for i in range(len(self.developers)):
            if self.developers[i] == developer:
                del self.developers[i]
                return


class QualityAssurance(Employee):
    def __init__(self, employee_id, name, address, phone_number, email, salary, position, rank):
        super().__init__(employee_id, name, address, phone_number, email, salary)
        self.position = position
        self.rank = rank

    def test(self, project):
        return f'{self.name} ({self.rank} {self.position}) is testing \'{project.title}\''


class ProjectManager(Employee):
    def __init__(self, employee_id, name, address, phone_number, email, salary, project=None):
        super().__init__(employee_id, name, address, phone_number, email, salary)
        self.project = project

    def discuss_progress(self, developer):
        if self.project is not None and self.project in developer.assigned_projects():
            return f'{self.name} (Project Manager of \'{self.project.title}\') is discussing progress with ' \
                   f'{developer.name} ({developer.rank} {developer.position})'
        else:
            return f'{self.name} and {developer.name} do not work on the same project'
