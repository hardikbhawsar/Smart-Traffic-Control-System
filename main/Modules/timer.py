import math

#######################################
class Timer:
    reference_timers ={
        "HHH": "075075075",
        "HHM": "065065050",
        "HHL": "075075030",
        "HMH": "065050065",
        "HMM": "075045045",
        "HML": "090060030",
        "HLH": "075030075",
        "HLM": "090030060",
        "HLL": "120030030",
        "MHH": "050065065",
        "MHM": "045075045",
        "MHL": "060090030",
        "MMH": "045045075",
        "MMM": "060060060",
        "MML": "045045030",
        "MLH": "060030090",
        "MLM": "075030075",
        "MLL": "060030030",
        "LHH": "030075075",
        "LHM": "030090060",
        "LHL": "030120030",
        "LMH": "030060090",
        "LMM": "030075075",
        "LML": "030060030",
        "LLH": "030030120",
        "LLM": "030030060",
        "LLL": "030030030",
    }

    def __init__(self):
        self.L1=0
        self.L2=0
        self.L3=0

        # Initial Threshold
        self.T = float((self.L1 + self.L2 + self.L3) / 3)

        self.Classes = {
            "L1": "M",
            "L2": "M",
            "L3": "M"
        }

        self.Timers = {
            "L1": 60,
            "L2": 60,
            "L3": 60
        }
    
    def alter_classes(self):
        """
        Converts the l,m,h classes of the lanes according to threshold.
        """
        p1 = (math.isclose(self.L1, self.L2, abs_tol = 20))
        p2 = (math.isclose(self.L1, self.L3, abs_tol = 20))
        p3 = (math.isclose(self.L2, self.L3, abs_tol = 20))
        
        p11 = (math.isclose(self.L1, self.T, abs_tol = 20))
        p12 = (math.isclose(self.L1, self.T, abs_tol = 20))
        p13 = (math.isclose(self.L2, self.T, abs_tol = 20))
        
        if self.T < 35 and all( (p11, p12, p13) ):
            u1 = {"L1" : "L"}
            self.Classes.update(u1)
            u1 = {"L2" : "L"}
            self.Classes.update(u1)
            u1 = {"L3" : "L"}
            self.Classes.update(u1)
            print(" : SPECIAL CASE 1: ")

        elif all( (p1, p2, p3, ) ) and 45 < self.T < 60:
            u1={"L1" : "M"}
            self.Classes.update(u1)
            u1={"L2" : "M"}
            self.Classes.update(u1)
            u1={"L3" : "M"}
            self.Classes.update(u1)
            print(" : SPECIAL CASE 2: ")

        elif self.T > 70 and self.L1 > 65 and self.L2 > 65 and self.L3 > 65:
            u1 = {"L1" : "H"}
            self.Classes.update(u1)
            u1 = {"L2" : "H"}
            self.Classes.update(u1)
            u1 = {"L3" : "H"}
            self.Classes.update(u1)
            print(" : SPECIAL CASE 3: ")
        ###########
        elif self.T>60 and (self.L1>39 and self.L2>39 and self.L3>75) or (self.L1>39 and self.L2>39 and self.L3>75)or(self.L1>75 and self.L2>39 and self.L3>39):
            if 40 < self.L1 and self.L2<67 :
                u1={"L1" : "M"}
                self.Classes.update(u1)
                u1={"L2" : "M"}
                self.Classes.update(u1)
                u1={"L3" : "H"}
                self.Classes.update(u1)
                
            elif 40<self.L2 and self.L3 <67:
                u1={"L2" : "M"}
                self.Classes.update(u1)
                u1={"L3" : "M"}
                self.Classes.update(u1)
                u1={"L1" : "H"}
                self.Classes.update(u1)
            elif 40<self.L1 and self.L3<67:
                u1={"L3" : "M"}
                self.Classes.update(u1)
                u1={"L1" : "M"}
                self.Classes.update(u1)
                u1={"L2" : "H"}
                self.Classes.update(u1)
                
        elif 31<self.T<40 and (self.L1<35 and self.L2<35 and self.L3>45) or (self.L1<35 and self.L3<35 and self.L2>45)or(self.L1>45 and self.L2<35 and self.L3<35):
            if 0<self.L1 and self.L2<38 :
                u1={"L1" : "L","L2" : "L","L3" : "M"}
                self.Classes.update(u1)
                
            if 0<self.L1 and self.L3<38 :
                u1={"L1" : "L","L2" : "M","L3" : "L"}
                self.Classes.update(u1)

            if 0<self.L3<38 and 0<self.L2<38 :
                u1={"L1" : "M","L2" : "L","L3" : "L"}
                self.Classes.update(u1)
            
        # ################    

        else:
            if self.L1 > self.T :
            
                p = (math.isclose(self.L1, self.T, abs_tol = 10))
                if p == True:
                    u1 = {"L1" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L1" : "H"}
                    self.Classes.update(u1)
                    
            elif self.L1 < self.T:
                p = (math.isclose(self.L1, self.T, abs_tol = 10))
                if p == True:
                    u1 = {"L1" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L1" : "L"}
                    self.Classes.update(u1)
            else:
                u1 = {"L1" : "M"}
                self.Classes.update(u1)
                
            if self.L2 > self.T :
                p = (math.isclose(self.L2, self.T, abs_tol = 10))
                if p == True:
                    u1 = {"L2" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L2" : "H"}
                    self.Classes.update(u1)
            elif self.L2 < self.T:
                p = (math.isclose(self.L2, self.T ,abs_tol = 10))
                if p == True:
                    u1 = {"L2" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L2" : "L"}
                    self.Classes.update(u1)
            else:
                u1 = {"L2" : "M"}
                self.Classes.update(u1)
                
            if self.L3 > self.T :
                p = (math.isclose(self.L3, self.T, abs_tol = 10))
                if p == True:
                    u1 = {"L3" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L3" : "H"}
                    self.Classes.update(u1)
                    
            elif self.L3 < self.T:
            
                p = (math.isclose(self.L3, self.T, abs_tol = 10))
                if p == True:
                    u1 = {"L3" : "M"}
                    self.Classes.update(u1)
                else:
                    u1 = {"L3" : "L"}
                    self.Classes.update(u1)
            else:
                u1 = {"L3" : "M"}
                self.Classes.update(u1)

    def updated_timer(self):
        a = self.Classes.get("L1")
        b = self.Classes.get("L2")
        c = self.Classes.get("L3")
        d = a + b + c
        #print(d)
        
        f = self.reference_timers.get(d)
        #print(f)
        
        z = int(int(f)%1000)
        f = int(int(f)/1000)
        y = int(int(f)%1000)
        f = int(int(f)/1000)
        x = int(int(f)%1000)
        #print(x,y,z)
        
        self.Timers.update({"L1": x})
        self.Timers.update({"L2": y})
        self.Timers.update({"L3": z})
        print("Updated timers ", self.Timers)

    def analyze(self, counts:list):
        print("\n"+("═")*50+"\n")
        
        self.L1, self.L2, self.L3 = list(map(float, counts))

        self.T = float( (self.L1 + self.L2 + self.L3) / 3 )

        print("Threshold value",self.T)

        self.alter_classes()

        print("Updated Classes", self.Classes)
        
        self.updated_timer()
        
        print("\n"+("═")*50+"\n")

#######################################


# print("\n***Initial Condition***\n")

# L1=0
# L2=0
# L3=0

# T = float((L1+L2+L3)/3) #Calculating threshold
# print("Threshold value",T)


# Classes = {
#   "L1": "M",
#   "L2": "M",
#   "L3": "M"
# }

# Timers = {
#   "L1": 60,
#   "L2": 60,
#   "L3": 60
# }

# print("Default Timers",Timers)

# reference_timers = {
#         "HHH": "075075075",
#         "HHM": "065065050",
#         "HHL": "075075030",
#         "HMH": "065050065",
#         "HMM": "070055055",
#         "HML": "090060030",
#         "HLH": "075030075",
#         "HLM": "090030060",
#         "HLL": "120030030",
#         "MHH": "050065065",
#         "MHM": "055070055",
#         "MHL": "060090030",
#         "MMH": "055055070",
#         "MMM": "060060060",
#         "MML": "045045030",
#         "MLH": "060030090",
#         "MLM": "075030075",
#         "MLL": "090045045",
#         "LHH": "030075075",
#         "LHM": "030090060",
#         "LHL": "030120030",
#         "LMH": "030060090",
#         "LMM": "030075075",
#         "LML": "030060090",
#         "LLH": "030030120",
#         "LLM": "045045090",
#         "LLL": "030030030",
# }

# print("Default Classes",Classes)

# def alter_classes():

#     p1= (math.isclose(L1,L2,abs_tol = 10))
#     p2= (math.isclose(L1,L3,abs_tol = 10))
#     p3= (math.isclose(L2,L3,abs_tol = 10))
    
#     p11=(math.isclose(L1,T,abs_tol = 10))
#     p12=(math.isclose(L1,T,abs_tol = 10))
#     p13=(math.isclose(L2,T,abs_tol = 10))
    

#     if T<17.5 and p11==p12==p13==True:
#         u1={"L1" : "L"}
#         Classes.update(u1)
#         u1={"L2" : "L"}
#         Classes.update(u1)
#         u1={"L3" : "L"}
#         Classes.update(u1)
#         print(" : SPECIAL CASE 1: ")

#     elif p1==p2==p3==True:
#         u1={"L1" : "M"}
#         Classes.update(u1)
#         u1={"L2" : "M"}
#         Classes.update(u1)
#         u1={"L3" : "M"}
#         Classes.update(u1)
#         print(" : SPECIAL CASE 2: ")
        
#     else :
        
#         if L1>T :
        
#             p=(math.isclose(L1,T,abs_tol = 5))
#             if p==True:
#                 u1={"L1" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L1" : "H"}
#                 Classes.update(u1)
                
#         elif L1<T:
        
#             p=(math.isclose(L1,T,abs_tol = 5))
#             if p==True:
#                 u1={"L1" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L1" : "L"}
#                 Classes.update(u1)
#         else:
        
#             u1={"L1" : "M"}
#             Classes.update(u1)
            
#         if L2>T :
        
#             p=(math.isclose(L2,T,abs_tol = 5))
#             if p==True:
#                 u1={"L2" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L2" : "H"}
#                 Classes.update(u1)
#         elif L2<T:
        
#             p=(math.isclose(L2,T,abs_tol = 5))
#             if p==True:
#                 u1={"L2" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L2" : "L"}
#                 Classes.update(u1)
#         else:
        
#             u1={"L2" : "M"}
#             Classes.update(u1)
            
#         if L3>T :
        
#             p=(math.isclose(L3,T,abs_tol = 5))
#             if p==True:
#                 u1={"L3" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L3" : "H"}
#                 Classes.update(u1)
                
#         elif L3<T:
        
#             p=(math.isclose(L3,T,abs_tol = 5))
#             if p==True:
#                 u1={"L3" : "M"}
#                 Classes.update(u1)
#             else:
#                 u1={"L3" : "L"}
#                 Classes.update(u1)
#         else:
        
#             u1={"L3" : "M"}
#             Classes.update(u1)
            

# def updated_timer():

#     a=Classes.get("L1")
#     b=Classes.get("L2")
#     c=Classes.get("L3")
#     d=a+b+c
#     #print(d)
    
#     f=reference_timers.get(d)
#     #print(f)
    
#     z=int(int(f)%1000)
#     f=int(int(f)/1000)
#     y=int(int(f)%1000)
#     f=int(int(f)/1000)
#     x=int(int(f)%1000)
#     #print(x,y,z)
    
#     Timers.update({"L1": x})
#     Timers.update({"L2": y})
#     Timers.update({"L3": z})
#     print("Updated timers ",Timers)

# #updated_timer()
# print("\n"+("*")*50+"\n")


# class Round_Robin(): # (ABC)(BCD)(CDA)(DAB)(ABC)
 
    
#     def __init__(self, size): 
#         self.size = size
        
#         self.queue = [None for i in range(size)]
#         self.front = self.rear = -1
 
#     def enqueue(self, data):
         
#             self.rear = (self.rear + 1) % self.size
#             self.queue[self.rear] = data
             
    
 
# ob=Round_Robin(4)
# ob.enqueue("A")
# ob.enqueue("B")
# ob.enqueue("C")
# ob.enqueue("D")
# #ob.display()

# if __name__ == "__main__":
#     m=0
#     for i in range(0,15):
#         s1=(ob.queue[((m+0)%4)])
#         s2=(ob.queue[((m+1)%4)])
#         s3=(ob.queue[((m+2)%4)])
#         #s3=(self.queue[((m+2)%4)])
                
#         L1 = float(input ("Enter Lane " + s1 + " Density :"))
#         L2 = float(input ("Enter Lane " + s2 + " Density :"))
#         L3 = float(input ("Enter Lane " + s3 + " Density :"))
#         T = float((L1+L2+L3)/3)
#         print("Threshold value",T)
#         alter_classes()
#         print("Updated Classes",Classes)
#         updated_timer()
#         print("\n"+("*")*50+"\n")
#         m=m+1
