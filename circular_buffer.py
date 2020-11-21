class circular_buffer:      
    def __init__(self,buffer_size):
        self.top = 0        #top of circular buffer
        self.botton  = 0    #botton of circular buffer
        
        self.buffer_size = buffer_size   #size of buffer

        self.buffer = [' '] * buffer_size   #init buffer

    def add_item(self,item):    #methode >>use add item into buffer
        if self.buffer[self.botton] == ' ': #  'x' 
            self.buffer[self.botton] = item #.append
            self.botton += 1
            if self.botton >= self.buffer_size:         #if buffer overflow   
                self.botton = 0
        else:
            print("over item")
            return None

    def remove_item(self):
        if self.buffer[self.top]  != ' ':
            data = self.buffer[self.top] 
            self.buffer[self.top] = ' '
            self.top += 1
            if self.top >= self.buffer_size:
                self.top = 0
            return data
        else:
            print("none item")
            return None

    def display(self):
        return self.buffer