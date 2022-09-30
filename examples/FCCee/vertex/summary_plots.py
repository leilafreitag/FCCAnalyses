import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,THStack,TH1

colors = [1,2,3,4,5,6,7]
linestyles = [1,2,3,4,5,6,7]

def parse_arguments(argv=None):
    
	parser = argparse.ArgumentParser()

	# List of input root files
	parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=True) 
	parser.add_argument("-a", "--analysis", help="Choose analysis to perform")
	return parser.parse_args(argv)

def fit_function():

	# Double gauss
#	ff = TF1("ff","[0]*exp(-0.5*((x-[1])/[2])**2) + [3]*exp(-0.5*((x-[1])/[4])**2)",-200,200)
#	ff.SetParameters(500,0,20,200,0,50)
#	ff.SetParLimits(0,0,10000)
#	ff.SetParLimits(1,-10,10)
#	ff.SetParLimits(2,3,80)
#	ff.SetParLimits(3,0,10000)
#	ff.SetParLimits(4,5,200)
	
	# Double crystal ball function with shared sigma and mean value
	ff = TF1("ff","[6]*(ROOT::Math::crystalball_function(x, [0], [1], [2], [3]) + [7]*ROOT::Math::crystalball_function(x, [4], [5], [2], [3]))",-100,100);
	ff.SetParLimits(0,0.0,5)					# alpha_L
	ff.SetParLimits(1,0.0,200.0)				# n_L
	ff.SetParLimits(2,5.0,100.0)				# sigma
	ff.SetParLimits(3,-10.0,10.0)				# mu
	ff.SetParLimits(4,-5.0,0.0)					# alpha_R
	ff.SetParLimits(5,0.0,200.0)				# n_R
	ff.SetParLimits(6,0,10000.0)				# scale
	ff.SetParLimits(7,0.0,1.0)					# frac
	ff.SetParameters(0.2,10,40,0,-0.2,10,200,0.5)

	return ff




def plot_impact_parameter(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)

    # D0
    stack = THStack("hs",";cos(#theta);D_0 resolution (Sqrt(RP_TRK_D0_cov)) (#mum)")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TProfile(f.Get("h_slices_D0"))
        hist.SetName(name)
        hist.SetTitle(name)
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack.Add(hist)

    c1 = TCanvas("c1","c1")
    stack.SetMaximum(7)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "D0_comparison.pdf")
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
    stack2 = THStack("hs2",";cos(#theta);Z_0 resolution (Sqrt(RP_TRK_Z0_cov)) (#mum)")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TProfile(f.Get("h_slices_Z0"))
        hist.SetName(name)
        hist.SetTitle(name)
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack2.Add(hist)

    c2 = TCanvas("c2","c2")
    stack2.SetMaximum(16)
    stack2.SetMinimum(0)
    stack2.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")
    
    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")
    
    c2.SaveAs(outDir + "/" + "Z0_comparison.pdf")
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


