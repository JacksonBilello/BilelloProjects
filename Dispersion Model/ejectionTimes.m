function [times] = ejectionTimes(k, dx, M_sat, nRows, thickness, RPM)
    %% Inputs
    % k - spring rate N/m
    % dx - spring displacement m
    % M_sat - mass of lunasat g
    % nRows - number of lunasats in a column
    % thickness - thickness of 1 lunasat m
    % RPM - RPM of bay
    %% Initialize
    M = nRows*M_sat*4 + 200;            %Initial mass of luna sats + push plate in grams
    R = 0.035;                          %luna sat radius (m)
    Uf = 0.5;                           %coefficient of friction (kapton and aluminum)
    W = RPM*0.10472;                    % rotational speed in rad/s
    times = zeros(1,nRows);             %Initialize the vector of ejection times for each row
    Mass = zeros(1,nRows);              %Mass change of the bay over time
    velocity = zeros(1,nRows);          %velocity of each row of luna sats
    accel = zeros(1, nRows);
    Fs = zeros(1, nRows);
    friction = zeros(1,nRows);
    Vi = 0;                             %Initial velocity of push plate before launch
    elapsedTime = 0;                    %Keeps track of the elapsed time  
    
   for i = 1:nRows                              %iterate through every row
       fric = Uf*(M/1000)*(W^2)*R;              %friction at speed   
       acc = ((k*dx) - fric)/(M/1000);          %acceleration of push plate (spring force - friction)/mass     
       Vf = sqrt((Vi^2) + 2*acc*thickness);     %final velocity after 1 displacement (m/s)
       t = (thickness*2)/(Vi+Vf);               %time elapsed over one displacement iteration
       elapsedTime = elapsedTime + t;           %elapsed time since last ejection
       times(i) = elapsedTime;                  %time stamp of when row is ejected
       velocity(i) = Vf;                        %Velocity at which lunasat is ejected
       Mass(i) = M;                             %Mass the LSB spring had to push
       accel(i) = acc;                          %acceleration over every time step
       Fs(i) = k*dx;
       friction(i) = fric;
       M = M - (M_sat*4);                       %New mass after 4 lunasat ejection
       dx = dx - thickness;                     %Spring compression - thickness of luna sat
       if (dx < 0)                              %if the spring as reached its equilibrium point, there is no more force
           dx = 0;
       end
       Vi = Vf;                                 %iterate velocity of plate
   end
   
   
   figure(1)
   yyaxis left 
   plot(1:nRows,times)
   ylabel('Ejection Times (s)')
   xlabel('rows ejected')
   
   yyaxis right
   plot(1:nRows,velocity)
   ylabel('Velocity (m/s)')
   
end