# Auto generated configuration file
# using: 
# Revision: 1.149 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: promptCollisionReco -s RAW2DIGI,L1Reco,RECO,DQM,ALCA:SiStripCalZeroBias --datatier RECO --eventcontent RECO --conditions CRAFT09_R_V4::All --scenario pp --no_exec --data --magField AutoFromDBCurrent -n 100
import FWCore.ParameterSet.Config as cms

process = cms.Process('spike')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/GeometryExtended_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/StandardSequences/RawToDigi_Data_cff')
process.load('Configuration/StandardSequences/L1Reco_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('DQMOffline/Configuration/DQMOffline_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    annotation = cms.untracked.string('rereco nevts:100'),
    name = cms.untracked.string('PyReleaseValidation')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound'),
    wantSummary = cms.untracked.bool(True) 
)
# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( 
            'file:/tmp/ferriff/rechit_skim.root'
#'/store/data/BeamCommissioning09/MinimumBias/RAW/v1/000/124/120/DC0FA50D-6BE8-DE11-8A92-000423D94E70.root'
#'file:/data/withvertex732.root'
#'/store/express/BeamCommissioning09/ExpressPhysics/FEVT/v2/000/123/615/38379AF1-B4E2-DE11-BB10-001617C3B706.root'
#'rfio:/castor.cern.ch/cms/store/data/BeamCommissioning09/castor/MinimumBias/RAW/v1/000/122/314/CC89C4BC-DE11-B365-0030487D0D3A.root'
    )
    #skipEvents = cms.untracked.uint32(200)
)

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

#### Output definition
###process.FEVT = cms.OutputModule("PoolOutputModule",
###    splitLevel = cms.untracked.int32(0),
###    outputCommands = process.RECOEventContent.outputCommands,
###    fileName = cms.untracked.string('promptReco_RAW2DIGI_L1Reco_RECO_DQM_ALCA.root'),
###    dataset = cms.untracked.PSet(
###        dataTier = cms.untracked.string('RECO'),
###        filterName = cms.untracked.string('')
###    )
###)

# Other statements
#process.GlobalTag.globaltag = 'GR09_R_35X_V2::All'
process.GlobalTag.globaltag = 'GR10_P_V3::All'



#####################################################################################################
####
####  Top level replaces for handling strange scenarios of early collisions
####

## TRACKING:
## Skip events with HV off
process.newSeedFromTriplets.ClusterCheckPSet.MaxNumberOfPixelClusters=2000
process.newSeedFromPairs.ClusterCheckPSet.MaxNumberOfCosmicClusters=10000
process.secTriplets.ClusterCheckPSet.MaxNumberOfPixelClusters=1000
process.fifthSeeds.ClusterCheckPSet.MaxNumberOfCosmicClusters = 5000
process.fourthPLSeeds.ClusterCheckPSet.MaxNumberOfCosmicClusters=10000

###### FIXES TRIPLETS FOR LARGE BS DISPLACEMENT ######

### pixelTracks
#---- replaces ----
process.pixelTracks.RegionFactoryPSet.ComponentName = 'GlobalRegionProducerFromBeamSpot' # was GlobalRegionProducer
process.pixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.useFixedPreFiltering = True     # was False
#---- new parameters ----
process.pixelTracks.RegionFactoryPSet.RegionPSet.nSigmaZ  = cms.double(4.06) # was originHalfLength = 15.9; translated assuming sigmaZ ~ 3.8
process.pixelTracks.RegionFactoryPSet.RegionPSet.beamSpot = cms.InputTag("offlineBeamSpot")

### 0th step of iterative tracking
#---- replaces ----
process.newSeedFromTriplets.RegionFactoryPSet.ComponentName = 'GlobalRegionProducerFromBeamSpot' # was GlobalRegionProducer
process.newSeedFromTriplets.OrderedHitsFactoryPSet.GeneratorPSet.useFixedPreFiltering = True     # was False
#---- new parameters ----
process.newSeedFromTriplets.RegionFactoryPSet.RegionPSet.nSigmaZ   = cms.double(4.06)  # was originHalfLength = 15.9; translated assuming sigmaZ ~ 3.8
process.newSeedFromTriplets.RegionFactoryPSet.RegionPSet.beamSpot = cms.InputTag("offlineBeamSpot")

