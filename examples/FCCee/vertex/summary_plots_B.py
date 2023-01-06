import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,THStack,TH1,TPaveText,TText
import math

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
    elif name == "FullSilicon": new_name = "Full Silicon"
    else: new_name = name
    return new_name

def change(old,new): #returns the percent change of a point
    x1=old
    x2=new
    return (x2-x1)/abs(x1)*100

def change_error(old,new,err_old,err_new): #returns the error of the percent change of a single point
    x1=old
    x2=new
    partial_old = -100*x2/(x1*abs(x1))
    partial_new = 100/(abs(x1))
    return math.sqrt((partial_old**2)*(err_old**2) + (partial_new**2)*(err_new**2))

def avg(l): #returns the average of a list
    return sum(l)/len(l)

def avg_error(l, err_l): #returns the propagated error for averaging the list. given the list and the list of errors
    length = len(l)
    errors_squared = [x**2 for x in err_l]
    temp = math.sqrt(sum(errors_squared))
    return temp/length

def calc_percent_change(vals_old, vals_new, errs_old, errs_new):

    #calc the percent change for each of the bins
    diff = [change(x1,x2) for x1, x2 in zip(vals_old, vals_new)]

    #calc the error on the percent change for each bin        
    err_diff = [change_error(x1,x2,err1,err2) for x1,x2,err1,err2 in zip(vals_old,vals_new,errs_old,errs_new)]

    #calc the average percent change over all the bins
    avg_diff = avg(diff)

    #calc the error on the average percent change
    err_avg_diff = avg_error(diff,err_diff)

    return avg_diff, err_avg_diff

