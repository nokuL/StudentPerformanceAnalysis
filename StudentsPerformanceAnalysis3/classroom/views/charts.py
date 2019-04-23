import pygal

from ..models import Fruit


class FruitPieChart():

    def __init__(self, student, **kwargs, ):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'Personality details'
        self.student = student

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        data = {self.student.personality.energy_title: 90, self.student.personality.information_title: 20,
                self.student.personality.decision_title: 70, self.student.personality.life_title: 30}

        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)