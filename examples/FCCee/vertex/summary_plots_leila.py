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

    colors_L=[1,2,6,8,4,4]
    markers_L=[20,21,24,47,22,26]

    gStyle.SetTitleSize(size=0.05, axis="X") #actually works, just for the plot after it. (axis title sizes)
    gStyle.SetTitleSize(size=0.05, axis="Y")
    gStyle.SetTitleOffset(offset=0.83, axis="Y")
    gStyle.SetTitleOffset(offset=0.95, axis="X")


    # mom transverse

    stack = THStack("hs",";|cos(#theta)|; MC Transverse Momentum [GeV]")
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
            hist = TProfile(f.Get("h_slices_momt"))
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

    cmomt = TCanvas("cmomt","cmomt")
    stack.SetMaximum(70)
    stack.SetMinimum(0.0)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.16,0.65,0.4,0.88,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    cmomt.SaveAs(outDir + "/" + "D0_mom_transverse_comparison.pdf")
    cmomt.Write()
    cmomt.Close()

    # mom

    stack = THStack("hs",";|cos(#theta)|; MC Momentum [GeV]")
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
            hist = TProfile(f.Get("h_slices_mom"))
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

    cmom = TCanvas("cmom","cmom")
    stack.SetMaximum(60)
    stack.SetMinimum(20.0)
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
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    cmom.SaveAs(outDir + "/" + "D0_mom_comparison.pdf")
    cmom.Write()
    cmom.Close()



    # D0
    stack = THStack("hs",";#theta [degrees]; \sigma_{D_{0}} [\mum]")
#    stack = THStack("hs",";cos(#theta); \sigma_{D_{0}} [\mum]")
#    stack = THStack("hs",";|cos(#theta)|; \sigma_{D_{0}} [\mum]")

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

            print(name)

            #want to fit each TProfile with a fit function to extract params a and b
#            f1 = TF1("f1","[0]+[1]/([2]*pow(sin(x*pi/180),3/2))",8,90)
#            f1 = TF1("f1","pow(pow([0],2)+pow([1],2)/(pow([2],2)*pow(sin(x*pi/180),3)),1/2)",8,90)
            f1 = TF1("f1","TMath::Sqrt(pow([0],2)+pow([1],2)/(pow([2],2)*pow(sin(x*pi/180),3)))",8,90)

            #set inital parameters
            f1.SetParameter(0,3) #param a should be around 3
            f1.SetParLimits(0,0.5,10) #0.5, 10
            f1.SetParameter(1,20) #param b should be around 15
            f1.SetParLimits(1,10,50) #10,50
            f1.SetParameter(2,44.44) #setting the momentum parameter to the momentum
            f1.SetParLimits(2,44.44-4.209,44.44+4.209) #fixing the momentum parameter

            f1.SetLineColor(colors_1[i])
            f1.SetLineWidth(1)
            f1.SetLineStyle(2)
            hist.Fit("f1")

            #print(f1.Eval(20))

            stack.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")

    f1.Draw()

    stack.SetMaximum(7.0) #last point is out of range
    stack.SetMinimum(1.0)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04) 
    gStyle.SetLegendTextSize(0.037)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()

    gPad.BuildLegend(0.21,0.61,0.4,0.88,"")

    leg = TLegend(0.23,0.55,0.4,0.61)
    f1.SetLineColor(1)
