#include "TGraph.h"
#include "TString.h"

Bool_t b_DrawFilled= true;

TGraph* SimplifiedModels_7TeV(TString Model, Bool_t DrawFilled=true)
{
  b_DrawFilled= DrawFilled;
  if(Model.Contains("GG_direct")) return SimplifiedModels_7TeV_GG_direct();
  else if (Model.Contains("SS_direct")) return SimplifiedModels_7TeV_SS_direct();
  else if (Model.Contains("GG_onestep_X05")) return SimplifiedModels_7TeV_GG_onestep_x05();
  else if (Model.Contains("GG_onestep_LSP60")) return SimplifiedModels_7TeV_GG_onestep_LSP60();
  else if (Model.Contains("SS_onestep_X05")) return SimplifiedModels_7TeV_SS_onestep_x05();
  else if (Model.Contains("SS_onestep_LSP60_small")) return  SimplifiedModels_7TeV_SS_onestep_LSP60_small();
  else if (Model.Contains("SS_onestep_LSP60")) return SimplifiedModels_7TeV_SS_onestep_LSP60();
  else std::cout << Model << " not in the model list" << std::endl;
  
}

TGraph* SimplifiedModels_7TeV_GG_direct(){    
   TGraph *graph = new TGraph(74);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,64.375,22.04389819);
   graph->SetPoint(1,84.70280313,41.7);
   graph->SetPoint(2,93.125,49.84389819);
   graph->SetPoint(3,113.4528031,69.5);
   graph->SetPoint(4,121.875,77.64389819);
   graph->SetPoint(5,142.2028031,97.3);
   graph->SetPoint(6,142.2028031,125.1);
   graph->SetPoint(7,150.625,133.2438982);
   graph->SetPoint(8,170.9528031,152.9);
   graph->SetPoint(9,179.375,161.0438982);
   graph->SetPoint(10,199.7028031,180.7);
   graph->SetPoint(11,208.125,188.8438982);
   graph->SetPoint(12,228.4528031,208.5);
   graph->SetPoint(13,236.875,216.6438982);
   graph->SetPoint(14,257.093601,236.3);
   graph->SetPoint(15,265.625,244.5494919);
   graph->SetPoint(16,280.4512627,264.1);
   graph->SetPoint(17,294.375,277.5636486);
   graph->SetPoint(18,306.5040741,291.9);
   graph->SetPoint(19,323.125,307.9717126);
   graph->SetPoint(20,336.7464009,319.7);
   graph->SetPoint(21,351.875,334.3286975);
   graph->SetPoint(22,367.6095969,347.5);
   graph->SetPoint(23,380.625,360.0853289);
   graph->SetPoint(24,397.4933724,375.3);
   graph->SetPoint(25,409.375,386.7890173);
   graph->SetPoint(26,426.322014,403.1);
   graph->SetPoint(27,438.125,414.5129743);
   graph->SetPoint(28,455.0017993,430.9);
   graph->SetPoint(29,466.875,442.3808689);
   graph->SetPoint(30,484.7734532,458.7);
   graph->SetPoint(31,495.625,469.1929739);
   graph->SetPoint(32,515.8892774,486.5);
   graph->SetPoint(33,524.375,494.7053248);
   graph->SetPoint(34,548.7777731,514.3);
   graph->SetPoint(35,553.125,518.5035794);
   graph->SetPoint(36,581.875,522.9872579);
   graph->SetPoint(37,588.5682665,514.3);
   graph->SetPoint(38,589.2998995,486.5);
   graph->SetPoint(39,593.4830887,458.7);
   graph->SetPoint(40,610.625,446.5581341);
   graph->SetPoint(41,639.375,449.2483605);
   graph->SetPoint(42,668.125,448.4200317);
   graph->SetPoint(43,696.875,436.5055147);
   graph->SetPoint(44,715.2523188,430.9);
   graph->SetPoint(45,725.625,429.6719176);
   graph->SetPoint(46,744.2442613,430.9);
   graph->SetPoint(47,754.375,431.7061117);
   graph->SetPoint(48,783.125,436.9605466);
   graph->SetPoint(49,811.875,442.0523816);
   graph->SetPoint(50,839.0239206,430.9);
   graph->SetPoint(51,840.625,429.4902084);
   graph->SetPoint(52,869.375,411.640305);
   graph->SetPoint(53,898.125,406.080462);
   graph->SetPoint(54,914.3966803,403.1);
   graph->SetPoint(55,926.875,397.9876688);
   graph->SetPoint(56,944.184723,375.3);
   graph->SetPoint(57,955.625,358.5246948);
   graph->SetPoint(58,961.7976442,347.5);
   graph->SetPoint(59,973.1241977,319.7);
   graph->SetPoint(60,970.506716,291.9);
   graph->SetPoint(61,967.9280771,264.1);
   graph->SetPoint(62,977.9823421,236.3);
   graph->SetPoint(63,970.3069202,208.5);
   graph->SetPoint(64,957.1372407,180.7);
   graph->SetPoint(65,955.625,167.9015223);
   graph->SetPoint(66,953.323935,152.9);
   graph->SetPoint(67,955.625,145.6670048);
   graph->SetPoint(68,963.9885691,125.1);
   graph->SetPoint(69,955.625,111.4280012);
   graph->SetPoint(70,950.3381433,97.3);
   graph->SetPoint(71,936.0235113,69.5);
   graph->SetPoint(72,937.8282889,41.7);
   graph->SetPoint(73,950.549451,13.9);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
    
   return graph;
}

