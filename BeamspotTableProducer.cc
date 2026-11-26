// One-row-per-event NanoAOD table of the offline beamspot (the BeamSpot_* branches).
// CMSSW_10_6 ships the EventSingletonSimpleFlatTableProducer template but not this
// instantiation, which later releases have in SimpleFlatTableProducerPlugins.cc.
#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

typedef EventSingletonSimpleFlatTableProducer<reco::BeamSpot> SimpleBeamspotFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleBeamspotFlatTableProducer);
