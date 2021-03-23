
#include <iostream>
#include <cstdlib>
#include <vector>

#include "awkward/Content.h"
#include "awkward/io/json.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/array/RecordArray.h"
#include "awkward/array/Record.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

#include "myUtils.h"
#include "VertexFitterActs.h"
#include "VertexFitterSimple.h"
#include "ReconstructedParticle.h"
#include "MCParticle.h"

using namespace myUtils;


ROOT::VecOps::RVec<float> myUtils::get_Vertex_x(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex){
    ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex.position.x);
  return result;
}
  
ROOT::VecOps::RVec<float> myUtils::get_Vertex_y(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex){
    ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex.position.y);
  return result;
}

ROOT::VecOps::RVec<float> myUtils::get_Vertex_z(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex){
  ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex.position.z);
  return result;
}

ROOT::VecOps::RVec<float> myUtils::get_Vertex_chi2(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex){
  ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex.chi2);
  return result;
}

ROOT::VecOps::RVec<int> myUtils::get_Vertex_ntracks(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex){
  ROOT::VecOps::RVec<int> result;
  for (auto &p:vertex)
    result.push_back(p.ntracks);
  return result;
}

ROOT::VecOps::RVec<int> myUtils::get_Vertex_indMC(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex,
						  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> mcver){

  ROOT::VecOps::RVec<int> result;
  for (auto &p:vertex){
    float distance = 99999999999.;
    int index=-1;
    for (size_t i = 0; i < mcver.size(); ++i){
      float distance2 = sqrt( pow(p.vertex.position.x - mcver.at(i).vertex[0] ,2) +
			      pow(p.vertex.position.y - mcver.at(i).vertex[1] ,2) +
			      pow(p.vertex.position.z - mcver.at(i).vertex[2] ,2) );

      if (distance2<distance){distance=distance2; index=i;}
    }
    if (index>-1)result.push_back(index);
    else std::cout <<"problem index myUtils::get_Vertex_indMC " << index <<std::endl;
  }
  return result;
  
}


ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>
myUtils::get_VertexObject(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> mcver,
			  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
			  ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
			  ROOT::VecOps::RVec<int> recin,
			  ROOT::VecOps::RVec<int> mcin){

  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> result;

  ROOT::VecOps::RVec< ROOT::VecOps::RVec<int> > rp2mc = ReconstructedParticle2MC::getRP2MC_indexVec(recin, mcin, reco);
  

  
  int counter=0;
  for (auto &p: mcver){
    ROOT::VecOps::RVec<int> mc_indRVec = p.mc_ind;
    std::vector<int> mc_ind;
    for (size_t i = 0; i < mc_indRVec.size(); ++i)mc_ind.push_back(mc_indRVec.at(i));
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles;
    for (size_t i = 0; i < rp2mc.size(); ++i){
      for (size_t j = 0; j < rp2mc.at(i).size(); ++j){

	std::vector<int>::iterator it = std::find(mc_ind.begin(), mc_ind.end(), rp2mc.at(i).at(j));
	if (it!=mc_ind.end())recoparticles.push_back(reco.at(i));
	
	
      } 
    }

    if (recoparticles.size()<2)continue;
    
    VertexingUtils::FCCAnalysesVertex TheVertex;
    if (counter==0) TheVertex = VertexFitterSimple::VertexFitter(1,recoparticles, tracks );
    else TheVertex = VertexFitterSimple::VertexFitter(0,recoparticles, tracks );
    counter+=1;
    result.push_back(TheVertex);    
  }

  //std::cout <<"n vtx reco "<< result.size()<<std::endl;
  for (auto&p:result){
    edm4hep::VertexData vertex = p.vertex;    
    //std::cout << "n tracks " << p.ntracks << "  chi2 " << vertex.chi2 << "  x=" << vertex.position.x << "  y=" << vertex.position.y << "  z=" << vertex.position.z <<std::endl;
  }
  
  return result;
}


ROOT::VecOps::RVec<TVector3> myUtils::get_MCVertex(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto &p:vertex)
    result.push_back(p.vertex);
  return result;
}

ROOT::VecOps::RVec<float> myUtils::get_MCVertex_x(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex[0]);
  return result;
}

ROOT::VecOps::RVec<float> myUtils::get_MCVertex_y(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex[1]);
  return result;
}
ROOT::VecOps::RVec<float> myUtils::get_MCVertex_z(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  ROOT::VecOps::RVec<float> result;
  for (auto &p:vertex)
    result.push_back(p.vertex[2]);
  return result;
}
ROOT::VecOps::RVec<int> myUtils::get_NTracksMCVertex(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  ROOT::VecOps::RVec<int> result;
  for (auto &p:vertex)
    result.push_back(p.mc_ind.size());
  return result;
}

