from textx import metamodel_from_file 
from graphviz import Digraph, Graph
import sys
import os
import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
cfg = metamodel_from_file('cfg.tx')
programFileName = sys.argv[1]
program =cfg.model_from_file(programFileName)
variableTable = {}
DSTypeTable = {}
tmpGraphSource = ""
imgCount = 0
codeLines =[]
class dsv:
    def interpret(program):
        for index,c in enumerate(program.functions):
            visualize(c)
            funcName = c.__class__.__name__
            match(funcName):
                case "VariableAssignment":
                    VariableAssignment(c)
                case "DataStructureDeclaration":
                    DSDeclaration(c)
                case "For":
                    ForLoop(c)
                case "While":
                    WhileLoop(c)
                case "Print":
                    print(variableTable[c.value]) if (c.text == "" ) else print(c.text)
                case "Expression":
                    ArithmeticHandler(c)
                case "If":
                    IfHandler(c)
                case "DataStructureManipulation":
                    DSManipulation(c)
                case "Visualize":
                    visualize(c)
                case _:
                    print("There is no method for", funcName)
def VariableAssignment(c):
    RHSFuncName = c.value.__class__.__name__
    match(RHSFuncName):
       case "Expression":
            variableTable[c.varName] = ArithmeticHandler(c.value)
       case "int":
           variableTable[c.varName] = c.value
       case _:
            variableTable[c.varName] = c.value
def ArithmeticHandler(c):
    operand1 = c.val1 if (c.val1.__class__.__name__!="str") else variableTable[c.val1]
    result= operand1;
    for i in range(len(c.val2)):
        operand2 = c.val2[i] if (c.val2[i].__class__.__name__!="str") else variableTable[c.val2[i]]
        match(c.op[i]):
            case '+':
                result+=operand2
            case '-':
                result-=operand2
            case '*':
                result*=operand2
            case '/':
                result/=operand2
            case '%':
                result%=operand2

        
    return result

def ComparisonHandler(c):
   for x in c.cond:
        conditionSwitch = True
        val1Type = x.val1.__class__.__name__
        val2Type = x.val2.__class__.__name__

        if(val1Type=="str"):
            val1= variableTable[x.val1]
        elif(val1Type=="Expression"):
            val1= ArithmeticHandler(x.val1)
        else:
            val1 = x.valComparisonHandler1
            
        if(val2Type=="str"):
            val2= variableTable[x.val2]
        elif(val2Type=="Expression"):
            val2= ArithmeticHandler(x.val2)
        else:
            val2 = x.val2
        
        match(x.op):
            case ">":
                if(not val1>val2):
                    conditionSwitch = False
                    return conditionSwitch

            case "<":
                if(not val1<val2):  
                    conditionSwitch = False
                    return conditionSwitch

            case ">=":
                if(not val1>=val2): 
                    conditionSwitch = False
                    return conditionSwitch

            case "<=":
                if(not val1<=val2):  
                    conditionSwitch = False
                    return conditionSwitch
            case "==":
                if(not val1==val2): 
                    conditionSwitch = False
                    return conditionSwitch


   return conditionSwitch

    
def IfHandler(c):
    if(ComparisonHandler(c.ifCond)):
        dsv.interpret(c.ifBody)
    else:
        for index,elifs in enumerate(c.elseCond):
            if(ComparisonHandler(elifs)):
                dsv.interpret(c.elseIfBody[index])
                return
        if("NoneType"!=c.elseBody.__class__.__name__):
            dsv.interpret(c.elseBody)
def ForLoop(c):#nested fors might be possible be creating a list of fors using * in the cfg
    VariableAssignment(c.initVar)
    while(ComparisonHandler(c.cond)):
        dsv.interpret(c.body)
        variableTable[c.initVar.varName]= variableTable[c.initVar.varName]+1 if (c.update=='++') else  variableTable[c.initVar.varName]-1