TGraph* SimplifiedModels_7TeV_SS_direct(){    
   TGraph *graph = new TGraph(51);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,64.375,22.04389819);
   graph->SetPoint(1,84.70280313,41.7);
   graph->SetPoint(2,93.125,49.84389819);
   graph->SetPoint(3,113.4528031,69.5);
   graph->SetPoint(4,121.875,77.64389819);
   graph->SetPoint(5,142.2028031,97.3);
   graph->SetPoint(6,142.2028031,125.1);
   graph->SetPoint(7,150.625,133.2438982);
   graph->SetPoint(8,170.9528031,152.9);
   graph->SetPoint(9,179.375,161.0438982);
   graph->SetPoint(10,199.7028031,180.7);
   graph->SetPoint(11,208.125,188.8438982);
   graph->SetPoint(12,228.2475785,208.5);
   graph->SetPoint(13,236.875,216.8423415);
   graph->SetPoint(14,255.140251,236.3);
   graph->SetPoint(15,265.625,246.4382965);
   graph->SetPoint(16,282.4690948,264.1);
   graph->SetPoint(17,294.375,275.6124926);
   graph->SetPoint(18,323.125,280.1352838);
   graph->SetPoint(19,351.875,274.1757194);
   graph->SetPoint(20,380.625,281.4941452);
   graph->SetPoint(21,409.375,283.1356723);
   graph->SetPoint(22,438.125,284.3945027);
   graph->SetPoint(23,466.875,280.7593791);
   graph->SetPoint(24,495.625,272.9694978);
   graph->SetPoint(25,524.375,264.9253007);
   graph->SetPoint(26,527.4655544,264.1);
   graph->SetPoint(27,553.125,258.4109218);
   graph->SetPoint(28,581.875,261.971704);
   graph->SetPoint(29,587.6169422,264.1);
   graph->SetPoint(30,610.625,270.6606192);
   graph->SetPoint(31,639.375,280.8202822);
   graph->SetPoint(32,666.3950395,291.9);
   graph->SetPoint(33,668.125,292.622736);
   graph->SetPoint(34,674.7129134,291.9);
   graph->SetPoint(35,696.875,287.4484);
   graph->SetPoint(36,725.625,279.9139235);
   graph->SetPoint(37,746.1204832,264.1);
   graph->SetPoint(38,754.375,252.3618429);
   graph->SetPoint(39,759.9961765,236.3);
   graph->SetPoint(40,755.3168396,208.5);
   graph->SetPoint(41,754.375,206.0768763);
   graph->SetPoint(42,744.8922766,180.7);
   graph->SetPoint(43,735.5991675,152.9);
   graph->SetPoint(44,744.7015449,125.1);
   graph->SetPoint(45,754.375,100.8113556);
   graph->SetPoint(46,755.6129347,97.3);
   graph->SetPoint(47,754.375,94.41115182);
   graph->SetPoint(48,743.9661555,69.5);
   graph->SetPoint(49,735.941132,41.7);
   graph->SetPoint(50,733.7263353,13.9);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
    
   return graph;
}   

