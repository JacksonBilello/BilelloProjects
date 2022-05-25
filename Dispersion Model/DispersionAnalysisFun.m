function [bayTraj, lunaTrajs, out3, out4, lunaImpactTs, lunaImpactPos] = DispersionAnalysisFun(g_,h_,satM_,bayM_, phi_, theta_, K_,DX_,k_,dx_,nCols_,nRows_,r_,RPS_)
    G = [0,0,-g_];                  %gravity vector (m/s^2)
    h = h_;                         %initial height (m)
    
    satM = satM_;                   %mass of one lunasat (kg)
    bayM = bayM_;                   %mass of the lunasat bay (kg)
    
    phi = (90-phi_)*pi/180;              %angle off of vertical (radians)
    theta = theta_;                 %azimuth angle (always 0º in this reference frame)
    
    K = K_;                         %launch spring spring rate (N/m)
    DX = DX_;                       %launch spring displacement (m)
    
    k = k_;                         %ejection spring spring rate (N/m)
    dx = dx_;                       %ejection spring displacement (m)
    
    nCols = nCols_;                 %number of stacks (always 4 in this case)
    nRows = nRows_;                 %number of luna sats per stack
    thickness = 0.00365;            %thickness of a luna sat m
    
    r = r_;                         %radius of the center of a luna sat (m)              
    RPS = RPS_;                     %rotational speed of the bay (Rot/s)
    
    liv = (RPS)*2*pi*r;             % Lunasat Linear velocity magnitude (m/s)
    
    % Calculations
    
    rowM = nCols*satM;                  % mass of a row of lunasats 
    satMTotal = nRows*rowM;             % mass of all lunasats
    M = bayM + satMTotal;               % total mass of lunasat bay (with all lunasats)
    N = nCols * nRows;                  % total number of lunasats
    springPE = (1/2)*K*DX^2;            % potential energy of compressed spring
    biv = sqrt(springPE * 2 / M);       % bay initial velocity calculation
    
    rotx = @(t) [1 0       0;...
                0  cos(t)  -sin(t);...
                0  sin(t)  cos(t)];

    roty = @(t) [cos(t)  0    -sin(t);...            % rotation matrices 
                 0       1    0;...                 % reference frame x - downrange, y - left, z - up
                 sin(t) 0    cos(t)] ;

    rotz = @(t) [cos(t)  -sin(t)  0;...
                 sin(t)  cos(t)   0;...
                 0       0        1];
    
    % Assume launch position on z axis. Initial launch coordinates
    Xb0 = [0,0,h];
    
    %Calculate Bay Initial Velocity Vector
    Vb0 = ([0,0,1]*biv)*roty(phi); % Bay initial velocity vector
    
    ejectRelPos = [0, 1, 0;...
                   1,  0, 0;...
                   0, -1, 0;...
                   -1, 0, 0]*r;
                                         %%%%%%NEED TO CHANGE
    ejectRelVel = [-1, 0, 0;...
                    0, 1, 0;...
                    1, 0, 0;...
                    0, -1, 0]*liv;
            
        
    syms Xb(t) Ab(t) eject1(t) eject2(t) eject3(t) eject4(t) Theta(t) XL1(et,t) XL2(et,t) XL3(et,t) XL4(et,t) bTraj(t)
    
    Theta(t) = RPS * t * 2*pi; %current rotational angle at time t (rad/s * s)
   
    Ab(t) = G;                  %gravitational acceleration
    
    Xb(t) = Xb0 + Vb0 * t + (1/2)*Ab(t)*t^2;        %bay position at time t
    
    bayTraj = Xb(t);                                %bay trajectory
    
    % Get Lunasat Ejection position
    
    ejectPos1(t) = (ejectRelPos(1,:)*rotz(Theta(t)))*roty(phi);           % gets rotational position as a function of launch angle and time
    ejectPos2(t) = (ejectRelPos(2,:)*rotz(Theta(t)))*roty(phi);           % take general position, first rotate about the y axis then about the z 
    ejectPos3(t) = (ejectRelPos(3,:)*rotz(Theta(t)))*roty(phi);           % matrix multiplication order is associative
    ejectPos4(t) = (ejectRelPos(4,:)*rotz(Theta(t)))*roty(phi);
                                                                          % need to check multiplication order
    ejectVel1(t) = (ejectRelVel(1,:)*rotz(Theta(t)))*roty(phi);           % gets velocity the same way
    ejectVel2(t) = (ejectRelVel(2,:)*rotz(Theta(t)))*roty(phi);
    ejectVel3(t) = (ejectRelVel(3,:)*rotz(Theta(t)))*roty(phi);
    ejectVel4(t) = (ejectRelVel(4,:)*rotz(Theta(t)))*roty(phi);             

    XL1(et,t) = (ejectPos1(et) + Xb(et)) + (ejectVel1(et) + Vb0) * t + (1/2)*G*t^2;         %(bay pos(et) + ejection pos(et))       
    XL2(et,t) = (ejectPos2(et) + Xb(et)) + (ejectVel2(et) + Vb0) * t + (1/2)*G*t^2;         % +(ejection vel(et) + bay initial vel)*time
    XL3(et,t) = (ejectPos3(et) + Xb(et)) + (ejectVel3(et) + Vb0) * t + (1/2)*G*t^2;         % 1/2 G t^2
    XL4(et,t) = (ejectPos4(et) + Xb(et)) + (ejectVel4(et) + Vb0) * t + (1/2)*G*t^2;         % X_o + V_o*t + 1/2*G*t^2

    %et is the elapsed time since the launch. This gives the proper
    %vector to the equations above to get the positions and velocites at
    %time of launch

    %t is the symbolic time vector in the equations above. allows us to
    %calculate the time of impact on the ground
    
    disp([XL1(0,0),XL2(0,0),XL3(0,0),XL4(0,0)])     %displays the positions at time = 0
    
    syms lunaTraj(et,t) lunaImpactPos;
    
    lunaTraj = [XL1(et,t); XL2(et,t); XL3(et,t); XL4(et,t)];
    lunaTrajs = [XL1(0,t); XL2(0,t); XL3(0,t); XL4(0,t)];

    lunaImpactTs = zeros(1,4);          %lunasat impact time
 
    syms traj(et,t) trajT(t) 
    n=1;
    lunaImpactPos = zeros(N,3);       %stores (x,y,z) landing coordinates of all the lunasats

    times = ejectionTimes(k,dx,satM*1000,nRows,thickness,RPS*60);
   
    for i = 1:nCols
       traj(et,t) = lunaTraj(i,:);              %one stack at a time ex. XL1(et,t) is the equation for 3D poition at a certain time
       for j = 1:nRows
           trajT(t) = traj(times(j),t);                 % uses ejection times function
                                                        % trajT(t) is now a 3D kinematic eqn with the correct rotations
           trajTZ = trajT(t);                           % assigns the symbolic eqn to call Z dim
           eqn = trajTZ(3) == 0;                        % eqn is set to z dimension = 0 of the parabolic trajectory 
           impact = double(solve(eqn,t));               % solves for t in z-axis kinematic eqn for when z = 0
           impactT = impact(2);                         % impact time of z axis equation, pulls second number as the other number will be negative
           impactPOS = double(trajT(impactT));          % (x,y,z) coordinates of landing location at time of landing
           lunaImpactPos(n,:) = impactPOS(:);           % add landing coordinates to array
           disp(n);
           n = n + 1;
       end
   end
       
    % Output ejection port locations at t=0 to check configuration
    out4 = [double(ejectPos1(0));double(ejectPos2(0));double(ejectPos3(0));double(ejectPos4(0))];
     
    % Solve for and extract bay impact time
    bayImpact = bayTraj(3)==0;                          % bayImpact eqn is z dim of bay trajectory = 0
    bayImpactT = solve(bayImpact,t,'Real',true);        % solves z dim eqn time variable for when z = 0
    bayImpactT = double(bayImpactT);                    % converts array to double
    bayImpactT = bayImpactT(2);                         % takes bay impact time as the second intercept as it is positive
    out3 = double(Xb(bayImpactT));                      % coordinates of bay impact
end