def WhileLoop(c):
    while(ComparisonHandler(c.cond)):
        dsv.interpret(c.body)





def DSDeclaration(c):
    match(c.dataType):
        case "array":
            variableTable[c.name] = c.value
            DSTypeTable[c.name] = "array"
        case "linked list":
            variableTable[c.name] = c.value
            DSTypeTable[c.name] = "linked"
        case "stack": # Direct Declaration goes in order of pushing from left to right, meaning the last element in the list will be on top 
            variableTable[c.name] = c.value
            DSTypeTable[c.name]= "stack"
        case "graph": # you start with root pair, all other nodes pair edges must be added through method calls
            variableTable[c.name] = c.value
            DSTypeTable[c.name]= "graph"
        case "tree": # start with only root node 
            variableTable[c.name] = c.value if(len(c.value)<=1) else print("Cannot declare tree with more than 1 root node")
            DSTypeTable[c.name]= "tree"

    

def DSManipulation(c):
    dataStructure = variableTable[c.varName] 
    val = c.val[0] if(c.val.__class__.__name__=="list" and c.val!=[]) else c.val
    match(c.func):
        case "append":
            dataStructure.append(c.val[0])if(c.val.__class__.__name__=="list") else dataStructure.append(c.val)
        case "prepend":
            dataStructure.insert(0,c.val[0])if(c.val.__class__.__name__=="list") else dataStructure.insert(0,c.val)
        case "remove": #deletes first instance of var
            for index, elem in enumerate(dataStructure):
                if(elem == val):
                    del dataStructure[index]
                    return;
            else:   print("No occurrences of",val ,"found")
        case "removeAt":
            if(c.val.__class__.__name__=="list"):
                del dataStructure[c.val[0]]
            else:
                del dataStructure[c.val]
        #Stack
        case "push":
            dataStructure.insert(len(dataStructure),val)
        case "pop":
            del dataStructure[len(dataStructure)-1]
        case "get":
            print(dataStructure[val])
        case "head":
            print(dataStructure[0])
        case "tail":
            print(dataStructure[len(dataStructure)-1])
        case "addPair": # create nodes and edges
            dataStructure.extend(c.val)
        