TGraph* SimplifiedModels_7TeV_SS_onestep_LSP60(){    
   TGraph *graph = new TGraph(29);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   Int_t ci=TColor::GetColor("kBlue-10");
   
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,212.5,0.1421178898);
   graph->SetPoint(1,216.1163921,0.1438596456);
   graph->SetPoint(2,237.5,0.1526735642);
   graph->SetPoint(3,262.5,0.1597468198);
   graph->SetPoint(4,287.5,0.1659946379);
   graph->SetPoint(5,312.5,0.1649670414);
   graph->SetPoint(6,337.5,0.1566640304);
   graph->SetPoint(7,362.5,0.1483610194);
   graph->SetPoint(8,376.0534381,0.1438596456);
   graph->SetPoint(9,387.5,0.136188409);
   graph->SetPoint(10,401.0326471,0.1192982427);
   graph->SetPoint(11,412.5,0.1034261454);
   graph->SetPoint(12,418.3157033,0.09473683988);
   graph->SetPoint(13,437.5,0.0745570078);
   graph->SetPoint(14,442.4044518,0.07017543702);
   graph->SetPoint(15,462.5,0.05961427673);
   graph->SetPoint(16,479.2924219,0.04561403417);
   graph->SetPoint(17,462.5,0.04254469252);
   graph->SetPoint(18,437.5,0.03984008559);
   graph->SetPoint(19,412.5,0.03782583413);
   graph->SetPoint(20,387.5,0.0366076655);
   graph->SetPoint(21,362.5,0.03592608091);
   graph->SetPoint(22,337.5,0.03530171976);
   graph->SetPoint(23,312.5,0.03472766595);
   graph->SetPoint(24,287.5,0.0344668071);
   graph->SetPoint(25,276.153715,0.04561403417);
   graph->SetPoint(26,262.5,0.06039138124);
   graph->SetPoint(27,237.5,0.06098693705);
   graph->SetPoint(28,212.5,0.06163251287);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
 
   graph = new TGraph(83);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,337.5,0.917751346);
   graph->SetPoint(1,362.5,0.9244330444);
   graph->SetPoint(2,373.9823479,0.9298245369);
   graph->SetPoint(3,381.9473968,0.9543859398);
   graph->SetPoint(4,387.5,0.955997631);
   graph->SetPoint(5,412.5,0.9583896264);
   graph->SetPoint(6,437.5,0.9571656412);
   graph->SetPoint(7,462.5,0.9557918378);
   graph->SetPoint(8,485.7126809,0.9543859398);
   graph->SetPoint(9,487.5,0.9509771474);
   graph->SetPoint(10,496.9257577,0.9298245369);
   graph->SetPoint(11,512.5,0.9177496929);
   graph->SetPoint(12,526.4589056,0.905263134);
   graph->SetPoint(13,537.5,0.8956831879);
   graph->SetPoint(14,550.4789956,0.8807017312);
   graph->SetPoint(15,558.7923625,0.8561403283);
   graph->SetPoint(16,562.5,0.8456925281);
   graph->SetPoint(17,567.4454852,0.8315789255);
   graph->SetPoint(18,576.3782762,0.8070175226);
   graph->SetPoint(19,582.9953228,0.7824561198);
   graph->SetPoint(20,587.5,0.7647660391);
   graph->SetPoint(21,589.4307774,0.7578947169);
   graph->SetPoint(22,594.1641551,0.7333333141);
   graph->SetPoint(23,588.0382516,0.7087719112);
   graph->SetPoint(24,587.5,0.706742525);
   graph->SetPoint(25,582.7423803,0.6842105084);
   graph->SetPoint(26,577.5562572,0.6596491055);
   graph->SetPoint(27,572.370134,0.6350877027);
   graph->SetPoint(28,567.1840108,0.6105262998);
   graph->SetPoint(29,562.5,0.6001813119);
   graph->SetPoint(30,550.9565724,0.5859648969);
   graph->SetPoint(31,537.5,0.5699916149);
   graph->SetPoint(32,531.2157047,0.5614034941);
   graph->SetPoint(33,529.4851904,0.5368420912);
   graph->SetPoint(34,527.7546761,0.5122806884);
   graph->SetPoint(35,526.6875671,0.4877192855);
   graph->SetPoint(36,529.5766054,0.4631578827);
   graph->SetPoint(37,534.856596,0.4385964798);
   graph->SetPoint(38,512.5,0.4145124612);
   graph->SetPoint(39,510.5905027,0.414035077);
   graph->SetPoint(40,487.5,0.4082623319);
   graph->SetPoint(41,481.3183225,0.414035077);
   graph->SetPoint(42,476.3510598,0.4385964798);
   graph->SetPoint(43,462.5,0.4583198583);
   graph->SetPoint(44,457.8004141,0.4631578827);
   graph->SetPoint(45,437.5,0.4750980363);
   graph->SetPoint(46,416.0416004,0.4877192855);
   graph->SetPoint(47,412.5,0.4898023589);
   graph->SetPoint(48,387.5,0.5045066816);
   graph->SetPoint(49,374.2827867,0.5122806884);
   graph->SetPoint(50,362.5,0.5183002611);
   graph->SetPoint(51,337.5,0.5221142582);
   graph->SetPoint(52,312.5,0.5239723382);
   graph->SetPoint(53,287.5,0.5132511431);
   graph->SetPoint(54,281.5963303,0.5122806884);
   graph->SetPoint(55,262.5,0.4979243468);
   graph->SetPoint(56,261.0863932,0.5122806884);
   graph->SetPoint(57,262.5,0.5202519768);
   graph->SetPoint(58,267.921877,0.5368420912);
   graph->SetPoint(59,269.7976991,0.5614034941);
   graph->SetPoint(60,274.153352,0.5859648969);
   graph->SetPoint(61,270.7155374,0.6105262998);
   graph->SetPoint(62,262.5,0.6212653538);
   graph->SetPoint(63,254.5119098,0.6350877027);
   graph->SetPoint(64,240.6584245,0.6596491055);
   graph->SetPoint(65,237.5,0.6702475614);
   graph->SetPoint(66,235.3347507,0.6842105084);
   graph->SetPoint(67,237.5,0.6965779308);
   graph->SetPoint(68,248.3920985,0.7087719112);
   graph->SetPoint(69,237.5,0.728496253);
   graph->SetPoint(70,235.4851289,0.7333333141);
   graph->SetPoint(71,229.2528095,0.7578947169);
   graph->SetPoint(72,226.9031359,0.7824561198);
   graph->SetPoint(73,224.5534624,0.8070175226);
   graph->SetPoint(74,232.7098731,0.8315789255);
   graph->SetPoint(75,227.4799602,0.8561403283);
   graph->SetPoint(76,222.7463224,0.8807017312);
   graph->SetPoint(77,218.0126846,0.905263134);
   graph->SetPoint(78,237.5,0.9103661837);
   graph->SetPoint(79,262.5,0.912386361);
   graph->SetPoint(80,287.5,0.9095819369);
   graph->SetPoint(81,312.5,0.9109740939);
   graph->SetPoint(82,337.5,0.917751346);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
 
   return graph;
}


