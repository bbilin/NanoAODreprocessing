from CRABClient.UserUtilities import config

config = config()

config.General.requestName = "SingleElectron_Run2017C"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "run_crab_data.py"
config.JobType.maxMemoryMB = 3000
#config.JobType.numCores = 8

config.Data.inputDataset = "/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD" 
config.Data.outLFNDirBase = "/store/group/METUCMS/photonana/reNanoAOD/"
config.Data.outputDatasetTag = "SingleElectron_Run2017C-RunIISummer20UL17_NanoAODv9"
config.Data.inputDBS = "global"
config.Data.lumiMask = "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = "T2_TR_METU"
config.Site.whitelist = ["T2_*","T3_*"]