std::vector<std::vector<int>> myUtils::get_MCindMCVertex(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> vertex){
  std::vector<std::vector<int>> result;
  for (auto &p:vertex){
    std::vector<int> tmp;
    for (size_t i = 0; i < p.mc_ind.size(); ++i) tmp.push_back(p.mc_ind.at(i));
    result.push_back(tmp);
  }
  return result;
}


ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> myUtils::get_MCVertexObject(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
										    ROOT::VecOps::RVec<int> ind){
  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertexMC> result;
  ROOT::VecOps::RVec<TVector3> tmpvec;
  ROOT::VecOps::RVec<int> tmpvecint;
  //std::cout <<"==========================new event==========================" << std::endl;
  for (size_t i = 0; i < mc.size(); ++i) {
    if (mc.at(i).charge==0)continue;
    if (mc.at(i).generatorStatus==1){
      TVector3 tmp;
      tmp[0]=mc.at(i).vertex.x;
      tmp[1]=mc.at(i).vertex.y;
      tmp[2]=mc.at(i).vertex.z;
      tmpvec.push_back(tmp);
      tmpvecint.push_back(i);
      //std::cout << "index=" << tmpvec.size()-1<<"  i="<<i<<"  PDG  " << mc.at(i).PDG << "  x=" <<tmp[0]<< "  y=" <<tmp[1]<< "  z=" <<tmp[2]<<std::endl;
    }
  }
  
  for (size_t i = 0; i < tmpvec.size(); ++i) {
    bool vertexfound=false;
    TVector3 vertexPos(tmpvec.at(i)[0],tmpvec.at(i)[1],tmpvec.at(i)[2]);

    if (result.size()==0){
      VertexingUtils::FCCAnalysesVertexMC vertex;
      ROOT::VecOps::RVec<int> ind;
      ind.push_back(tmpvecint.at(i));
      vertex.vertex=vertexPos;
      vertex.mc_ind=ind;
      result.push_back(vertex);
    }
    else{
      for (size_t j = 0; j < result.size(); ++j) {
	if (get_distance(result.at(j).vertex,vertexPos)<0.0001){
	  result.at(j).mc_ind.push_back(tmpvecint.at(i));
	  vertexfound=true;
	  break;
	}
      }
      if (vertexfound==false){
	VertexingUtils::FCCAnalysesVertexMC vertex;
	ROOT::VecOps::RVec<int> ind2;
	ind2.push_back(tmpvecint.at(i));
	vertex.vertex=vertexPos;
	vertex.mc_ind=ind2;
	result.push_back(vertex);
      }
    }
  }


  //std::cout << "====================size MC " << mc.size() << " size assoc  " << ind.size() << std::endl;
  //adding the mother particles
  //std::cout <<"nvx MC  " << result.size()<<std::endl;
  for (auto& p:result) {
    std::vector<int> mother_ind;

    //std::cout <<"n part="<<p.mc_ind.size()<<"  x=" << p.vertex[0] <<"  y=" << p.vertex[1] <<"  z=" << p.vertex[2] <<std::endl;
    ROOT::VecOps::RVec<int> mc_ind = p.mc_ind;
    for (size_t i = 0; i < mc_ind.size(); ++i){

      //std::cout << "i="<< i << "  mc_ind  "<< mc_ind.at(i) <<"  parent begin " << mc.at(mc_ind.at(i)).parents_begin <<"  parent end " << mc.at(mc_ind.at(i)).parents_end << " end-beg  "  << mc.at(mc_ind.at(i)).parents_end-mc.at(mc_ind.at(i)).parents_begin<< std::endl;

      
      
      for (size_t j = mc.at(mc_ind.at(i)).parents_begin; j < mc.at(mc_ind.at(i)).parents_end; ++j){
	//std::cout << "     j="<<j << "  index  " << ind.at(j) << "  PDG ID " << mc.at(ind.at(j)).PDG << std::endl;
	std::vector<int>::iterator it = std::find(mother_ind.begin(), mother_ind.end(), ind.at(j));
	if (it==mother_ind.end())mother_ind.push_back(ind.at(j));
      }
    }

    ROOT::VecOps::RVec<int> mother_indRVec;
    for (size_t i = 0; i < mother_ind.size(); ++i)mother_indRVec.push_back(mother_ind.at(i));
    p.mother_ind = mother_indRVec;
    //std::cout << "found n mothers="<<mother_ind.size()<<std::endl;
    
  }
  
  /*std::cout <<"nvx MC  " << result.size()<<std::endl;
  for (size_t j = 0; j < result.size(); ++j)
  std::cout <<"n part="<<result.at(j).mc_ind.size()<<"  x=" << result.at(j).vertex[0] <<"  y=" << result.at(j).vertex[1] <<"  z=" << result.at(j).vertex[2] <<std::endl;*/

  return result;
}

float myUtils::get_distance(TVector3 v1, TVector3 v2){

  return sqrt( pow( v1[0] - v2[0], 2) +
	       pow( v1[1] - v2[1], 2) +
	       pow( v1[2] - v2[2], 2));
}

float myUtils::get_distanceVertex(edm4hep::VertexData v1, edm4hep::VertexData v2){

  return sqrt( pow( v1.position.x - v2.position.x, 2) +
	       pow( v1.position.y - v2.position.y, 2) +
	       pow( v1.position.z - v2.position.z, 2));
}




sel_PV::sel_PV(bool arg_closest):m_closest(arg_closest){};
VertexingUtils::FCCAnalysesVertex
myUtils::sel_PV::operator()(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> pv){

  VertexingUtils::FCCAnalysesVertex result;

  float min=999999;
  for (auto& p: pv){
    edm4hep::VertexData v = p.vertex;
    float dist=sqrt( pow( v.position.x, 2) + pow( v.position.y, 2) + pow( v.position.z, 2));
    if (dist < min) {min=dist; result = p;}
  }
  return result;
}
  


ROOT::VecOps::RVec<float> myUtils::get_flightDistanceVertex(ROOT::VecOps::RVec<FCCAnalysesComposite> in, edm4hep::VertexData pv){
  ROOT::VecOps::RVec<float> result;

  for (auto &sv: in){
    edm4hep::VertexData theSV = sv.vertex;
    result.push_back(get_distanceVertex(pv, theSV));
  }
  
  return result;
}


ROOT::VecOps::RVec<float> myUtils::get_flightDistanceVertex(ROOT::VecOps::RVec<FCCAnalysesComposite> in, 
							    VertexingUtils::FCCAnalysesVertex pv){

  ROOT::VecOps::RVec<float> result;
  edm4hep::VertexData thePV = pv.vertex;

  return get_flightDistanceVertex(in, thePV);
  
}


ROOT::VecOps::RVec<int> myUtils::getMC_daughter(int daughterindex, 
						ROOT::VecOps::RVec<edm4hep::MCParticleData> in, 
						ROOT::VecOps::RVec<int> ind){
  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (daughterindex+1>in.at(i).daughters_end-in.at(i).daughters_begin) {
      result.push_back(-999);
    }
    else {
      result.push_back(ind.at(in.at(i).daughters_begin+daughterindex));
    }
  }
  return result;
}

