#!/usr/bin/env python3
"""Write one CRAB config per dataset into submit_<year>/.

    python3 make_crab_cfgs.py datasets_lpair.txt datasets_minnlo.txt datasets_2016.txt

Each list holds full dataset names, one per line (# starts a comment): UL
MiniAODv2 MC (MINIAODSIM, run with run_crab_mc.py) or UL MiniAODv2 data
(MINIAOD, run with run_crab_data.py on the golden luminosity sections of
its year). The year folder comes from the campaign
or the run era (HIPM runs are 2016preAPV), the request name from the dataset name.
Every dataset is checked in DBS first: it must be VALID, and its events per file
set unitsPerJob so that a job reads about EVENTS_PER_JOB events. Needs a grid
proxy and dasgoclient (/cvmfs/cms.cern.ch/common/dasgoclient).
"""
import json
import os
import re
import subprocess
import sys

EVENTS_PER_JOB = 100000

# campaign -> (submit folder suffix, short year tag)
CAMPAIGNS = {
    "RunIISummer20UL16MiniAODAPVv2": ("2016preAPV", "16APV"),
    "RunIISummer20UL16MiniAODv2": ("2016postAPV", "16"),
    "RunIISummer20UL17MiniAODv2": ("2017", "17"),
    "RunIISummer20UL18MiniAODv2": ("2018", "18"),
}

# golden JSON of each year, which the data configs pass to CRAB as Data.lumiMask
CERT = "https://cms-service-dqmdc.web.cern.ch/CAF/certification/"
GOLDEN_JSON = {
    "2016": CERT + "Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2017": CERT + "Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
    "2018": CERT + "Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
}

# primary dataset prefix -> config name, the names the 2017 and 2018 configs use
BACKGROUNDS = {
    "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX": "DY",
    "TTTo2L2Nu_": "TTTo2L2Nu",
    "WWTo2L2Nu_": "WW2L2Nu",
    "WZTo3LNu_": "WZ3LNu",
    "WZTo2Q2L_": "WZ2Q2L",
    "ZZTo2L2Nu_": "ZZ2L2Nu",
    "ZZTo2Q2L_": "ZZ2L2Q",
    "ZZTo4L_": "ZZ4L",
}

TEMPLATE = """from CRABClient.UserUtilities import config

config = config()

config.General.requestName = "{request}"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "Analysis"
config.JobType.psetName = "{pset}"
config.JobType.maxMemoryMB = 3000

config.Data.inputDataset = "{dataset}"
config.Data.outLFNDirBase = "/store/group/METUCMS/photonana/reNanoAOD/"
config.Data.outputDatasetTag = "{tag}"
config.Data.inputDBS = "global"
{lumimask}config.Data.splitting = "FileBased"
config.Data.unitsPerJob = {units}
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = "T2_TR_METU"
config.Site.whitelist = ["T2_*","T3_*"]
"""


def das(query):
    env = dict(os.environ)
    env.pop("PYTHONHOME", None)  # the LCG view's PYTHONHOME breaks dasgoclient's python
    out = subprocess.run(["dasgoclient", "-query", query, "-json"], env=env,
                         stdout=subprocess.PIPE, check=True).stdout
    return json.loads(out)


def dbs_info(dataset):
    # An exact dataset name is returned whatever its status, so read the access type.
    access = {r.get("dataset_access_type")
              for d in das("dataset dataset=%s status=*" % dataset)
              for r in d.get("dataset", []) if r.get("dataset_access_type")}
    summary = das("summary dataset=%s" % dataset)[0]["summary"][0]
    return access, summary["nevents"], summary["nfiles"]


def short_name(primary):
    for prefix, name in BACKGROUNDS.items():
        if primary.startswith(prefix):
            return name
    if primary.startswith("GGTo"):  # GGToMuMu_Pt-5_Mll-50To200_Inel-Inel_13TeV-CepGen-...
        return primary.split("_13TeV")[0]
    m = re.match(r"(DYJetsTo[A-Za-z]+_M-[0-9A-Za-z]+)_.*powhegMiNNLO", primary)
    if m:  # DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-... -> DYJetsToMuMu_M-50_MiNNLO
        return m.group(1) + "_MiNNLO"
    sys.exit("no naming rule for " + primary)


def main(lists):
    datasets = []
    for path in lists:
        with open(path) as f:
            datasets += [l.strip() for l in f if l.strip() and not l.startswith("#")]

    seen = {}
    for dataset in datasets:
        _, primary, processed, tier = dataset.split("/")
        if tier == "MINIAOD":  # data: /SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD
            m = re.match(r"(Run(201[678])[A-H](?:-ver\d)?([-_]HIPM)?)[-_]UL201[678]_MiniAODv2(?:_GT36)?-v\d+$",
                         processed)
            if not m:
                sys.exit("not a UL MiniAODv2 data dataset: " + dataset)
            era, run_year, hipm = m.groups()
            year = {"2016": "2016postAPV", "2017": "2017", "2018": "2018"}[run_year]
            if hipm:
                year = "2016preAPV"
            yy = {"2016preAPV": "16APV", "2016postAPV": "16", "2017": "17", "2018": "18"}[year]
            name, pset, suffix = "%s_%s" % (primary, era), "run_crab_data.py", ""
            request, tag = name, "%s-RunIISummer20UL%s_NanoAODv9" % (name, yy)
            lumimask = 'config.Data.lumiMask = "%s"\n' % GOLDEN_JSON[run_year]
        else:
            campaign = processed.split("-")[0]
            if tier != "MINIAODSIM" or campaign not in CAMPAIGNS:
                sys.exit("not a UL MiniAODv2 MC dataset: " + dataset)
            year, yy = CAMPAIGNS[campaign]
            ext = re.search(r"_(ext\d+)-v\d+$", processed)
            suffix = "_" + ext.group(1) if ext else ""
            name, pset = short_name(primary) + suffix, "run_crab_mc.py"
            request, tag = "%s_%s" % (name, year), "RunIISummer20UL%s_NanoAODv9%s" % (yy, suffix)
            lumimask = ""
        cfg = "submit_%s/submit_crab_%s.py" % (year, name)
        if cfg in seen:
            sys.exit("%s and %s both map to %s" % (seen[cfg], dataset, cfg))
        seen[cfg] = dataset

        access, nevents, nfiles = dbs_info(dataset)
        if access != {"VALID"}:
            sys.exit("%s is %s in DBS" % (dataset, ",".join(sorted(access)) or "missing"))
        units = max(1, int(round(EVENTS_PER_JOB * nfiles / float(nevents))))
        njobs = -(-nfiles // units)
        if njobs > 10000:  # CRAB's limit of jobs per task
            sys.exit("%s would need %d jobs" % (dataset, njobs))

        os.makedirs("submit_" + year, exist_ok=True)
        with open(cfg, "w") as f:
            f.write(TEMPLATE.format(request=request, pset=pset, dataset=dataset, tag=tag, units=units,
                                    lumimask=lumimask))
        print("%-75s %4d files/job %5d jobs %11d events" % (cfg, units, njobs, nevents))


if __name__ == "__main__":
    main(sys.argv[1:])
