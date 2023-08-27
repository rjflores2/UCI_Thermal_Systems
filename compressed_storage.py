# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:21:45 2023

@author: rhl
"""
"Tank parameters:"
T_in_max = 80; # [deg C]
T_in_rated = 15; # [deg C]
P_in_rated = 345; # [bar]
cap_rated = 18; # [kg]

"Determination of H2 inlet temperature based on length of pipe:"

%% TANK DATA

outsidetemp=273+20;     % Outside temperature in K

Qin=100;                 % Constant heat flow to the tank (J/s)
finput=0.15;             % Constant mass flow into the tank (kg/s)
fout=0;                 % Constant mass flow out of the tank (kg/s)

vtank=205;              % Tank volume in liters
maxp=15;                % Tank maximum allowed pressure, in MPa

H2densini=3;            % Initial H2 density (g/L)
ttankini=45;            % Initial H2 temperature (K)

tinput=30;              % H2 input temperature



%% SIMULATION PARAMETERS

%   sampling
tstep=0.01;              % Time step in seconds
tsim=100;               % Duration of simulation in seconds

%% Constants
R=8.314;                % Universal gas constant [J/(mol*K)]
Rlit=0.0820578;         % Universal gas constant [L*atm/(mol*K)]
F=96485;                % Faraday's constant
H2hhv=141.7*10^6;       % Hydrogen fuel high heating value [J/kg]. = 286000 J/mol
H2lhv=119.96*10^6;      % Hydrogen fuel low heating value [J/kg].
xO2air=0.21;            % Molar fraction of oxigen in air
xN2air=0.79;            % Molar fraction of nytrogen in air
CpO2T=(28.91+30.30)/2;  % O2 (gas) molar heat capacity. We assume it as constant, using cp's mean value from 298.15K to 380K. [J/mol*K]
CpH2T=(28.84+29.15)/2;  % H2 (gas) molar heat capacity. We assume it as constant, using cp's mean value from 298.15K to 380K. [J/mol*K]


%% Resultant parameters

t=0:tstep:tsim;
vtankm3=vtank*0.001;        % tank volume in m3


%% REFPROP

RP=py.ctREFPROP.ctREFPROP.REFPROPFunctionLibrary('C:\Program Files (x86)\REFPROP');
MASSSI=RP.GETENUMdll(int8(0),'MASS BASE SI').iEnum;
iMass = int8(1); % 0: molar fractions; 1: mass fractions
iFlag = int8(0); % 0: don't call SATSPLN; 1: call SATSPLN
z = {1.0}; % mole fractions, here a pure fluid, so mole fraction of 1.0

%% Conversion factors
H2O_kg_mol=18.01528/1000; % Conversion of liquid water: 1 mol is equal to 0.1801528 kg
H2_kg_mol=2*1.00794/1000;
O2_kg_mol=2*15.9994/1000;

%% Initialization of variables
Qin=zeros(size(t))+Qin;     % assumed constant
fin=zeros(size(t));         % assumed constant
fout=zeros(size(t))+fout;   % assumed constant
Utank=zeros(1,size(t,2));
utank=zeros(1,size(t,2));
ttank=zeros(1,size(t,2));
ptank=zeros(1,size(t,2));
htank=zeros(1,size(t,2));
stank=zeros(1,size(t,2));
ssat0=zeros(1,size(t,2));
ssat1=zeros(1,size(t,2));
ptankbar=zeros(1,size(t,2));
mtank=zeros(1,size(t,2));
H2Qua=zeros(1,size(t,2));


%% Model t=t
% tstep 0
i=1;
fin(i)=finput;
netf(i)=fin(i)-fout(i);
mtank(i)=vtankm3*H2densini;
h2dens(i)=H2densini;
ttank(i)=ttankini;
% calculation of pressure [Pa]
r=RP.REFPROPdll('hydrogen','TD','P',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
o=double(r.Output);
ptank(i)=o(1);
ptankbar(i)=ptank(i)/100000;
% calculation of internal energy [J/kg]
r=RP.REFPROPdll('hydrogen','TD','E',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
o=double(r.Output);
utank(i)=o(1);
Utank(i)=utank(i)*mtank(i);
% calculation of tank's average enthalpy [J/kg]
r=RP.REFPROPdll('hydrogen','TD','H',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
o=double(r.Output);
htank(i)=o(1);
% calculation of tank's average entropy [J/kg]
r=RP.REFPROPdll('hydrogen','TD','S',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
o=double(r.Output);
stank(i)=o(1);
% calculation of quality [0=saturated liquid ; 1=saturated vapor]
r=RP.REFPROPdll('hydrogen','TD','QMOLE',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
o=double(r.Output);
H2Qua(i)=o(1);

wb = waitbar(0,sprintf('Please wait... %2.2f%%',0));  % Creation of progress bar

% simulaton loop
for i=2:1:size(t,2)
    if ptank(i-1)>maxp*1000000  % If pressure in the previous step exceeds the maximum allowed pressure, refueling stops
        fin(i)=0;
        netf(i)=fin(i)-fout(i);
        mtank(i)=mtank(i-1)+netf(i)*tstep;
        h2dens(i)=mtank(i)/(vtank*0.001);
        pinput=ptank(i-1)*1.1;
        % Calculation of input fluid's enthalpy
        r=RP.REFPROPdll('hydrogen','PT','H',MASSSI,iMass,iFlag,pinput,tinput,z);
        o=double(r.Output);
        hh2in=o(1);
        % Calculation of total internal energy inside of the tank
        Utank(i)=((fin(i).*hh2in-fout(i-1).*htank(i-1))*tstep+Qin(i-1)*tstep+Utank(i-1));
        utank(i)=Utank(i)./mtank(i);
        % Calculation of tank pressure
        r=RP.REFPROPdll('hydrogen','DE','P',MASSSI,iMass,iFlag,h2dens(i-1),utank(i),z);
        o=double(r.Output);
        ptank(i)=o(1);
        ptankbar(i)=ptank(i)/100000;
        % Calculation of tank temperature
        r=RP.REFPROPdll('hydrogen','DE','T',MASSSI,iMass,iFlag,h2dens(i-1),utank(i),z);
        o=double(r.Output);
        ttank(i)=o(1);
        % Calculation of tank's average enthalpy [J/kg]
        r=RP.REFPROPdll('hydrogen','PD','H',MASSSI,iMass,iFlag,ptank(i),h2dens(i-1),z);
        o=double(r.Output);
        htank(i)=o(1);
        % calculation of tank's average entropy [J/kg]
        r=RP.REFPROPdll('hydrogen','TD','S',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
        o=double(r.Output);
        stank(i)=o(1);
        % Calculation of tank's hydrogen vapor quality
        r=RP.REFPROPdll('hydrogen','PD','QMOLE',MASSSI,iMass,iFlag,ptank(i),h2dens(i-1),z);
        o=double(r.Output);
        H2Qua(i)=o(1);

    else     % If pressure in the previous step is below the maximum allowed pressure, refueling continues
        fin(i)=finput;
        netf(i)=fin(i)-fout(i);
        mtank(i)=mtank(i-1)+netf(i)*tstep;
        h2dens(i)=mtank(i)/(vtank*0.001);
        pinput=ptank(i-1)*1.1;
        % Calculation of input fluid's enthalpy
        r=RP.REFPROPdll('hydrogen','PT','H',MASSSI,iMass,iFlag,pinput,tinput,z);
        o=double(r.Output);
        hh2in=o(1);
        % Calculation of total internal energy inside of the tank
        Utank(i)=((fin(i).*hh2in-fout(i-1).*htank(i-1))*tstep+Qin(i-1)*tstep+Utank(i-1));
        utank(i)=Utank(i)./mtank(i);
        % Calculation of tank pressure
        r=RP.REFPROPdll('hydrogen','DE','P',MASSSI,iMass,iFlag,h2dens(i-1),utank(i),z);
        o=double(r.Output);
        ptank(i)=o(1);
        ptankbar(i)=ptank(i)/100000;
        % Calculation of tank temperature
        r=RP.REFPROPdll('hydrogen','DE','T',MASSSI,iMass,iFlag,h2dens(i-1),utank(i),z);
        o=double(r.Output);
        ttank(i)=o(1);
        % Calculation of tank's average enthalpy [J/kg]
        r=RP.REFPROPdll('hydrogen','PD','H',MASSSI,iMass,iFlag,ptank(i),h2dens(i-1),z);
        o=double(r.Output);
        htank(i)=o(1);
         % calculation of tank's average entropy [J/kg]
        r=RP.REFPROPdll('hydrogen','TD','S',MASSSI,iMass,iFlag,ttank(i),h2dens(i),z);
        o=double(r.Output);
        stank(i)=o(1);
        % Calculation of tank's hydrogen vapor quality
        r=RP.REFPROPdll('hydrogen','PD','QMOLE',MASSSI,iMass,iFlag,ptank(i),h2dens(i-1),z);
        o=double(r.Output);
        H2Qua(i)=o(1);
    end

% Update of progress bar
        waitbar(i/size(t,2),wb,sprintf('Please wait... %2.2f%%',(i/size(t,2)*100))); % Progress bar update

end
close(wb)

%% Post-processing

stank(stank<1)=stank(find(stank<1)-1); % Change negative values of stank for the previous value

% Calculation of saturation line for Ts diagram
Tsat=(0:0.01:35);
for k=1:1:size(Tsat,2)
    r=RP.REFPROPdll('hydrogen','TQ','S',MASSSI,iMass,iFlag,Tsat(k),0,z);
    o=double(r.Output);
    ssat0(k)=o(1);
end

for k=1:1:size(Tsat,2)
    r=RP.REFPROPdll('hydrogen','TQ','S',MASSSI,iMass,iFlag,Tsat(k),1,z);
    o=double(r.Output);
    ssat1(k)=o(1);
end


%% PLOTS

% uplot=round((H2utilization_plot-H2u(1))/(H2u(end)-H2u(1))*(size(H2u,2)-1)+1);

set(0, 'DefaultLineLineWidth', 1.5,'DefaultAxesXGrid','on','DefaultAxesYGrid','on');

figure;plot(t,mtank);
title('Mass H2 tank')
xlabel('time [s]')
ylabel('H2 mass [kg]')

figure;plot(t,ttank);
title('Temperature H2 tank')
xlabel('time [s]')
ylabel('H2 temp [K]')
% saveas(gcf,'temp.jpg')

figure;plot(t,ptankbar);
title('Pressure H2 tank')
xlabel('time [s]')
ylabel('H2 press [bar]')
% saveas(gcf,'press.jpg')

figure;plot(t,mtank/(vtank*0.001));
title('Density of H2 stored')
xlabel('time [s]')
ylabel('H2 density [g/L]')
% saveas(gcf,'dens.jpg')

figure;plot(t,H2Qua);
title('Vapor quality of H2 stored')
xlabel('time [s]')
ylabel('Vapor quality')
ylim([0 1]);
xlim([0 tsim]);
% saveas(gcf,'vq.jpg')

if tinput<=33           % if we allow phase change, we plot vapor quality
    figure;yyaxis left
    plot(t,ttank);
    title('Temperature H2 tank + vapor quality')
    xlabel('time [s]')
    ylabel('H2 temp [K]')
    yyaxis right
    plot(t,H2Qua)
    ylim([0 1]);
    legend('H2 temperature','Vapor quality')
    saveas(gcf,'TempQua.jpg')
end

figure;yyaxis left
plot(t,ttank);
title('H2 Temperature + pressure')
xlabel('time [s]')
ylabel('H2 temp [K]')
yyaxis right
plot(t,ptankbar)
ylabel('H2 press [bar]')
legend('H2 temperature','H2 pressure')
saveas(gcf,'TempPress.jpg')

% figure;plot(t,H2Qua);
% title('Vapor quality of H2 stored')
% xlabel('time [s]')
% ylabel('Vapor quality')

% figure;plot(mtank/(vtank*0.001),ttank,color='red');
% title('Temperature H2 tank')
% xlim([0 85]);
% ylim([0 100]);
% xlabel('H2 density [g/L]')
% ylabel('H2 temp [K]')

% figure;plot(mtank/(vtank*0.001),ptankbar);
% title('Pressure H2 tank')
% xlabel('H2 density [g/L]')
% ylabel('H2 press [bar]')
% xlim([0 85]);

figure;plot(stank/1000,ttank,ssat0(ssat0>0)/1000,Tsat(ssat0>0),ssat1(ssat1>0)/1000,Tsat(ssat1>0));
title('Hydrogen T-s diagram')
xlabel('Entropy [kJ/kg*K]')
ylabel('Temperature [K]')

hold on
plot(stank/1000,ttank, color='blue');
title('Hydrogen T-s diagram')
xlabel('Entropy [kJ/kg*K]')
ylabel('Temperature [K]')
plot(ssat0(ssat0>0)/1000,Tsat(ssat0>0),color='red');
plot(ssat1(ssat1>0)/1000,Tsat(ssat1>0),color='red')
saveas(gcf,'TSdiagram.jpg')