ROOT::VecOps::RVec<int> myUtils::getMC_parent(int parentindex, 
					      ROOT::VecOps::RVec<edm4hep::MCParticleData> in,  
					      ROOT::VecOps::RVec<int> ind){
  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (parentindex+1>in.at(i).parents_end-in.at(i).parents_begin) {
      result.push_back(-999);
    }
    else {
      result.push_back(ind.at(in.at(i).parents_begin+parentindex));
    }
  }
  return result;
}

int myUtils::getMC_parent(int parentindex, 
			  edm4hep::MCParticleData in,  
			  ROOT::VecOps::RVec<int> ind){
  int result;
  if (parentindex+1>in.parents_end-in.parents_begin)
    result = -999;
  else 
    result = ind.at(in.parents_begin+parentindex);
  return result;
}


ROOT::VecOps::RVec<FCCAnalysesComposite> myUtils::add_truthmatched(ROOT::VecOps::RVec<FCCAnalysesComposite> comp,
								   ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
								   //ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> rp2mc){
								   ROOT::VecOps::RVec<int> rp2mc,
								   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
								   ROOT::VecOps::RVec<int> ind){


  for (size_t i = 0; i < rp2mc.size(); ++i) {
    int mcassoc = rp2mc.at(i);

    //std::cout <<"i="<<i<<" mc p " << sqrt(pow(mc.at(mcassoc).momentum.z,2)+pow(mc.at(mcassoc).momentum.y,2)+pow(mc.at(mcassoc).momentum.x,2)) << "  rp p " << ReconstructedParticle::get_p(recop.at(i))<<std::endl;


  }

  //ROOT::VecOps::RVec<FCCAnalysesComposite> result = comp;

  for (size_t i = 0; i < comp.size(); ++i) {
    //std::cout << "compo " << i << "  charge " << comp.at(i).charge<< std::endl;
    ROOT::VecOps::RVec<int> index = comp.at(i).index;
    ROOT::VecOps::RVec<int> mother;
    ROOT::VecOps::RVec<int> motherPDG;

    for (size_t j = 0; j < index.size(); ++j) {

      //ROOT::VecOps::RVec<int> mcassoc = rp2mc.at(index.at(j));
      int mcassoc = rp2mc.at(index.at(j));
      //if (mcassoc.size()==1){
      //mother.push_back(mcassoc.at(0));
      int mother1=getMC_parent(0, mc.at(mcassoc), ind);
      int mother2=getMC_parent(1, mc.at(mcassoc), ind);
      
      mother.push_back(mother1);
      motherPDG.push_back(mc.at(mother1).PDG);
      //std::cout << "mother 1 "<<mother1<<"  mother2  " << mother2<< std::endl;
      //std::cout << " mc assoc j " << j << "  rp index  "<< index.at(j) << " mc index " << mcassoc <<  "  PDG ID  " << mc.at(mcassoc).PDG << "  charge "<< mc.at(mcassoc).charge<< " mc p="<<sqrt(pow(mc.at(mcassoc).momentum.z,2)+pow(mc.at(mcassoc).momentum.y,2)+pow(mc.at(mcassoc).momentum.x,2)) << "  rp p " << ReconstructedParticle::get_p(recop.at(index.at(j)))<<std::endl; 
      
      //std::cout << " mc assoc j " << j << "   " << mcassoc.at(0) <<  "  PDG ID  " << mc.at(mcassoc.at(0)).PDG << "  charge "<< mc.at(mcassoc.at(0)).charge<< "  px="<< mc.at(mcassoc.at(0)).momentum.x << "  py="<< mc.at(mcassoc.at(0)).momentum.y << "  pz="<< mc.at(mcassoc.at(0)).momentum.z << "  p="<<sqrt(pow(mc.at(mcassoc.at(0)).momentum.z,2)+pow(mc.at(mcassoc.at(0)).momentum.y,2)+pow(mc.at(mcassoc.at(0)).momentum.x,2))<<std::endl;
      //}
	//else std::cout <<"================================================================================================================MORE THAN 1 ASSOC"<<std::endl;
    }

    if (mother.size()>0){
      bool truthmatched=true;
      int tmpmother = mother.at(0);
      int tmpmotherpdg = motherPDG.at(0);
      for (size_t k = 1; k < mother.size(); ++k) {
	if (tmpmother!=mother.at(k) || tmpmotherpdg!=motherPDG.at(k))truthmatched=false;
      }

      if (truthmatched==true) {comp.at(i).mc_index=mother.at(0); }//std::cout <<"==============================mthchehhfewefkwefkwfwf"<<std::endl;}
      else comp.at(i).mc_index=-999;

    }


  }
  
    /*  for (size_t i = 0; i < rp2mc.size(); ++i) {
     std::cout <<"RP " << i << std::endl;
     for (size_t j = 0; j < rp2mc.at(i).size(); ++j) {
       std::cout << "  MC  " << rp2mc.at(i).at(j) << std::endl;
     

     }
     }*/
   return comp;
}

ROOT::VecOps::RVec<int> myUtils::get_compmc(ROOT::VecOps::RVec<FCCAnalysesComposite> in){

  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < in.size(); ++i)result.push_back(in.at(i).mc_index);
  return result;
}


