from CRABClient.UserUtilities import config

config = config()

config.General.requestName = "WZ2Q2L_2016postAPV"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "run_crab_mc.py"
config.JobType.maxMemoryMB = 3000

config.Data.inputDataset = "/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM"
config.Data.outLFNDirBase = "/store/group/METUCMS/photonana/reNanoAOD/"
config.Data.outputDatasetTag = "RunIISummer20UL16_NanoAODv9"
config.Data.inputDBS = "global"
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = "T2_TR_METU"
config.Site.whitelist = ["T2_*","T3_*"]