#    leg.AddEntry(f1,"fit function = (a^{2} + b^{2}/(p^{2} sin^{3}(#theta)))^{1/2}", "L")
    leg.AddEntry(f1,"fit function = a #oplus b/(p sin^{3/2}(#theta))", "L")
 
    leg.Draw("same")
    leg.SetFillStyle(0)

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")

    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison.pdf")
    c1.Write()
    c1.Close()




    # D0 comparison without disks
    stack_nodisks = THStack("hs_nodisks",";#theta [degrees]; \sigma_{D_{0}} [\mum]")
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
    stack_nodisks.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack_nodisks.GetYaxis().SetLabelSize(0.04)
    gPad.BuildLegend(0.12,0.61,0.36,0.88,"") #x1 y1 x2 y2 coordinates of legend


    #AddText(0.5,0.5,"IDEA Delphes Simulation")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison_nodisks.pdf")
    c1.Write()
    c1.Close()


    # D0 comparison WITH disks
    stack_disks = THStack("hs_disks",";#theta [degrees]; \sigma_{D_{0}} [\mum]")
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
            #hist.SetMinimum(1.5) #have to set individ hist minimum to >0 for log scale to work
            hists.append(hist)

       	    print(name)

            #want to fit each TProfile with a fit function to extract params a and b
            f1 = TF1("f1","TMath::Sqrt(pow([0],2)+pow([1],2)/(pow([2],2)*pow(sin(x*pi/180),3)))",8,90)

            #set inital parameters
            f1.SetParameter(0,3) #param a should be around 3
            f1.SetParLimits(0,0.5,10) #0.5, 10
            f1.SetParameter(1,20) #param b should be around 15
            f1.SetParLimits(1,10,50) #10,50
            f1.SetParameter(2,44.44) #setting the momentum parameter to the momentum
            f1.SetParLimits(2,44.44-4.209,44.44+4.209) #fixing the momentum parameter

            f1.SetLineColor(colors_2[i])
            f1.SetLineWidth(1)
            f1.SetLineStyle(2)
            hist.Fit("f1")

            #print(f1.Eval(20))

            stack_disks.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")

    #gStyle.SetPadTickY(1)
    #gPad.SetLogy(1)
    #gPad.Update()
    
    f1.Draw()

    stack_disks.SetMaximum(5.5)
    stack_disks.SetMinimum(1.5)
    stack_disks.Draw("nostack,e1pl")
    stack_disks.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack_disks.GetYaxis().SetLabelSize(0.04)
    
    #stack_disks.GetXaxis().SetMoreLogLabels() #didnt do anything

    gPad.BuildLegend(0.30,0.6,0.45,0.88,"") #x1 y1 x2 y2 coordinates of legend

    leg = TLegend(0.3+0.02,0.6-0.06,0.45,0.88-0.27)
    f1.SetLineColor(1)
    leg.AddEntry(f1,"fit function = a #oplus b/(p sin^{3/2}(#theta))", "L")

    leg.Draw("same")
    leg.SetFillStyle(0)

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
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
    stack = THStack("hs",";#theta [degrees]; \sigma_{Z_{0}} [\mum]")
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

            #want to fit each TProfile with a fit function to extract params a and b
#            f1 = TF1("f1","[0]+[1]/([2]*pow(sin(x*pi/180),3/2))",9,90)
#            f1 = TF1("f1","TMath::Sqrt(pow([0],2)+pow([1],2)/(pow([2],2)*pow(sin(x*pi/180),3)))",8,90)
#            #set inital parameters
#            f1.SetParameter(0,2) #param a should be around 3
#            f1.SetParLimits(0,0.5,10)
#            f1.SetParameter(1,30) #param b should be around 15
#            f1.SetParLimits(1,15,50)
#            f1.SetParameter(2,45) #setting the momentum parameter to the momentum
#            f1.SetParLimits(2,45,45) #fixing the momentum parameter

#            f1.SetLineColor(colors_1[i])
#            f1.SetLineWidth(1)
#            f1.SetLineStyle(2)
#            hist.Fit("f1")

            stack.Add(hist)
            i+=1

    c2 = TCanvas("c2","c2")

#    f1.Draw()

    stack.SetMaximum(30)
    stack.SetMinimum(1)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    gStyle.SetLegendTextSize(0.035)
    #gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.26,0.65,0.4,0.88,"")

#    leg = TLegend(0.28,0.60,0.4,0.65)
#    f1.SetLineColor(1)
#    leg.AddEntry(f1,"fit function = a + b/(p sin^{3/2}(#theta))", "L")
#    leg.AddEntry(f1,"fit function = (a^{2} + b^{2}/(p^{2} sin^{3}(#theta)))^{1/2}", "L")
#    leg.Draw("same")
#    leg.SetFillStyle(0)

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison.pdf")
    c2.Write()
    c2.Close()



    # Z0 comparison without disks
    stack2_nodisks = THStack("hs2_nodisks",";#theta [degrees]; \sigma_{Z_{0}} [\mum]")
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
    stack2_nodisks.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack2_nodisks.GetYaxis().SetLabelSize(0.04)
    gPad.BuildLegend(0.26,0.6,0.45,0.88,"")
    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Z0_comparison_nodisks.pdf")
    c2.Write()
    c2.Close()



    # Z0 comparison WITH disks
    stack_disks = THStack("hs_disks",";#theta [degrees]; \sigma_{Z_{0}} [\mum]")
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
    stack_disks.SetMaximum(25)
    stack_disks.SetMinimum(1.5)
    stack_disks.Draw("nostack,e1pl")
    stack_disks.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack_disks.GetYaxis().SetLabelSize(0.04)
    gStyle.SetLegendTextSize(0.04)
    gPad.BuildLegend(0.30,0.6,0.45,0.88,"") #x1 y1 x2 y2 coordinates of legend

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Z #rightarrow \mu^{+}\mu^{-}}")
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


