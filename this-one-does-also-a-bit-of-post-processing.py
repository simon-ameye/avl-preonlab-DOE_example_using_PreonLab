#The aim of this script is to launch ref_0bulk.prscene PreonLab E-motor model with several values of injection flow rates and rotation speeds
#For more information about this script, please contact simon.ameye@avl.com
#A description af all PreonLab Python functions is available at : http://fifty2.eu/PreonLab/preonpy-4.1/

import preonpy #Here, we import the Python interface of preonlab. For more information, please refer to PreonLab manual.
import numpy as np #We will use numpy to create arrays

SimuList = [0, 1, 2, 3, 4, 5, 6] #Will be useful to get index of each load case
OilFlowRate = np.array([120,120,120,66,66,120,66]) #L/min The list of flow rates
ShaftVelocity = np.array([2530,2530,1500,2530,520,520,1500]) #RPM The list of rotation speeds
NbOfRotations = 10
NbOfFramesPerSimu = 200 #The number of frames we want to save for each case
NbOfSources = 75
OilDensity = np.array([930,902,930,930,930,930,930]) #kg/m3
OilViscosity = np.array([0.00699,0.00321,0.00699,0.00699,0.00699,0.00699,0.00699]) #Pa.s
OilSurfaceTension = np.array([0.0293,0.0275,0.0293,0.0293,0.0293,0.0293,0.0293]) #N/m
OilTemperature = np.array([80,120,80,80,80,80,80]) #°C
Spacing = 0.0002
DOEdir = "C:/Data/PREONLAB/---/"


for SimuRef in SimuList: #We create a loop to iterate over SimuList
    print("Simulating "+str(ShaftVelocity[SimuRef])+" RPM, "+str(OilFlowRate[SimuRef])+" l/min, "+str(OilTemperature[SimuRef])+" °C") #Text : current loadcase
    s=preonpy.Scene("C:/Data/PREONLAB/---/REF.prscene") #Opens the reference case
    ModelName = str(OilFlowRate[SimuRef]).replace('.','')+"lmin"+str(ShaftVelocity[SimuRef])+"RPM"+str(OilTemperature[SimuRef])+"C"
    s.save(DOEdir+ModelName+".prscene", as_portable=False) #Saves the case as a new file in a folder
    Rotation = s.find_object("Rotation") #Here, a transform group named "ROTATION" is master for the transformation of all shaft parts. We will set its rotation speed to the desired one.
    Rotation["revolutions per second"] = ShaftVelocity[SimuRef]/60 #Sets the rotation speed in rotation per second accordind to ShaftVelocity list
    
    for obj_name in s.object_names:
        obj = s.find_object(obj_name)
        if obj.type == "Area source":
            s.find_object(obj_name)["volume flow rate"]  = OilFlowRate[SimuRef]/1000/60/NbOfSources #We set the flow rate in m3/s according to OilFlowRate list
            print(obj_name + " is area source")
            
    SimulationTime = np.round(1/ShaftVelocity[SimuRef]*60*NbOfRotations,4)
    s['view frame rate'] = np.floor(NbOfFramesPerSimu/SimulationTime) #We set the framerate so that NbOfFramesPerSimu frames are saved in SimulationTime duration
    s['simulation frame rate'] = np.floor(NbOfFramesPerSimu/SimulationTime) #We set the view framerate equal to simulation framerate
    Solver = s.find_object("PreonSolver_1")
    Solver["cohesion"] = OilSurfaceTension[SimuRef]
    Solver["shear viscosity"] = OilViscosity[SimuRef]
    Solver["spacing"] = Spacing
    Solver["rest density"] = OilDensity[SimuRef]

    s.save() #save the current configuration
    s.simulate(0, str(SimulationTime)+"s") #Launches the simulation according to SimulationTime duration
    
    s.find_object("Total flow rate SensorPlane").write_statistics_to_csv(DOEdir+"Total flow rate SensorPlane"+ModelName+".csv",False)
    s.find_object("End SensorPlane").write_statistics_to_csv(DOEdir+"End SensorPlane"+ModelName+".csv",False)
    s.find_object("Total volume").write_statistics_to_csv(DOEdir+"Total volume"+ModelName+".csv",False)
    s.find_object("Poach volume").write_statistics_to_csv(DOEdir+"Poach volume"+ModelName+".csv",False)
    
    HeightSensor = s.find_object("HeightField_1")
    HeightSensor["behavior"] = "active"
    Renderer = s.find_object("PreonRenderer_1")
    Renderer["behavior"] = "active"
    
    s.post_process(0, NbOfFramesPerSimu, [HeightSensor, Renderer])

    
    
    
    

    
    
