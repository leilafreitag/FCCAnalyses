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
    else: new_name = name
    return new_name

def plot_impact_parameter(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)

    # D0
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
        if name	== "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
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

    c1 = TCanvas("c1","c1")
    stack.SetMaximum(4.0) #last point is out of range
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
    gPad.BuildLegend(0.16,0.65,0.4,0.88,"")
    
    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison.pdf")
    c1.Write()
    c1.Close()

    # D0 comparison without disks
    stack_nodisks = THStack("hs_nodisks",";cos(#theta); \sigma_{D0} [\mum]")
    hists = list()

    colors_2 = [1,2,8,40,4]
    markers_2 = [20,21,47,29,33]
    markers_2 = [20,21,24,25,22]#47
    #markers_2 = [20,20,20,20,20]
    i = 0 

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        legend_name = name_for_legend(name)
        is_disk = name.split("_")[-1] 
        if is_disk != "DSK":
            hist = TProfile(f.Get("h_slices_D0"))
            hist.SetName(name)
            hist.SetTitle(legend_name) #changes the label in the legend
            hist.SetMarkerColor(colors_2[i])
            hist.SetMarkerStyle(markers_2[i])
            hist.SetLineColor(colors_2[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.6)
            hists.append(hist)
            stack_nodisks.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")
    stack_nodisks.SetMaximum(4.5)
    stack_nodisks.SetMinimum(1.75)
    stack_nodisks.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.3,0.88,"") #x1 y1 x2 y2 coordinates of legend

    gStyle.SetLegendTextSize(0.03)
    #AddText(0.5,0.5,"IDEA Delphes Simulation")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison_nodisks.pdf")
    c1.Write()
    c1.Close()


    # D0 comparison WITH disks
    stack_disks = THStack("hs_disks",";cos(#theta); \sigma_{D0} [\mum]")
    hists = list()

    colors_2 = [1,1,2,2,4,4]
    markers_2 = [20,24,21,25,22,26]#47
    #markers_2 = [20,20,20,20,20]
    i = 0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        legend_name = name_for_legend(name)
        if name != "standard" and name !="R1.3":
            hist = TProfile(f.Get("h_slices_D0"))
            hist.SetName(name)
            hist.SetTitle(legend_name) #changes the label in the legend
            hist.SetMarkerColor(colors_2[i])
            hist.SetMarkerStyle(markers_2[i])
            hist.SetLineColor(colors_2[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.6)
            hists.append(hist)
            stack_disks.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")
    stack_disks.SetMaximum(3.2)
    stack_disks.SetMinimum(1.8)
    stack_disks.Draw("nostack,e1pl")
    gPad.BuildLegend(0.30,0.6,0.45,0.88,"") #x1 y1 x2 y2 coordinates of legend

    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison_disks.pdf")
    c1.Write()
    c1.Close()


    # D0 zoom
    stack_zoom = THStack("hs_zoom",";cos(#theta);D_0 resolution (Sqrt(RP_TRK_D0_cov)) (#mum)")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TProfile(f.Get("h_slices_D0_zoom"))
        hist.SetName(name)
        hist.SetTitle(name)
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack_zoom.Add(hist)

    c1_zoom = TCanvas("c1_zoom","c1_zoom")
    stack_zoom.SetMaximum(80)
    stack_zoom.SetMinimum(0)
    stack_zoom.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1_zoom.SaveAs(outDir + "/" + "D0_comparison_zoom.pdf")
    c1_zoom.Write()
    c1_zoom.Close()



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
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison.pdf")
    c2.Write()
    c2.Close()



    # Z0 comparison without disks
    stack2_nodisks = THStack("hs2_nodisks",";cos(#theta); \sigma_{Z0} [\mum]")
    hists = list()

    colors_2 = [1,2,8,40,4]
    markers_2 = [20,21,47,29,33]
    markers_2 = [20,21,24,25,22]#47
    i = 0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        legend_name = name_for_legend(name)
        is_disk = name.split("_")[-1]
        if is_disk != "DSK":
            hist = TProfile(f.Get("h_slices_Z0"))
            hist.SetName(name)
            hist.SetTitle(legend_name) #changes the label in the legend
            hist.SetMarkerColor(colors_2[i])
            hist.SetMarkerStyle(markers_2[i])
            hist.SetLineColor(colors_2[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.6)
            hists.append(hist)
            stack2_nodisks.Add(hist)
            i+=1

    c2 = TCanvas("c2","c2")
    stack2_nodisks.SetMaximum(7)
    stack2_nodisks.SetMinimum(1.5)
    stack2_nodisks.Draw("nostack,e1pl")
    gPad.BuildLegend(0.26,0.6,0.45,0.88,"")
    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison_nodisks.pdf")
    c2.Write()
    c2.Close()



    # Z0 comparison WITH disks
    stack_disks = THStack("hs_disks",";cos(#theta); \sigma_{Z0} [\mum]")
    hists = list()

    colors_2 = [1,1,2,2,4,4]
    markers_2 = [20,24,21,25,22,26]#47
    #markers_2 = [20,20,20,20,20]
    i = 0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        legend_name = name_for_legend(name)
        if name != "standard" and name !="R1.3":
            hist = TProfile(f.Get("h_slices_Z0"))
            hist.SetName(name)
            hist.SetTitle(legend_name) #changes the label in the legend
            hist.SetMarkerColor(colors_2[i])
            hist.SetMarkerStyle(markers_2[i])
            hist.SetLineColor(colors_2[i])
            hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(0)
            hist.SetMarkerSize(0.6)
            hists.append(hist)
            stack_disks.Add(hist)
            i+=1

    c2 = TCanvas("c2","c2")
    stack_disks.SetMaximum(7)
    stack_disks.SetMinimum(1.5)
    stack_disks.Draw("nostack,e1pl")
    gPad.BuildLegend(0.30,0.6,0.45,0.88,"") #x1 y1 x2 y2 coordinates of legend

    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison_disks.pdf")
    c2.Write()
    c2.Close()



    # Z0 zoom
    stack2_zoom = THStack("hs2_zoom",";cos(#theta);Z_0 resolution (Sqrt(RP_TRK_Z0_cov)) (#mum)")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TProfile(f.Get("h_slices_Z0_zoom"))
        hist.SetName(name)
        hist.SetTitle(name)
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack2_zoom.Add(hist)

    c2_zoom = TCanvas("c2_zoom","c2_zoom")
    stack2_zoom.SetMaximum(100)
    stack2_zoom.SetMinimum(0)
    stack2_zoom.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_zoom.SaveAs(outDir + "/" + "Z0_comparison_zoom.pdf")
    c2_zoom.Write()
    c2_zoom.Close()




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


