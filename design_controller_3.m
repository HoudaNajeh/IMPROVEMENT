yalmip('clear')
clear all; 
close all; clc;
syms U_c eta A_c rho_c c_c V_c 
syms A_t U_t rho c  V_ct V_t
syms  Tcout    Tcin    Toa   Fc   I 
syms Ttout Ttin Ft

 C_c   = rho*c*V_c;
 C_t   =  rho*c*V_t;   
 C_ct  =  rho_c*c_c*V_ct; 

% differential equations for solar collector and heat exchager 

state_1    =  (A_c*eta/C_c)*I + (-U_c*A_c/C_c)*((Tcin+Tcout)/2-Toa) + Fc/V_c*(Tcin-Tcout);           

state_2    =  (V_ct^-1)*Fc*(Tcout-Tcin) +(U_t*A_t/C_ct)*(Ttout-Tcin);

state_3    =  (V_t^-1)*Ft*(Ttin-Ttout) -(U_t*A_t/C_t)*(Ttout-Tcin); 

states = [state_1;state_2;state_3]; 

A_solar_tank=jacobian([state_1;state_2;state_3],[Tcout Tcin Ttout]);

B_solar_tank=jacobian([state_1;state_2;state_3],[Fc Ft I Toa Ttin]) ;


% substituting values                               
U_c      =          7;              % solar heat loss coefficient (W m-2 K-1)
eta      =        1.2;              % optical efficiency (dimentionaless)
A_c      =         2;               % solar collector plate surface area (m2)
rho_c    =       1043;              % solar collector fluid density (kg m-3)
c_c      =       4180;              % Solar collector plate specific heat (J kg °C)
V_c      =     0.0075;              % Solar collector fliud volume (m3)

A_t      =      0.5;              % area of hot water tank for heat exchange (m2)
U_t      =      250;            % solar heat loss coefficient (W m-2 K-1)
rho      =     1000;            % water density (kg m-3)
c        =     4200;            % water specific heat (J kg °C)
V_ct     =    0.075;            % solar fluid vomule to heat trannsfer (m3)
V_t      =    0.075;            % hot water tank volume (m3)

C_c   = rho*c*V_c;
C_t    =  rho*c*V_t;   
C_ct    =  rho_c*c_c*V_ct;   
            

% MPC data
nx = 3; % Number of states
nu = 2; % Number of inputs
ny = 2; % Number of outputs
nd=3;% Number of disturbances
Q = 10*eye(1);
R = 0.10*eye(2);
N = 5;
tsim = 50;

r=[2, 2.5]';
r_fct=[89, 50]'+r;
u_fct=[1.5e-5, 1.0e-5]';
d_fct=[1000, 20, 10]';
y_fct=[89, 50]';
umax= 6.5e-5;
umin= 0.5e-5;
xref=[89, 63.6, 50]'



implementedU = u_fct;
implementedY = y_fct;
distp_fct=[1000, 20, 10]';
U=u_fct; 
constraints_nom = [];
constraints_def=[];
objective_nom=0;
objective_def = 0;
%---without OP
xwtop = [0, 0, 0]';
ywtop = [0, 0]';
dwtop = [ 0, 0, 0]';
%---withOP
xx = [60;27.5;47.5];   % initial states operating point 
%xx=[89, 63.6, 50]';
uu = [1.5e-5;1e-5];    % initial inputs operating point
dd = d_fct;

for i = 1:5

    [distp,distt]    =   dist_predicition_N1(i,N)
    % linearized system at every instant 
    % states OP
    Tcout    =     xx(1); %initial states operating point 
    Tcin     =     xx(2); 
    Ttout    =     xx(3);    
    % Input OP
    Fc       =     uu(1,1);
    Ft       =     uu(2,1);    
%     Fc       =     U(1);
%     Ft       =     U(2);   
    % dist OP
    I        =     distt(1);
    Toa      =     distt(2); 
    Ttin     =     distt(3);                                                   
    % state space model 
    A_solar_tank_1      =     eval(A_solar_tank);
    B_solar_tank_1      =     eval(B_solar_tank(:,1:2));
    Bd_solar_tank_1     =     eval(B_solar_tank(:,3:5));
    C_solar_tank_1      =     [1,0,0;0,0,1];
    D_solar_tank_1      =     zeros(2,2);
    Ba=[B_solar_tank_1 ,  Bd_solar_tank_1];
    A= A_solar_tank_1 ;
    B=B_solar_tank_1 ;
    C=C_solar_tank_1 ;
    D=D_solar_tank_1 ;
    Da=[ D_solar_tank_1  zeros(2, 3)];
    %Da=[[D_solar_tank_1, zeros(2, 1)]', zeros(3, 3)]
    sys_nom=ss(A, Ba, C, Da);
    sysd_nom=c2d(sys_nom, 360);
    %controleur   
    
    for k = 1:N-1
           u = sdpvar(repmat(nu,1,N),repmat(1,1,N));%création de variables symboliques
           x = sdpvar(repmat(nx,1,N),repmat(1,1,N));
           y = sdpvar(repmat(ny,1,N),repmat(1,1,N));
           d = sdpvar(repmat(nd,1,N),repmat(1,1,N));
           objective_nom =   objective_nom + (r-C*x{k})'*Q*(r-C*x{k})+(u{k})'*R*(u{k})
           constraints_nom = [constraints_nom, x{k+1} == sysd_nom.A*x{k} + sysd_nom.B(:,1:2)*u{k}+sysd_nom.B(:,3:5)*d{k}];
           constraints_nom = [constraints_nom, y{k} == sysd_nom.C*x{k}];
           constraints_nom = [constraints_nom, -u_fct <= u{k}<= umax-u_fct];
           %constraints_nom = [constraints_nom, y{k}== r];
    
    end

    ops = sdpsettings('solver','fmincon');
    %ops = sdpsettings('verbose',0)
    controller_nom = optimizer(constraints_nom, objective_nom,ops,{x{1},[d{:}]},[u{:}]);     
    
   
    U = controller_nom{xwtop, distp-distp_fct}
    %without OP
    xwtop = sysd_nom.A*xwtop(:) + sysd_nom.B(:, 1:2)*U(1:2, 1)+sysd_nom.B(:,3:5)*(distt-d_fct)%; + sysd_nom.B(:, 1:2)*U(:, 1);
    y = sysd_nom.C*xwtop; 
    %with OP
    %xx=xx+xwtop;%
     %uu=uu+U(1:2, 1);
    %dd=dd-distt



    %implementedU = [implementedU U(:, 1)+u_fct];
    implementedY = [implementedY y+y_fct];
end  

figure(1)
subplot(2, 1, 1)
plot(implementedY(:, 1), 'b','lineWidth',1);
hold on;
plot(r_fct(1)*ones(1, tsim), 'r','lineWidth',1,'LineStyle','--')
ylabel('y1 (Tcout)');
title('System Outputs')
legend('Tcout','Tcout_{ref}')
%ylim([88.5 91.2]);
grid; xlabel('Time')
% 
% subplot(2, 1, 2)
% plot(implementedY(2, :), 'b');
% hold on;plot(r_fct(2)*ones(1, tsim), 'r','lineWidth',2,'LineStyle','--');
% ylabel('y2 (Ttout)');
% legend('Ttout','Ttout_{ref}')
% %ylim([49.5 53.55]);
% grid;  xlabel('Time')