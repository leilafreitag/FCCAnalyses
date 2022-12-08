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

def plot_stuff(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)

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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "Bs_FD_reso_comparison.pdf")
    c1.Write()
    c1.Close()



    # SV resol (with no fit) dR_min

    stack = THStack("hs",";cos(#theta); R Distance of closest SV to MC B_{S} vertex [\mum]")
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
            hist = TProfile(f.Get("h_slices_SV_dR_min_nofit"))
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_min.pdf")
    c2.Write()
    c2.Close()



    # SV resol (no fit) with just d_min

    stack = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{S} vertex [\mum]")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_d_min.pdf")
    c2_2.Write()
    c2_2.Close()





    # SV resol (with no fit) dR

    stack = THStack("hs",";cos(#theta); R Distance of SV to MC B_{S} vertex [\mum]")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison.pdf")
    c2.Write()
    c2.Close()



    # SV resol (no fit) with just d

    stack = THStack("hs",";cos(#theta); Distance of SV to MC B_{S} vertex [\mum]")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_d.pdf")
    c2_2.Write()
    c2_2.Close()















    # SV reso with armin's plotting method, TH1D with errors? and fit?
    stack = THStack("hs",";cos(#theta); R Distance of closest SV to MC B_{S} vertex [\mum]")
    hists = list()

    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TH1D(f.Get("h_slicesReco"))
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

    c3 = TCanvas("c3","c3")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c3.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_ver2.pdf")
    c3.Write()
    c3.Close()





    # SV reso with armin's plotting method, TH1D with errors? and fit? again, but this time with absval.
    stack = THStack("hs",";cos(#theta); R Distance of closest SV to MC B_{S} vertex [\mum]")
    hists = list()

    i=0
    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TH1D(f.Get("h_slicesReco_abs"))
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

    c3_2 = TCanvas("c3_2","c3_2")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c3_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_ver2_abs.pdf")
    c3_2.Write()
    c3_2.Close()








    # SV reso with armin's plotting method, but this time with d instead of dR
    stack = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{S} vertex [\mum]")
    hists = list()

    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TH1D(f.Get("h_slicesReco_d"))
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
    c4 = TCanvas("c4","c4")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c4.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_ver2_d.pdf")
    c4.Write()
    c4.Close()


   # SV reso with armin's plotting method, but this time with d instead of dR AND absval method
    stack = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{S} vertex [\mum]")
    hists = list()

    i=0

    for input_file in input_files:
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        if name == "standard" or name =="R1.3" or name =="R1.3_w100" or name =="R1.3_w30" or name=="R1.3_w30_DSK":
            hist = TH1D(f.Get("h_slicesReco_d_abs"))
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
    c4_2 = TCanvas("c4_2","c4_2")
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
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c4_2.SaveAs(outDir + "/" + "Bs_SV_reso_comparison_ver2_d_abs.pdf")
    c4_2.Write()
    c4_2.Close()






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


