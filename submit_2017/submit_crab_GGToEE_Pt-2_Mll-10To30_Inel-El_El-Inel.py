from CRABClient.UserUtilities import config

config = config()

config.General.requestName = "GGToEE_Pt-2_Mll-10To30_Inel-El_El-Inel_2017"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "run_crab_mc.py"
config.JobType.maxMemoryMB = 3000

config.Data.inputDataset = "/GGToEE_Pt-2_Mll-10To30_Inel-El_El-Inel_13TeV-CepGen-lpair-SY-pythia6/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"
config.Data.outLFNDirBase = "/store/group/METUCMS/photonana/reNanoAOD/"
config.Data.outputDatasetTag = "RunIISummer20UL17_NanoAODv9"
config.Data.inputDBS = "global"
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = "T2_TR_METU"
config.Site.whitelist = ["T2_*","T3_*"]