TGraph* SimplifiedModels_7TeV_SS_onestep_LSP60_small(){    
   TGraph *graph = new TGraph(29);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   Int_t ci=TColor::GetColor("kBlue-10");
   
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,212.5,0.1421178898);
   graph->SetPoint(1,216.1163921,0.1438596456);
   graph->SetPoint(2,237.5,0.1526735642);
   graph->SetPoint(3,262.5,0.1597468198);
   graph->SetPoint(4,287.5,0.1659946379);
   graph->SetPoint(5,312.5,0.1649670414);
   graph->SetPoint(6,337.5,0.1566640304);
   graph->SetPoint(7,362.5,0.1483610194);
   graph->SetPoint(8,376.0534381,0.1438596456);
   graph->SetPoint(9,387.5,0.136188409);
   graph->SetPoint(10,401.0326471,0.1192982427);
   graph->SetPoint(11,412.5,0.1034261454);
   graph->SetPoint(12,418.3157033,0.09473683988);
   graph->SetPoint(13,437.5,0.0745570078);
   graph->SetPoint(14,442.4044518,0.07017543702);
   graph->SetPoint(15,462.5,0.05961427673);
   graph->SetPoint(16,479.2924219,0.04561403417);
   graph->SetPoint(17,462.5,0.04254469252);
   graph->SetPoint(18,437.5,0.03984008559);
   graph->SetPoint(19,412.5,0.03782583413);
   graph->SetPoint(20,387.5,0.0366076655);
   graph->SetPoint(21,362.5,0.03592608091);
   graph->SetPoint(22,337.5,0.03530171976);
   graph->SetPoint(23,312.5,0.03472766595);
   graph->SetPoint(24,287.5,0.0344668071);
   graph->SetPoint(25,276.153715,0.04561403417);
   graph->SetPoint(26,262.5,0.06039138124);
   graph->SetPoint(27,237.5,0.06098693705);
   graph->SetPoint(28,212.5,0.06163251287);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
  
   return graph;
}

