import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D

def parse_arguments(argv=None):
    
	parser = argparse.ArgumentParser()

	# List of input root files
	parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=True) 
	parser.add_argument("-a", "--analysis", help="Choose analysis to perform")
	return parser.parse_args(argv)

def fit_function():

	# Double gauss
#	ff = TF1("ff","[0]*exp(-0.5*((x-[1])/[2])**2) + [0]*[3]*exp(-0.5*((x-[1])/([2]*[4]))**2)",-200,200)
#	ff.SetParameters(500,0,20,0.25,2.0)
#	ff.SetParLimits(0,10,10000)
#	ff.SetParLimits(1,-100,100)
#	ff.SetParLimits(2,3,200)
#	ff.SetParLimits(3,0.0,0.5)
#	ff.SetParLimits(4,1.5,20)
	
	# Double crystal ball function with shared sigma and mean value
	ff = TF1("ff","[6]*(ROOT::Math::crystalball_function(x, [0], [1], [2], [3]) + [6]*ROOT::Math::crystalball_function(x, [4], [5], [2], [3]))",-200,200);
	ff.SetParLimits(0,0.0,5)					# alpha_L
	ff.SetParLimits(1,0.0,500.0)				# n_L
	ff.SetParLimits(2,8.0,200.0)				# sigma
	ff.SetParLimits(3,-50.0,50.0)				# mu
	ff.SetParLimits(4,-5.0,0.0)					# alpha_R
	ff.SetParLimits(5,0.0,500.0)				# n_R
	ff.SetParLimits(6,0,10000.0)				# scale
#	ff.SetParLimits(7,0.0,1.0)					# frac
    
	ff.SetParameters(0.2,10,20,0,-0.2,10,200)

	return ff


