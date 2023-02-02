import sys, argparse, os
import ROOT
from ROOT import gROOT,TFile,TCanvas,TH1F,TH2F,TProfile,TStyle,gStyle,TLatex,TPad,gPad,TCut,TLegend,TF1,TMath,TObjArray,TH1D,THStack,TH1,TPaveText,TText,TGraph,TMultiGraph,TGraphErrors,TFormula
from array import array

linestyles = [1,2,3,4,5,6,7,8,9,10]


def parse_arguments(argv=None):

        parser = argparse.ArgumentParser()

        # List of input root files
        parser.add_argument("-i", "--input_files", help="Input root files", nargs="*", required=False)
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

def get_filepath(geometry,momentum,angle):
    return f"FCCee/vertex/ParticleGun_Mu_{geometry}_{momentum}GeV_{angle}degrees_plots/plots.root"


def plot_impact_parameter(outDir, geometries,momenta,nameToSave,colors,markers):
    TH1.AddDirectory(False)
    gStyle.SetErrorX(0)

    num_legends = len(geometries)*len(momenta)
    
    # D0 resolution vs theta for diff momenta

    #USING MULTIGRAPH
    mg = TMultiGraph()    

    angles=[10,20,30,40,50,60,70,80,89]
    #colors_momenta = [1,2,3,4,5,6,7,8,9,10,11]
    #markers_momenta = [20,21,47,22,26,4,25,20,21]
    i=0
    for mom in momenta:
        for geometry in geometries:
            n = len(angles)
            x, y, ex, ey = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
            for angle in angles:
                filename = get_filepath(geometry,mom,angle)
                f = TFile(filename,"READ")
                g = TGraphErrors(f.Get("h_slices_D0_graph"))
                x.append(g.GetPointX(0))
                y.append(g.GetPointY(0))
                ey.append(g.GetErrorY(0))
#                ey.append(2)
                #print(g.GetErrorY(0))
                ex.append(0)
                if angle == 80:
                    print(g.GetPointX(0), g.GetPointY(0))
                    print(g.GetErrorY(0))
            g_temp = TGraphErrors(n,x,y,ex,ey)
            print(x)
            if len(geometries)==1:
                g_temp.SetTitle(name_for_legend(f"{mom}GeV"))
            else:
                g_temp.SetTitle(name_for_legend(f"{mom}GeV, {name_for_legend(geometry)}"))
            g_temp.SetMarkerStyle(markers[i])
            #g_temp.SetLineColor(colors[i])
            #g_temp.SetLineStyle(linestyles[i])
            g_temp.SetLineWidth(0)
            if nameToSave =="all_mom":
                g_temp.SetMarkerColorAlpha(colors[i],0.7)
                g_temp.SetMarkerSize(0.7)
            else:
                g_temp.SetMarkerColor(colors[i])
                g_temp.SetMarkerSize(0.9)
            mg.Add(g_temp)

            print(mom,geometry)
            #want to fit each g_temp with a fit function to extract params a and b
#            f1 = TF1("f1","[0]+[1]/([2]*pow(sin(x*pi/180),3/2))",9,90)
            f1 = TF1("f1","TMath::Sqrt(pow([0],2)+pow([1],2)/(pow([2],2)*pow(sin(x*pi/180),3)))",8,90)
 
            #set inital parameters
            f1.SetParameter(0,2) #param a should be around 3
            f1.SetParLimits(0,1,25) #1,25
            f1.SetParameter(1,15) #param b should be around 15
            f1.SetParLimits(1,7,40)
            f1.SetParameter(2,mom) #setting the momentum parameter to the momentum
            f1.SetParLimits(2,mom,mom) #fixing the momentum parameter

            f1.SetLineColor(colors[i])
            f1.SetLineWidth(1)
            f1.SetLineStyle(2)

            g_temp.Fit("f1")
            i+=1

    gStyle.SetPadTickY(1)
    #gStyle.SetPadTickX(1)
    c1_gun = TCanvas("c1_gun","c1_gun")
    
    f1.Draw()

    mg.SetMaximum(3000.0)
    mg.SetMinimum(1.)
    mg.Draw("AP")
    #mg.Draw("AP,nostack,e1pl")
    mg.GetYaxis().SetTitle("\sigma_{d_{0}} [\mum]")
    mg.GetXaxis().SetTitle("#theta [degrees]")
    gPad.SetLogy(1) 
    gPad.Update()
    gStyle.SetLegendTextSize(0.035)
    if nameToSave == "all_mom": gStyle.SetLegendTextSize(0.03)
    gStyle.SetLegendBorderSize(0)

    if nameToSave == "DSK_vs_noDSK_30" or nameToSave == "DSK_vs_noDSK":
        x_left=0.40
    else: x_left=0.18
    if len(geometries) == 1:
        x_left=0.23
        y_move_down=0.04
    else: y_move_down=0
    if nameToSave == "all_mom":
        num_legends=7
        x_left=.25
    gPad.BuildLegend(x_left+0.02,0.75-(num_legends-3)*0.05-y_move_down,x_left+0.14,0.88-y_move_down,"")


    #manually adding fit fkt to the legend