/*ROOT::VecOps::RVec<FCCAnalysesComposite> myUtils::add_truthmatched(ROOT::VecOps::RVec<FCCAnalysesComposite> comp,
								   ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,  
								   ROOT::VecOps::RVec<int> mcind,
								   ROOT::VecOps::RVec<int> recoind){


  ROOT::VecOps::RVec<FCCAnalysesComposite> result;
  
  for (size_t i = 0; i < comp.size(); ++i) {
    ROOT::VecOps::RVec<int> index = i.index;
    for (size_t j = 0; j < index.size(); ++j) {

      

    }
  }

    if (parentindex+1>in.at(i).parents_end-in.at(i).parents_begin) {
      result.push_back(-999);
    }
    else {
      result.push_back(ind.at(in.at(i).parents_begin+parentindex));
    }
  }
  return result;
}

}*/

ROOT::VecOps::RVec<FCCAnalysesComposite> myUtils::build_Bu2D0Pi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
								ROOT::VecOps::RVec<FCCAnalysesComposite> d0, 
								ROOT::VecOps::RVec<int> pions){

  ROOT::VecOps::RVec<FCCAnalysesComposite> result;
  for (size_t i = 0; i < d0.size(); ++i) {
    ROOT::VecOps::RVec<int> d0index = d0.at(i).index;
    float kaoncharge = 0;
    //std::cout << "index sise "<< d0index.size() << " ind 0 " << d0index.at(0)<< " ind 1 " << d0index.at(1)  <<std::endl;
    //std::cout << " recop.at(index.at(0)) "<<recop.at(d0index.at(0)).type<< " recop.at(index.at(1)) "<<recop.at(d0index.at(1)).type<< std::endl;

    if (recop.at(d0index.at(0)).type==321)kaoncharge=recop.at(d0index.at(0)).charge;
    else if (recop.at(d0index.at(1)).type==321)kaoncharge=recop.at(d0index.at(1)).charge;
    else std::cout <<"huston there iis a problem no kaon found myUtils::build_Bu2D0Pi" <<std::endl;
    for (size_t j = 0; j < pions.size(); ++j) {
      if (ReconstructedParticle::get_p(recop.at(pions.at(j)))<1.)continue;
      if (kaoncharge!=recop.at(pions.at(j)).charge)continue;
    
      //Mass cut
      TLorentzVector tlvpion = ReconstructedParticle::get_tlv(recop.at(pions.at(j)));
      TLorentzVector tlvd0   = d0.at(i).particle;
      TLorentzVector tlvB = tlvpion+tlvd0;

      FCCAnalysesComposite B;
      ROOT::VecOps::RVec<int> index;
      index.push_back(d0index.at(0));
      index.push_back(d0index.at(1));
      index.push_back(pions.at(j));
      B.particle = tlvB;
      B.index = index;
      result.push_back(B);

      //if (fabs(tlvD0.M()-1.86483)>m_mass)continue;
 

    }
  }
  return result;
}


filter_PV::filter_PV(bool arg_pv):m_pv(arg_pv){};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> 
myUtils::filter_PV::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, 
			       ROOT::VecOps::RVec<int> index){

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;

  for (auto & p: in) {
    bool found=false;
    for (size_t i = 0; i < index.size(); ++i) {
      if (p.tracks_begin==index.at(i)){found=true; break;}
    }
    if (found==false && m_pv==false)result.push_back(p);
    else if (found==true && m_pv==true)result.push_back(p);
  }
  return result;
}


int myUtils::getFCCAnalysesComposite_N(ROOT::VecOps::RVec<FCCAnalysesComposite> in){
  return in.size();
}

