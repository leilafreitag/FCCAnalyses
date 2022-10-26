import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,TPaveStats

def parse_arguments(argv=None):

        parser = argparse.ArgumentParser()

        # List of input root files
        parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=True)
        parser.add_argument("-a", "--analysis", help="Choose analysis to perform")
        return parser.parse_args(argv)

def plot_raw(outDir):
    # D0 :

    #Histogram of D0
    c_D0 = TCanvas("testname","testtitle")
    h_D0 = TH1F("h_D0", "Transverse impact parameter D_{0};D_{0} [\mum]",100,-50,50) #name,title,numbins,bounds?
    events.Draw("1e3*RP_TRK_D0>>h_D0","TMath::Abs(RP_TRK_D0)<0.1")
    #s = (TPaveStats)h_D0.GetListOfFunctions().FindObject("stats");
    #s.SetX1NDC(.1);
    #s.SetX2NDC(.6);


    c_D0.SaveAs(outDir + "/" + "D0_histogram.pdf")
    c_D0.Write()

    #cleila1 = TCanvas("RP_TRK_D0","RP_TRK_D0")
    #cleila1.Divide(2,1)
    #cleila1.cd(1)
    #h1 = TH1F("h1", "RP_TRK_D0;D0 [\mum]",100,-50,50)
    #events.Draw("1e3*RP_TRK_D0>>h1","TMath::Abs(RP_TRK_D0)<0.1")
    #cleila1.cd(2)
    #h2 = TH1F("h2", "Sqrt(RP_TRK_D0_cov);\sigma_{D0} [\mum]",100,0,10)
    #events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov)>>h2","TMath::Sqrt(RP_TRK_D0_cov) < 1e+1")
    #cleila1.SaveAs(outDir + "/" + "RP_TRK_D0_leila.pdf")
    #cleila1.Write()


    c1 = TCanvas("RP_TRK_D0","RP_TRK_D0")
    c1.Divide(4,1)

    c1.cd(1)
    h1 = TH1F("h1", "RP_TRK_D0",100,-50,50)
    events.Draw("1e3*RP_TRK_D0>>h1","TMath::Abs(RP_TRK_D0)<0.1")

    c1.cd(2)
    h2 = TH1F("h2", "Sqrt(RP_TRK_D0_cov)",100,0,10)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov)>>h2","TMath::Sqrt(RP_TRK_D0_cov) < 1e+1")

    c1.cd(3)
    h3 = TH1F("h3", "RP_TRK_D0 / TMath::Sqrt(RP_TRK_D0_cov)",100,-5,5)
    events.Draw("RP_TRK_D0 / TMath::Sqrt(RP_TRK_D0_cov)>>h3")  # sigma = 1 as it should

    c1.cd(4)
    hD02D = TProfile("hD02D", "Sqrt(RP_TRK_D0_cov) vs. |cos(#theta)|", 20, 0, 1, 0, 20)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov):TMath::Abs(TMath::Cos(RP_theta))>>hD02D")
    hD02D.SetMaximum(10)
    hD02D.SetMinimum(0.000)
    #hD02D.GetXaxis().SetRangeUser(0,1.2)
    hD02D.SetName("h_slices_D0")
    hD02D.Write()

    c1.SaveAs(outDir + "/" + "RP_TRK_D0.pdf")
    c1.Write()

    hD02D_zoom = TProfile("hD02D_zoom", "Sqrt(RP_TRK_Z0_cov) vs. |cos(#theta)|", 20, 0.9, 1, 0, 100)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov):TMath::Abs(TMath::Cos(RP_theta))>>hD02D_zoom")
    hD02D_zoom.SetName("h_slices_D0_zoom")
    hD02D_zoom.Write()


    # Z0 :
    cleila = TCanvas("RP_TRK_Z0","RP_TRK_Z0")
    cleila.Divide(2,1)

    cleila.cd(1)
    h4 = TH1F("h4","RP_TRK_Z0;Z0 [\mum]",100,-1500,1500)
    events.Draw("1e3*RP_TRK_Z0>>h4")

    cleila.cd(2)
    h5 = TH1F("h5","Sqrt(RP_TRK_Z0_cov);\sigma_{Z0} [\mum]",100,0,30)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov)>>h5")

    cleila.SaveAs(outDir + "/" + "RP_TRK_Z0_leila.pdf")
    cleila.Write()


    c2 = TCanvas("RP_TRK_Z0","RP_TRK_Z0")
    c2.Divide(4,1)

    c2.cd(1)
    h4 = TH1F("h4","RP_TRK_Z0",100,-1500,1500)
    events.Draw("1e3*RP_TRK_Z0>>h4")
    h4.Fit("gaus")

    c2.cd(2)
    h5 = TH1F("h5","Sqrt(RP_TRK_Z0_cov)",50,0,50)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov)>>h5")

    c2.cd(3)
    h6 = TH1F("h6","RP_TRK_Z0 / TMath::Sqrt(RP_TRK_Z0_cov)",100,-10,10)
    events.Draw("RP_TRK_Z0 / TMath::Sqrt(RP_TRK_Z0_cov)>>h6")

    c2.cd(4)
    hZ02D = TProfile("hZ02D", "Sqrt(RP_TRK_Z0_cov) vs. |cos(#theta)|", 20, 0, 1, 0, 20)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov):TMath::Abs(TMath::Cos(RP_theta))>>hZ02D")
    hZ02D.SetMaximum(20)
    hZ02D.SetMinimum(0.000)
    hZ02D.SetName("h_slices_Z0")
    hZ02D.Write()

    c2.SaveAs(outDir + "/" + "RP_TRK_Z0.pdf")
    c2.Write()
    hZ02D_zoom = TProfile("hZ02D_zoom", "Sqrt(RP_TRK_Z0_cov) vs. |cos(#theta)|", 20, 0.9, 1, 0, 100)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov):TMath::Abs(TMath::Cos(RP_theta))>>hZ02D_zoom")
    hZ02D_zoom.SetName("h_slices_Z0_zoom")
    hZ02D_zoom.Write()

    # matching between the reco'ed particles and the MC-matched : Phi
    c3 = TCanvas("Reco-MC matching in Phi","Reco-MC matching in Phi")
    c3.Divide(2,1)

    c3.cd(1)
    events.Draw("RP_TRK_phi:RP_MC_tlv.Phi()")

    c3.cd(2)
    events.Draw("(RP_TRK_phi-RP_MC_tlv.Phi())/TMath::Sqrt(RP_TRK_phi_cov)")

    c3.SaveAs(outDir + "/" + "RP_TRK_phi.pdf")
    c3.Write()

    # matching between the reco'ed particles and the MC-matched : Tan Lambda
    c4 = TCanvas("Reco-MC matching in tan(lambda)","Reco-MC matching in tan(lambda)")
    c4.Divide(2,1)

    c4.cd(1)
    events.Draw("RP_TRK_tanlambda:1./TMath::Tan(RP_MC_tlv.Theta())")  # tan(lambda) = cotan(theta)

    c4.cd(2)
    events.Draw("( RP_TRK_tanlambda - 1./TMath::Tan(RP_MC_tlv.Theta()) ) / TMath::Sqrt( RP_TRK_tanlambda_cov) ")  # OK

    c4.SaveAs(outDir + "/" + "RP_TRK_tanlambda.pdf")
    c4.Write()

    # compare pT of the MC particle with the curvature of the track :
    # pT (GeV) = 0.3 * B ( Tesla ) / rho (m)
    c5 = TCanvas("compare pT of the MC particle with the curvature of the track", "compare pT of the MC particle with the curvature of the track")
    c5.Divide(3,1)

    c5.cd(1)
    events.Draw("1e-3 * 0.3*2*TMath::Abs(1./RP_TRK_omega):RP_MC_tlv.Pt()")

    c5.cd(2)
    events.Draw("TMath::Abs(RP_TRK_omega) :1e-3*0.3*2*(1./RP_MC_tlv.Pt()) "," 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) < 0.0009")

    c5.cd(3)
    events.Draw(" ( TMath::Abs(RP_TRK_omega) - 1e-3*0.3*2*(1./RP_MC_tlv.Pt()) ) / TMath::Sqrt( RP_TRK_omega_cov)")

    c5.SaveAs(outDir + "/" + "curvature.pdf")
    c5.Write()

    c6 = TCanvas("Angular distribution", "Angular distribution")
    events.Draw("TMath::Abs(TMath::Cos(RP_theta))")
    c6.SaveAs(outDir + "/" + "cosTheta.pdf")
    c6.Write()


if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetTitleSize(0.045,"x")
    gStyle.SetTitleSize(0.045,"y")
    gStyle.SetLabelSize(0.04)

    # Argument parsing
    args = parse_arguments(sys.argv[1:])


    #Individual plots
    for input_file in args.input_files:
        print("Working on file " + input_file)
        outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'+input_file.split('/')[-1].split(".root")[0] + "_plots"
        os.system("mkdir -p {}".format(outDir))

        gROOT.Reset()

        f = TFile(input_file, "READ")
        events = f.Get("events")

        outfile = outDir+ "/plots.root"
        outf=TFile.Open(outfile,"RECREATE")

        plot_raw(outDir)

        outf.Close()


