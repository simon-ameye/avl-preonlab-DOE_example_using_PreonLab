#The aim of this script is to launch ref_0bulk.prscene PreonLab E-motor model with several values of injection flow rates and rotation speeds
#For more information about this script, please contact simon.ameye@avl.com
#A description of all PreonLab Python functions is available at : http://fifty2.eu/PreonLab/preonpy-4.1/

import preonpy #Here, we import the Python interface of PreonLab. For more information, please refer to PreonLab manual.
import numpy as np #We will use numpy to create arrays

SimuList = [0, 1, 2, 3, 4, 5, 6, 7] #Will be useful to get index of each load case
OilFlowRate = np.array([0.5, 0.5, 3, 3, 1, 1, 1, 1]) #L/min The list of flow rates
ShaftVelocity = np.array([2000, 14000, 2000, 14000, 2000, 4000, 7000, 14000]) #RPM The list of rotation speeds
SimulationTime = np.array([0.6, 0.2, 0.6, 0.2, 0.6, 0.5, 0.3, 0.2]) #as higher rotation speed makes simulation faster to converge, we will set the simulation time for each case.
NbOfFramesPerSimu = 50 #The number of frames we want to save for each case

for SimuRef in SimuList: #We create a loop to iterate over SimuList
    print("Simulating "+str(ShaftVelocity[SimuRef])+" RPM, "+str(OilFlowRate[SimuRef])+" l/min, "+str(SimulationTime[SimuRef])+" s") #Text : current load case
    s=preonpy.Scene("C:/Data/PREONLAB/ref_0bulk.prscene") #Opens the reference case
    s.save("C:/Data/PREONLAB/Simulation/DOE/"+"FR"+str(OilFlowRate[SimuRef]).replace('.','')+"ShaftVel"+str(ShaftVelocity[SimuRef])+".prscene", as_portable=False) #Saves the case as a new file in a folder
    Rotation = s.find_object("ROTATION") #Here, a transform group named "ROTATION" is master for the transformation of all shaft parts. We will set its rotation speed to the desired one.
    Rotation["revolutions per second"] = ShaftVelocity[SimuRef]/60 #Sets the rotation speed in rotation per second according to ShaftVelocity list
    Source = s.find_object("AreaSource_1") #The injector source is named "AreaSource_1"
    Source["volume flow rate"] = OilFlowRate[SimuRef]/1000/60 #We set the flow rate in m3/s according to OilFlowRate list
    s.framerate = NbOfFramesPerSimu/SimulationTime[SimuRef] #We set the framerate so that NbOfFramesPerSimu frames are saved in SimulationTime duration
    s.view_framerate = NbOfFramesPerSimu/SimulationTime[SimuRef] #We set the view framerate equal to simulation framerate
    s.save() #save the current configuration
    s.simulate(0, str(SimulationTime[SimuRef])+"s") #Launches the simulation according to SimulationTime duration
    
    
    
    
    
    
    
    