ROOT::VecOps::RVec<float> myUtils::getFCCAnalysesComposite_mass(ROOT::VecOps::RVec<FCCAnalysesComposite> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.particle.M());
  }
  return result;
}
ROOT::VecOps::RVec<TLorentzVector> myUtils::getFCCAnalysesComposite_particle(ROOT::VecOps::RVec<FCCAnalysesComposite> in){
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    result.push_back(p.particle);
  }
  return result;
}


ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> myUtils::getFCCAnalysesComposite_index(ROOT::VecOps::RVec<FCCAnalysesComposite> in){
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  for (auto & p: in) {
    result.push_back(p.index);
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::VertexData> myUtils::getFCCAnalysesComposite_vertex(ROOT::VecOps::RVec<FCCAnalysesComposite> in){
  ROOT::VecOps::RVec<edm4hep::VertexData> result;
  for (auto & p: in) {
    result.push_back(p.vertex);
  }
  return result;
}

bool myUtils::isPV(edm4hep::ReconstructedParticleData recop, ROOT::VecOps::RVec<int> pvindex){

  for (size_t i = 0; i < pvindex.size(); ++i) {
    if (recop.tracks_begin==pvindex.at(i))return true;
  }
  return false;
}


build_composite_vertex::build_composite_vertex(int arg_n, int arg_charge, float arg_masslow, float arg_masshigh, float arg_p, bool arg_cc, bool arg_filterPV): m_n(arg_n),m_charge(arg_charge),m_masslow(arg_masslow),m_masshigh(arg_masshigh),m_p(arg_p),m_cc(arg_cc),m_filterPV(arg_filterPV){};
ROOT::VecOps::RVec<FCCAnalysesComposite> 
myUtils::build_composite_vertex::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
					     ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
					     ROOT::VecOps::RVec<int> in,
					     ROOT::VecOps::RVec<int> pvindex){

  ROOT::VecOps::RVec<FCCAnalysesComposite> result;

  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  for (size_t i = 0; i < in.size(); ++i) {
    if (ReconstructedParticle::get_p(recop.at(in.at(i)))<m_p) continue;
    if (m_filterPV && isPV(recop.at(in.at(i)), pvindex) ) continue;
    builder.integer(in.at(i));
  }
  std::shared_ptr<awkward::Content> array = builder.snapshot();  
  //std::cout << array.get()->tojson(false, 1)<<std::endl;
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(m_n, false, nullptr, awkward::util::Parameters(), 0, 0);
  int64_t length = comb->length();


  //loop over combinations
  for (int64_t i=0;i<length;i++){
    //std::cout <<"mew comb"<<std::endl;
    awkward::ContentPtr item = comb.get()->getitem_at(i);
    awkward::Record* recitem = dynamic_cast<awkward::Record*>(item.get());
    std::vector<std::shared_ptr<awkward::Content>> contentvec = recitem->contents();
    //loop over items of the comb
    ROOT::VecOps::RVec<int> tmpvec;

    for (size_t j=0;j<contentvec.size();j++){
      awkward::NumpyArray* numpyraw = dynamic_cast<awkward::NumpyArray*>(contentvec.at(j).get());
      int64_t lengthnp = numpyraw->length();

      //loop over the items of the items and get the data (if nested array)
      for (int64_t k=0;k<lengthnp;k++){
	awkward::ContentPtr item2 = numpyraw->getitem_at(k);
	awkward::NumpyArray* npitem = dynamic_cast<awkward::NumpyArray*>(item2.get());	
	int32_t value = *reinterpret_cast<int32_t*>(npitem->data());
	if (k==0)tmpvec.push_back(value);
	else tmpvec.push_back(value);
      }
      //in case the data structure is a simple array (and not an array with a nested array)
      if (lengthnp<0){
	int32_t value = *reinterpret_cast<int32_t*>(numpyraw->data());
	tmpvec.push_back(value);
      }
    }

    int charge=0;
    for (size_t k=0;k<tmpvec.size();k++){
      charge+=recop[tmpvec.at(k)].charge;
      //std::cout << "charge in builing " <<recop[tmpvec.at(k)].charge << "  px="<<recop[tmpvec.at(k)].momentum.x<< "  py="<<recop[tmpvec.at(k)].momentum.y<< "   pz="<<recop[tmpvec.at(k)].momentum.z<< "  p=" << ReconstructedParticle::get_p(recop[tmpvec.at(k)])<<std::endl;
    }
    if (m_cc==true && fabs(charge)!=fabs(m_charge))continue;
    if (m_cc==false && charge!=m_charge)continue;
    
    float mass=build_invmass(recop,tmpvec);
    if (mass<m_masslow)continue;
    if (mass>m_masshigh)continue;
        
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles;
    for (size_t k=0;k<tmpvec.size();k++){
      recoparticles.push_back(recop.at(tmpvec.at(k)));
    }
 
    VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterSimple::VertexFitter(0,recoparticles, tracks );
    float chi2 = TheVertex.vertex.chi2;
  
    if (chi2<0.01)continue;
    if (chi2>10.)continue;

    //std::cout << "SELECTED----------------"<<std::endl;
    //std::cout << "charge " << charge << std::endl;
    //std::cout << "mass   " << mass << std::endl;
    //std::cout << "chi2   " << chi2 << std::endl;
    //std::cout << "ntrk   " << TheVertex.ntracks << std::endl;

    FCCAnalysesComposite comp;
    ROOT::VecOps::RVec<int> index;
    for (size_t k=0;k<tmpvec.size();k++)index.push_back(tmpvec.at(k));
    comp.vertex = TheVertex.vertex;
    comp.particle = build_tlv(recop,tmpvec);
    comp.index = index;
    comp.charge = charge;
    
    result.push_back(comp);
  }

  
  return result;
}

build_D0::build_D0(float arg_mass, float arg_p, bool arg_filterPV): m_mass(arg_mass),m_p(arg_p),m_filterPV(arg_filterPV){};
ROOT::VecOps::RVec<FCCAnalysesComposite> 
myUtils::build_D0::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
			       ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
			       ROOT::VecOps::RVec<int> pions,
			       ROOT::VecOps::RVec<int> kaons,
			       ROOT::VecOps::RVec<int> pvindex){
 
  ROOT::VecOps::RVec<FCCAnalysesComposite> result;

  /*awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  builder.beginlist();
  for (size_t i = 0; i < pions.size(); ++i) builder.integer(pions.at(i));
  builder.endlist();
  builder.beginlist();
  for (size_t i = 0; i < kaons.size(); ++i) builder.integer(kaons.at(i));
  builder.endlist();

  std::shared_ptr<awkward::Content> array = builder.snapshot();  
  std::cout << array.get()->tojson(false, 1)<<std::endl;
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(2, false, nullptr, awkward::util::Parameters(), 2, 0);
  int64_t length = comb->length();

  for (int64_t i = 0; i < length; ++i){
    std::shared_ptr<awkward::Content> selection = comb.get()->getitem_at(i);
    std::cout << "i="<<i<<selection.get()->tojson(false, 1) << std::endl;
    }*/


  for (size_t i = 0; i < pions.size(); ++i){
    //pion p cut
    if (ReconstructedParticle::get_p(recop.at(pions.at(i)))<m_p)continue;
    if (m_filterPV && isPV(recop.at(pions.at(i)), pvindex) ) continue;
    for (size_t j = 0; j < kaons.size(); ++j){
      //kaon p cut
      if (ReconstructedParticle::get_p(recop.at(kaons.at(j)))<m_p)continue;
      if (m_filterPV && isPV(recop.at(kaons.at(j)), pvindex) ) continue;
      //std::cout << "i " << i << "  j " << j << "  pion a i " << pions.at(i) << "  kaons at j "<< kaons.at(j) << " nrecop  " << recop.size()<< std::endl;
      //charge cut
      int charge=recop.at(pions.at(i)).charge + recop.at(kaons.at(j)).charge;
      if (charge!=0)continue;

      //Mass cut
      TLorentzVector tlvpion = ReconstructedParticle::get_tlv(recop.at(pions.at(i)));
      TLorentzVector tlvkaon = ReconstructedParticle::get_tlv(recop.at(kaons.at(j)));
      TLorentzVector tlvD0 = tlvpion+tlvkaon;
      if (fabs(tlvD0.M()-1.86483)>m_mass)continue;
      
      //vertex cut
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> seltracks;
      seltracks.push_back(recop.at(pions.at(i)));
      seltracks.push_back(recop.at(kaons.at(j)));
      VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterSimple::VertexFitter(0,seltracks, tracks );
      float chi2 = TheVertex.vertex.chi2;
      
      if (chi2<0.01)continue;
      if (chi2>10.)continue;
      
      FCCAnalysesComposite D0;
      ROOT::VecOps::RVec<int> index;
      index.push_back(pions.at(i));
      index.push_back(kaons.at(j));
      D0.charge=charge;
      //std::cout << "in d0 builder pion Index " << pions.at(i) << " type " << recop.at(pions.at(i)).type << "  kaon index " <<kaons.at(j)<<" type " << recop.at(kaons.at(j)).type  <<std::endl;
      D0.vertex = TheVertex.vertex;
      D0.particle = tlvD0;
      D0.index = index;
      result.push_back(D0);
    }
  }
  
  return result;
}


  sel_PID::sel_PID( int arg_PDG): m_PDG(arg_PDG){} ;