TGraph* SimplifiedModels_7TeV_SS_onestep_x05(){    
   TGraph *graph = new TGraph(19);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,305.5252616,19.5875);
   graph->SetPoint(1,297.8197676,48.7625);
   graph->SetPoint(2,316.6,62.37407582);
   graph->SetPoint(3,341.4,76.07901805);
   graph->SetPoint(4,342.9756887,77.9375);
   graph->SetPoint(5,355.3127851,107.1125);
   graph->SetPoint(6,366.2,115.2512462);
   graph->SetPoint(7,391,119.23208);
   graph->SetPoint(8,415.8,121.5381818);
   graph->SetPoint(9,440.6,130.6599845);
   graph->SetPoint(10,465.4,135.6640176);
   graph->SetPoint(11,490.2,128.5760133);
   graph->SetPoint(12,515,119.1524996);
   graph->SetPoint(13,528.7198116,107.1125);
   graph->SetPoint(14,539.8,87.80747718);
   graph->SetPoint(15,544.4973244,77.9375);
   graph->SetPoint(16,544.8928068,48.7625);
   graph->SetPoint(17,539.8,37.01794809);
   graph->SetPoint(18,531.6966638,19.5875);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
 
   graph = new TGraph(15);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,217.4,169.3656269);
   graph->SetPoint(1,241.6143878,194.6375);
   graph->SetPoint(2,242.2,195.3264208);
   graph->SetPoint(3,243.6030307,194.6375);
   graph->SetPoint(4,242.2,171.0484831);
   graph->SetPoint(5,241.3132725,165.4625);
   graph->SetPoint(6,242.2,163.8291601);
   graph->SetPoint(7,253.1987114,136.2875);
   graph->SetPoint(8,267,110.7151679);
   graph->SetPoint(9,268.5543814,107.1125);
   graph->SetPoint(10,267,99.29789882);
   graph->SetPoint(11,265.7278056,107.1125);
   graph->SetPoint(12,242.2,129.453886);
   graph->SetPoint(13,218.3252698,107.1125);
   graph->SetPoint(14,217.4,106.1614873);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
 
   
   graph = new TGraph(13);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,342.2702249,311.3375);
   graph->SetPoint(1,341.4,307.8077489);
   graph->SetPoint(2,334.7654741,282.1625);
   graph->SetPoint(3,322.3554556,252.9875);
   graph->SetPoint(4,316.6,241.8430942);
   graph->SetPoint(5,291.8,227.9973866);
   graph->SetPoint(6,286.595703,252.9875);
   graph->SetPoint(7,291.8,259.1098938);
   graph->SetPoint(8,311.17441,282.1625);
   graph->SetPoint(9,316.6,288.5452253);
   graph->SetPoint(10,341.0557298,311.3375);
   graph->SetPoint(11,341.4,311.7425034);
   graph->SetPoint(12,342.2702249,311.3375);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
  
   return graph;
}
  