def vertex_resolution(outDir,events,cut,ff):
    
    # x, y and z resolution	
    c2r = TCanvas("reso","reso")
    c2r.Divide(3,1)
    c2r.cd(1)
    hx = TH1F("hx",";(vtx_{reco} - vtx_{gen}).x (#mum); Events",100,-100,100)
    events.Draw("1e3*(BsVertex.position.x-BsMCDecayVertex.x[0]) >>hx",cut)
    hx.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    
    c2r.cd(2)
    hy = TH1F("hy",";(vtx_{reco} - vtx_{gen}).y (#mum); Events",100,-100,100)
    events.Draw("1e3*(BsVertex.position.y-BsMCDecayVertex.y[0]) >>hy",cut)
    hy.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    
    c2r.cd(3)
    hz = TH1F("hz",";(vtx_{reco} - vtx_{gen}).z (#mum); Events",100,-100,100)
    events.Draw("1e3*(BsVertex.position.z-BsMCDecayVertex.z[0]) >>hz",cut)
    hz.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    
    c2r.SaveAs(outDir + "/" + "vertex_mc_reco.pdf")
    c2r.Write()
    
    # R_reco - R_true
    c_flight_distance_reso = TCanvas("c_flight_distance_reso","c_flight_distance_reso")
    h_flight_distance_reso = TH1F("h_flight_distance_reso","All #theta;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> h_flight_distance_reso", cut)
    h_flight_distance_reso.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    c_flight_distance_reso.SaveAs(outDir + "/" + "Bs_flight_distance_reso.pdf")
    c_flight_distance_reso.Write()
    
    # Overview plot
    c_vertexCosTheta_all = TCanvas("c_vertexCosTheta_all","c_vertexCosTheta_all")
    h_vertexCosTheta_all = TH2F("h_vertexCosTheta_all",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0,1,2000,-500,500)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ): TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexCosTheta_all", cut)
    c_vertexCosTheta_all.SaveAs(outDir + "/" + "Bs_vertex_distribution.pdf")
    c_vertexCosTheta_all.Write()

    # cos(theta) 0 - 1
    h_vertexCosTheta = TH2F("h_vertexCosTheta",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",10,0,1,100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ): TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexCosTheta", cut)
    
    # cos(theta) 0.9 - 1
    h_vertexCosThetaZoom = TH2F("h_vertexCosThetaZoom",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",10,0.9,1,100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ): TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexCosThetaZoom", cut)
    
    # cos(theta) 0.98 - 1
    h_vertexCosThetaZoom2 = TH2F("h_vertexCosThetaZoom2",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",10,0.98,1,100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ): TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexCosThetaZoom2", cut)

    c_slices_fit = TCanvas("c_slices_fit","c_slices_fit")
    arr = TObjArray()	
    h_vertexCosTheta.FitSlicesY(ff,0,-1,0,"R",arr)
    hxi = TH1D(arr[2])
    hxi.SetTitle(";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
    hxi.SetName("h_slices")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    c_slices_fit.SaveAs(outDir + "/" + "Bs_vertex_slices.pdf")
    c_slices_fit.Write()	
    hxi.Write()
    
    c_slices_fit_zoom = TCanvas("c_slices_fit_zoom","c_slices_fit_zoom")
    arr2 = TObjArray()
    h_vertexCosThetaZoom.FitSlicesY(ff,0,-1,0,"R",arr2)
    hxi = TH1D(arr2[2])
    hxi.SetName("h_slices_zoom")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    c_slices_fit_zoom.SaveAs(outDir + "/" + "Bs_vertex_slices_zoom.pdf")
    c_slices_fit_zoom.Write()
    hxi.Write()
    
    c_slices_fit_zoom2 = TCanvas("c_slices_fit_zoom2","c_slices_fit_zoom2")
    arr3 = TObjArray()
    h_vertexCosThetaZoom2.FitSlicesY(ff,0,-1,0,"R",arr3)
    hxi = TH1D(arr3[2])
    hxi.SetName("h_slices_zoom2")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(150)
    c_slices_fit_zoom2.SaveAs(outDir + "/" + "Bs_vertex_slices_zoom2.pdf")
    c_slices_fit_zoom2.Write()
    hxi.Write()

    
    cResoCentralForward = TCanvas("cResoCentralForward","cResoCentralForward")
    cResoCentralForward.Divide(2,1)
    
    cResoCentralForward.cd(1)
    hResoCentralForward = TH1F("hResoCentralForward","|cos(#theta)|<0.5;;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward", cut + " && TMath::Abs(TMath::Cos(Bs_theta)) < 0.5")
    hResoCentralForward.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    
    cResoCentralForward.cd(2)
    hResoCentralForward2 = TH1F("hResoCentralForward2","|cos(#theta)|>=0.5;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-200,200)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward2", cut + " && TMath::Abs(TMath::Cos(Bs_theta)) >= 0.5")
    hResoCentralForward2.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward.SaveAs(outDir + "/" + "Bs_flight_distance_reso_theta.pdf")
    cResoCentralForward.Write()

    cResoCentralForward150mrad = TCanvas("cResoCentralForward150mrad","cResoCentralForward150mrad")
    hResoCentralForward150mrad = TH1F("hResoCentralForward150mrad","150 mrad < #theta < 175 mrad;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-500,500)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward150mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.15 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.175")
    hResoCentralForward150mrad.Fit("ff","l")
    fun1 = TF1("fun1","[4]*(ROOT::Math::crystalball_function(x, [0], [1], [2], [3])", -200, 200)
    fun1.SetParameters(ff.GetParameter(0),ff.GetParameter(1),ff.GetParameter(2),ff.GetParameter(3),ff.GetParameter(6))
    fun1.Draw("same")
    fun2 = TF1("fun2","[4]*(ROOT::Math::crystalball_function(x, [0], [1], [2], [3])", -200, 200)
    fun2.SetParameters(ff.GetParameter(4),ff.GetParameter(5),ff.GetParameter(2),ff.GetParameter(3),ff.GetParameter(6))
    fun2.Draw("same")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward150mrad.SaveAs(outDir + "/" + "Bs_flight_distance_reso_theta150mrad.pdf")
    cResoCentralForward150mrad.Write()

    cResoCentralForward140mrad = TCanvas("cResoCentralForward140mrad","cResoCentralForward140mrad")
    hResoCentralForward140mrad = TH1F("hResoCentralForward140mrad","140 mrad < #theta < 150 mrad;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-500,500)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward140mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.14 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.15")
    hResoCentralForward140mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward140mrad.SaveAs(outDir + "/" + "Bs_flight_distance_reso_theta140mrad.pdf")
    cResoCentralForward140mrad.Write()

    cResoCentralForward130mrad = TCanvas("cResoCentralForward130mrad","cResoCentralForward130mrad")
    hResoCentralForward130mrad = TH1F("hResoCentralForward130mrad","130 mrad < #theta < 140 mrad;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-500,500)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward130mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.130 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.14")
    hResoCentralForward130mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward130mrad.SaveAs(outDir + "/" + "Bs_flight_distance_reso_theta130mrad.pdf")
    cResoCentralForward130mrad.Write()

    cResoCentralForward120mrad = TCanvas("cResoCentralForward120mrad","cResoCentralForward120mrad")
    hResoCentralForward120mrad = TH1F("hResoCentralForward120mrad","120 mrad < #theta < 130 mrad;Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum);",100,-500,500)
    events.Draw("TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) >> hResoCentralForward120mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.120 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.13")
    hResoCentralForward120mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward120mrad.SaveAs(outDir + "/" + "Bs_flight_distance_reso_theta120mrad.pdf")
    cResoCentralForward120mrad.Write()

    cResoVsTheta = TCanvas("cResoVsTheta","cResoVsTheta")
    hResoVsTheta = TProfile("hResoVsTheta",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0,1,-500,500,"s") # light distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)  vs.|cos(#theta)| (#mum)
    events.Draw("(TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) ): TMath::Abs(TMath::Cos(Bs_theta))>>hResoVsTheta",cut)
    cResoVsTheta.SaveAs(outDir + "/" + "Bs_reco_mc_vertex_theta.pdf")
    cResoVsTheta.Write()
    
    # Zoom to forward region
    cResoVsThetaZoom = TCanvas("cResoVsThetaZoom","cResoVsThetaZoom")
    hResoVsThetaZoom = TProfile("hResoVsThetaZoom",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0.9,1,-500,500,"s") # light distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)  vs.|cos(#theta)| (#mum)
    events.Draw("(TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) ): TMath::Abs(TMath::Cos(Bs_theta))>>hResoVsThetaZoom",cut)
    hResoVsThetaZoom.SetMaximum(300)
    hResoVsThetaZoom.SetMinimum(-300)
    hResoVsThetaZoom.Write()
    cResoVsThetaZoom.SaveAs(outDir + "/" + "Bs_reco_mc_vertex_theta_zoom.pdf")
    cResoVsThetaZoom.Write()
    
    cResoVsThetaZoom2 = TCanvas("cResoVsThetaZoom2","cResoVsThetaZoom2")
    hResoVsThetaZoom2 = TProfile("hResoVsThetaZoom2",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0.9,1,-500,500,"s") # light distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)  vs.|cos(#theta)| (#mum)
    events.Draw("(TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) ): TMath::Abs(TMath::Cos(Bs_theta))>>hResoVsThetaZoom2",cut)
    hResoVsThetaZoom2.SetMaximum(300)
    hResoVsThetaZoom2.SetMinimum(-300)
    cResoVsThetaZoom2.SaveAs(outDir + "/" + "Bs_reco_mc_vertex_theta_zoom2.pdf")
    cResoVsThetaZoom2.Write()
    
    # Close
    cResoVsTheta = TCanvas("cResoVsTheta","cResoVsTheta")
    hResoVsTheta = TProfile("hResoVsTheta",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0,1,-200,200,"s") # light distance resolution (#Delta R_{reco} - #Delta R_{MC}) (#mum)  vs.|cos(#theta)| (#mum)
    events.Draw("(TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) ): TMath::Abs(TMath::Cos(Bs_theta))>>hResoVsTheta",cut)
    cResoVsTheta.SaveAs(outDir + "/" + "Bs_reco_mc_vertex_theta_close.pdf")
    cResoVsTheta.Write()

    # Vertex resolution vs. R
    hResoVsR = TH2F("hResoVsR","|cos(#theta)<0.5|;B_{s}^{0} truth decay R [mm];Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0,20,100,-200,200)
    events.Draw("(TMath::Sqrt(pow(1e3*BsVertex.position.x,2) + pow(1e3*BsVertex.position.y,2) + pow(1e3*BsVertex.position.z,2) ) - TMath::Sqrt(pow(1e3*BsMCDecayVertex.x[0],2) + pow(1e3*BsMCDecayVertex.y[0],2) + pow(1e3*BsMCDecayVertex.z[0],2) ) ):TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2)) >> hResoVsR",cut + "&& TMath::Abs(TMath::Cos(Bs_theta))<0.5")

    cResoVsR = TCanvas("cResoVsR","cResoVsR")
    arr2 = TObjArray()
    hResoVsR.FitSlicesY(ff,0,-1,0,"R",arr2)
    hxi = TH1D(arr2[2])
    hxi.SetName("hResoVsR_slices")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    hxi.SetTitle("|cos(#theta)<0.5|;B_{s}^{0} truth decay R [mm];Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)")
    cResoVsR.SaveAs(outDir + "/" + "Bs_reco_mc_vertex_R.pdf")
    cResoVsR.Write()
    hxi.Write()







def plot_raw(outDir):
    
#    ff = fit_function()
#    ff.SetParLimits(0,0.0,5)                    # alpha_L
#    ff.SetParLimits(1,0.0,200.0)                # n_L
#    ff.SetParLimits(2,1.0,30.0)                 # sigma
#    ff.SetParLimits(3,-10.0,10.0)               # mu
#    ff.SetParLimits(4,-5.0,0.0)                 # alpha_R
#    ff.SetParLimits(5,0.0,200.0)                # n_R
#    ff.SetParLimits(6,0,10000.0)                # scale
#    ff.SetParLimits(7,0.0,0.7)                  # frac
#    ff.SetParameters(0.2,10,10,0,-0.2,10,1000,0.5)

    # D0 :
    cleila1 = TCanvas("RP_TRK_D0","RP_TRK_D0")
    cleila1.Divide(2,1)

    cleila1.cd(1)
    h1 = TH1F("h1", "RP_TRK_D0;D0 [\mum]",100,-50,50)
    events.Draw("1e3*RP_TRK_D0>>h1","TMath::Abs(RP_TRK_D0)<0.1")

    cleila1.cd(2)
    h2 = TH1F("h2", "Sqrt(RP_TRK_D0_cov);\sigma_{D0} [\mum]",100,0,10)
    events.Draw("1e3*TMath::Sqrt(RP_TRK_D0_cov)>>h2","TMath::Sqrt(RP_TRK_D0_cov) < 1e+1")

    cleila1.SaveAs(outDir + "/" + "RP_TRK_D0_leila.pdf")
    cleila1.Write()


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
    
    
def plot_Bs2DsK(outDir):

	cut0 = "n_Bs == 1  && n_DsTracks == 3"
	
	# Number of tracks
	c1 = TCanvas("Number of Ds tracks","Number of Ds tracks")
	h1 = TH1F("h1",";N( Ds tracks ); a.u.",5,0,5)
	events.Draw("n_DsTracks >>h1",  "n_Bs==1")
	h1.Draw()
	tt = TLatex()
	tt.SetTextSize(0.05)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	gPad.SetLogy(1)
	c1.SaveAs(outDir + "/" + "nDs_tracks.pdf")
	c1.Write()
	
	# Chi2 of the Ds vertex fit 
	cchi2 = TCanvas("cchi2","cxhi2")
	hchi2 = TH1F("hchi2",";#chi^{2}/n.d.f.; a.u.",100,0.,10.)
	events.Draw("DsVertex.chi2 >>hchi2",cut0+"&& DsVertex.chi2>0")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	gPad.SetLogy(1)
	#cchi2.SaveAs("plots/Bs2DsK_Ds_chi2.pdf")
	
	
	c2 = TCanvas("flight_distance_Ds","flight_distance_Ds")
	cut = cut0 + " && DsVertex.chi2[0] > 0 && DsVertex.chi2[0] < 10 "
	
	# "Flight distance" of the Ds - rather the position of the Ds decay vertex
	
	fld = "TMath::Sqrt( pow( 1e3*DsVertex.position.x, 2) + pow( 1e3*DsVertex.position.y,2) + pow( 1e3*DsVertex.position.z,2))"
	fld_gen = "TMath::Sqrt( pow( 1e3*DsMCDecayVertex.x[0], 2) + pow( 1e3*DsMCDecayVertex.y[0],2) + pow( 1e3*DsMCDecayVertex.z[0],2)   )"
	fld_res =  fld + " - " + fld_gen
	
	hfld = TH1F("hfld","; tertiary vtx position (rec-true) (#mum); Events",100,-70,70)
	events.Draw(fld_res+ " >> hfld", cut)
	hfld.Fit("gaus")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	c2.SaveAs(outDir + "/" + "Ds_vertex_position.pdf")
	c2.Write()
	
	# Pull of the Ds vertex position
	
	c3 = TCanvas("pull_flight_distance_Ds","pull_flight_distance_Ds")
	fld_mm = "TMath::Sqrt( pow( DsVertex.position.x, 2) + pow( DsVertex.position.y,2) + pow( DsVertex.position.z,2))"
	fld_gen_mm = "TMath::Sqrt( pow( DsMCDecayVertex.x[0], 2) + pow( DsMCDecayVertex.y[0],2) + pow( DsMCDecayVertex.z[0],2)   )"
	fld_res_mm =  fld_mm + " - " + fld_gen_mm
	term1 = " DsVertex.position.x * ( DsVertex.covMatrix[0] * DsVertex.position.x + DsVertex.covMatrix[1] * DsVertex.position.y + DsVertex.covMatrix[3] * DsVertex.position.z ) " 
	term2 = " DsVertex.position.y * ( DsVertex.covMatrix[1] * DsVertex.position.x + DsVertex.covMatrix[2] * DsVertex.position.y + DsVertex.covMatrix[4] * DsVertex.position.z ) " 
	term3 = " DsVertex.position.z * ( DsVertex.covMatrix[3] * DsVertex.position.x + DsVertex.covMatrix[4] * DsVertex.position.y + DsVertex.covMatrix[5] * DsVertex.position.z ) "
	tsum = term1 + " + " + term2 + " + " + term3
	fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) "
	fld_pull = "( " + fld_res_mm + " ) / " + fld_unc
	h_fld_pull = TH1F("h_fld_pull","; Pull tertiary vtx position; a.u.",100,-5,5)
	events.Draw(fld_pull+" >> h_fld_pull" , cut)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	c3.SaveAs(outDir + "/" + "pull_Ds_vertex_position.pdf")
	c3.Write()
	
	
	
	# -----------------------------------------------------------------------------------------
	#
	# the propagated tracks at the vertex of the  Ds : show that the corrected Ds
	# is better than the non corrected one
	#
	# -----------------------------------------------------------------------------------------
	
	c4 = TCanvas("Ds_mass","Ds_mass")
	h1 = TH1F("h1","; D_{s} mass (GeV); a.u.",100,1.95,1.99)
	events.Draw("RecoDs_mass>>h1",cut0)
	h2 = TH1F("h2","; D_{s} mass (GeV); a.u.",100,1.95,1.99)
	events.Draw("RecoDs_atVertex_mass>>h2",cut0)
	h1.SetLineColor(2)
	h2.Draw()
	h1.Draw("same")
	#h2.Fit("gaus")
	
#	gStyle.SetOptStat(0)
	
	leg = TLegend(0.66,0.15,0.94,0.3)
	leg.SetFillColor(0) 
	leg.SetBorderSize(0)
	leg.SetTextSize(0.04) 
	leg.AddEntry( h1, "w/o vtx correction","l")
	leg.AddEntry( h2, "with vtx correction","l")
	leg.Draw()
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	c4.SaveAs(outDir + "/" + "Ds_mass.pdf")
	c4.Write()
	
	
	
	#
	# Bs vertex :
	#
	
	# chi2 of the Bs vertex
	c_Bs_vertex = TCanvas("Bs_vertex","Bs_vertex")
	cut = cut + " && n_BsTracks >=2" ;   # remove events for which the bachelor K did not make a reco'ed track
	cc = TCanvas("Bschi2","Bschi2")
	hbschi2 = TH1F("hbschi2",";#chi^{2}/n.d.f.;a.u.",100,0.,10.)
	#hbschi2 = TH1F("hbschi2",";#chi^{2}/n.d.f.;a.u.",100,0.,5.)
	events.Draw("BsVertex_Cov.chi2 >>hbschi2",cut)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex")
	c_Bs_vertex.SaveAs(outDir + "/" + "Bs_vertex_chi.pdf")
	c_Bs_vertex.Write()


	ff = fit_function()

	#  resolution on flight  distance :
	vertex_resolution(outDir,events,cut,ff)	
	
	# pulls
	c6 = TCanvas("pull_Bs_vertex_x","pull_Bs_vertex_x")
	c6.Divide(3,1)
	c6.cd(1)	
	
	Bpx = TH1F("Bpx",";Pull x_{vtx}; a.u.",100,-5,5) 
	Bpullx = "(BsVertex_Cov.position.x-BsMCDecayVertex.x)/TMath::Sqrt(BsVertex_Cov.covMatrix[0])>>Bpx"
	events.Draw(Bpullx, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	gStyle.SetOptStat(1110)
	tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex")
	Bpx.Fit("gaus")
	
	c6.cd(2)
	Bpy = TH1F("Bpy",";Pull y_{vtx}; a.u.",100,-5,5) 
	Bpully = "(BsVertex_Cov.position.y-BsMCDecayVertex.y)/TMath::Sqrt(BsVertex_Cov.covMatrix[2])>>Bpy"
	events.Draw(Bpully, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	gStyle.SetOptStat(1110)
	tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex")
	Bpy.Fit("gaus")
	
	c6.cd(3)
	Bpz = TH1F("Bpz",";Pull z_{vtx}; a.u.",100,-5,5) 
	Bpullz = "(BsVertex_Cov.position.z-BsMCDecayVertex.z)/TMath::Sqrt(BsVertex_Cov.covMatrix[5])>>Bpz"
	events.Draw(Bpullz, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	gStyle.SetOptStat(1110)
	tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex")
	Bpz.Fit("gaus")
	
	c6.SaveAs(outDir + "/" + "Bsvertex_pull.pdf")
	c6.Write()	
	
	
	# pulls on the Bs vertex position
	c7 = TCanvas("pull_flight_distance_Bs","pull_flight_distance_Bs")
	bfld_mm = "TMath::Sqrt( pow( BsVertex_Cov.position.x, 2) + pow( BsVertex_Cov.position.y,2) + pow( BsVertex_Cov.position.z,2))"
	bfld_gen_mm = "TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) + pow( BsMCDecayVertex.z[0],2)   )"
	bfld_res_mm =  bfld_mm + " - " + bfld_gen_mm
	bterm1 = " BsVertex_Cov.position.x * ( BsVertex_Cov.covMatrix[0] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[1] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[3] * BsVertex_Cov.position.z ) " 
	bterm2 = " BsVertex_Cov.position.y * ( BsVertex_Cov.covMatrix[1] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[2] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[4] * BsVertex_Cov.position.z ) " 
	bterm3 = " BsVertex_Cov.position.z * ( BsVertex_Cov.covMatrix[3] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[4] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[5] * BsVertex_Cov.position.z ) "
	btsum = bterm1 + " + " + bterm2 + " + " + bterm3
	bfld_unc = " ( TMath::Sqrt( " + btsum + ") / " + bfld_mm +" ) "
	bfld_pull = "( " + bfld_res_mm + " ) / " + bfld_unc
	h_bfld_pull = TH1F("h_bfld_pull","; Pull Bs flight distance; a.u.",100,-5,5)
	events.Draw(bfld_pull+" >> h_bfld_pull" , cut)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK")
	h_bfld_pull.Fit("gaus");
	c7.SaveAs(outDir + "/" + "pull_flight_distance_Bs.pdf")
	c7.Write()
	


def plot_Bs2JpsiPhi(outDir):

	cut0 = "BsMCDecayVertex.position.z < 1e10" ;   #  a Bs.mumuKK has been found in MCParticle
	
	#  Number of tracks
	c0 = TCanvas("Ntracks","Ntracks")
	hntr = TH1F("hntr",";N( Bs tracks ); a.u.",5,-0.5,4.5)
	events.Draw("n_BsTracks >>hntr", cut0)
	gStyle.SetOptStat(10);   #  Entries only
	hntr.Draw()
	gStyle.SetOptStat(10)
	tt = TLatex()
	tt.SetTextSize(0.05)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	gPad.SetLogy(1)
	c0.SaveAs(outDir + "/" + "n_BsTracks.pdf")
	c0.Write()
	
	#  Chi2 of the vertex fit
	gStyle.SetOptStat(1110)
	c1 = TCanvas("chi2","chi2")
	hchi2 = TH1F("hchi2",";#chi^{2}/n.d.f.; a.u.",100,0.,10.)
	gStyle.SetOptStat(1110)
	events.Draw("BsVertex.chi2 >>hchi2",cut0+"&& BsVertex.chi2>0")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	gPad.SetLogy(1)
	c1.SaveAs(outDir + "/" + "chi2.pdf")
	c1.Write()	
	
	c2 = TCanvas("pulls","pulls")
	c2.Divide(2,2)
	
	cut = cut0+" && BsVertex.chi2 < 10"
	
	c2.cd(1)
	#  Pulls of the vertex in x, y, z
	px = TH1F("px",";Pull x_{vtx}; a.u.",100,-5,5) 
	events.Draw("(BsVertex.position.x-BsMCDecayVertex.x[0])/TMath::Sqrt(BsVertex.covMatrix[0])>>px",cut)
	px.Draw(); px.Fit("gaus")
	
	c2.cd(2)
	py = TH1F("py",";Pull y_{vtx}; a.u.",100,-5,5)
	events.Draw("(BsVertex.position.y-BsMCDecayVertex.y[0])/TMath::Sqrt(BsVertex.covMatrix[2])>>py",cut)
	py.Draw();py.Fit("gaus")
	
	c2.cd(3)
	pz = TH1F("pz",";Pull z_{vtx}; a.u.",100,-5,5)
	events.Draw("(BsVertex.position.z-BsMCDecayVertex.z[0])/TMath::Sqrt(BsVertex.covMatrix[5])>>pz",cut)
	pz.Draw(); pz.Fit("gaus")
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	
	
	#  resolutions on the Bs decay vertex :
	ff = fit_function()
	vertex_resolution(outDir,events,cut,ff)
	
	c4 = TCanvas("pull_fd","pull_fd")
	
	#  Pull of the flight distance :
	
	fld_mm = "TMath::Sqrt( pow( BsVertex.position.x, 2) + pow( BsVertex.position.y,2) + pow( BsVertex.position.z,2))"
	fld_gen_mm = "TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) + pow( BsMCDecayVertex.z[0],2)   )"
	fld_res_mm =  fld_mm + " - " + fld_gen_mm
	term1 = " BsVertex.position.x * ( BsVertex.covMatrix[0] * BsVertex.position.x + BsVertex.covMatrix[1] * BsVertex.position.y + BsVertex.covMatrix[3] * BsVertex.position.z ) " 
	term2 = " BsVertex.position.y * ( BsVertex.covMatrix[1] * BsVertex.position.x + BsVertex.covMatrix[2] * BsVertex.position.y + BsVertex.covMatrix[4] * BsVertex.position.z ) " 
	term3 = " BsVertex.position.z * ( BsVertex.covMatrix[3] * BsVertex.position.x + BsVertex.covMatrix[4] * BsVertex.position.y + BsVertex.covMatrix[5] * BsVertex.position.z ) "
	tsum = term1 + " + " + term2 + " + " + term3
	fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) "
	fld_pull = "( " + fld_res_mm + " ) / " + fld_unc
	h_fld_pull = TH1F("h_fld_pull","; Pull flight distance; a.u.",100,-5,5)
	events.Draw(fld_pull+" >> h_fld_pull" , cut)
	h_fld_pull.Fit("gaus")
	c4.SaveAs(outDir + "/" + "flight_distance_pull.pdf")
	c4.Write()	
	
	c5 = TCanvas("profiles","profiles")
	c5.Divide(2,2)
	
	cut4 = cut + " && n_BsTracks == 4"
	
	fld_unc_mum = "1000*"+fld_unc
	
	#  Profile of the flight distance resolution versus the uncertainty on the FD, nTracks = 4
	c5.cd(1)
	pro_unc = TProfile("pro_unc",";uncertainty on the FD (#mum); flight distance (rec-true) (#mum)", 4,10.,50.,-70,70,"s")
	events.Draw(fld_res_mm+":"+fld_unc_mum+" >>pro_unc",cut4)
	pro_unc.Draw()
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	tt.DrawLatexNDC(0.2,0.9,"N( B_{s} tracks ) = 4")
	# c1.SaveAs("plots/profile_FD_uncertainty_on_FD_Ntra4.pdf")
	
	#  Profile of the flight distance resolution versus the theta of the Bs
	c5.cd(2)
	ptheta = TProfile("ptheta",";#theta of B_{s} (rad); flight distance (rec-true) (#mum)",10,0.,TMath.Pi(),-70.,70.,"s")
	events.Draw(fld_res_mm+":Bs_theta >>ptheta",cut4)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	tt.DrawLatexNDC(0.2,0.9,"N( B_{s} tracks ) = 4")
	gPad.SetGridx(1)
	gPad.SetGridy(1)
	# c1.SaveAs("plots/profile_FD_theta_Bs.pdf")
	
	#  Profile of the flight distance resolution versus the flight distance
	c5.cd(3)
	pfld = TProfile("pfld",";flight distance (mm); flight distance (rec-true) (#mum)", 4,0.,12.,-70,70,"s")
	events.Draw(fld_res_mm+":"+fld_mm+" >>pfld",cut4)
	tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
	tt.DrawLatexNDC(0.7,0.9,"N( B_{s} tracks ) = 4")
	
	c5.SaveAs(outDir + "/" + "flight_distance_profile.pdf")
	c5.Write()	
	
	c6 = TCanvas("distances","distances")
	c6.Divide(2,2)
	#  angular separations
	c6.cd(1)
	dmax = TH1F("dmax",";#Delta#alpha max (rad); a.u.",100,0.,1.)
	events.Draw("deltaAlpha_max >>dmax",cut)
	c6.cd(2)
	dmin = TH1F("dmin",";#Delta#alpha min (rad); a.u.",100,0.,0.2)
	events.Draw("deltaAlpha_min >>dmin",cut)
	c6.cd(3)
	dave = TH1F("dave",";#Delta#alpha average (rad); a.u.",100,0.,1)
	events.Draw("deltaAlpha_ave>>dave",cut);
	
	c6.SaveAs(outDir + "/" + "angular_separation.pdf")
	c6.Write()

    
def plot_SV(outDir):
    cut0 = "BsMCDecayVertex.position.z < 1e10" ;   #  a Bs.mumuKK has been found in MCParticle
    ff = fit_function()

    # number of SV
    c1 = TCanvas("n_SV","n_SV")
    h1 = TH1F("h1","; Number of reconstructed secondary vertices; Events",8,0,8)
    events.Draw("n_SV >> h1", cut0)
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK")
    c1.SaveAs(outDir + "/" + "n_SV.pdf")
    c1.Write()

    # SV resolution
    cut = cut0 + "&& n_SV>0"
    c0 = TCanvas("SV_resolution","SV_resolution")
    h0 = TH1F("h0","; Distance of closest SV to MC B_{s}^{0} vertex [#mum]; Events",100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex >> h0", cut)
    h0.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK, n(SV)>0")

    tt2 = TLatex()
    tt2.SetTextSize(0.04)
    tt2.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))

    c0.SaveAs(outDir + "/" + "SV_resolution.pdf")
    c0.Write()

    # SV resolution vs flight distance    
    hResoVsR = TH2F("hResoVsR","",20,0,20,100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex:TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) +  pow( BsMCDecayVertex.z[0],2)) >> hResoVsR",cut + "&& TMath::Abs(TMath::Cos(Bs_theta))<0.5")
    cResoVsR = TCanvas("cResoVsR","cResoVsR")
    arr2 = TObjArray()
    hResoVsR.FitSlicesY(ff,0,-1,0,"R",arr2)
    hxi = TH1D(arr2[2])
    hxi.SetName("hResoVsR_slices")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    hxi.SetTitle("|cos(#theta)<0.5|;B_{s}^{0} truth flight distance [mm];Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    cResoVsR.SaveAs(outDir + "/" + "SV_resolution_vs_flight_distance.pdf")
    cResoVsR.Write()
    hxi.Write()

    hResoVsR2 = TH2F("hResoVsR2","",20,0,20,100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex:TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) +  pow( BsMCDecayVertex.z[0],2)) >> hResoVsR2",cut)
    cResoVsR2 = TCanvas("cResoVsR2","cResoVsR2")
    arr3 = TObjArray()
    hResoVsR2.FitSlicesY(ff,0,-1,0,"R",arr3)
    hxi2 = TH1D(arr3[2])
    hxi2.SetName("hResoVsR_slices2")
    hxi2.Draw()
    hxi2.SetMinimum(0)
    hxi2.SetMaximum(60)
    hxi2.SetTitle("All #theta;B_{s}^{0} truth flight distance [mm];Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    cResoVsR2.SaveAs(outDir + "/" + "SV_resolution_vs_flight_distance_allTheta.pdf")
    cResoVsR2.Write()
    hxi2.Write()


    ### Reco SV resolution vs theta ###
    # cos(theta) overview
    c_vertexRecoCosTheta_all = TCanvas("c_vertexRecoCosTheta_all","c_vertexRecoCosTheta_all")
    h_vertexRecoCosTheta_all = TH2F("h_vertexRecoCosTheta_all",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0,1,2000,-500,500)
    events.Draw("dR_min_SV_BsMCDecayVertex: TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexRecoCosTheta_all", cut)
    c_vertexRecoCosTheta_all.SaveAs(outDir + "/" + "Bs_vertexReco_distribution.pdf")
    c_vertexRecoCosTheta_all.Write()

    # cos(theta) 0.0 - 1.0
    h_vertexRecoCosTheta = TH2F("h_vertexRecoCosTheta",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",10,0,1,100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex: TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexRecoCosTheta", cut)
    c_slices_fit = TCanvas("c_slices_fit","c_slices_fit")
    arr = TObjArray()
    h_vertexRecoCosTheta.FitSlicesY(ff,0,-1,0,"R",arr)
    hxi = TH1D(arr[2])
    hxi.SetTitle(";cos(#theta);Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    hxi.SetName("h_slicesReco")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    c_slices_fit.SaveAs(outDir + "/" + "Bs_vertex_reco_slices.pdf")
    c_slices_fit.Write()
    hxi.Write()

    # cos(theta) 0.9 - 1
    h_vertexRecoCosThetaZoom = TH2F("h_vertexRecoCosThetaZoom",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",20,0.9,1,100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex: TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexRecoCosThetaZoom", cut)
    c_slices_fit_zoom = TCanvas("c_slices_fit_zoom","c_slices_fit_zoom")
    arr2 = TObjArray()
    h_vertexRecoCosThetaZoom.FitSlicesY(ff,0,-1,0,"R",arr2)
    hxi = TH1D(arr2[2])
    hxi.SetTitle(";cos(#theta);Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    hxi.SetName("h_slicesReco_zoom")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(60)
    c_slices_fit_zoom.SaveAs(outDir + "/" + "Bs_vertex_reco_slices_zoom.pdf")
    c_slices_fit_zoom.Write()
    hxi.Write()

    # cos(theta) 0.98 - 1
    h_vertexRecoCosThetaZoom2 = TH2F("h_vertexRecoCosThetaZoom2",";cos(#theta);Flight distance resolution  (#Delta R_{reco} - #Delta R_{MC}) (#mum)",10,0.98,1,100,-200,200)
    events.Draw("dR_min_SV_BsMCDecayVertex: TMath::Abs(TMath::Cos(Bs_theta)) >> h_vertexRecoCosThetaZoom2", cut)
    c_slices_fit_zoom2 = TCanvas("c_slices_fit_zoom2","c_slices_fit_zoom2")
    arr3 = TObjArray()
    h_vertexRecoCosThetaZoom2.FitSlicesY(ff,0,-1,0,"R",arr3)
    hxi = TH1D(arr3[2])
    hxi.SetTitle(";cos(#theta);Distance of closest SV to MC B_{s}^{0} vertex [#mum]")
    hxi.SetName("h_slicesReco_zoom2")
    hxi.Draw()
    hxi.SetMinimum(0)
    hxi.SetMaximum(150)
    c_slices_fit_zoom2.SaveAs(outDir + "/" + "Bs_vertex_reco_slices_zoom2.pdf")
    c_slices_fit_zoom2.Write()
    hxi.Write()

    ### small theta plot ###
    cResoCentralForward140mrad = TCanvas("cResoCentralForward140mrad","cResoCentralForward140mrad")
    hResoCentralForward140mrad = TH1F("hResoCentralForward140mrad","140 mrad < #theta < 150 mrad;Distance of closest SV to MC B_{s}^{0} vertex [#mum];",100,-500,500)
    events.Draw("dR_min_SV_BsMCDecayVertex >> hResoCentralForward140mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.14 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.15")
    hResoCentralForward140mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward140mrad.SaveAs(outDir + "/" + "Bs_flight_distance_resoReco_theta140mrad.pdf")
    cResoCentralForward140mrad.Write()

    cResoCentralForward130mrad = TCanvas("cResoCentralForward130mrad","cResoCentralForward130mrad")
    hResoCentralForward130mrad = TH1F("hResoCentralForward130mrad","130 mrad < #theta < 140 mrad;Distance of closest SV to MC B_{s}^{0} vertex [#mum];",100,-500,500)
    events.Draw("dR_min_SV_BsMCDecayVertex >> hResoCentralForward130mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.130 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.14")
    hResoCentralForward130mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward130mrad.SaveAs(outDir + "/" + "Bs_flight_distance_resoReco_theta130mrad.pdf")
    cResoCentralForward130mrad.Write()

    cResoCentralForward120mrad = TCanvas("cResoCentralForward120mrad","cResoCentralForward120mrad")
    hResoCentralForward120mrad = TH1F("hResoCentralForward120mrad","120 mrad < #theta < 130 mrad;Distance of closest SV to MC B_{s}^{0} vertex [#mum];",100,-500,500)
    events.Draw("dR_min_SV_BsMCDecayVertex >> hResoCentralForward120mrad", cut + " && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) > 0.120 && TMath::Abs(Bs_theta < TMath::Pi()/2 ? Bs_theta : TMath::Pi()-Bs_theta) <= 0.13")
    hResoCentralForward120mrad.Fit("ff","l")
    tt = TLatex()
    tt.SetTextSize(0.05)
    tt.DrawLatexNDC(0.15,0.8,"#sigma = {0:.1f} #pm {1:.1f} #mum".format(ff.GetParameter(2), ff.GetParError(2)))
    cResoCentralForward120mrad.SaveAs(outDir + "/" + "Bs_flight_distance_resoReco_theta120mrad.pdf")
    cResoCentralForward120mrad.Write()

if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetTitleSize(0.045,"x")
    gStyle.SetTitleSize(0.045,"y")
    gStyle.SetLabelSize(0.04)
    
    # Argument parsing
    args = parse_arguments(sys.argv[1:])
    
    for input_file in args.input_files:
        print("Working on file " + input_file)
        outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'+input_file.split('/')[-1].split(".root")[0] + "_plots"
        os.system("mkdir -p {}".format(outDir))
        
        gROOT.Reset()
        
        f = TFile(input_file, "READ")
        events = f.Get("events")
        
        outfile = outDir+ "/plots.root"
        outf=TFile.Open(outfile,"RECREATE")
        
        if args.analysis=="Bs2DsK":
        	plot_Bs2DsK(outDir)
        elif args.analysis=="Bs2JpsiPhi":
        	plot_Bs2JpsiPhi(outDir)
        else:	
        	plot_raw(outDir)
        
        plot_SV(outDir)
        outf.Close()