def plot(outDir,input_files,process_name):

    TH1.AddDirectory(False)        
    gStyle.SetErrorX(0)
    
    # cos(theta) 0 - 1
    stack = THStack("hs",";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slices"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack.Add(hist)
  
    c1 = TCanvas("c1","c1")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "vertex_reso_comparison.pdf")
    c1.Write()
    c1.Close()

    # cos(theta) 0.9 - 1
    stack2 = THStack("hs2",";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
    hists2 = list()
    
    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slices_zoom"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerSize(0.6)
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hists2.append(hist)
        stack2.Add(hist)
    
    c2 = TCanvas("c2","c2")
    c2.cd()
    stack2.SetMaximum(80)
    stack2.SetMinimum(0)
    stack2.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "vertex_reso_comparison_zoom.pdf")
    c2.Write()

    # cos(theta) 0.98 - 1
    stack3 = THStack("hs3",";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
    hists3 = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slices_zoom2"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerSize(0.6)
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hists3.append(hist)
        stack3.Add(hist)

    c3 = TCanvas("c3","c3")
    c3.cd()
    stack3.SetMaximum(110)
    stack3.SetMinimum(0)
    stack3.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c3.SaveAs(outDir + "/" + "vertex_reso_comparison_zoom2.pdf")
    c3.Write()

    outf.Close()

def plot_reco_SV(outDir,input_files,process_name):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)


    # cos(theta) 0 - 1
    stack = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
    hists = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slicesReco"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists.append(hist)
        stack.Add(hist)

    c1 = TCanvas("c1","c1")
    stack.SetMaximum(50)
    stack.SetMinimum(0)
    stack.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1.SaveAs(outDir + "/" + "vertexReco_reso_vs_theta.pdf")
    c1.Write()
    c1.Close()

    # cos(theta) 0.9 - 1
    stack3 = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
    hists3 = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slicesReco_zoom"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists3.append(hist)
        stack3.Add(hist)

    c3 = TCanvas("c3","c3")
    stack3.SetMaximum(50)
    stack3.SetMinimum(0)
    stack3.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c3.SaveAs(outDir + "/" + "vertexReco_reso_vs_theta_zoom.pdf")
    c3.Write()
    c3.Close()

    # cos(theta) 0.98 - 1
    stack4 = THStack("hs",";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
    hists4 = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("h_slicesReco_zoom2"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta); Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hist.SetMarkerSize(0.6)
        hists4.append(hist)
        stack4.Add(hist)

    c4 = TCanvas("c4","c4")
    stack4.SetMaximum(50)
    stack4.SetMinimum(0)
    stack4.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.6,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c4.SaveAs(outDir + "/" + "vertexReco_reso_vs_theta_zoom2.pdf")
    c4.Write()
    c4.Close()

    # Truth flight distance
    stack2 = THStack("hs2",";B_{s}^{0} truth flight distance [mm];Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    hists2 = list()

    for i, input_file in enumerate(input_files):
        f = TFile(input_file,"READ")
        print(f)
        name = input_file.split("_plots/plots.root")[0].split(process_name)[-1]
        hist = TH1D(f.Get("hResoVsR_slices2"))
        hist.SetName(name)
        hist.SetTitle(";cos(#theta);Flight distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerSize(0.6)
        hist.SetMarkerStyle(20)
        hist.SetLineColor(colors[i])
        hist.SetLineStyle(linestyles[i])
        hists2.append(hist)
        stack2.Add(hist)

    c2 = TCanvas("c2","c2")
    c2.cd()
    stack2.SetMaximum(80)
    stack2.SetMinimum(0)
    stack2.Draw("nostack,e1pl")
    gPad.BuildLegend(0.15,0.7,0.5,0.88,"")

    outfile = outDir+ "/plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2.SaveAs(outDir + "/" + "vertexReco_reso_vs_flightDistance.pdf")
    c2.Write()
    outf.Close()

if __name__ == "__main__":
    
    gROOT.SetBatch(True)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    gStyle.SetTitleSize(0.045,"x")
    gStyle.SetTitleSize(0.045,"y")
    gStyle.SetLabelSize(0.04)
   
 
    # Argument parsing
    args = parse_arguments(sys.argv[1:])
    
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'+"comparison_plots"
    os.system("mkdir -p {}".format(outDir))
        
    gROOT.Reset()
   
    if args.analysis=="Bs2JpsiPhi":
        process_name="evtGen_ecm91_Bs2JpsiPhi_"        
        plot(outDir,args.input_files,process_name)
        plot_reco_SV(outDir,args.input_files,process_name)        
    elif args.analysis=="impact_parameter":
        process_name="Zmumu_ecm91_"        
        plot_impact_parameter(outDir,args.input_files,process_name)
    elif args.analysis=="forward":
        process_name="evtGen_ecm91_Bs2JpsiPhi_forward_"
        plot(outDir,args.input_files,process_name)        
        plot_reco_SV(outDir,args.input_files,process_name)
