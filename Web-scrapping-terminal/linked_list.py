class Node:

    def __init__(self, value = None):
        
        self.value = value
        self.next = None

class LinkedList:

    def __init__(self):
        
        self.head = None
        self.tail = None

    def createNode(self):

        value = int(input("Enter the value: "))

        if(self.head == None):

            self.tail= Node(value)
            self.head = self.tail
            return 
        
        self.tail.next = Node(value)
        self.tail = self.tail.next

    def print_linked_list(self):

        print("The values in linked list are:")

        current = self.head

        while(current != None):

            print(current.value)

            current = current.next

obj = LinkedList()

value = int(input("Enter the number of elements to be entered: "))

for i in range(value):

    obj.createNode()

obj.print_linked_list()
