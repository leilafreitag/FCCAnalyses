import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D

def parse_arguments(argv=None):
    
	parser = argparse.ArgumentParser()

	# List of input root files
	parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=True) 
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
        
        plot_Bs2JpsiPhi(outDir)
        
        plot_SV(outDir)
        outf.Close()
