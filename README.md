# Artifact for the Paper "SURE: A Visualized Failure Indexing Approach using Program Memory Spectrum"



+ ***Code/***
  
  + `network/`
    + `siamese-AlexNet.py` provides the architecture of AlexNet.
    + `siamese-ResNet.py` provides the architecture of ResNet.
    + `siamese-VGG16.py` provides the architecture of VGG16.
    + `utils_fit.py` is the process of training and validation.
    
  + `getSpectrum.py` gets the spectrum from the code coverage.
  
  + `SBFL_Formula_DStar.py` calculates suspiciousness for each program statement.
  
  + `collect_MIs.py` collects the run-time memory information for each failed test case.
  
  + `get_GDB_var.py` is the collection script using GDB.
  
  + `get_JDB_var.py` is the collection script using JDB.
  
  + `getMemoryImage.py` transforms the gathered memory information into PMS images.
  
  + `PMSDistance.py` measures the distance between a pair of PMS images.
  
  + `clustering.py` is the clustering algorithm, which enables all failures to be indexed according to their own root cause.
  
    
  
+ ***Faulty_Program/***
  
  * `SIR/`
    * `$project/src` is the clean version of the C benchmark project.
    * `$project/AllMutants ($project).xls` is the mutants used to create faulty versions.
    
  * `Defects4J/`
    * `$project/v$x` contains the faulty version of the Java benchmark project and the corresponding test suite.
    
    * `$project/trans` contains the transplanted failed test cases.
    
      
  
+ ***HumanStudy/***
  
  * `Participant-$x/` gives the questionnaire collected from the x-th participant and the time cost.
    
    * `Result/` is the collected questionnaire.
    
    * `Time.xlsx` is the time cost of completing the tasks.
    
      
  
+ ***Model/***
  
  * `AlexNet-0.1-ep027-loss0.016-val_loss0.035.zip` is the trained model based on the breakpoint determination threshold of 10% and the feature extraction network of AlexNet.
  
  * `ResNet-0.1-ep013-loss0.030-val_loss0.029.zip` is the trained model based on the breakpoint determination threshold of 10% and the feature extraction network of ResNet.
  
  * `Vgg16-0.1-ep027-loss0.016-val_loss0.039.zip` is the trained model based on the breakpoint determination threshold of 10% and the feature extraction network of Vgg16.
  
    
  
+ ***PMS_Images/***
  
  + `SIR/` contains PMS_Images of SIR benchmarks.
  + `Defects4J/` contains PMS_Images of Defects4J benchmarks.