TGraph* SimplifiedModels_7TeV_GG_onestep_x05(){    
   TGraph *graph = new TGraph(84);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,217.25,134.8208283);
   graph->SetPoint(1,227.4417455,154.4625);
   graph->SetPoint(2,228.1801862,181.6375);
   graph->SetPoint(3,234.1016714,208.8125);
   graph->SetPoint(4,241.75,217.2959012);
   graph->SetPoint(5,266.25,225.981422);
   graph->SetPoint(6,269.9207875,235.9875);
   graph->SetPoint(7,277.0701891,263.1625);
   graph->SetPoint(8,290.75,278.3359229);
   graph->SetPoint(9,315.25,277.3034827);
   graph->SetPoint(10,326.2239921,290.3375);
   graph->SetPoint(11,339.75,305.3403272);
   graph->SetPoint(12,351.0101708,317.5125);
   graph->SetPoint(13,364.25,332.1979023);
   graph->SetPoint(14,376.2202792,344.6875);
   graph->SetPoint(15,388.75,358.5852617);
   graph->SetPoint(16,401.8851268,371.8625);
   graph->SetPoint(17,413.25,384.4682318);
   graph->SetPoint(18,427.0943927,399.0375);
   graph->SetPoint(19,437.75,410.8565257);
   graph->SetPoint(20,452.3846281,426.2125);
   graph->SetPoint(21,462.25,437.1550095);
   graph->SetPoint(22,477.5800281,453.3875);
   graph->SetPoint(23,486.75,463.5586831);
   graph->SetPoint(24,504.4335661,480.5625);
   graph->SetPoint(25,511.25,488.1231772);
   graph->SetPoint(26,532.1408236,507.7375);
   graph->SetPoint(27,535.75,511.7407395);
   graph->SetPoint(28,557.3467122,507.7375);
   graph->SetPoint(29,560.25,487.773583);
   graph->SetPoint(30,560.6805204,480.5625);
   graph->SetPoint(31,560.25,479.3509175);
   graph->SetPoint(32,550.9433771,453.3875);
   graph->SetPoint(33,541.0557042,426.2125);
   graph->SetPoint(34,535.75,411.5695602);
   graph->SetPoint(35,530.5372762,399.0375);
   graph->SetPoint(36,515.0674059,371.8625);
   graph->SetPoint(37,511.25,363.2768407);
   graph->SetPoint(38,501.7308065,344.6875);
   graph->SetPoint(39,511.25,327.1190842);
   graph->SetPoint(40,535.75,331.0569857);
   graph->SetPoint(41,560.25,339.8130547);
   graph->SetPoint(42,574.5379339,344.6875);
   graph->SetPoint(43,584.75,346.9948611);
   graph->SetPoint(44,609.25,350.0139512);
   graph->SetPoint(45,633.75,352.2353462);
   graph->SetPoint(46,658.25,359.2293363);
   graph->SetPoint(47,682.75,367.6234219);
   graph->SetPoint(48,699.1972452,371.8625);
   graph->SetPoint(49,707.25,373.8787488);
   graph->SetPoint(50,731.75,374.7559179);
   graph->SetPoint(51,756.25,374.6179069);
   graph->SetPoint(52,780.75,377.182147);
   graph->SetPoint(53,805.25,375.8770049);
   graph->SetPoint(54,812.7218004,371.8625);
   graph->SetPoint(55,829.75,362.8419563);
   graph->SetPoint(56,854.25,360.0691544);
   graph->SetPoint(57,878.75,367.5663515);
   graph->SetPoint(58,897.0271158,371.8625);
   graph->SetPoint(59,903.25,373.2026714);
   graph->SetPoint(60,927.75,380.8492627);
   graph->SetPoint(61,952.25,381.7597141);
   graph->SetPoint(62,968.1429306,371.8625);
   graph->SetPoint(63,976.75,363.2641483);
   graph->SetPoint(64,984.4746829,344.6875);
   graph->SetPoint(65,978.9920726,317.5125);
   graph->SetPoint(66,976.75,310.7974978);
   graph->SetPoint(67,970.4512692,290.3375);
   graph->SetPoint(68,966.5232035,263.1625);
   graph->SetPoint(69,976.75,246.6909214);
   graph->SetPoint(70,986.6573965,235.9875);
   graph->SetPoint(71,988.7695756,208.8125);
   graph->SetPoint(72,987.509323,181.6375);
   graph->SetPoint(73,986.2490704,154.4625);
   graph->SetPoint(74,985.6084732,127.2875);
   graph->SetPoint(75,983.5685697,100.1125);
   graph->SetPoint(76,986.3744556,72.9375);
   graph->SetPoint(77,988.8037627,45.7625);
   graph->SetPoint(78,976.75,43.31799178);
   graph->SetPoint(79,952.25,39.50808096);
   graph->SetPoint(80,927.75,36.72141417);
   graph->SetPoint(81,903.25,23.35674538);
   graph->SetPoint(82,878.75,21.75175994);
   graph->SetPoint(83,865.2512426,18.5875);
   AddPointsAtEdges(graph);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
    
   return graph;
}

