import FWCore.ParameterSet.Config as cms

prunedForJets = cms.EDProducer("GenParticlePruner",
                src = cms.InputTag("genParticles"),
                select = cms.vstring(
                        "keep *",
                        "drop (pdgId == 22 && isPromptFinalState())"
                        )
                )

from DQMServices.Core.DQMEDAnalyzer import DQMEDAnalyzer
gjetValidation = DQMEDAnalyzer('GJetValidation',
                               hepmcCollection = cms.InputTag("generatorSmeared"),
                               genParticleCollection = cms.InputTag("genParticles"),
                               genjetCollection = cms.InputTag("ak4GenJets"),
                               UseWeightFromHepMC = cms.bool(True)
                               )
