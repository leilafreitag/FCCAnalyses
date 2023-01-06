import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,THStack,TH1,TPaveText,TText

colors = [1,2,3,4,5,6,7,8]
linestyles = [1,2,3,4,5,6,7,8]


def parse_arguments(argv=None):

        parser = argparse.ArgumentParser()

        # List of input root files
        parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=True)
        parser.add_argument("-a", "--analysis", help="Choose analysis to perform")
        return parser.parse_args(argv)


def name_for_legend(name):
    if name == "standard": new_name = "Standard IDEA: R(Layer_{1}) = 1.7 cm, w(VTX layers) = 280 \mum"
    elif name == "R1.3": new_name = "+ R(Layer_{1}) = 1.3 cm"
    elif name == "R1.3_w30": new_name = "+ w(first 3 VTX layers) = 30 \mum"
    elif name == "R1.3_w50": new_name = "+ w(first 3 VTX layers) = 50 \mum"
    elif name == "R1.3_w100": new_name = "+ w(first 3 VTX layers) = 100 \mum"
    elif name == "R1.3_w30_DSK": new_name = "+ w(8 VTX disc layers) = 30 \mum"
    elif name == "R1.3_w50_DSK": new_name = "+ w(8 VTX disc layers) = 50 \mum"
    elif name == "R1.3_w100_DSK": new_name = "+ w(8 VTX disc layers) = 100 \mum"
    elif name == "R1.3_L1_w30": new_name = "+ w(Layer_{1}) = 30 \mum"
    else: new_name = name
    return new_name

def plot_impact_parameter(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)

    gStyle.SetTitleSize(size=0.05, axis="X") #actually works, just for the plot after it.
    gStyle.SetTitleSize(size=0.05, axis="Y")
    gStyle.SetTitleOffset(offset=0.83, axis="Y")
    gStyle.SetTitleOffset(offset=0.95, axis="X")

    # D0 with L1
    stack = THStack("hs",";cos(#theta); \sigma_{D0} [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[1,2,8,4,4]
    markers_1=[20,21,47,22,26]
    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name == "R1.3_L1_w30" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TProfile(f.Get("h_slices_D0"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c1l = TCanvas("c1l","c1l")
    stack.SetMaximum(4.0) #last point is out of range
    stack.SetMinimum(1.5)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.04)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.12,0.61,0.36,0.88,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1l.SaveAs(outDir + "/" + "D0_comparison_L1.pdf")
    c1l.Write()
    c1l.Close()


    # Z0
    stack = THStack("hs",";cos(#theta); \sigma_{Z0} [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[1,2,8,4,4]
    markers_1=[20,21,47,22,26]
    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_L1_w30" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TProfile(f.Get("h_slices_Z0"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c2 = TCanvas("c2","c2")
    stack.SetMaximum(7.0)
    stack.SetMinimum(1.5)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #gStyle.SetTitleSize(0.02, axis="X") #not working, doesnt change anything
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.25,0.65,0.4,0.88,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison_L1.pdf")
    c2.Write()
    c2.Close()


if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetTitleSize(0.045,"x")
    gStyle.SetTitleSize(0.045,"y")
    gStyle.SetLabelSize(0.04)

    # Argument parsing
    args = parse_arguments(sys.argv[1:])

    #Summary comparison plots
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'+"comparison_plots"
    os.system("mkdir -p {}".format(outDir))

    gROOT.Reset()

    if args.analysis=="impact_parameter":
        process_name="Zmumu_ecm91_"
        plot_impact_parameter(outDir,args.input_files,process_name)