### 2nd step of iterative tracking
#---- replaces ----
process.secTriplets.RegionFactoryPSet.ComponentName = 'GlobalRegionProducerFromBeamSpot' # was GlobalRegionProducer
process.secTriplets.OrderedHitsFactoryPSet.GeneratorPSet.useFixedPreFiltering = True     # was False
#---- new parameters ----
process.secTriplets.RegionFactoryPSet.RegionPSet.nSigmaZ  = cms.double(4.47)  # was originHalfLength = 17.5; translated assuming sigmaZ ~ 3.8
process.secTriplets.RegionFactoryPSet.RegionPSet.beamSpot = cms.InputTag("offlineBeamSpot")

## Primary Vertex
process.offlinePrimaryVerticesWithBS.PVSelParameters.maxDistanceToBeam = 2
process.offlinePrimaryVerticesWithBS.TkFilterParameters.maxNormalizedChi2 = 20
process.offlinePrimaryVerticesWithBS.TkFilterParameters.minSiliconHits = 6
process.offlinePrimaryVerticesWithBS.TkFilterParameters.maxD0Significance = 100
process.offlinePrimaryVerticesWithBS.TkFilterParameters.minPixelHits = 1
process.offlinePrimaryVerticesWithBS.TkClusParameters.zSeparation = 10
process.offlinePrimaryVertices.PVSelParameters.maxDistanceToBeam = 2
process.offlinePrimaryVertices.TkFilterParameters.maxNormalizedChi2 = 20
process.offlinePrimaryVertices.TkFilterParameters.minSiliconHits = 6
process.offlinePrimaryVertices.TkFilterParameters.maxD0Significance = 100
process.offlinePrimaryVertices.TkFilterParameters.minPixelHits = 1
process.offlinePrimaryVertices.TkClusParameters.zSeparation = 10

## ECAL 
process.ecalRecHit.ChannelStatusToBeExcluded = [ 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 78, 142 ]
#process.ecalRecHit.ChannelStatusToBeExcluded = [ ]

##Preshower
process.ecalPreshowerRecHit.ESGain = 2
process.ecalPreshowerRecHit.ESBaseline = 0
process.ecalPreshowerRecHit.ESMIPADC = 55

##only for 34X
process.ecalPreshowerRecHit.ESRecoAlgo = cms.untracked.int32(1)

## HCAL temporary fixes
process.hfreco.firstSample  = 3
process.hfreco.samplesToAdd = 4

process.zdcreco.firstSample = 4
process.zdcreco.samplesToAdd = 3

## EGAMMA
process.ecalDrivenElectronSeeds.SCEtCut = cms.double(1.0)
process.ecalDrivenElectronSeeds.applyHOverECut = cms.bool(False)
process.ecalDrivenElectronSeeds.SeedConfiguration.z2MinB = cms.double(-0.9)
process.ecalDrivenElectronSeeds.SeedConfiguration.z2MaxB = cms.double(0.9)
process.ecalDrivenElectronSeeds.SeedConfiguration.r2MinF = cms.double(-1.5)
process.ecalDrivenElectronSeeds.SeedConfiguration.r2MaxF = cms.double(1.5)
process.ecalDrivenElectronSeeds.SeedConfiguration.rMinI = cms.double(-2.)
process.ecalDrivenElectronSeeds.SeedConfiguration.rMaxI = cms.double(2.)
process.ecalDrivenElectronSeeds.SeedConfiguration.DeltaPhi1Low = cms.double(0.3)
process.ecalDrivenElectronSeeds.SeedConfiguration.DeltaPhi1High = cms.double(0.3)
process.ecalDrivenElectronSeeds.SeedConfiguration.DeltaPhi2 = cms.double(0.3)
process.gsfElectrons.applyPreselection = cms.bool(False)
process.photons.minSCEtBarrel = 1.
process.photons.minSCEtEndcap =1.
process.photonCore.minSCEt = 1.
process.conversionTrackCandidates.minSCEt =1.
process.conversions.minSCEt =1.
process.trackerOnlyConversions.AllowTrackBC = cms.bool(False)
process.trackerOnlyConversions.AllowRightBC = cms.bool(False)
process.trackerOnlyConversions.MinApproach = cms.double(-.25)
process.trackerOnlyConversions.DeltaCotTheta = cms.double(.07)
process.trackerOnlyConversions.DeltaPhi = cms.double(.2)

