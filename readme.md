# Data Structure Visualizer Language

DSVLang - Intuitive and uniform declaration structure for all data structures
Structure-Type Name = [values, go, here, for, ALL, data, structures]
Examples:
array myArray = [1,2,3,4]
linked list myLinkedList = [5,6,7,8]

DSVLang generates Two Visualizations After Code Generation.
Image - A PNG file is created, showing all of the data structures at the completion of the code
Video - An MP4 file is created, showing the progression of the creation, and manipulation of data, as well as the line of code in DSVLang that caused the change

## Example Image Output

![image](https://github.com/user-attachments/assets/b1a7cccb-c74a-4604-83e8-088952c7518b)


## Example Video Output

https://github.com/user-attachments/assets/92adb9be-f658-4be7-8120-3d555209b0aa

### Syntax

Variable Declaration -> variableName = value 

Data Structure Declaration -> Structure-Type Name = [values, in, here]
  - Quirks:
    - Stacks are declared in order that they would be pushed, from left to right. For example, stack myStack = [1,2,3,4,5] would create a stack as if you were to first push 1 to the stack, then push 2, then 3 etc, creating a stack with 5 on the top and 1 on the bottom.
    - Trees and graphs are manipulated using addPair(value 1,value2) which will both create the node(s) if they do not exist and also create an edge between the two.
   
**Data Structure Functions**

append(value)
prepend(value)
removeAt(index)
push(value)
pop()
remove(value) 
head()
tail()
get(index)
addPair(nodeOne, nodeTwo)

**Loops**

for(initialVariable = value ; condition ; update){
body statements
}

while(condition){
body
}

**Other**

print("text" or variable)

if(condition){
body
}else if (condition){
else if body
}else{
else body
}

**Visualize**
End your code in ***Visualize()*** to create a functioning visualization.

