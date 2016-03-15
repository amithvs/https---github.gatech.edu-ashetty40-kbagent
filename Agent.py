# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image

# Install Numpy and uncomment this line to access matrix operations.
import numpy as np
import copy
import math, operator
from PIL import Image
import time

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass


    ################HELPER FUNCTIONS #################
    
    def check_reflection(self, orangle , newangle):
        # find angle difference

        if orangle == 45 and newangle == 135:
            return True
        elif  orangle == 315 and newangle == 225:
            return True
        diff = abs(newangle - orangle)


        x = self.findRefAngle(diff)
        if diff == x:
            return True
        else:
            return False
        
        return False
    def findRefAngle(self, angle):
        if angle >=0 and angle <= 180:
            return 180 - angle
        else:
            return 540 - angle


    def remove_dict_blanks(self , dictXtemp):
        ll = []
        for key in dictXtemp:
            if dictXtemp[key] == '' or str(dictXtemp[key]) == '0':
                ll.append(key)

        for s in ll:
            del dictXtemp[s]




    def chkAlignment(self, firstval , secondval):
        lfsymm = False
        lsSymm = False

        if firstval == secondval:
            lfsymm = lsSymm = True
        elif firstval == 0 or secondval == 0:
            lfsymm = lsSymm = False
        else:
            lf = firstval.split(':')
            ls = secondval.split(':')
            b = False

            lfsub1 = lf[0].split('-')
            lfsub2 = lf[1].split('-')
            lssub1 = ls[0].split('-')
            lssub2 = ls[1].split('-')


            if lfsub1[0] == lfsub2[0]: #means both r bottom or top
                if lfsub1[1] != lfsub2[1]: #means its symmetrical
                    lfsymm = True


            if lssub1[0] == lssub2[0]: #means both r bottom or top
                if lssub1[1] != lssub2[1]: #means its symmetrical
                    lsSymm = True
        return lfsymm and lsSymm #firstval == secondval
    ###################################################

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a list representing its
    # confidence on each of the answers to the question: for example 
    # [.1,.1,.1,.1,.5,.1] for 6 answer problems or [.3,.2,.1,.1,0,0,.2,.1] for 8 answer problems.
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as a python list* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def find_image_error(self , h1 , h1a , hC , problem):
        #h1 = Image.open("D:/gatech/7367 KBAI/Code/Problems/Basic Problems B/Basic Problem B-01/A.png") #.histogram()
        gray = h1.convert('L')
        bw = np.asarray(gray).copy()
        bw[bw < 44] = 0    # Black
        bw[bw >= 44] = 1 # White
        
        graya = h1a.convert('L')
        bwa = np.asarray(graya).copy()
        bwa[bwa < 44] = 0    # Black
        bwa[bwa >= 44] = 1 # White
        

        grayc = hC.convert('L')
        bwc = np.asarray(grayc).copy()
        bwc[bwc < 44] = 0    # Black
        bwc[bwc >= 44] = 1 # White


        bw = bw[::2, ::2]
        bwa = bwa[::2, ::2]
        bwc = bwc[::2, ::2]
        


        # check for mirror image 

        trans = ''
        transmatrix = {'rot90':0,'ref':0,'xor':0 , 'rot270':0 ,  'rot180':0 , 'refv' : 0 }
        transpixel = {'rot90':0,'ref':0,'xor':0 , 'rot270':0 , 'rot180':0  , 'refv' : 0 }


        #lets turn right 90 degrees
        x = np.rot90(bw, 3)
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        transmatrix['rot90'] = err
        transpixel['rot90'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

        x = np.rot90(bw, 2)
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        transmatrix['rot180'] = err
        transpixel['rot180'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

        x = np.rot90(bw )
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        transmatrix['rot270'] = err
        transpixel['rot270'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

         
        x = np.fliplr(bw)
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        transmatrix['ref'] = err
        transpixel['ref'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

        x = np.flipud(bw)
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        transmatrix['refv'] = err
        transpixel['refv'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

         
        #x =  vfunc(bw, bwa) #
        x = np.where(bw == bwa,bw,1)
        #now check if x == bwa
        err = np.sum((x.astype("float") - bwa.astype("float")) ** 2)
        err /= float(x.shape[0] * x.shape[1])
        #self.save_image(x , "xor")
        transmatrix['xor'] = err
        transpixel['xor'] = np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)
        #print "error" , err , "diff" ,  np.size(bwa) -  np.count_nonzero(bwa) -  np.size(x)  +  np.count_nonzero(x)

        #get minimum from matrix

        trans = min(transmatrix, key=transmatrix.get)
        #trans = 'ref'

        if (transmatrix['ref'] == 0 or transmatrix['refv'] == 0):
            if transmatrix['ref'] == 0:
                trans = 'ref'
            else:
                trans = 'refv'
        else:
            ft = transmatrix[trans]
            #newA = dict(sorted(transmatrix.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
            #print "error" , ft
            if (trans == 'xor' and ft > 0.01) or ( trans != 'xor' and  ft > 0.04):
                trans = ''

            r = sorted(transmatrix.items(), key=lambda x:x[1])

            if abs(r[0][1] - r[1][1]) < 0.001:
                #too close
                #xd = sorted(transpixel.items(), key=lambda x:x[1])
                t1 =   r[0][0]
                t2 =   r[1][0]
                #get their diff vals
                q1 = transpixel[t1]
                q2 = transpixel[t2]
                if q1 < q2:
                    trans = t1
                else:
                    trans = t2

            if ft > 0.04:
                trans = ''

        if sum(transmatrix.values()) == 0:
            trans = 'none'

        q = np.zeros(6)

        if trans != '':
            for i in range (1 , 7):
                hx = Image.open(problem.figures[str(i)].visualFilename)

                grayx = hx.convert('L')
                bwx = np.asarray(grayx).copy()
                bwx[bwx < 44] = 0    # Black
                bwx[bwx >= 44] = 1 # White
                bwx = bwx[::2, ::2]
                #self.save_image(bwc ,"bwxx")
                x = []
                if trans == 'xor':
                    #x =  vfunc(bwc, bwx) #
                    x = np.where(bwc == bwx,bwc,1)
                elif trans == 'ref':
                    x = np.fliplr(bwc)
                elif trans == 'rot90':
                    x = np.rot90(bwc, 3)
                elif trans == 'rot180':
                    x = np.rot90(bwc, 2)
                elif trans == 'rot270':
                    x = np.rot90(bwc)
                elif trans == 'refv':
                    x = np.flipud(bwc)
                elif trans == 'none':
                    x = (bwc)

                #self.save_image(x , str(i) + "ff")

                #now check if x == bwa
                err = np.sum((x.astype("float") - bwx.astype("float")) ** 2)
                err /= float(x.shape[0] * x.shape[1])

                #print "i=" , i , "err" , err , "sum=" ,  np.size(bwx) -  np.count_nonzero(bwx) -  np.size(x) +  np.count_nonzero(x)

                #x[x == 1] = 255
                #x[x == 0] = 0
                q[i - 1] = err




 

        return q # np.argmin(q) # err

    def save_image(self, x , str):
        z = np.copy(x)
        z[z == 1] = 255
        z[z == 0] = 0
        imfile = Image.fromarray(z)
        imfile.save(str + "1result_bw.png")
        pass

 


    def process_image(self, problem):

        #start_time = time.time()
        im1 = problem.figures["A"].visualFilename

        hA = Image.open(problem.figures["A"].visualFilename) 
        hB = Image.open(problem.figures["B"].visualFilename) 




        hC = Image.open(problem.figures["C"].visualFilename) 

        q = self.find_image_error(hA, hB , hC , problem)
        mino = np.sum(q)

        if mino == 0:
            q = self.find_image_error(hA, hC , hB , problem)

        idx =   np.argmin(q)
        mino = np.sum(q)
        ft = []
        for l in range (0,6):
            if mino == 0:
                val = 1/ 6.0
            elif l == idx:
                val = 1
            else:
                val = 0
            ft.append(val) # ( 1 if l == idx else 1/0.6 if idx == 0 else 0  )



        return ft # [0,0,0,0,0,0]


        #bw = np.flipud(bw)

        #imfile = Image.fromarray(bw)

        


        #imfile.save("result_bw.png")
        i=1

        #h1 = h1.convert('1') 
        #pix = np.array(h1)
        #i=1
        #pix[::] = 0
        #im = Image.fromarray(np.uint8(pix))
        #im.save('out.png')
        #rms = math.sqrt(reduce(operator.add,
        #map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

    def compare_dicts(self, objA, objB):
        dic = {'shape':'','fill':'','size':'','angle':'', 'reflection':0, 'alignment':0 , 'inside' :'' , 'above' : '' , 'overlaps' : '', 'left-of' : '' , 'vertical-flip':0}
        obj1inA = objA #figA.objects.values()[0]
        #obj1inAshape = obj1inA.attributes["shape"]
        obj1inB = objB # figB.objects.values()[0]
        
        obj1inBshape = obj1inB.attributes["shape"]
        obj1inAshape = obj1inA.attributes["shape"]

        #see how attribs transformed
        orangle = 0
        for attributeName in obj1inA.attributes:
            if attributeName == "angle":
                if ( obj1inA.attributes[attributeName] != ""):
                    orangle = int( obj1inA.attributes[attributeName])
                    dic[attributeName] = 0
            else:
                dic[attributeName] = obj1inA.attributes[attributeName]
        
        for attributeName in obj1inB.attributes:
            if attributeName == "angle":
                if obj1inB.attributes[attributeName] != "":
                    if obj1inBshape == "circle":
                        xxx = 0
                    else:
                        newangle = int(obj1inB.attributes[attributeName])
                        ##xxx =str( 360 - abs(( int(orangle) - int(obj1inB.attributes[attributeName]) )))
                        if (int(obj1inB.attributes[attributeName]) - int(orangle) < 0 ):
                            xxx = 360 - (  int(orangle) - newangle )
                        else:
                            xxx = newangle - int(orangle)
        
                        myang = abs(newangle - orangle)
                        xxx = myang 
                        refangle = self.findRefAngle(orangle)

                        ref = self.check_reflection(orangle , newangle)

                        ##if refangle == newangle: #we have a rotation here
                        if ref == True :
                            dic['reflection'] = 1
                else:
                    xxx = "0"
            else:
                xxx= obj1inB.attributes[attributeName]
            if  (xxx) == dic[attributeName]:
                dic[attributeName] = 0
            else:
                dic[attributeName] =  str(dic[attributeName]) +':' +  str(xxx)


        #if any shape is circle or octagon, we can remove it
        if obj1inAshape == "circle" or  obj1inAshape == "octagon" or  obj1inBshape == "circle" or  obj1inBshape == "octagon" :
            del dic["angle"]
        return dic
    def check_if_match(self,obj1inXR ,  count, dic, dic2, dicMatches, dicOutside, obj1inC, orangle ):
        #obj1inX = setXOutside[count] #first object in the block
        dictX = copy.deepcopy(dic2)
        match = 0 

        if len(obj1inXR) == len(dicOutside) == 0:
            return    1
        elif len(obj1inXR) == 0 or  len(dicOutside) == 0 :
            return 0
        obj1inX = obj1inXR[count]



        shape = dictX['shape'] 

        for attributeName in obj1inX.attributes:
            if attributeName == "angle":
                if obj1inX.attributes[attributeName] != "":
                    newangle = int(obj1inX.attributes[attributeName])
                    if (newangle - int(orangle) < 0 ):
                        xxx = 360 - ( int(orangle) - newangle  )
                    else:
                        xxx = newangle - int(orangle)
        
                    refangle = self.findRefAngle(orangle)
                    if 1 == 0 : #refangle == newangle: #we have a rotation here
                        dictX['reflection'] = 1

                else:
                    xxx = "0"
            else:
                xxx= obj1inX.attributes[attributeName]
        
            if str(xxx) == str( dic2[attributeName]): #str(obj1inC.attributes[attributeName]):
                dictX[attributeName] = 0
            else:
                dictX[attributeName] = str( dictX[attributeName]) +':' +  str(xxx)





        dicOutsidetemp = copy.deepcopy(dicOutside)
        dictXtemp = copy.deepcopy(dictX)


        #if shape = circle, angle not needed
        if    shape  == "circle":
            if "angle" in dicOutsidetemp:
                del dicOutsidetemp['angle']
            if "angle" in dictXtemp:
                del dictXtemp['angle']

        #given all else same, if reflection matches, this is the answer
        
        xx = 0
        yy = 0
        if dicOutsidetemp['reflection'] == 1 and dictXtemp['reflection'] == 1:
            dicangle = dic['angle']
            dicXangle = dictX['angle']
            del dicOutsidetemp['angle']
            del dictXtemp['angle']
            xx = 1
        else:
            dicref = dicOutside['reflection']
            dicXref = dictXtemp['reflection']
            del dicOutsidetemp['reflection']
            del dictXtemp['reflection']
            yy = 1
        



        #check if alignments are equal
        alSymm =  self.chkAlignment(dicOutsidetemp['alignment'] , dictXtemp['alignment'])
        

        


        #if symm, we dont care of alignment
        if alSymm:
            dicalg = dicOutside['alignment']
            dicXalg = dictX['alignment']
            del dicOutsidetemp['alignment']
            del dictXtemp['alignment']
        
        #also ignore insides
        if "inside" in dic and "inside" in dictX:
            dicinside = dic['inside']
            dicXinside = dictX['inside']
            del dicOutsidetemp['inside']
            del dictXtemp['inside']
            poo = 1

        if "above" in dic and "above" in dictX:
            dicinside = dic['above']
            dicXinside = dictX['above']
            del dicOutsidetemp['above']
            del dictXtemp['above']
            goo = 1

        if "overlaps" in dic and "overlaps" in dictX:
            dicinside = dic['overlaps']
            dicXinside = dictX['overlaps']
            del dicOutsidetemp['overlaps']
            del dictXtemp['overlaps']
            olap = 1

        if "left-of" in dic and "left-of" in dictX:
            dicinside = dic['left-of']
            dicXinside = dictX['left-of']
            del dicOutsidetemp['left-of']
            del dictXtemp['left-of']
            leftof = 1
        
        self.remove_dict_blanks(dicOutsidetemp)
        self.remove_dict_blanks(dictXtemp)

        if cmp(dicOutsidetemp, dictXtemp) == 0:
            match = 1
            #if xx == 1:
            #    finale.append(2)
            #else:
            #    finale.append(1)
        
        #else:
        #    finale.append(0)
        
        #if xx == 1:
        #    dicOutside['angle'] = dicangle
        #    dictX['angle'] = dicXangle
        
        #if yy == 1:
        #    dicOutside['reflection'] = dicref
        #    dictX['reflection'] = dicXref
        
        #if poo == 1:
        #    dicOutside['inside'] = dicinside
        #    dictX['inside'] = dicXinside

        #if goo == 1:
        #    dicOutside['above'] = dicinside
        #    dictX['above'] = dicXinside

        #if olap == 1:
        #    dicOutside['overlaps'] = dicinside
        #    dictX['overlaps'] = dicXinside

        #if leftof == 1:
        #    dicOutside['left-of'] = dicinside
        #    dictX['left-of'] = dicXinside

        #if alSymm:
        #    dicOutside['alignment'] = dicalg
        #    dictX['alignment'] = dicXalg
        return    match

    def text_compare(self, finale, problem , thisFigureA , thisFigureB , thisFigureC):
        if problem.problemType == "2x2":
            dic = {'shape':'','fill':'','size':'','angle':'', 'reflection':0, 'alignment':0 , 'inside' :'' , 'above' : '' , 'overlaps' : '' , 'left-of' : '' , 'vertical-flip':0}
            dic2 ={'shape':'','fill':'','size':'','angle':'', 'reflection':0, 'alignment':0 , 'inside' :'' , 'above' : '' , 'overlaps' : '' , 'left-of' : '' , 'vertical-flip':0}
            #get first figure: A
            #thisFigureA = problem.figures["A"]
        
            if len(thisFigureA.objects) > 1:
                #thisFigureB = problem.figures["B"]
                #thisFigureC = problem.figures["C"]
        
                setAInside , setAOutside = self.sortObjects(thisFigureA)
                setBInside , setBOutside = self.sortObjects(thisFigureB)
        
        
                #now see transformation matrix between outside and inside
                count = 0
        
        
                dicOutside = self.compare_dicts(setAOutside[count] , setBOutside[count])
                dicInside = {}
        
                if len(setAInside) > 0 and len(setBInside) > 0:
                    dicInside = self.compare_dicts(setAInside[count] , setBInside[count])
        
                setCInside , setCOutside = self.sortObjects(thisFigureC)
        
                dicMatches = {}
        
                #are the outsides same?
                orangle = 0
                obj1inC = setCOutside[count]
                for attributeName in obj1inC.attributes:
                    if attributeName == "angle":
                        if ( obj1inC.attributes[attributeName] != ""):
                            orangle = int( obj1inC.attributes[attributeName])
                            dic2[attributeName] = 0
                    else:
                        dic2[attributeName] = obj1inC.attributes[attributeName]
        
                lil = []
                for x in range(1, 7):
                    thisFigureX = problem.figures[str(x)]
                    setXInside , setXOutside = self.sortObjects(thisFigureX)
                    count = 0
                    
                    #find if similar object is there
                    if 1 == 1: # len(thisFigureX.objects) == 1:
                        match = self.check_if_match(setXOutside  , count, dic, dic2, dicMatches, dicOutside, obj1inC, orangle )
                        if match > 0 :
                            lil.append(x)
                lol = []
        
                #change sort order of setCInside based on insides value
        
                #     for objectName in thisFigure.objects:
                #         thisObject = thisFigure.objects[objectName]
                #         print("      ", "Object:" , objectName)
                #         for attributeName in thisObject.attributes:
                #             attributeValue = thisObject.attributes[attributeName]
                j = 20
        
                temp = None

                for xx in setCInside :
                    if "inside" in setCInside[xx].attributes:
                        if len(setCInside[xx].attributes["inside"]) < j:
                            j = len(setCInside[xx].attributes["inside"])
                            temp = setCInside[xx]
                    elif "above" in setCInside[xx].attributes:
                        if len(setCInside[xx].attributes["above"]) < j:
                            j = len(setCInside[xx].attributes["above"])
                            temp = setCInside[xx]
                    elif "overlaps" in setCInside[xx].attributes:
                        if len(setCInside[xx].attributes["overlaps"]) < j:
                            j = len(setCInside[xx].attributes["overlaps"])
                            temp = setCInside[xx]
                    elif "left-of" in setCInside[xx].attributes:
                        if len(setCInside[xx].attributes["left-of"]) < j:
                            j = len(setCInside[xx].attributes["left-of"])
                            temp = setCInside[xx]
        
                #we have smallest inside temp
                            
        
        
                orangle = 0


                if temp != None:
                    obj1inC = temp # setCInside[count]
                for attributeName in obj1inC.attributes:
                    if attributeName == "angle":
                        if ( obj1inC.attributes[attributeName] != ""):
                            orangle = int( obj1inC.attributes[attributeName])
                            dic2[attributeName] = 0
                    else:
                        dic2[attributeName] = obj1inC.attributes[attributeName]
        
                #now we loop through the list lil
                for ooo in lil:
                    thisFigureX = problem.figures[str(ooo)]
                    setXInside , setXOutside = self.sortObjects(thisFigureX)
                    count = 0
                    
                    #put another sort here
        
                    j = 20
                    temp = {}
                    for xx in setXInside :
                        if "inside" in setXInside[xx].attributes:
                            if len(setXInside[xx].attributes["inside"]) < j:
                                j = len(setXInside[xx].attributes["inside"])
                                temp = setXInside[xx]
                        elif "above" in setXInside[xx].attributes:
                            if len(setXInside[xx].attributes["above"]) < j:
                                j = len(setXInside[xx].attributes["above"])
                                temp = setXInside[xx]
                        elif "overlaps" in setXInside[xx].attributes:
                            if len(setXInside[xx].attributes["overlaps"]) < j:
                                j = len(setXInside[xx].attributes["overlaps"])
                                temp = setXInside[xx]    
                        elif "left-of" in setXInside[xx].attributes:
                            if len(setXInside[xx].attributes["left-of"]) < j:
                                j = len(setXInside[xx].attributes["left-of"])
                                temp = setXInside[xx] 
                                                                    
                    bbb= []
                    if j != 20:
                        bbb.append(temp)
                    #find if similar object is there
                    if 1 == 1: # len(thisFigureX.objects) == 1:
                        match = self.check_if_match(bbb  , count, dic, dic2, dicMatches, dicInside, obj1inC, orangle )
                        if match > 0 :
                            lol.append(ooo)
        
                found = 0
                for x in range(1, 7):
                    for p in lol:
                        if x == p:
                            found = 1
                    if found == 1:
                        finale.append(1)
                        found = 0
                    else:
                        finale.append(0)
                #print "ddd"
        
        
                #i now have 
        
            if len(thisFigureA.objects) == 1:
        
                obj1inA = thisFigureA.objects.values()[0]
                obj1inAshape = obj1inA.attributes["shape"]
                #thisFigureB = problem.figures["B"]
                obj1inB = thisFigureB.objects.values()[0]
        
                dic = self.compare_dicts(obj1inA , obj1inB)
        
                #now take shape C ...create a transformation and check
                #thisFigureC = problem.figures["C"]
                obj1inC = thisFigureC.objects.values()[0]
                obj1inCshape = obj1inC.attributes["shape"]
                orangle = 0
                for attributeName in obj1inC.attributes:
                    if attributeName == "angle":
                        if ( obj1inC.attributes[attributeName] != ""):
                            orangle = int( obj1inC.attributes[attributeName])
                            dic2[attributeName] = 0
 
                    else:
                        dic2[attributeName] = obj1inC.attributes[attributeName]
        
                #loop through all the solution pics and generate dict2 and compare to dict2
                for x in range(1, 7):
                    thisFigureX = problem.figures[str(x)]
                    #find if similar object is there
                    if len(thisFigureX.objects) == 1:
                        obj1inX = thisFigureX.objects.values()[0] #first object in the block
                        dictX = copy.deepcopy(dic2)
                        obj1inXshape = obj1inC.attributes["shape"]
                        for attributeName in obj1inX.attributes:
                            if attributeName == "angle":
                                if obj1inX.attributes[attributeName] != "":
                                    newangle = int(obj1inX.attributes[attributeName])
                                    ##xxx =str( 360 - abs(( int(orangle) - int(obj1inB.attributes[attributeName]) )))
                                    if (newangle - int(orangle) < 0 ):
                                        xxx = 360 - ( int(orangle) - newangle  )
                                    else:
                                        xxx = newangle - int(orangle)
        
                                    refangle = self.findRefAngle(orangle)

                                    ref = self.check_reflection(orangle , newangle)

                                    #if refangle == newangle: #we have a rotation here
                                    if ref == True:
                                        dictX['reflection'] = 1
        
                                else:
                                    xxx = "0"
                            else:
                                xxx= obj1inX.attributes[attributeName]
        
                            if attributeName not in obj1inC.attributes or   str(xxx) == obj1inC.attributes[attributeName]:
                                dictX[attributeName] = 0
                            else:
                                dictX[attributeName] = str( dictX[attributeName]) +':' +  str(xxx)
                        #given all else same, if reflection matches, this is the answer
        
                        xx = 0
                        yy = 0


                        dictemp = copy.deepcopy(dic)
                        dictXtemp = copy.deepcopy(dictX)



                        if dictemp['reflection'] == 1 and dictXtemp['reflection'] == 1:
                            #dicangle = dic['angle']
                            #dicXangle = dictX['angle']
                            del dictemp['angle']
                            del dictXtemp['angle']
                            xx = 1
                        else:
                            #dicref = dic['reflection']
                            #dicXref = dictX['reflection']
                            del dictemp['reflection']
                            del dictXtemp['reflection']
                            yy = 1
        
                        #check if alignments are equal
                        alSymm =  self.chkAlignment(dictemp['alignment'] , dictXtemp['alignment'])
        
                        #if symm, we dont care of alignment
                        if alSymm:
                            #dicalg = dic['alignment']
                            #dicXalg = dictX['alignment']
                            del dictemp['alignment']
                            del dictXtemp['alignment']
        



                        if obj1inCshape == "circle" or  obj1inCshape == "octagon" or  obj1inXshape == "circle" or  obj1inXshape == "octagon" :
                            if "angle" in dictemp:
                                del dictemp["angle"]
                            if "reflection" in dictemp:
                                del dictemp["reflection"]
                            if "angle" in dictXtemp:
                                del dictXtemp["angle"]
                            if "reflection" in dictXtemp:
                                del dictXtemp["reflection"]

                        #remove blanks
                        self.remove_dict_blanks(dictemp)
                        self.remove_dict_blanks(dictXtemp)


                        if cmp(dictemp, dictXtemp) == 0:
                            if xx == 1:
                                finale.append(5)
                            else:
                                finale.append(1)
        
                        else:
                            finale.append(0)
                        
                        #if xx == 1:
                        #    dic['angle'] = dicangle
                        #    dictX['angle'] = dicXangle
        
                        #if yy == 1:
                        #    dic['reflection'] = dicref
                        #    dictX['reflection'] = dicXref
        
                        #if alSymm:
                        #    dic['alignment'] = dicalg
                        #    dictX['alignment'] = dicXalg
                    else:
                        #ignore this
                        finale.append(0)
                        continue
        
                    #print ("aaa" , x )
                ###end if (obj1inAshape == obj1inBshape):
        
        
        
        elif problem.problemType == "3x3":
            print "not ready yet"
        else:
            print "not ready yet"
        return  

    def process_textual(self, finale, problem):

        thisFigureA = problem.figures["A"]
        thisFigureB = problem.figures["B"]
        thisFigureC = problem.figures["C"]

        self.text_compare(finale, problem , thisFigureA , thisFigureB , thisFigureC)
        return  

    def Solve(self,problem):
    
        print ("Working on Problem - " +  problem.name)

        try:
            finale = []
            self.process_textual(finale, problem)
            tot = sum(finale)  

            if tot == 0 :
                #lets try to solve this visually
                    ww= self.process_image(problem)
            else:
                ww = map(lambda x: x/float(sum(finale)), finale)

            max_value = max(ww)
            max_index = ww.index(max_value)
            #print ww , problem.correctAnswer , max_index + 1
            return ww 
        except:
            ##as a backup in case things break
            ll = [1 / 6.0] * 6
            return ll

        


    def sortObjects(self, thisFigureA):
        setA = copy.deepcopy(thisFigureA.objects) #
        setX = []

        setInsde = {}
        setOutside = {}
        iInside = 0
        iOutside = 0
        for objectName in setA:
            thisObject = thisFigureA.objects[objectName]
            inside = 0
            #print len(thisObject.attributes)
            for attributeName in thisObject.attributes:
                if attributeName == "inside" or attributeName == "above" or attributeName == "overlaps"  or attributeName == "left-of" :
                    inside = 1
                    break
                attributeValue = thisObject.attributes[attributeName]
                #print("               ", "Attribs:", attributeName, "-", attributeValue)

            if inside == 0:
                setX.append(thisObject)
                setOutside[iOutside]= thisObject
                iOutside = iOutside  + 1 
            else:
                setInsde[iInside]= thisObject
                iInside = iInside  + 1 
            
                # setA.remove(thisObject)
        for o in setX:
            del setA[o.name]

        for objectName in setA:
            setX.append(thisObject)

        return setInsde , setOutside



