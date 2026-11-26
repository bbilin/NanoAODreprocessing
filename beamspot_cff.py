import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

# Same branches as the BeamSpot table of later NanoAOD releases, plus x, y and the slopes.
# In MC this is the simulated beamspot of the global tag.
beamspotTable = cms.EDProducer("SimpleBeamspotFlatTableProducer",
    src = cms.InputTag("offlineBeamSpot"),
    name = cms.string("BeamSpot"),
    doc = cms.string("offlineBeamSpot, the offline reconstructed beamspot"),
    variables = cms.PSet(
        # The 10_6 BeamSpotProducer leaves the type unset, so this reads -1 (Unknown).
        type = Var("type()", int, doc="BeamSpot type (Unknown = -1, Fake = 0, LHC = 1, Tracker = 2)"),
        x = Var("x0()", float, doc="BeamSpot center, x coordinate (cm)", precision=-1),
        y = Var("y0()", float, doc="BeamSpot center, y coordinate (cm)", precision=-1),
        z = Var("z0()", float, doc="BeamSpot center, z coordinate (cm)", precision=-1),
        zError = Var("z0Error()", float, doc="Error on BeamSpot center, z coordinate (cm)", precision=-1),
        sigmaZ = Var("sigmaZ()", float, doc="Width of BeamSpot in z (cm)", precision=-1),
        sigmaZError = Var("sigmaZ0Error()", float, doc="Error on width of BeamSpot in z (cm)", precision=-1),
        dxdz = Var("dxdz()", float, doc="BeamSpot slope dx/dz", precision=-1),
        dydz = Var("dydz()", float, doc="BeamSpot slope dy/dz", precision=-1),
    )
)

beamspotTables = cms.Sequence(beamspotTable)