def plot_stuff(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)


    # FD resol for standard - compare with and without using reconstructed primary vertex
    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[94,1,8,4,4]
    markers_1=[21,20,47,22,26]
    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard":
            hist = TProfile(f.Get("h_slices_FD"))
            hist.SetName(name)
            hist.SetTitle("Standard IDEA: Using PV = origin")
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

            hist = TProfile(f.Get("h_slices_FD_adjusted_for_Reco_PV"))
            hist.SetName(name)
            hist.SetTitle("Standard IDEA: Using PV = reconstructed PV")
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)              
            stack.Add(hist)
            i+=1

    cs = TCanvas("cs","cs")
    stack.SetMaximum(25)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #gStyle.SetTitleSize(0.02, axis="X") #not working, doesnt change anything
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.04)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.16,0.75,0.4,0.87,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    cs.SaveAs(outDir + "/" + "Bs_FD_reso_standard_comparison_PV.pdf")
    cs.Write()
    cs.Close()





    # FD resol    

    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
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
            hist = TProfile(f.Get("h_slices_FD"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")
    stack.SetMaximum(25)
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "Bs_FD_reso_comparison_1.pdf")
    c1.Write()
    c1.Close()



  # FD resol more realistic (adjusted for reconstructed PV, not assuming 0 with smearing anymore. but still assuming we know exactly which track to take)

    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
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
            hist = TProfile(f.Get("h_slices_FD_adjusted_for_Reco_PV"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c1_2 = TCanvas("c1_2","c1_2")
    stack.SetMaximum(25)
    stack.SetMinimum(0)
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
#    tt.SetTextSize(0.035)
#    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1_2.SaveAs(outDir + "/" + "Bs_FD_reso_comparison_2_from_reco_PV.pdf")
    c1_2.Write()
    c1_2.Close()




    # FD resol (with no fit) dR_min

    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[1,2,8,4,4]
    markers_1=[20,21,47,22,26]
    i=0

    vals_R13, vals_R13_w30, vals_R13_w30_DSK, vals_R13_w100 = [],[],[],[]
    errs_R13,errs_R13_w30,errs_R13_w30_DSK,errs_R13_w100 = [],[],[],[]

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TProfile(f.Get("h_slices_SV_dR_min_nofit"))

            #Getting the numbers for percent improvement calculation
            for bin in range(1,11):
                print(name, bin, hist.GetBinContent(bin), hist.GetBinError(bin))
                if name == "R1.3":
                    vals_R13.append(hist.GetBinContent(bin))
                    errs_R13.append(hist.GetBinError(bin))
                if name == "R1.3_w30": 
                    vals_R13_w30.append(hist.GetBinContent(bin))
       	       	    errs_R13_w30.append(hist.GetBinError(bin))
                if name == "R1.3_w30_DSK": 
                    vals_R13_w30_DSK.append(hist.GetBinContent(bin))
       	       	    errs_R13_w30_DSK.append(hist.GetBinError(bin))
                if name == "R1.3_w100":
                    vals_R13_w100.append(hist.GetBinContent(bin))
                    errs_R13_w100.append(hist.GetBinError(bin))

            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    #Calc average percent changes

    print("average percent change of FD reso from R1.3 to w100:", calc_percent_change(vals_R13,vals_R13_w100,errs_R13,errs_R13_w100)[0], \
      "with error", calc_percent_change(vals_R13,vals_R13_w100,errs_R13,errs_R13_w100)[1])

    print("average percent change of FD reso from R1.3 to w30:", calc_percent_change(vals_R13,vals_R13_w30,errs_R13,errs_R13_w30)[0], \
      "with error", calc_percent_change(vals_R13,vals_R13_w30,errs_R13,errs_R13_w30)[1])

    print("average percent change of FD reso from R1.3 to w30_DSK:", calc_percent_change(vals_R13,vals_R13_w30_DSK,errs_R13,errs_R13_w30_DSK)[0], \
      "with error", calc_percent_change(vals_R13,vals_R13_w30_DSK,errs_R13,errs_R13_w30_DSK)[1])

    c2 = TCanvas("c2","c2")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Bs_FD_reso_comparison_4_dR_min.pdf")
    c2.Write()
    c2.Close()



    # SV resol (no fit) with just d_min

    stack = THStack("hs",";cos(#theta); Secondary vertex (B_{S}^{0}) resolution [\mum]")
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
            hist = TProfile(f.Get("h_slices_SV_d_min_nofit"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c2_2 = TCanvas("c2_2","c2_2")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_d_min.pdf")
    c2_2.Write()
    c2_2.Close()




    # Comparing Standard IDEA (w/ Drift chamber) to Full Silicon SV resol

    stack = THStack("hs",";cos(#theta);  Secondary vertex (B_{S}^{0}) resolution [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[1,2,8,4,4]
    markers_1=[20,21,47,22,26]
    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="FullSilicon":
            hist = TProfile(f.Get("h_slices_SV_d_min_nofit"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    cfull = TCanvas("cfull","cfull")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #gStyle.SetTitleSize(0.02, axis="X") #not working, doesnt change anything
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.16,0.75,0.4,0.85,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    cfull.SaveAs(outDir + "/" + "Bs_SV_reso_fullsilicon_comparison_d_min.pdf")
    cfull.Write()
    cfull.Close()


    # Comparing Standard IDEA (w/ Drift chamber) to Full Silicon FD Reso

    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
    hists = list()

    colors_all=[1,2,3,3,4,4,6,6]
    markers_all=[20,21,20,4,21,25,22,26]
    colors_1=[1,2,8,4,4]
    markers_1=[20,21,47,22,26]
    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="FullSilicon":
            hist = TProfile(f.Get("h_slices_FD"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c1 = TCanvas("c1","c1")
    stack.SetMaximum(40)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    stack.GetXaxis().SetLabelSize(0.04) #changes the size of the x axis values
    stack.GetYaxis().SetLabelSize(0.04)
    #gStyle.SetTitleSize(0.02, axis="X") #not working, doesnt change anything
    #stack.GetXaxis().SetTitleSize(0.15)
    #stack.GetYaxis().ChangeLabel(labSize=30)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    #gStyle.SetLegendFillColor()
    gPad.BuildLegend(0.16,0.75,0.4,0.85,"")

    tt=TLatex()
    tt.SetTextSize(0.04)
    tt.DrawLatexNDC(0.58,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "Bs_FD_reso_fullsilicon_comparison.pdf")
    c1.Write()
    c1.Close()

























    # FD resol (with no fit) dR


    stack = THStack("hs",";cos(#theta); Flight distance resolution (|R_{reco}-R_{MC}|) [\mum]")
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
            hist = TProfile(f.Get("h_slices_SV_dR_nofit"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c2 = TCanvas("c2","c2")
    stack.SetMaximum(70)
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Bs_FD_reso_comparison_3_dR.pdf")
    c2.Write()
    c2.Close()



    # SV resol (no fit) with just d

    stack = THStack("hs",";cos(#theta); Secondary vertex (B_{S}^{0}) resolution [\mum]")
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
            hist = TProfile(f.Get("h_slices_SV_d_nofit"))
            hist.SetName(name)
            hist.SetTitle(name_for_legend(name))
            hist.SetMarkerColor(colors_1[i])
            hist.SetMarkerStyle(markers_1[i])
            hist.SetLineColor(colors_1[i])
            #hist.SetLineStyle(linestyles[i])
            hist.SetLineWidth(1)
            hist.SetMarkerSize(0.7)
            hists.append(hist)
            stack.Add(hist)
            i+=1

    c2_2 = TCanvas("c2_2","c2_2")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_d.pdf")
    c2_2.Write()
    c2_2.Close()




    # momentum of Bs? h_slices_mom
    
    stack = THStack("hs",";cos(#theta); MC Bs Energy [GeV]")
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
    stack.SetMinimum(0)
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
    tt.DrawLatexNDC(0.14,0.915,"#bf{B_{s}^{0} #rightarrow J/#psi #rightarrow #mu^{+} #mu^{-} K^{+} K^{-}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    cmom.SaveAs(outDir + "/" + "Bs_mom_comparison.pdf")
    cmom.Write()
    cmom.Close()







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

    if args.analysis=="stuff":
        process_name="evtGen_ecm91_Bs2JpsiPhi_"
        plot_stuff(outDir,args.input_files,process_name)


