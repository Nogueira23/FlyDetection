class ReportPapper:
    def __init__(self):
        self.head = 'FlytType;Amount\n'
        self.amount = 0
        self.line = f'Tephritidae;{0}'
    

    def Registrer(self):
        try:
            with open('results.csv', 'r') as results:
                pass  
        except FileNotFoundError:
            with open('results.csv', 'w') as results:
                results.write(self.head)
                results.write(self.line)

    def Update(self):
        with open('results.csv', 'w') as results:
            self.line = f'Tephritidae;{self.amount}'
            results.write(self.head)
            results.write(self.line)