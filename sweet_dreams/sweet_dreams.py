from stenographer import Stenographer

class SweetDreams:
    """
    Sweet dreams is a trading bot that allows you to make money even 
    while you sleep. It is the next stage of evolution of polaroid.
    """

    def __init__(self):
        self.stenographer = Stengrapher()

    def perform_task(self, task):
        # Task can be either db update or trade decision
        if task['task'] == 'update':
            self._update_price(task)

        last_order = self.stenographer.repeat_order()


    def _update_price(self, task)
