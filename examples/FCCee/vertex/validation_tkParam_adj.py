import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesFlavour")
ROOT.gErrorIgnoreLevel = ROOT.kInfo
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_bs  = ROOT.dummyLoaderFlavour

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


#ROOT.ROOT.EnableThreadSafety()
#ROOT.ROOT.EnableImplicitMT(1)
ROOT.TTree.SetMaxTreeSize(100000000000)

#
# Example file:
# /eos/experiment/fcc/ee/examples/lowerTriangle/dummy_zmumu_for_covMat_events_IFSROFF.root
#
processList = {
    'p8_ee_Zmumu_ecm91':{}
}


class RDFanalysis():

    def analysers(df):

        df2 = (
            df
            # MC event primary vertex
            .Define("MC_PrimaryVertex", "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

            .Define("has_Bs","FCCAnalyses::MCParticle::filter_pdgID(-531, true)(Particle)==true")

            .Define("RP_TRK_D0",
                    "ReconstructedParticle2Track::getRP2TRK_D0(ReconstructedParticles, EFlowTrack_1)")    #  d0 and z0 in mm
            .Define("RP_TRK_Z0",
                    "ReconstructedParticle2Track::getRP2TRK_Z0(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_omega",
                    "ReconstructedParticle2Track::getRP2TRK_omega(ReconstructedParticles, EFlowTrack_1)")  # rho, in mm-1
            .Define("RP_TRK_phi",
                    "ReconstructedParticle2Track::getRP2TRK_phi(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_tanlambda",
                    "ReconstructedParticle2Track::getRP2TRK_tanLambda(ReconstructedParticles, EFlowTrack_1)")

            .Define("RP_TRK_D0_cov",
                    "ReconstructedParticle2Track::getRP2TRK_D0_cov(ReconstructedParticles, EFlowTrack_1)")    
            .Define("RP_TRK_Z0_cov",
                    "ReconstructedParticle2Track::getRP2TRK_Z0_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_omega_cov",
                    "ReconstructedParticle2Track::getRP2TRK_omega_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_phi_cov",
                    "ReconstructedParticle2Track::getRP2TRK_phi_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_tanlambda_cov",
                    "ReconstructedParticle2Track::getRP2TRK_tanLambda_cov(ReconstructedParticles, EFlowTrack_1)")

	        .Define("RP_TRK_d0_phi0_cov",
                       "ReconstructedParticle2Track::getRP2TRK_d0_phi0_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_d0_omega_cov",
                    "ReconstructedParticle2Track::getRP2TRK_d0_omega_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_d0_z0_cov",
                    "ReconstructedParticle2Track::getRP2TRK_d0_z0_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_d0_tanlambda_cov",
                    "ReconstructedParticle2Track::getRP2TRK_d0_tanlambda_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_phi0_omega_cov",
                    "ReconstructedParticle2Track::getRP2TRK_phi0_omega_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_phi0_z0_cov",
                    "ReconstructedParticle2Track::getRP2TRK_phi0_z0_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_phi0_tanlambda_cov",
                    "ReconstructedParticle2Track::getRP2TRK_phi0_tanlambda_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_omega_z0_cov",
                    "ReconstructedParticle2Track::getRP2TRK_omega_z0_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_omega_tanlambda_cov",
                    "ReconstructedParticle2Track::getRP2TRK_omega_tanlambda_cov(ReconstructedParticles, EFlowTrack_1)")
            .Define("RP_TRK_z0_tanlambda_cov",
                    "ReconstructedParticle2Track::getRP2TRK_z0_tanlambda_cov(ReconstructedParticles, EFlowTrack_1)")

            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Alias("Particle0", "Particle#0.index")
            .Alias("Particle1", "Particle#1.index")

            #.Define('RP_MC_index',
            #"ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_p',
                    "ReconstructedParticle2MC::getRP2MC_p(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_px',
                    "ReconstructedParticle2MC::getRP2MC_px(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_py',
                    "ReconstructedParticle2MC::getRP2MC_py(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_pz',
                    "ReconstructedParticle2MC::getRP2MC_pz(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_pdg',
                    "ReconstructedParticle2MC::getRP2MC_pdg(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_charge',
                    "ReconstructedParticle2MC::getRP2MC_charge(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            .Define('RP_MC_tlv',
                    "ReconstructedParticle2MC::getRP2MC_tlv(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            #.Define('RP_MC_mass',
            #"ReconstructedParticle2MC::getRP2MC_mass(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            #.Define('RP_MC_parentindex',
            #"ReconstructedParticle2MC::getRP2MC_parentid(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, Particle0)")


			### Added for Z -> mu mu reconstruction ###
			.Define("RP_theta","ReconstructedParticle::get_theta(ReconstructedParticles)")


            # MC event primary vertex
            .Define("PrimaryTracks",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
            .Define("nPrimaryTracks", "ReconstructedParticle::get_n(PrimaryTracks)")

            # number of tracks
            .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

	        # Z -> mu+ mu-
            .Define("Zmumu_indices", "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay( 23, {13, -13}, true, true) ( Particle, Particle1)" )
	        .Define("Z", "selMC_leg(0) (Zmumu_indices, Particle)")
            .Define("FoundZ", "FCCAnalyses::MCParticle::get_n( Z )")
	
	        .Define("mu1", "selMC_leg(1) (Zmumu_indices, Particle)")
	        .Define("mu2", "selMC_leg(2) (Zmumu_indices, Particle)")
	
            .Define("Z_theta", "FCCAnalyses::MCParticle::get_theta( Z )")
            .Define("mu1_theta", "FCCAnalyses::MCParticle::get_theta( mu1 )")
            .Define("mu2_theta", "FCCAnalyses::MCParticle::get_theta( mu2 )")

            .Define("mu1_pt", "FCCAnalyses::MCParticle::get_pt( mu1 )")
            .Define("mu2_pt", "FCCAnalyses::MCParticle::get_pt( mu2 )")


            ### Z vertex reconstruction

            .Define("ZRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Zmumu_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

            # the corresponding tracks - here, dummy particles, if any, are removed
            .Define("ZTracks",  "ReconstructedParticle2Track::getRP2TRK( ZRecoParticles, EFlowTrack_1)" )

            # number of tracks used to reconstruct the Ds vertex
            .Define("n_ZTracks", "ReconstructedParticle2Track::getTK_n( ZTracks )")

            # Reco'ed vertex of the Kstar  ( = reco'ed decay vertex of the Bd from the K+ and Pi- tracks only)
            .Define("ZVertexObject",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 2, ZTracks, true, 4.5, 20e-3, 300)" )
            .Define("ZVertex",  "VertexingUtils::get_VertexData( ZVertexObject )")

            # MC production vertex of the Kstar ( = MC decay vertex ot th Bd, = MC decay vertex of the Kstar)
            .Define("ZMCDecayVertex", " FCCAnalyses::MCParticle::get_vertex( Z )")

            # MC indices of the decay Bs -> Ds+ K-
            # In the file I process, only the Bs0 (not the Bsbar) has been forced to decay into Ds+ K-
            # Look for (Ds+ K-) in the list of unstable decays of a Bs - hence oscillations are
            # not accounted for. So there should be at most one such decay per event. In any case,
            # would there be > 1, the method gives the first one encountered.
            # Returns the indices of : mother Bs, Ds+, K-

            .Define("Bs2DsK_indices", "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay( -531, {431, -321}, false, false) ( Particle, Particle1)" )


            # MC indices of (this) Ds+ -> K+ K- Pi+
            # Do not want *any* Ds here, hence use custom code in Bs2DsK.cc
            # Returns the indices of:  mother Ds+, K+ K- Pi+
            .Define("Ds2KKPi_indices",  "getMC_indices_Ds2KKPi( Bs2DsK_indices, Particle, Particle1) ")

            # MC indices of Bs -> ( K+ K- Pi+ ) K-
            # Return the indices of:  mother Bs, ( K+ K- Pi+ ) K-
            .Define("Bs2KKPiK_indices",  "getMC_indices_Bs2KKPiK( Bs2DsK_indices,  Ds2KKPi_indices)" )

            # the MC Bs :
            .Define("Bs",  "selMC_leg(0) ( Bs2DsK_indices, Particle )")
            .Define("n_Bs", "FCCAnalyses::MCParticle::get_n( Bs )" )
            # the MC Ds :
            .Define("Ds",  "selMC_leg(1) ( Bs2DsK_indices, Particle )")
            # the MC bachelor K- from the Bs decay :
            .Define("BachelorK",  "selMC_leg(2) ( Bs2DsK_indices, Particle )")

        	# the angle between the MC Ds and the MC K
            .Define("Angle_DsK",  "FCCAnalyses::MCParticle::AngleBetweenTwoMCParticles( Ds, BachelorK ) ")

            # The MC legs from the Ds decay
            .Define("Kplus",   "selMC_leg(1) ( Bs2KKPiK_indices, Particle )")
            .Define("Kminus",   "selMC_leg(2) ( Bs2KKPiK_indices, Particle )")
            .Define("Piplus",   "selMC_leg(3) ( Bs2KKPiK_indices, Particle )")

            .Define("Kplus_E",  "FCCAnalyses::MCParticle::get_e( Kplus )")
            .Define("Kminus_E",  "FCCAnalyses::MCParticle::get_e( Kminus )")
            .Define("Piplus_E",   "FCCAnalyses::MCParticle::get_e( Piplus )")


            # the Ds kinematics 
            .Define("Ds_E",  "FCCAnalyses::MCParticle::get_e( Ds )")
            .Define("Ds_pt", "FCCAnalyses::MCParticle::get_pt( Ds ) ")
            .Define("Ds_theta", "FCCAnalyses::MCParticle::get_theta( Ds )")
            .Define("Ds_phi", "FCCAnalyses::MCParticle::get_phi( Ds )")

            # the bachelor K kinematics
            .Define("BachelorK_E",  "FCCAnalyses::MCParticle::get_e( BachelorK )")
            .Define("BachelorK_theta",  "FCCAnalyses::MCParticle::get_theta( BachelorK )")
            .Define("BachelorK_phi",  "FCCAnalyses::MCParticle::get_phi( BachelorK )")

            # Decay vertex of the Ds
            # This takes the production vertex of the 1st non mother particle in Bs2KKPiK_indices, i.e.
            # of the K+ from the Ds, that's what we want. Need to change the name of this method, give it a more general name !
            .Define("DsMCDecayVertex",  "BsMCDecayVertex( Ds2KKPi_indices, Particle ) ")

            # Decay vertex of the Bs :
            # Use the BsMCDecayVertex coded for Bs2JPsiPhi: take the production vertex of the Ds. 
            .Define("BsMCDecayVertex",  "BsMCDecayVertex( Bs2DsK_indices, Particle ) ")


            # RecoParticles associated with the Ds decay
            # the size of this collection is always 3 provided that Ds2KKPi_indices is not empty.
            # In case one of the Ds legs did not make a RecoParticle, a "dummy" particle is inserted in the liat.
            # This is done on purpose, to maintain the mapping with the indices.
            .Define("DsRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Ds2KKPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

            # the corresponding tracks - here, dummy particles, if any, are removed
            .Define("DsTracks",  "ReconstructedParticle2Track::getRP2TRK( DsRecoParticles, EFlowTrack_1)" )

            # number of tracks used to reconstruct the Ds vertex
            .Define("n_DsTracks", "ReconstructedParticle2Track::getTK_n( DsTracks )")

            # the RecoParticles associated with the K+, K- and Pi+ of teh Ds decay
            .Define("RecoKplus",  "selRP_leg(0)( DsRecoParticles )" )
            .Define("RecoKminus", "selRP_leg(1)( DsRecoParticles )" )
            .Define("RecoPiplus", "selRP_leg(2)( DsRecoParticles )" )
            

			 # Reco'ed vertex of the Ds
            .Define("DsVertexObject",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 3, DsTracks)" )
            .Define("DsVertex",  "VertexingUtils::get_VertexData( DsVertexObject )")

            # ----------  Reconstruction of the Bs vertex 

            # the reco'ed legs of the Ds, with the momenta at the Ds decay vertex
            .Define("RecoKplus_atVertex",  "selRP_leg_atVertex(0)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")
            .Define("RecoKminus_atVertex",  "selRP_leg_atVertex(1)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")
            .Define("RecoPiplus_atVertex",  "selRP_leg_atVertex(2)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")

            # the  RecoParticle associated with  the bachelor K
             .Define("BsRecoParticles", "ReconstructedParticle2MC::selRP_matched_to_list( Bs2KKPiK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
             .Define("RecoBachelorK",  "selRP_leg(3)( BsRecoParticles )")
            # and the corresponding track
             .Define("BachelorKTrack",  "ReconstructedParticle2Track::getRP2TRK(  RecoBachelorK, EFlowTrack_1)" )

            # Reconstructed Ds
             .Define("RecoDs", " ReconstructedDs( RecoKplus, RecoKminus, RecoPiplus ) ")
             .Define("RecoDs_atVertex",  " ReconstructedDs( RecoKplus_atVertex, RecoKminus_atVertex, RecoPiplus_atVertex) ")

             .Define("RecoDs_pt",  "ReconstructedParticle::get_pt( RecoDs )")
             .Define("RecoDs_theta",  "ReconstructedParticle::get_theta( RecoDs ) ")
             .Define("RecoDs_phi",   "ReconstructedParticle::get_phi( RecoDs )")
             .Define("RecoDs_mass",  "ReconstructedParticle::get_mass( RecoDs )")

             .Define("RecoDs_atVertex_pt",  "ReconstructedParticle::get_pt( RecoDs_atVertex )")
             .Define("RecoDs_atVertex_theta",  "ReconstructedParticle::get_theta( RecoDs_atVertex )")
             .Define("RecoDs_atVertex_phi",   "ReconstructedParticle::get_phi( RecoDs_atVertex )")
             .Define("RecoDs_atVertex_mass",  "ReconstructedParticle::get_mass( RecoDs_atVertex )")

             # the list of tracks to reconstruct the Bs vertex
             # here, a TrackState is built from the RecoDs_atVertex, but the elements of the covariance matrix are
             # set arbitrarily - use a relative uncertainty of 5% for the parameters.
             # See below for a better way to do it.
             .Define("BsTracks",  "tracks_for_fitting_the_Bs_vertex( RecoDs_atVertex, BachelorKTrack, Ds, DsMCDecayVertex )" )
             .Define("n_BsTracks", "ReconstructedParticle2Track::getTK_n( BsTracks )")

             # Reco'ed Bs vertex
             .Define("BsVertexObject",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 2, BsTracks, true, 4.5, 20e-3, 300)" )
             .Define("BsVertex",  "VertexingUtils::get_VertexData( BsVertexObject )")


             # Try to better account for the covariance matrix of the Ds pseudo-track
             .Define("ReconstructedDs_atVertex_TrackState", "ReconstructedDs_atVertex_TrackState( RecoDs_atVertex, Ds, DsMCDecayVertex )" )
             .Define("RecoDs_atVertex_TrackState_Cov",  "ReconstructedDs_atVertex_TrackState_withCovariance( DsTracks, ReconstructedDs_atVertex_TrackState, DsVertexObject) ")
             .Define("BsTracks_Cov",  "tracks_for_fitting_the_Bs_vertex( RecoDs_atVertex_TrackState_Cov, BachelorKTrack) ")
             .Define("BsVertexObject_Cov",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 2, BsTracks_Cov, true, 4.5, 20e-3, 300)" )
             # This is the final Bs vertex
             .Define("BsVertex_Cov",  "VertexingUtils::get_VertexData( BsVertexObject_Cov )")

             .Define("Kplus_phi",  "FCCAnalyses::MCParticle::get_phi( Kplus )")
             .Define("RecoKplus_phi",  "ReconstructedParticle::get_phi( RecoKplus ) " )
             .Define("RecoKplus_atVertex_phi", "ReconstructedParticle::get_phi( RecoKplus_atVertex ) ")

             .Define("RecoBachelorK_E",  "ReconstructedParticle::get_e( RecoBachelorK )")
             )
        return df2

    def output():
        # select branches for output file
        branchList = [
		  "MC_PrimaryVertex",
		  "has_Bs",
          "RP_TRK_D0",
          "RP_TRK_Z0",
          "RP_TRK_omega",
          "RP_TRK_phi",
          "RP_TRK_tanlambda",

          "RP_TRK_D0_cov",
          "RP_TRK_Z0_cov",
          "RP_TRK_omega_cov",
          "RP_TRK_phi_cov",
          "RP_TRK_tanlambda_cov",

		  "RP_TRK_d0_phi0_cov",
		  "RP_TRK_d0_omega_cov",
		  "RP_TRK_d0_z0_cov",
		  "RP_TRK_d0_tanlambda_cov",
		  "RP_TRK_phi0_omega_cov",
		  "RP_TRK_phi0_z0_cov",
		  "RP_TRK_phi0_tanlambda_cov",
		  "RP_TRK_omega_z0_cov",
		  "RP_TRK_omega_tanlambda_cov",
		  "RP_TRK_z0_tanlambda_cov",

          "RP_MC_p",
          "RP_MC_px",
          "RP_MC_py",
          "RP_MC_pz",
          "RP_MC_pdg",
          "RP_MC_charge",
          "RP_MC_tlv",
		  "RP_theta",
          #"RP_MC_index",
          #"RP_MC_parentindex",

          "ntracks",
          "nPrimaryTracks",
		  "FoundZ",
		  "Z_theta",
		  "mu1_theta",
		  "mu2_theta",
          "mu1_pt",
          "mu2_pt",
		  "ZMCDecayVertex",
		  "n_ZTracks",
		  "ZVertex",
		  "Z",
          "Bs",
		  "n_Bs",
          "Ds",
          #"BachelorK",
          "Ds_E",
          "Ds_pt",
          "Ds_theta",
          "Ds_phi",
          "BachelorK_E",
          "BachelorK_theta",
          "BachelorK_phi",
           #"Kplus",
           #"Kminus",
           #"Piplus",
           "DsMCDecayVertex",
           "BsMCDecayVertex",
           #"DsTracks",
           "n_DsTracks",
           #"RecoKplus",
           #"RecoKminus",
           #"RecoPiplus",
           "DsVertex",
           "RecoDs",
           #"RecoDs_atVertex",
           "RecoDs_pt",
           "RecoDs_theta",
           "RecoDs_phi",
           "RecoDs_mass",
           #"RecoDs_atVertex_pt",
           "RecoDs_atVertex_theta",
           "RecoDs_atVertex_phi",
           "RecoDs_atVertex_mass",
           #"RecoBachelorK",
           "RecoBachelorK_E",
           "BsVertex",
           "n_BsTracks",
           #"RecoDs_atVertex_TrackState_Cov"

           "BsVertex_Cov",
           "Kplus_phi",
           "RecoKplus_phi",
           "RecoKplus_atVertex_phi",
           "Angle_DsK",
           "Kplus_E",
           "Kminus_E",
           "Piplus_E"
        ]
        return branchList