TGraph* SimplifiedModels_7TeV_GG_onestep_LSP60(){    
   TGraph *graph = new TGraph(15);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);
   graph->SetPoint(0,530.1763506,0.02104208875);
   graph->SetPoint(1,512.5,0.03839341908);
   graph->SetPoint(2,487.5,0.03839341908);
   graph->SetPoint(3,462.5,0.03839341908);
   graph->SetPoint(4,437.5,0.03839341908);
   graph->SetPoint(5,412.5,0.03839341908);
   graph->SetPoint(6,387.5,0.03839341908);
   graph->SetPoint(7,362.5,0.03839341908);
   graph->SetPoint(8,337.5,0.03839341908);
   graph->SetPoint(9,312.5,0.03839341908);
   graph->SetPoint(10,287.5,0.03839341908);
   graph->SetPoint(11,280.1763506,0.04558240646);
   graph->SetPoint(12,262.5,0.0629337368);
   graph->SetPoint(13,237.5,0.0629337368);
   graph->SetPoint(14,212.5,0.0629337368);
   //graph->Draw("same cf");
   TGraph *gr1= (TGraph*)graph->Clone("gr1");
  
   graph = new TGraph(52);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1);   
   graph->SetPoint(0,907.472273,0.9781144795);
   graph->SetPoint(1,894.0392159,0.9535741617);
   graph->SetPoint(2,893.0763762,0.929033844);
   graph->SetPoint(3,896.985158,0.9044935263);
   graph->SetPoint(4,901.5988483,0.8799532086);
   graph->SetPoint(5,912.5,0.863751182);
   graph->SetPoint(6,916.1161815,0.8554128909);
   graph->SetPoint(7,928.5022554,0.8308725732);
   graph->SetPoint(8,937.5,0.8153940055);
   graph->SetPoint(9,942.7676264,0.8063322555);
   graph->SetPoint(10,954.5014147,0.7817919378);
   graph->SetPoint(11,962.2692725,0.7572516201);
   graph->SetPoint(12,962.5,0.7562809376);
   graph->SetPoint(13,967.8448118,0.7327113023);
   graph->SetPoint(14,969.7838306,0.7081709846);
   graph->SetPoint(15,971.7228493,0.6836306669);
   graph->SetPoint(16,973.9824549,0.6590903492);
   graph->SetPoint(17,977.221647,0.6345500315);
   graph->SetPoint(18,980.6436804,0.6100097138);
   graph->SetPoint(19,984.0069235,0.5854693961);
   graph->SetPoint(20,987.3701665,0.5609290784);
   graph->SetPoint(21,987.5,0.5597737681);
   graph->SetPoint(22,990.4593757,0.5363887607);
   graph->SetPoint(23,988.9439288,0.511848443);
   graph->SetPoint(24,987.5,0.492015597);
   graph->SetPoint(25,987.1547222,0.4873081252);
   graph->SetPoint(26,985.3547694,0.4627678075);
   graph->SetPoint(27,983.4682649,0.4382274898);
   graph->SetPoint(28,979.7159112,0.4136871721);
   graph->SetPoint(29,974.4625029,0.3891468544);
   graph->SetPoint(30,968.9167704,0.3646065367);
   graph->SetPoint(31,963.3710378,0.340066219);
   graph->SetPoint(32,962.5,0.3377739472);
   graph->SetPoint(33,953.3073636,0.3155259013);
   graph->SetPoint(34,941.6338705,0.2909855836);
   graph->SetPoint(35,937.5,0.28215297);
   graph->SetPoint(36,930.0927085,0.2664452659);
   graph->SetPoint(37,919.3810328,0.2419049481);
   graph->SetPoint(38,912.5,0.2338841666);
   graph->SetPoint(39,902.6156812,0.2173646304);
   graph->SetPoint(40,887.5,0.1964033402);
   graph->SetPoint(41,885.6720974,0.1928243127);
   graph->SetPoint(42,873.1387176,0.168283995);
   graph->SetPoint(43,862.5,0.1474534197);
   graph->SetPoint(44,860.6053379,0.1437436773);
   graph->SetPoint(45,854.1999308,0.1192033596);
   graph->SetPoint(46,862.5,0.0948815577);
   graph->SetPoint(47,862.5835223,0.09466304188);
   graph->SetPoint(48,876.5013011,0.07012272417);
   graph->SetPoint(49,887.3017097,0.04558240646);
   graph->SetPoint(50,887.5,0.04485787303);
   graph->SetPoint(51,899.1850971,0.02104208875);
   //graph->Draw("same cf");
   TGraph *gr2= (TGraph*)graph->Clone("gr2");
   
   graph = new TGraph(15);
   graph->SetName("Graph");
   graph->SetTitle("Graph");
   graph->SetFillColor(kBlue-10);
   graph->SetLineColor(kGray+1); 
   graph->SetPoint(0,212.5,0.9362228314);
   graph->SetPoint(1,237.5,0.9362228314);
   graph->SetPoint(2,262.5,0.9362228314);
   graph->SetPoint(3,280.1763506,0.9535741617);
   graph->SetPoint(4,287.5,0.9607631491);
   graph->SetPoint(5,312.5,0.9607631491);
   graph->SetPoint(6,337.5,0.9607631491);
   graph->SetPoint(7,362.5,0.9607631491);
   graph->SetPoint(8,387.5,0.9607631491);
   graph->SetPoint(9,412.5,0.9607631491);
   graph->SetPoint(10,437.5,0.9607631491);
   graph->SetPoint(11,462.5,0.9607631491);
   graph->SetPoint(12,487.5,0.9607631491);
   graph->SetPoint(13,512.5,0.9607631491);
   graph->SetPoint(14,530.1763506,0.9781144795);
   //graph->Draw("same cf");
   TGraph *gr3= (TGraph*)graph->Clone("gr3");
   
   graph= ConnectSeparatedContours(gr1,gr2,gr3);
   if(b_DrawFilled) graph->Draw("same cf");
   else graph->Draw("same c");
 
   return graph;
}


