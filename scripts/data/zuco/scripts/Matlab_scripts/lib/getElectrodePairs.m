function [ pairs] = getElectrodePair(  )
%GETELECTRODEPAIR Summary of this function goes here
%   Detailed explanation goes here

pairs{1,1}='E22';pairs{1,2}='E9'; %FP1/2
pairs{2,1}='E26';pairs{2,2}='E2'; %AF7/8
pairs{3,1}='E23';pairs{3,2}='E3'; %AF3/4
pairs{4,1}='E33';pairs{4,2}='E122'; %F7/8
pairs{5,1}='E27';pairs{5,2}='E123'; %F5/F6
pairs{6,1}='E19';pairs{6,2}='E4'; % F1/2
pairs{7,1}='E24';pairs{7,2}='E124'; %F3/4
pairs{8,1}='E34';pairs{8,2}='E116'; %FT7/FT8
pairs{9,1}='E28';pairs{9,2}='E117'; %FC5/FC6
pairs{10,1}='E20';pairs{10,2}='E118';
pairs{11,1}='E35';pairs{11,2}='E110';
pairs{12,1}='E29';pairs{12,2}='E111';
pairs{13,1}='E13';pairs{13,2}='E112';
pairs{14,1}='E30';pairs{14,2}='E105';
pairs{15,1}='E36';pairs{15,2}='E104';
pairs{16,1}='E41';pairs{16,2}='E103';
pairs{17,1}='E45';pairs{17,2}='E108';
pairs{18,1}='E46';pairs{18,2}='E102';
pairs{19,1}='E47';pairs{19,2}='E98';
pairs{20,1}='E42';pairs{20,2}='E93';
pairs{21,1}='E37';pairs{21,2}='E87';
pairs{22,1}='E53';pairs{22,2}='E86';
pairs{23,1}='E52';pairs{23,2}='E92';
pairs{24,1}='E51';pairs{24,2}='E97';
pairs{25,1}='E50';pairs{25,2}='E101';
pairs{26,1}='E60';pairs{26,2}='E85';
pairs{27,1}='E59';pairs{27,2}='E91';
pairs{28,1}='E58';pairs{28,2}='E96';
pairs{29,1}='E66';pairs{29,2}='E84';
pairs{30,1}='E65';pairs{30,2}='E90';
pairs{31,1}='E70';pairs{31,2}='E83';

%Pairs above are from older analysis, based Wang paper, however with 4
%additional electrodes within thies cluster

%Pais below are the remaining electrodes which build paris in the EGi
%system:
pairs{32,1}='E38';pairs{32,2}='E121';
pairs{33,1}='E44';pairs{33,2}='E114';
pairs{34,1}='E43';pairs{34,2}='E120';
pairs{35,1}='E39';pairs{35,2}='E115';
pairs{36,1}='E40';pairs{36,2}='E109';

pairs{37,1}='E57';pairs{37,2}='E100';
pairs{38,1}='E64';pairs{38,2}='E95';
pairs{39,1}='E69';pairs{39,2}='E89';
pairs{40,1}='E74';pairs{40,2}='E82';
pairs{41,1}='E71';pairs{41,2}='E76';
pairs{42,1}='E67';pairs{42,2}='E77';
pairs{43,1}='E61';pairs{43,2}='E78';
pairs{44,1}='E54';pairs{44,2}='E79';
pairs{45,1}='E31';pairs{45,2}='E80';
pairs{46,1}='E7';pairs{46,2}='E106';

pairs{47,1}='E12';pairs{47,2}='E5';
pairs{48,1}='E18';pairs{48,2}='E10';


end

