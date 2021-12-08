from abc import ABCMeta, abstractmethod
import random


class Feature:
    def __init__(self, feature_id: int, expected_quality: int):
        self.id = feature_id
        self.is_complete = False
        self.expected_quality = expected_quality
        self.quality = 0


class Software(metaclass=ABCMeta):
    def __init__(self):
        self.features = []


class MobileApp(Software):
    def __init__(self, platform: str):
        super().__init__()
        self.platform = platform

    
class WebApp(Software):
    def __init__(self, backend: str, frontend: str):
        super().__init__()
        self.backend = backend
        self.fronted = frontend


class DatabaseAPI(Software):
    def __init__(self, database: str):
        super().__init__()
        self.database = database


class Containerization(Software):
    def __init__(self, content, dependencies):
        self.content = content
        self.dependencies = dependencies


class Deployment(Software):
    def __init__(self, app, system):
        self.app = app
        self.system = system


class Employee(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name = name


class Developer(Employee):
    def __init__(self, name: str, skill: int):
        super().__init__(name)
        self.skill = skill
    
    def work_on_feature(self, feature: Feature):
        feature.quality += random.randint(0, self.skill)


class SoftwareArchitect(Employee):
    def __init__(self, name: str):
        super().__init__(name)
    
    def design_features(self, app: Software, feature_count: int):
        for i in range(feature_count):
            app.features.append(Feature(len(app.features), random.randint(5, 30)))


# Decorator
class TeamLead(Developer):
    def __init__(self, developer: Developer):
        self._developer = developer
        self.name = developer.name
        self.assignments = {}
        self.idle_developers = []
    
    @property
    def skill(self):
        return self._developer.skill
    
    @skill.setter
    def skill(self, value: int):
        self._developer.skill = value

    def work_on_feature(self, feature: Feature):
        self._developer.work_on_feature(feature)
    
    # Observer
    def assign_tasks(self, facade):
        for feature in facade.app.features:
            self.assignments[feature] = []
        
        self.idle_developers = facade.developers

        for feature in self.assignments:
            if len(self.assignments[feature]) == 0:
                self.assignments[feature].append(self.idle_developers.pop(0))
            if len(self.idle_developers) <= 0:
                break
        
        self.distribute_spare_devs()
    
    def distribute_spare_devs(self):
        while len(self.idle_developers) > 0:
            for feature in self.assignments:
                self.assignments[feature].append(self.idle_developers.pop(0))
                if len(self.idle_developers) <= 0:
                    break
    
    def order_work(self):
        modified_features = []

        for feature in self.assignments:
            if len(self.assignments[feature]) > 0:
                modified_features.append(feature)
                for developer in self.assignments[feature]:
                    developer.work_on_feature(feature)
        
        return modified_features
    
    # Observer
    def reassign_tasks(self, facade):
        for feature in facade.completed_features:
            self.idle_developers += self.assignments[feature]
            self.assignments.pop(feature)
        
        if len(self.assignments) <= 0:
            return True
        
        self.distribute_spare_devs()
        return False


class QualityAssurance(Employee):
    def __init__(self, name: str):
        super().__init__(name)
    
    # Observer
    def test_features(self, facade):
        completed_features = []
        for feature in facade.modified_features:
            if feature.quality >= feature.expected_quality:
                completed_features.append(feature)
                print(f'Feature {feature.id} has been completed')
        
        return completed_features


class BusinessAnalyst(Employee):
    def __init__(self, name: str):
        super().__init__(name)
    
    def distribute_budget(self, budget: float):
        feature_count = budget // 200
        return feature_count


# Facade
class SoftwareDevelopmentFacade:
    def __init__(self, business_analyst: BusinessAnalyst, software_architect: SoftwareArchitect, 
        team_lead: TeamLead, developers, quality_assurance: QualityAssurance):
        self.business_analyst = business_analyst
        self.software_architect = software_architect
        self.team_lead = team_lead
        self.developers = developers
        self.quality_assurance = quality_assurance

        self.modified_features = []
        self.completed_features = []
        self.app = None
    
    def develop_software(self, budget: float, type: str, *args):
        # Factory
        if type == 'mobile':
            self.app = MobileApp(*args)
        elif type == 'web':
            self.app = WebApp(*args)
        elif type == 'api':
            self.app = DatabaseAPI(*args)
        elif type == 'container':
            self.app = Containerization(*args)
        elif type == 'deploy':
            self.app = Deployment(*args)
        else:
            return None

        feature_count = self.business_analyst.distribute_budget(budget)
        self.software_architect.design_features(self.app, feature_count)

        self.team_lead.assign_tasks(self)
        is_completed = False

        while not is_completed:
            self.modified_features = self.team_lead.order_work()
            self.completed_features = self.quality_assurance.test_features(self)
            self.modified_features = []
            is_completed = self.team_lead.reassign_tasks(self)
            self.completed_features = []
        
        print('App has been completed')
        
        result = self.app
        self.app = None

        return result

business_analyst = BusinessAnalyst('A')
software_architect = SoftwareArchitect('B')
developers = [
    TeamLead(Developer('D', 5)),
    Developer('E', 7),
    Developer('F', 9)
]
quality_assurance = QualityAssurance('G')

facade = SoftwareDevelopmentFacade(business_analyst, software_architect, developers[0], developers, quality_assurance)
app = facade.develop_software(2000, 'mobile', 'Android')