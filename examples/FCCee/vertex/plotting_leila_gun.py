import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,TPaveStats,TGraph, TGraphErrors
from array import array

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


    gStyle.SetStatW(0.38)
    gStyle.SetStatH(0.2)
    gStyle.SetLabelSize(0.05,"xy") #0.035
    gStyle.SetTitleSize(0.05,"xy")
    gStyle.SetTitleSize(0.067,"xy")
    gStyle.SetOptStat("rme")

    cleila1 = TCanvas("RP_TRK_D0","RP_TRK_D0",0,0,600,500)
    #cleila1.Divide(2,1)
    cleila1.SetLeftMargin(0.12)
    cleila1.SetBottomMargin(0.16)
    #cleila1.cd(1)
    h1 = TH1F("h1", ";d_{0} [\mum]",100,-50,50)
    events.Draw("1e3*RP_TRK_D0>>h1","TMath::Abs(RP_TRK_D0)<0.1")
    cleila1.SaveAs(outDir + "/" + "RP_TRK_D0_leila.pdf")
    cleila1.Write()

    cleila1 = TCanvas("RP_TRK_D0","RP_TRK_D0",0,0,600,500)
    cleila1.SetLeftMargin(0.12)
    cleila1.SetBottomMargin(0.16)
    #cleila1.cd(2)
    h1.GetXaxis().SetLabelSize(0.04)
    h1.GetYaxis().SetLabelSize(0.04)
    h2 = TH1F("h2", ";\sigma_{d_{0}} [\mum]",1000,0,3000)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov)>>h2","TMath::Sqrt(RP_TRK_D0_cov) < 1e+1")
#    h2.GetXaxis().SetLabelSize(0.05)
#    h2.GetYaxis().SetLabelSize(0.05)
    cleila1.SaveAs(outDir + "/" + "RP_TRK_sig_D0_leila.pdf")
    cleila1.Write()



   # cleila1 = TCanvas("RP_TRK_D0","RP_TRK_D0")
   # cleila1.Divide(2,1)
   # cleila1.cd(1)
   # h1 = TH1F("h1", "RP_TRK_D0;d_{0} [\mum]",100,-50,50)
   # events.Draw("1e3*RP_TRK_D0>>h1","TMath::Abs(RP_TRK_D0)<0.1")
   # cleila1.cd(2)
   # h2 = TH1F("h2", "Sqrt(RP_TRK_D0_cov);\sigma_{d_{0}} [\mum]",1000,0,1000)
   # events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov)>>h2","TMath::Sqrt(RP_TRK_D0_cov) < 1e+1")
   # cleila1.SaveAs(outDir + "/" + "RP_TRK_D0_leila.pdf")
   # cleila1.Write()


    #Average D0 resolution vs theta data point, for comparison with other in summary plots
    p = TProfile("p", "Sqrt(RP_TRK_D0_cov) vs. |#theta|", 10000, 5, 95, 1, 1000) 
    events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov):TMath::Abs(RP_theta*180/TMath::Pi())>>p")
    p.SetMaximum(10)
    p.SetMinimum(1.000)
    #gPad.SetLogy() #doesnt do anything to the data points that are in h slices i think
    #gPad.Update()
    p.SetName("h_slices_D0")
    p.Write()
    
    #THE IMPORTANT PART: NOW USING A TGraph :D
    angle = float(outDir.split("_")[-2].split("degrees")[0])
    mean = h2.GetMean()
    error = h2.GetRMS()
    
    n=1
    x, y, ex, ey = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
    for i in range(n):
        x.append(angle)
        y.append(mean)
        ey.append(error)
        ex.append(0)

    #print(angle, type(angle))
    #print(x, type(x))
    #print(mean, type(mean))
    #print(y, type(y))
    g = TGraphErrors(n,x,y,ex,ey)
    g.SetMaximum(10)
    g.SetMinimum(1.000)
    g.SetName("h_slices_D0_graph")
    g.Draw()
    g.Write()


    # Z0 :
    cleila = TCanvas("RP_TRK_Z0","RP_TRK_Z0")
    cleila.Divide(2,1)

    cleila.cd(1)
    h4 = TH1F("h4","RP_TRK_Z0;z_{0} [\mum]",100,-1500,1500)
    events.Draw("1e3*RP_TRK_Z0>>h4")

    cleila.cd(2)
    h5 = TH1F("h5","Sqrt(RP_TRK_Z0_cov);\sigma_{z_{0}} [\mum]",1000,0,3000)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_Z0_cov)>>h5")

    cleila.SaveAs(outDir + "/" + "RP_TRK_Z0_leila.pdf")
    cleila.Write()


    #THE IMPORTANT PART for Z0 now: NOW USING A TGraph :D
    meanZ = h5.GetMean()
    errorZ = h5.GetRMS()

    n=1
    x2, y2, ex2, ey2 = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
    for i in range(n):
        x2.append(angle)
        y2.append(meanZ)
       	ey2.append(errorZ)
       	ex2.append(0)

    g = TGraphErrors(n,x2,y2,ex2,ey2)
    g.SetMaximum(10)
    g.SetMinimum(1.000)
    g.SetName("h_slices_Z0_graph")
    g.Draw()
    g.Write()


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

    

