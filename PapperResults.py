from datetime import datetime

class ReportPapper:
    def __init__(self):
        self.head = 'FlytType;id;data\n'
    

    def Registrer(self):
        try:
            with open('results.csv', 'r') as results:
                pass  
        except FileNotFoundError:
            with open('results.csv', 'w') as results:
                results.write(self.head)

    def Update(self, flys):
        with open('results.csv', 'w') as results:
            for fly in flys:
                line = f'MoscaFruta;{fly[0]};{fly[-1]}'
                results.write(line)