ROOT::VecOps::RVec<int> 
myUtils::sel_PID::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop){
  ROOT::VecOps::RVec<int> result;
  for (size_t i = 0; i < recop.size(); ++i) {
    if (recop.at(i).type==m_PDG)
      result.push_back(i);
  }
  return result;
}


ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> 
myUtils::PID(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
	     ROOT::VecOps::RVec<int> recind, 
	     ROOT::VecOps::RVec<int> mcind, 
	     ROOT::VecOps::RVec<edm4hep::MCParticleData> mc){


  for (size_t i = 0; i < recind.size(); ++i) {
    
    //id a pion
    if (fabs(mc.at(mcind.at(i)).PDG)==211){
      recop.at(recind.at(i)).type = 211;
      recop.at(recind.at(i)).mass = 0.13957039;
      recop.at(recind.at(i)).energy = sqrt(pow(recop.at(recind.at(i)).momentum.x,2) + 
					   pow(recop.at(recind.at(i)).momentum.y,2) + 
					   pow(recop.at(recind.at(i)).momentum.z,2) + 
					   pow(recop.at(recind.at(i)).mass,2));
    }
    //id a kaon
    else if (fabs(mc.at(mcind.at(i)).PDG)==321){
      recop.at(recind.at(i)).type = 321;
      recop.at(recind.at(i)).mass = 0.493677;
      recop.at(recind.at(i)).energy = sqrt(pow(recop.at(recind.at(i)).momentum.x,2) + 
					   pow(recop.at(recind.at(i)).momentum.y,2) + 
					   pow(recop.at(recind.at(i)).momentum.z,2) + 
					   pow(recop.at(recind.at(i)).mass,2));
    }
    //id a proton
    else if (fabs(mc.at(mcind.at(i)).PDG)==2212){
      recop.at(recind.at(i)).type = 2212;
      recop.at(recind.at(i)).mass = 0.938272081;
      recop.at(recind.at(i)).energy = sqrt(pow(recop.at(recind.at(i)).momentum.x,2) + 
					   pow(recop.at(recind.at(i)).momentum.y,2) + 
					   pow(recop.at(recind.at(i)).momentum.z,2) + 
					   pow(recop.at(recind.at(i)).mass,2));
    }
  }
  return recop;
}




