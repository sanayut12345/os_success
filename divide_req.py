class divide_req:
    def __init__(self,request_all,number_thread):
        self.request = request_all
        self.number = number_thread
        self.list = [0]*self.number
        self.index = 0
        while self.request > 0:
            self.list[self.index] = self.list[self.index] + 1
            self.index = self.index + 1
            self.request = self.request - 1    
            if self.index >= self.number:
                self.index = 0
    def value(self):
        return self.list

