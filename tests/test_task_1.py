import unittest
from task_1 import *
import datetime


class TestTask1(unittest.TestCase):
    def setUp(self):
        self.developers = [
            Developer(1, 'Turkish', '3328 Ferry Street', '256-617-8682', 'a@b.com', 950, 'Python Developer', 'Junior'),
            Developer(2, 'Tommy', '2095 Whispering Pines Circle', '214-636-2426', 'b@b.com', 1000, 'Python Developer', 'Junior'),
            Developer(3, 'George', '4206 Murphy Court', '612-799-3741', 'c@b.com', 1150, 'Python Developer', 'Junior'),
            Developer(4, 'Mickey', '4839 Lighthouse Drive', '774-261-9375', 'd@b.com', 1100, 'Python Developer', 'Junior'),
        ]

        self.qas = [
            QualityAssurance(5, 'Vinny', '917 Hall Street', '217-216-9562', 'e@b.com', 1500, 'QA Engineer', 'Middle'),
            QualityAssurance(6, 'Sol', '2820 Woodstock Drive', '323-819-5353', 'f@b.com', 1600, 'QA Engineer', 'Middle')
        ]

        self.pms = [
            ProjectManager(7, 'Brick Top', '2398 Kooter Lane', '704-466-2756', 'g@b.com', 2000),
            ProjectManager(8, 'Avi', '223 Moore Avenue', '214-498-7396', 'h@b.com', 2000)
        ]

        self.projects = [
            Project('Design Patterns Homework', datetime.date(2021, 9, 1)),
            Project('Functional Programming Homework', datetime.date(2021, 9, 1))
        ]

    def test_assign(self):
        self.developers[0].assign(self.projects[0])
        self.developers[0].assign(self.projects[0])
        self.developers[0].assign(self.projects[1])
        self.developers[0].assign(self.projects[1])

        self.developers[1].assign(self.projects[0])
        self.developers[1].assign(self.projects[0])
        self.developers[1].assign(self.projects[0])

        self.developers[2].assign(self.projects[1])
        self.developers[2].assign(self.projects[1])
        self.developers[2].assign(self.projects[1])
        self.developers[2].assign(self.projects[1])
        self.developers[2].assign(self.projects[1])

        self.assertEqual(len(self.developers[0].assigned_projects()), 2)
        self.assertEqual(len(self.developers[1].assigned_projects()), 1)
        self.assertEqual(len(self.developers[2].assigned_projects()), 1)
        self.assertEqual(len(self.developers[3].assigned_projects()), 0)

        self.assertEqual(len(self.projects[0].developers), 2)
        self.assertEqual(len(self.projects[1].developers), 2)

    def test_assign_possibility(self):
        self.developers[0].assign(self.projects[0])
        self.developers[0].assign(self.projects[1])
        self.developers[1].assign(self.projects[0])
        self.developers[2].assign(self.projects[1])

        self.assertFalse(self.developers[0].assign_possibility(self.projects[0]))
        self.assertFalse(self.developers[0].assign_possibility(self.projects[1]))

        self.assertFalse(self.developers[1].assign_possibility(self.projects[0]))
        self.assertTrue(self.developers[1].assign_possibility(self.projects[1]))

        self.assertTrue(self.developers[2].assign_possibility(self.projects[0]))
        self.assertFalse(self.developers[2].assign_possibility(self.projects[1]))

        self.assertTrue(self.developers[3].assign_possibility(self.projects[0]))
        self.assertTrue(self.developers[3].assign_possibility(self.projects[1]))

    def test_unassign(self):
        self.developers[0].assign(self.projects[0])
        self.developers[0].assign(self.projects[1])

        self.developers[0].unassign(self.projects[0])
        self.developers[0].unassign(self.projects[1])

        self.assertEqual(len(self.developers[0].assigned_projects()), 0)
        self.assertEqual(len(self.projects[0].developers), 0)
        self.assertEqual(len(self.projects[1].developers), 0)

    def test_get_tasks_to_date(self):
        self.developers[0].assign(self.projects[0])
        self.developers[0].assignments[0].received_tasks[datetime.date(2021, 9, 2)] = 'lab_1'
        self.developers[0].assignments[0].received_tasks[datetime.date(2021, 9, 9)] = 'lab_1_2'

        self.assertEqual(self.developers[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 2)), 'lab_1')
        self.assertEqual(self.developers[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 9)), 'lab_1_2')
        self.assertEqual(self.developers[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 16)), None)

    def test_add_developer(self):
        self.projects[0].add_developer(self.developers[0])
        self.projects[0].add_developer(self.developers[1])
        self.projects[0].add_developer(self.developers[2])

        self.assertTrue(self.developers[0] in self.projects[0].developers)
        self.assertTrue(self.developers[1] in self.projects[0].developers)
        self.assertTrue(self.developers[2] in self.projects[0].developers)
        self.assertFalse(self.developers[3] in self.projects[0].developers)

    def test_remove_developer(self):
        self.projects[0].add_developer(self.developers[0])
        self.projects[0].add_developer(self.developers[1])
        self.projects[0].add_developer(self.developers[2])
        self.projects[0].add_developer(self.developers[3])

        self.projects[0].remove_developer(self.developers[0])
        self.projects[0].remove_developer(self.developers[2])

        self.assertFalse(self.developers[0] in self.projects[0].developers)
        self.assertTrue(self.developers[1] in self.projects[0].developers)
        self.assertFalse(self.developers[2] in self.projects[0].developers)
        self.assertTrue(self.developers[3] in self.projects[0].developers)

    def test_test(self):
        self.assertEqual(self.qas[0].test(self.projects[0]), 'Vinny (Middle QA Engineer) is testing ' +
                         '\'Design Patterns Homework\'')
        self.assertEqual(self.qas[0].test(self.projects[1]), 'Vinny (Middle QA Engineer) is testing ' +
                         '\'Functional Programming Homework\'')
        self.assertEqual(self.qas[1].test(self.projects[0]), 'Sol (Middle QA Engineer) is testing ' +
                         '\'Design Patterns Homework\'')
        self.assertEqual(self.qas[1].test(self.projects[1]), 'Sol (Middle QA Engineer) is testing ' +
                         '\'Functional Programming Homework\'')

    def test_discuss_progress(self):
        self.pms[0].project = self.projects[0]
        self.pms[1].project = self.projects[1]

        self.developers[0].assign(self.projects[0])
        self.developers[1].assign(self.projects[0])
        self.developers[2].assign(self.projects[1])
        self.developers[3].assign(self.projects[1])

        self.assertEqual(self.pms[0].discuss_progress(self.developers[0]),
                         'Brick Top (Project Manager of \'Design Patterns Homework\') is discussing progress with ' +
                         'Turkish (Junior Python Developer)')
        self.assertEqual(self.pms[0].discuss_progress(self.developers[1]),
                         'Brick Top (Project Manager of \'Design Patterns Homework\') is discussing progress with ' +
                         'Tommy (Junior Python Developer)')
        self.assertEqual(self.pms[0].discuss_progress(self.developers[2]),
                         'Brick Top and George do not work on the same project')
        self.assertEqual(self.pms[0].discuss_progress(self.developers[3]),
                         'Brick Top and Mickey do not work on the same project')

        self.assertEqual(self.pms[1].discuss_progress(self.developers[0]),
                         'Avi and Turkish do not work on the same project')
        self.assertEqual(self.pms[1].discuss_progress(self.developers[1]),
                         'Avi and Tommy do not work on the same project')
        self.assertEqual(self.pms[1].discuss_progress(self.developers[2]),
                         'Avi (Project Manager of \'Functional Programming Homework\') is discussing progress with ' +
                         'George (Junior Python Developer)')
        self.assertEqual(self.pms[1].discuss_progress(self.developers[3]),
                         'Avi (Project Manager of \'Functional Programming Homework\') is discussing progress with ' +
                         'Mickey (Junior Python Developer)')
