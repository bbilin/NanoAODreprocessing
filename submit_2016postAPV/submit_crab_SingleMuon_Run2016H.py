from CRABClient.UserUtilities import config

config = config()

config.General.requestName = "SingleMuon_Run2016H"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "run_crab_data.py"
config.JobType.maxMemoryMB = 3000

config.Data.inputDataset = "/SingleMuon/Run2016H-UL2016_MiniAODv2-v2/MINIAOD"
config.Data.outLFNDirBase = "/store/group/METUCMS/photonana/reNanoAOD/"
config.Data.outputDatasetTag = "SingleMuon_Run2016H-RunIISummer20UL16_NanoAODv9"
config.Data.inputDBS = "global"
config.Data.lumiMask = "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = "T2_TR_METU"
config.Site.whitelist = ["T2_*","T3_*"]