def visualize(c):
    vis = Digraph(graph_attr={'rankdir': 'TB'})
    vis.attr(label="Data Structure Visualization: "+programFileName, fontsize='36', fontcolor='black',rankdir='TB' )
    for dataKey in variableTable:
        dataSet = variableTable[dataKey]
        if(dataSet.__class__.__name__ == "list"):
            match(DSTypeTable[dataKey]):
                case "array":
                    with vis.subgraph(name="cluster_array") as array:
                        array.attr(label = "Array",rankdir='TB')
                        n = "cluster_" +str(dataKey)
                        with array.subgraph(name=n)as n:
                            n.attr(label = str(dataKey),fontsize='19',rankdir='LR')    
                            for index, element in enumerate(dataSet): 
                                n.node(str(index)+str(dataKey),str(element)+"\n"+ hex(id(element))+"\nindex: " +str(index),shape = 'rectangle')
                case "linked":
                   with vis.subgraph(name="cluster_linked") as linked:
                        linked.attr(label = "Linked List")
                        n = "cluster_" +str(dataKey)
                        with linked.subgraph(name=n)as n:
                            n.attr(label = str(dataKey),fontsize='19',rankdir='LR')    
                            for index, element in enumerate(dataSet): 
                                n.node(str(index)+str(dataKey),str(element)+"\n"+ hex(id(element)))
                                if(index < len(dataSet)-1):    n.edge(str(index)+str(dataKey),str(index+1)+str(dataKey),contraint='false',minlen='.1',maxlen='0.1') 
                case "stack":
                   with vis.subgraph(name="cluster_stack") as stack:
                        stack.attr(label = "Stack",rankdir='TB')
                        n = "cluster_" +str(dataKey)
                        with stack.subgraph(name=n)as n:
                            n.attr(label = str(dataKey),fontsize='19',rankdir='TB')    
                           
                            for index, element in enumerate(reversed(dataSet)): 
                                n.node(str(index)+str(dataKey),str(element)+"\n"+ hex(id(element)),shape = 'rectangle')
                                if(index < len(dataSet)-1):    n.edge(str(index)+str(dataKey),str(index+1)+str(dataKey),contraint='false',minlen='.1',maxlen='0.1',style='invis') 
                case "graph":
                   with vis.subgraph(name="cluster_graph") as graph:
                        graph.attr(label = "Graph")
                        n = "cluster_" +str(dataKey)
                        with graph.subgraph(name=n)as n:
                            n.attr(label = str(dataKey),fontsize='19',rankdir='LR')    
                            tmp = []
                            for index, element in enumerate(dataSet): 
                                tmp.append(element)
                                if(tmp.count(element)==1):
                                    n.node(str(element),str(element)+"\n"+ hex(id(element)),shape = 'ellipse')   
                            for index, element in enumerate(dataSet):
                                if(index%2==0):
                                    if(index < len(dataSet)-1):    n.edge(str(element),dataSet[index+1])
                case "tree":
                   with vis.subgraph(name="cluster_tree") as tree:
                        tree.attr(label = "Tree",rankdir='TB')
                        n = "cluster_" +str(dataKey)
                        with tree.subgraph(name=n)as n:
                            n.attr(label = str(dataKey),fontsize='19')    
                            tmp = []
                            for index, element in enumerate(dataSet): 
                                tmp.append(element)
                                if(tmp.count(element)==1):
                                    n.node(str(element),str(element)+"\n"+ hex(id(element)),shape = 'ellipse')   
                            for index, element in enumerate(dataSet):
                                if(index%2!=0):
                                    if(index < len(dataSet)-1):    n.edge(str(element),dataSet[index+1])

    


    #print(vis.source)
    global tmpGraphSource,imgCount
    if(tmpGraphSource != vis.source):
        codeLines.append(LineAtNthChar(programFileName,c._tx_position))
        tmpGraphSource = vis.source
        vis.render('frame'+str(imgCount),format='png',cleanup=True)
        imgCount+=1
    vis.render('finalImg',format='png',cleanup=True)

def LineAtNthChar(filename,n):
    with open(filename) as file:
        count = 0
        lineNum =1
        for line in file:
            count+=len(line)
            if(n<=count):
                return(line)
                break
            else:
                lineNum+=1

filename = 'file.txt'
class systemFunction:
    def createVid(imgCount):
        fps = .3
        video_size = (1920,1088)
        with imageio.get_writer('slideshow.mp4', fps=fps) as writer:
            for index,img in enumerate(range(imgCount)):
                image = Image.open("frame" + str(index)+".png")
                if(index!=0):
                    image = image.resize((int(video_size[0] * 0.8), int(video_size[1] * 0.5)))  
                else:
                    image = image.resize((int(video_size[0] * 0.8), int(video_size[1] * 0.2)))  
                
                white_screen = Image.new('RGB', video_size, (255, 255, 255))  
                position = ((video_size[0] - image.width) // 2, (video_size[1] - image.height) // 2)
                white_screen.paste(image, position)
                draw = ImageDraw.Draw(white_screen)
                text_position = (0,890)
                if(index!=0):
                    draw.text(text_position, codeLines[index], fill=(0,0,0),font_size=100)
                image_array = np.array(white_screen)
                writer.append_data(image_array)
        print("Video created successfully!")

    def cleanDir(imgCount):
        for index,img in enumerate(range(imgCount)):
            try:
                os.remove("frame"+str(index)+".png")
            except FileNotFoundError:
                print("file not found error")
            except PermissionError:
                print("error")

dsv.interpret(program)
systemFunction.createVid(imgCount)
systemFunction.cleanDir(imgCount)