#    leg = TLegend(x_left+0.02,0.75-(num_legends-3)*0.05-y_move_down-0.06,x_left+0.12,0.88-y_move_down-0.27)
    leg = TLegend(x_left+0.03,0.75-(num_legends-3)*0.05-y_move_down,x_left+0.3,0.88-y_move_down-0.37)
    f1.SetLineColor(1)
    leg.AddEntry(f1,"fit function = a #oplus b/(p sin^{3/2}(#theta))", "L")

    leg.Draw("same")
    leg.SetFillStyle(0)

    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Particle gun muons}")
    if len(geometries) == 1:
        if geometries[0] == "standard":
            tt.DrawLatexNDC(x_left,0.85,"#bf{Standard IDEA: R(Layer_{1}) = 1.7 cm, w(VTX layers) = 280 \mum}")


    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/gun_plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1_gun.SaveAs(outDir + "/" + f"gun_D0_comparison_{nameToSave}.pdf")
    c1_gun.Write()
    c1_gun.Close()


    # Z0 resolution vs theta for diff momenta (USING MULTIGRAPH)
    mg = TMultiGraph()

    i=0
    for mom in momenta:
        for geometry in geometries:
            n = len(angles)
            x, y, ex, ey = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
            for angle in angles:
                filename = get_filepath(geometry,mom,angle)
                f = TFile(filename,"READ")
                g = TGraphErrors(f.Get("h_slices_Z0_graph"))
                x.append(g.GetPointX(0))
                y.append(g.GetPointY(0))
       	       	ey.append(g.GetErrorY(0))
       	       	ex.append(0)
            g_temp = TGraphErrors(n,x,y,ex,ey)
            if len(geometries)==1:
                g_temp.SetTitle(name_for_legend(f"{mom}GeV"))
            else:
                g_temp.SetTitle(name_for_legend(f"{mom}GeV, {name_for_legend(geometry)}"))
            g_temp.SetMarkerStyle(markers[i])
            g_temp.SetLineColor(colors[i])
            g_temp.SetLineStyle(linestyles[i])
            g_temp.SetLineWidth(0)
            if nameToSave =="all_mom":
                g_temp.SetMarkerColorAlpha(colors[i],0.7)
                g_temp.SetMarkerSize(0.7)
            else:
                g_temp.SetMarkerColor(colors[i])
                g_temp.SetMarkerSize(0.9)
            mg.Add(g_temp)
            i+=1

    c2_gun = TCanvas("c2_gun","c2_gun")
    mg.SetMaximum(3000.0)
    mg.SetMinimum(1.)
    mg.Draw("AP")
    #mg.Draw("nostack,e1pl")
    mg.GetYaxis().SetTitle("\sigma_{z_{0}} [\mum]")
    mg.GetXaxis().SetTitle("#theta [degrees]")
    mg.GetYaxis().SetTitleOffset(0.9)
    gPad.SetLogy(1)
    gPad.Update()
    gStyle.SetPadTickY(1)
    #gStyle.SetPadTickX(1)
    gStyle.SetLegendTextSize(0.035)
    if nameToSave == "all_mom": gStyle.SetLegendTextSize(0.03)
    gStyle.SetLegendBorderSize(0)

    if nameToSave == "DSK_vs_noDSK_30" or nameToSave == "DSK_vs_noDSK":
        x_left=0.40
    else: x_left=0.18
    if len(geometries) == 1:
        x_left=0.23
        y_move_down=0.04
    else: y_move_down=0
    if nameToSave == "all_mom":
        num_legends=7
        x_left=.25
    gPad.BuildLegend(x_left,0.75-(num_legends-3)*0.05-y_move_down,x_left+0.12,0.88-y_move_down,"")

    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.63,0.915,"#it{IDEA Delphes simulation}")
    tt.DrawLatexNDC(0.14,0.915,"#bf{Particle gun muons}")
    if len(geometries) == 1:
        if geometries[0] == "standard":
            tt.DrawLatexNDC(x_left,0.85,"#bf{Standard IDEA: R(Layer_{1}) = 1.7 cm, w(VTX layers) = 280 \mum}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/gun_plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c2_gun.SaveAs(outDir + "/" + f"gun_Z0_comparison_{nameToSave}.pdf")
    c2_gun.Write()
    c2_gun.Close()





''' #OLD VERSION WITH STACK for D0 resolution vs theta for diff momenta
    stack = THStack("hs",";#theta [degrees]; \sigma_{D0} [\mum]")
    hists = list()

    geometries=["standard"]
    momenta=[1,10,100]
    angles=[10,20,30,40,50,60,70,80,89]
    colors_momenta = [1,2,3,4,5,6,7,8,9,10,11]
    markers_momenta = [20,21,47,22,26,4,25,20,21]
    i=0
    for geometry in geometries:
        for mom in momenta:
            for angle in angles:
                filename = get_filepath(geometry,mom,angle)
                f = TFile(filename,"READ") 
       	       	if angle == 10:
                    hist = TProfile(f.Get("h_slices_D0"))
                    hist.SetName(geometry)
                    hist.SetTitle(name_for_legend(f"{name_for_legend(geometry)},{mom}GeV"))
                    hist.SetMarkerColor(colors_momenta[i])
                    hist.SetMarkerStyle(markers_momenta[i])
                    hist.SetLineColor(colors_momenta[i])
                    hist.SetLineStyle(linestyles[i])
                    hist.SetLineWidth(0)
                    hist.SetMarkerSize(0.6)
                else:
                    hist_temp = TProfile(f.Get("h_slices_D0"))
                    hist.Add(hist_temp)
                #hists.append(hist)
            stack.Add(hist)
            i+=1

    c1_gun = TCanvas("c1_gun","c1_gun")
    stack.SetMaximum(1000.0) 
    stack.SetMinimum(1.)
    stack.Draw("nostack,e1pl")
    gPad.SetLogy(1) #seems like it only sets the axis log scale but the data is lost
    gPad.Update()
    gStyle.SetPadTickY(1)
    #gStyle.SetPadTickX(1)
    gStyle.SetLegendTextSize(0.035)
    gStyle.SetLegendBorderSize(0)
    gPad.BuildLegend(0.4,0.75,0.8,0.88,"")

    tt=TLatex()
    tt.SetTextSize(0.035)
    tt.DrawLatexNDC(0.65,0.915,"#bf{#it{IDEA Delphes simulation}}")
    gPad.Modified()
    gPad.Update()

    outfile = outDir+ "/gun_plots.root"
    outf=TFile.Open(outfile,"RECREATE")

    c1_gun.SaveAs(outDir + "/" + "gun_D0_comparison.pdf")
    c1_gun.Write()
    c1_gun.Close()
'''


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

    geometries=["standard"]
    momenta=[1,10,100]
    
    

    if args.analysis=="impact_parameter": 
        plot_impact_parameter(outDir,["standard","R1.3","R1.3_w30"],[1,10,100],"all_mom",[1,1,1,2,2,2,4,4,4],[20,21,26,20,21,26,20,21,26])

#        plot_impact_parameter(outDir,["R1.3_w100","R1.3_w100_DSK"],[1,10,100],"DSK_vs_noDSK",[1,1,2,2,4,4],[20,4,21,25,22,26])
#        plot_impact_parameter(outDir,["R1.3_w30","R1.3_w30_DSK"],[1,10,100],"DSK_vs_noDSK_30",[1,1,2,2,4,4],[20,4,21,25,22,26])
        plot_impact_parameter(outDir,["standard"],[1,10,100],"standard",[1,2,4],[20,21,22])
#        plot_impact_parameter(outDir,["standard","R1.3","R1.3_w100","R1.3_w30","R1.3_w30_DSK"],[1],"1GeV",[1,2,8,4,4],[20,21,47,22,26])
#        plot_impact_parameter(outDir,["standard","R1.3","R1.3_w100","R1.3_w30","R1.3_w30_DSK"],[10],"10GeV",[1,2,8,4,4],[20,21,47,22,26])
#        plot_impact_parameter(outDir,["standard","R1.3","R1.3_w100","R1.3_w30","R1.3_w30_DSK"],[100],"100GeV",[1,2,8,4,4],[20,21,47,22,26])

