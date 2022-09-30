import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesFlavour")
ROOT.gErrorIgnoreLevel = ROOT.kInfo # ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_bs  = ROOT.dummyLoaderFlavour


print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


### For Z -> mu+ mu-

# Require that there is a Z boson
Filter="MCParticle::filter_pdgID(23, true)(Particle)==true"


#
# Example file : 
#    /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zuds_IDEAtrkCov.root
#    ( these events were generated at (0,0,0) i.e. no vertex smearing
#
# Example file from spring2021, with vertex smearing :
#    /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zuds_ecm91/events_125841058.root


class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        #df2 = (self.df.Range(0,5000)
        df2 = (self.df

               # Select primary tracks based on the matching to MC
                  # This can be used  to select primary tracks when the
                  # gen-level primary vertex  is not  (0,0,0)
	       .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

	       # Require that there is a Z boson
	       .Filter( Filter )


               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )
               .Define("PrimaryTracks",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               .Define("nPrimaryTracks", "ReconstructedParticle::get_n(PrimaryTracks)")

               # number of tracks
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

	       .Define("Z", "selMC_leg(0) (Zmumu_indices, Particle)")
	       .Define("FoundZ", "MCParticle::get_n( Z )")             

	       .Define("mu1", "selMC_leg(1) (Zmumu_indices, Particle)")
           .Define("mu2", "selMC_leg(2) (Zmumu_indices, Particle)")

               .Define("mu2", "selMC_leg(2) (Zmumu_indices, Particle)")
           .Define("mu1_theta", "MCParticle::get_theta( mu1 )")
           .Define("mu2_theta", "MCParticle::get_theta( mu2 )")
               .Define("mu1_theta", "MCParticle::get_theta( mu1 )")
               .Define("mu2_theta", "MCParticle::get_theta( mu2 )")

               .Define("ZRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Zmumu_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("ZTracks",  "ReconstructedParticle2Track::getRP2TRK( ZRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Ds vertex
               .Define("n_ZTracks", "ReconstructedParticle2Track::getTK_n( ZTracks )")

               # Reco'ed vertex of the Kstar  ( = reco'ed decay vertex of the Bd from the K+ and Pi- tracks only)
               .Define("ZVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 2, ZTracks, true, 4.5, 20e-3, 300)" )
               .Define("ZVertex",  "VertexingUtils::get_VertexData( ZVertexObject )")

               # MC production vertex of the Kstar ( = MC decay vertex ot th Bd, = MC decay vertex of the Kstar)
               .Define("ZMCDecayVertex", " MCParticle::get_vertex( Z )")
               # alternatively, one could use this, which returns a Vector3d instead of a vector of Vector3d:
               # .Define("KstMCDecayVertex", " if ( Kstar.size() > 0) return Kstar[0].vertex; else return  edm4hep::Vector3d(1e12, 1e12, 1e12) ; ")
	       

	       ### Vertexing 

               # Reconstruct the vertex from these primary tracks :
               .Define("VertexObject_primaryTracks",  "VertexFitterSimple::VertexFitter ( 1, PrimaryTracks, EFlowTrack_1) ")
               .Define("Vertex_primaryTracks",   "VertexingUtils::get_VertexData( VertexObject_primaryTracks )")   # primary vertex, in mm

               # Idem, but adding the beam-spot constraint to the vertex fitter
                  # At the Z peak, the beam-spot size is ( 4.5 mum, 20 nm, 0.3 mm)
                  # The beam-spot dimensions are passed in mum :
               .Define("VertexObject_primaryTracks_BSC",  "VertexFitterSimple::VertexFitter ( 1, PrimaryTracks, EFlowTrack_1, true, 4.5, 20e-3, 300) ")
               .Define("Vertex_primaryTracks_BSC",   "VertexingUtils::get_VertexData( VertexObject_primaryTracks_BSC )")   # primary vertex, in mm


               #Run the Acts AMVF vertex finder
               .Define("VertexObject_actsFinder","VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               .Define("Vertex_actsFinder",   "VertexingUtils::get_VertexData( VertexObject_actsFinder )")   # primary vertex, in mm
#               .Define("nPrimaryTracks_actsFinder", "VertexingUtils::get_VertexNtrk(VertexObject_actsFinder)")

               #Run the Acts full Billoir vertex fitter
               .Define("VertexObject_primaryTracks_actsFitter","VertexFitterActs::VertexFitterFullBilloir(PrimaryTracks, EFlowTrack_1)")
               .Define("Vertex_primaryTracks_actsFitter", "VertexingUtils::get_VertexData( VertexObject_primaryTracks_actsFitter )")   # primary vertex, in mm



        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                "nPrimaryTracks",
                "Vertex_primaryTracks",     
                "Vertex_primaryTracks_BSC",    
		"FoundZ", 
		"Z_theta",
		"mu1_theta",
		"mu2_theta",
		"ZMCDecayVertex",
		"n_ZTracks",
		"ZVertex",

                #"nPrimaryTracks_actsFinder",
		#
                # commented out temporarily, very slow !?
                #
                #"Vertex_actsFinder",     # on Zuds: both track selections lead to very similar results for the vertex
                #"Vertex_primaryTracks_actsFitter",     # on Zuds: both track selections lead to very similar results for the vertex


                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