###
###  end of top level replacements
###
###############################################################################################

# produce L1 trigger object maps (temporary fix for HLT mistake 
# in event content definition of RAW datatier for stream A)
import L1Trigger.GlobalTrigger.gtDigis_cfi
process.hltL1GtObjectMap = L1Trigger.GlobalTrigger.gtDigis_cfi.gtDigis.clone()
process.hltL1GtObjectMap.GmtInputTag = cms.InputTag( "gtDigis" )
process.hltL1GtObjectMap.GctInputTag = cms.InputTag( "gctDigis" )
process.hltL1GtObjectMap.CastorInputTag = cms.InputTag( "castorL1Digis" )
process.hltL1GtObjectMap.ProduceL1GtDaqRecord = cms.bool( False )
process.hltL1GtObjectMap.ProduceL1GtEvmRecord = cms.bool( False )
process.hltL1GtObjectMap.ProduceL1GtObjectMapRecord = cms.bool( True )
process.hltL1GtObjectMap.WritePsbL1GtDaqRecord = cms.bool( False )
process.hltL1GtObjectMap.ReadTechnicalTriggerRecords = cms.bool( True )
process.hltL1GtObjectMap.EmulateBxInEvent = cms.int32( 1 )
process.hltL1GtObjectMap.AlternativeNrBxBoardDaq = cms.uint32( 0 )
process.hltL1GtObjectMap.AlternativeNrBxBoardEvm = cms.uint32( 0 )
process.hltL1GtObjectMap.BstLengthBytes = cms.int32( -1 )
process.hltL1GtObjectMap.TechnicalTriggersInputTags = cms.VInputTag( 'simBscDigis' )
process.hltL1GtObjectMap.RecordLength = cms.vint32( 3, 0 )


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1GtObjectMap_step = cms.Path(process.hltL1GtObjectMap)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction_withPixellessTk)
process.reconstruction_step.remove( process.globalreco_plusPL )
process.reconstruction_step.remove( process.highlevelreco )
process.reconstruction_step.remove( process.muoncosmicreco )
process.reconstruction_step.remove( process.logErrorHarvester )
process.localreco.remove( process.trackerlocalreco )
process.localreco.remove( process.muonlocalreco )
process.localreco.remove( process.particleFlowCluster )
process.localreco.remove( process.castorreco )
process.localreco.remove( process.lumiProducer )

process.dqmoffline_step = cms.Path(process.DQMOffline)
process.endjob_step = cms.Path(process.endOfProcess)
#process.out_step = cms.EndPath(process.FEVT)


process.ntupleMaker = cms.EDProducer("NtupleMaker",
        recHitCollection_EB = cms.InputTag("ecalRecHit:EcalRecHitsEB"),
        recHitCollection_EE = cms.InputTag("ecalRecHit:EcalRecHitsEE"),
        uncalibRecHitCollection_EB = cms.InputTag("ecalGlobalUncalibRecHit:EcalUncalibRecHitsEB"),
        uncalibRecHitCollection_EE = cms.InputTag("ecalGlobalUncalibRecHit:EcalUncalibRecHitsEE"),
        digiCollection_EB = cms.InputTag("ecalDigis:ebDigis"),
        digiCollection_EE = cms.InputTag("ecalDigis:ebDigis"),
        l1InputTag = cms.InputTag("gtDigis"),
        outputFile = cms.string("ntu_output.root"),
        energyThreshold = cms.double(2.)
)
process.ntuple = cms.Path( process.ntupleMaker )

# Schedule definition
#process.schedule = cms.Schedule(process.raw2digi_step,process.L1GtObjectMap_step,process.L1Reco_step,process.reconstruction_step,process.dqmoffline_step,process.endjob_step,process.out_step)
process.schedule = cms.Schedule(process.raw2digi_step,process.L1GtObjectMap_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.ntuple)