void AddPointsAtEdges(TGraph *graph){   

   Double_t xfirst=0, yfirst=0;
   graph->GetPoint(0, xfirst,yfirst);
   
   Int_t N= graph->GetN();
   Double_t xlast=0, ylast=0;
   graph->GetPoint(N-1, xlast,ylast);


   TGraph *gr_tmp= (TGraph *) graph->Clone();
   if(yfirst<xfirst) graph->SetPoint(0,xfirst,-100);
   else if(xfirst<yfirst) graph->SetPoint(0,-100,yfirst);
   
   Double_t x,y;
   for(Int_t i=1; i<=N; ++i){
     gr_tmp->GetPoint(i-1,x,y);
     graph->SetPoint(i,x,y);
   }
  
   if(ylast<xlast) graph->SetPoint(N+1,xlast,-100);
   else if(xlast<ylast) graph->SetPoint(N+1,-100,ylast);
}

TGraph* ConnectSeparatedContours(TGraph *gr1,TGraph *gr2,TGraph *gr3){   
   
   Int_t N1= gr1->GetN();
   Int_t N2= gr2->GetN();
   Int_t N3= gr3->GetN();
   
   Double_t xlast=0, ylast=0;
   gr1->GetPoint(N1-1, xlast,ylast);
   TGraph *gr_tmp= (TGraph *) gr1->Clone();
   gr_tmp->SetPoint(N1,185,ylast);
   gr_tmp->SetPoint(N1+1,185,0.5);
    
   Double_t x=0, y=0;
   gr3->GetPoint(0,x,y);
   
   for(Int_t i=0; i<gr3->GetN(); ++i){
     gr3->GetPoint(i,x,y);
     gr_tmp->SetPoint(N1+i+1,x,y);
   }
   Int_t N= gr_tmp->GetN();
   gr_tmp->SetPoint(N,800.,1.);
   
   for(Int_t i=0; i<gr2->GetN(); ++i){
     gr2->GetPoint(i,x,y);
     gr_tmp->SetPoint(N+i+1,x,y);
   }
   
   return gr_tmp;
}