ROOT::VecOps::RVec<float> myUtils::awkwardtest(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,  
					       ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
					       ROOT::VecOps::RVec<int> recind, 
					       ROOT::VecOps::RVec<int> mcind, 
					       ROOT::VecOps::RVec<edm4hep::MCParticleData> mc){
  
  ROOT::VecOps::RVec<float> result;
  ROOT::VecOps::RVec<int> rp_ind;
  ROOT::VecOps::RVec<int> tk_ind;

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> seltracks = VertexingUtils::selTracks(0.,3.,0.,3.)( recop, tracks);
  VertexingUtils::FCCAnalysesVertex ThePVertex = VertexFitterSimple::VertexFitter(0,seltracks, tracks );

  int PV_ntrk   = ThePVertex.ntracks;
  float PV_chi2 = ThePVertex.vertex.chi2;
  ROOT::VecOps::RVec<int> reco_ind = ThePVertex.reco_ind;

  std::cout << "ntracks PV " << PV_ntrk << " nreco ind " <<reco_ind.size() << std::endl;

  for (size_t i = 0; i < recop.size(); ++i) {
    auto & p = recop[i];
    if (p.tracks_begin<tracks.size()) {
      if(std::find(reco_ind.begin(), reco_ind.end(), p.tracks_begin) != reco_ind.end()) continue;
      rp_ind.push_back(i);
      tk_ind.push_back(p.tracks_begin);
    }
  }

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco;
  for (size_t i = 0; i < rp_ind.size(); ++i) {
    reco.push_back(recop[rp_ind.at(i)]);
  }
  std::cout <<"beofre"<<std::endl;
  ROOT::VecOps::RVec<int> pions = ReconstructedParticle2MC::selRP_PDG_index(211,true)(recind, mcind, recop, mc) ;
  ROOT::VecOps::RVec<int> kaons = ReconstructedParticle2MC::selRP_PDG_index(321,true)(recind, mcind, recop, mc) ;
  
  std::cout << "n pions " << pions.size() << std::endl;
  std::cout << "n kaons " << kaons.size() << std::endl;

  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  for (size_t i = 0; i < rp_ind.size(); ++i) {
    builder.beginlist();
    builder.integer(rp_ind.at(i));
    builder.integer(tk_ind.at(i));
    builder.endlist();
  }

  std::shared_ptr<awkward::Content> array = builder.snapshot();  
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(2, false, nullptr, awkward::util::Parameters(), 0, 0);
  int64_t length = comb->length();
 
  std::cout << "recarray ntracks     : " << tracks.size()<< "  length 2 comb " << length << std::endl;

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> vec_rp;
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> vec_tk;
  
  //loop over combinations
  for (int64_t i=0;i<length;i++){
    awkward::ContentPtr item = comb.get()->getitem_at(i);
    awkward::Record* recitem = dynamic_cast<awkward::Record*>(item.get());
    std::vector<std::shared_ptr<awkward::Content>> contentvec = recitem->contents();
    //loop over items of the comb
    ROOT::VecOps::RVec<int> tmpvec_rp;
    ROOT::VecOps::RVec<int> tmpvec_tk;

    for (size_t j=0;j<contentvec.size();j++){
      awkward::NumpyArray* numpyraw = dynamic_cast<awkward::NumpyArray*>(contentvec.at(j).get());
      int64_t lengthnp = numpyraw->length();

      //loop over the items of the items and get the data (if nested array)
      for (int64_t k=0;k<lengthnp;k++){
	awkward::ContentPtr item2 = numpyraw->getitem_at(k);
	awkward::NumpyArray* npitem = dynamic_cast<awkward::NumpyArray*>(item2.get());	
	int32_t value = *reinterpret_cast<int32_t*>(npitem->data());
	if (k==0)tmpvec_rp.push_back(value);
	else tmpvec_tk.push_back(value);
      }
      //in case the data structure is a simple array (and not an array with a nested array)
      if (lengthnp<0){
	int32_t value = *reinterpret_cast<int32_t*>(numpyraw->data());
      }
    }

    int charge=0;
    bool pcut=false;
    for (size_t k=0;k<tmpvec_rp.size();k++){
      charge+=recop[tmpvec_rp.at(k)].charge;
      if (ReconstructedParticle::get_p(recop[tmpvec_rp.at(k)])<2.)pcut=true;
    }
    if (charge!=0)continue;
    if (pcut==true)continue;
    
    //PID
    //if( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(0)) != pions.end()) && (std::find(pions.begin(), pions.end(), tmpvec_rp.at(1)) != pions.end())) continue;
    //if( (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(0)) != kaons.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(1)) != kaons.end())) continue;

    float mass=0;
    if ( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(0)) != pions.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(1)) != kaons.end())){
      TLorentzVector tlvpion;
      tlvpion.SetXYZM(recop.at(tmpvec_rp.at(0)).momentum.x, recop.at(tmpvec_rp.at(0)).momentum.y, recop.at(tmpvec_rp.at(0)).momentum.z, 0.13957039000000002);
      TLorentzVector tlvkaon;
      tlvkaon.SetXYZM(recop.at(tmpvec_rp.at(1)).momentum.x, recop.at(tmpvec_rp.at(1)).momentum.y, recop.at(tmpvec_rp.at(1)).momentum.z, 0.49367700000000003);
      tlvpion+=tlvkaon;
      mass=tlvpion.M();
    }
    else if ( (std::find(pions.begin(), pions.end(), tmpvec_rp.at(1)) != pions.end()) && (std::find(kaons.begin(), kaons.end(), tmpvec_rp.at(0)) != kaons.end())){
      TLorentzVector tlvpion;
      tlvpion.SetXYZM(recop.at(tmpvec_rp.at(1)).momentum.x, recop.at(tmpvec_rp.at(1)).momentum.y, recop.at(tmpvec_rp.at(1)).momentum.z, 0.13957039000000002);
      TLorentzVector tlvkaon;
      tlvkaon.SetXYZM(recop.at(tmpvec_rp.at(0)).momentum.x, recop.at(tmpvec_rp.at(0)).momentum.y, recop.at(tmpvec_rp.at(0)).momentum.z, 0.49367700000000003);
      tlvpion+=tlvkaon;
      mass=tlvpion.M();
    }
    else mass=-9999;
    //float mass=build_invmass(recop,tmpvec_rp);
    


    if (fabs(mass-1.86483)>0.05)continue;



    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles;
    ROOT::VecOps::RVec<edm4hep::TrackState> thetracks;
    for (size_t k=0;k<tmpvec_rp.size();k++){
      recoparticles.push_back(recop.at(tmpvec_rp.at(k)));
      thetracks.push_back(tracks.at(tmpvec_tk.at(k)));
    }
 
    //VertexingUtils::FCCAnalysesVertex TheVertexActs = VertexFitterActs::VertexFitterFullBilloir(recoparticles, tracks );
    VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterSimple::VertexFitter(0,recoparticles, tracks );
    float chi2 = TheVertex.vertex.chi2;
  
    if (chi2<0.01)continue;
    if (chi2>10.)continue;

    std::cout << "SELECTED----------------"<<std::endl;
    std::cout << "charge " << charge << std::endl;
    std::cout << "mass   " << mass << std::endl;
    std::cout << "chi2   " << chi2 << std::endl;
    std::cout << "ntrk   " << TheVertex.ntracks << std::endl;
    vec_rp.push_back(tmpvec_rp);
    vec_tk.push_back(tmpvec_tk);
    result.push_back(mass);
  }

  std::cout << "nresults " << result.size()<<std::endl;
  return result;
}


float myUtils::build_invmass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, ROOT::VecOps::RVec<int> index){
  float result=0;
  TLorentzVector tlv;
  for (size_t i=0;i<index.size();i++){
    TLorentzVector tmp_tlv = ReconstructedParticle::get_tlv(recop[index.at(i)]);
    tlv+=tmp_tlv;
  }
  return tlv.M();
}

TLorentzVector myUtils::build_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, ROOT::VecOps::RVec<int> index){
  float result=0;
  TLorentzVector tlv;
  for (size_t i=0;i<index.size();i++){
    TLorentzVector tmp_tlv = ReconstructedParticle::get_tlv(recop[index.at(i)]);
    tlv+=tmp_tlv;
  }
  return tlv;
}



build_tau23pi::build_tau23pi(int arg_charge, float arg_masslow, float arg_masshigh, float arg_p, float arg_angle, bool arg_cc, bool arg_filterPV, bool arg_rho):m_charge(arg_charge),m_masslow(arg_masslow),m_masshigh(arg_masshigh),m_p(arg_p),m_angle(arg_angle),m_cc(arg_cc),m_filterPV(arg_filterPV),m_rho(arg_rho){};
ROOT::VecOps::RVec<FCCAnalysesComposite> 
myUtils::build_tau23pi::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
				    ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
				    ROOT::VecOps::RVec<int> in,
				    ROOT::VecOps::RVec<int> pvindex){

  ROOT::VecOps::RVec<FCCAnalysesComposite> result;

  awkward::ArrayBuilder builder(awkward::ArrayBuilderOptions(1024, 2.0));
  for (size_t i = 0; i < in.size(); ++i) {
    if (ReconstructedParticle::get_p(recop.at(in.at(i)))<m_p) continue;
    if (m_filterPV && isPV(recop.at(in.at(i)), pvindex) ) continue;
    builder.integer(in.at(i));
  }
  std::shared_ptr<awkward::Content> array = builder.snapshot();  
  //std::cout << array.get()->tojson(false, 1)<<std::endl;
  std::shared_ptr<awkward::Content> comb  = array.get()->combinations(3, false, nullptr, awkward::util::Parameters(), 0, 0);
  int64_t length = comb->length();


  //loop over combinations
  for (int64_t i=0;i<length;i++){
    //std::cout <<"mew comb"<<std::endl;
    awkward::ContentPtr item = comb.get()->getitem_at(i);
    awkward::Record* recitem = dynamic_cast<awkward::Record*>(item.get());
    std::vector<std::shared_ptr<awkward::Content>> contentvec = recitem->contents();
    //loop over items of the comb
    ROOT::VecOps::RVec<int> tmpvec;

    for (size_t j=0;j<contentvec.size();j++){
      awkward::NumpyArray* numpyraw = dynamic_cast<awkward::NumpyArray*>(contentvec.at(j).get());
      int64_t lengthnp = numpyraw->length();

      //loop over the items of the items and get the data (if nested array)
      for (int64_t k=0;k<lengthnp;k++){
	awkward::ContentPtr item2 = numpyraw->getitem_at(k);
	awkward::NumpyArray* npitem = dynamic_cast<awkward::NumpyArray*>(item2.get());	
	int32_t value = *reinterpret_cast<int32_t*>(npitem->data());
	if (k==0)tmpvec.push_back(value);
	else tmpvec.push_back(value);
      }
      //in case the data structure is a simple array (and not an array with a nested array)
      if (lengthnp<0){
	int32_t value = *reinterpret_cast<int32_t*>(numpyraw->data());
	tmpvec.push_back(value);
      }
    }
    int charge=0;
    for (size_t k=0;k<tmpvec.size();k++)
      charge+=recop[tmpvec.at(k)].charge;
    
    if (m_cc==true && fabs(charge)!=fabs(m_charge))continue;
    if (m_cc==false && charge!=m_charge)continue;
    
    float mass=build_invmass(recop,tmpvec);
    if (mass<m_masslow)continue;
    if (mass>m_masshigh)continue;

    if (m_rho){
      ROOT::VecOps::RVec<int> tmpvec_rho;
      if (recop[tmpvec.at(0)].charge!=recop[tmpvec.at(1)].charge){
	tmpvec_rho.push_back(tmpvec.at(0));
	tmpvec_rho.push_back(tmpvec.at(1));
	float mass_rho=build_invmass(recop,tmpvec_rho);
	std::cout <<"rho mass comd 1 " << mass_rho << std::endl;
	if (mass_rho<0.6)continue;
	if (mass_rho>0.9)continue;
      }
      else if (recop[tmpvec.at(0)].charge!=recop[tmpvec.at(2)].charge){
	tmpvec_rho.push_back(tmpvec.at(0));
	tmpvec_rho.push_back(tmpvec.at(2));
	float mass_rho=build_invmass(recop,tmpvec_rho);
	std::cout <<"rho mass comd 2 " << mass_rho << std::endl;
	if (mass_rho<0.6)continue;
	if (mass_rho>0.9)continue;
      }
      else if (recop[tmpvec.at(1)].charge!=recop[tmpvec.at(2)].charge){
	tmpvec_rho.push_back(tmpvec.at(1));
	tmpvec_rho.push_back(tmpvec.at(2));
	float mass_rho=build_invmass(recop,tmpvec_rho);
	std::cout <<"rho mass comd 3 " << mass_rho << std::endl;
	if (mass_rho<0.6)continue;
	if (mass_rho>0.9)continue;
      }
      else
	std::cout <<"unpexted things happening build_tau23pi::build_tau23pi" <<std::endl;
    }
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles;
    for (size_t k=0;k<tmpvec.size();k++){
      recoparticles.push_back(recop.at(tmpvec.at(k)));
    }
 
    VertexingUtils::FCCAnalysesVertex TheVertex = VertexFitterSimple::VertexFitter(0,recoparticles, tracks );
    float chi2 = TheVertex.vertex.chi2;
  
    if (chi2<0.01)continue;
    if (chi2>10.)continue;

    //std::cout << "SELECTED----------------"<<std::endl;
    //std::cout << "charge " << charge << std::endl;
    //std::cout << "mass   " << mass << std::endl;
    //std::cout << "chi2   " << chi2 << std::endl;
    //std::cout << "ntrk   " << TheVertex.ntracks << std::endl;

    FCCAnalysesComposite comp;
    ROOT::VecOps::RVec<int> index;
    for (size_t k=0;k<tmpvec.size();k++)index.push_back(tmpvec.at(k));
    comp.vertex = TheVertex.vertex;
    comp.particle = build_tlv(recop,tmpvec);
    comp.index = index;
    comp.charge = charge;
    
    result.push_back(comp);
  }

  
  return result;
}
