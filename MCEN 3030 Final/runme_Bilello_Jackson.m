%Jackson Bilello
%Final Exam
%MCEN 3030
%12-13-20
close all
clear
clc

%% Question 1
fprintf('Question 1\n');
x = linspace(-2,2,500);
f = -5.74*x.^3 - 4.33*x.^2 + 7.26*x - 1.05;
figure(1)
plot(x,f)
hold on 
plot([-2 2],[0 0])
title('question 1')

%Bisection
xl = 0.5;
xu = 1;
iter = 1;
xr = xl;
maxi = 4;
T1 = zeros(3,5);
f = @(x) (-5.74*x.^3 - 4.33*x.^2 + 7.26*x - 1.05);

while(iter<maxi)
    T1(iter,1) = iter; 
    T1(iter,2) = xl; 
    T1(iter,3) = xr;  
    T1(iter,4) = xu;   
    T1(iter,5) = f(xr);
    xr = (xl + xu)/2;
    
    if(f(xl)*f(xr) < 0)
        xu = xr; 
    elseif(f(xr)*f(xu) < 0) 
        xl = xr; 
    end
    iter=iter+1;
end
T1

%Newton-Raphson
xl = -2;
xu = -1;
xOld = -2;
iter = 1;
T2 = zeros(3,5);
syms x
f = @(x) (-5.74*x.^3 - 4.33*x.^2 + 7.26*x - 1.05);
df_dx = diff(f,x);
while(iter < maxi) 
    fOrig = double(f(xOld));
    temp = subs(df_dx,x,xOld);
    fDer = double(temp);
    xNew = xOld - ((fOrig)/(fDer));
    T2(iter,1) = iter;
    T2(iter,2) = xl;
    T2(iter,3) = xNew;
    T2(iter,4) = xu;
    T2(iter,5) = f(xNew);
    xOld = xNew;
    iter = iter + 1;
end
T2


%% Question 2
fprintf('Question 2\n')
fprintf('To be accurate to 7 figures, our stopping error criteria would be 0.5*10^(2-7) which is %.2d \n',0.5*10^(-5));

xL=-1.5; 
xU=-0.5; 
Es=0.5*10^(-5);
maxi = 4;
iter = 1;
Ea = 100;
R = (sqrt(5)-1)/2;
d = R*(xU-xL); 
x1 = xL+d; 
x2 = xU-d; 
xOpt = x1;
T3 = zeros(3,4);
while(Ea>Es && iter < maxi)
    T3(iter,1) = iter;
    T3(iter,2) = xOpt;
    T3(iter,3) = f(xOpt);
    T3(iter,4) = Ea;
    if(f(x1) < f(x2))
        xL = x2; 
        d = R*(xU-xL);
        x1 = xL+d; 
        x2 = xU-d;
        xOpt = x1;
        Ea = (1-R)*abs((xU-xL)/(xOpt));
    else 
        xU = x1; 
        d = R*(xU-xL);
        x1 = xL+d;
        x2 = xU-d;
        
        xOpt = x2;
        Ea = (1-R)*abs((xU-xL)/(xOpt));
    end
    iter = iter+1;
end
T3
x = linspace(-2,2,500);
f = -5.74*x.^3 - 4.33*x.^2 + 7.26*x - 1.05;
figure(2)
plot(x,f)
hold on
plot(T3(:,2),T3(:,3),'o')
legend('f(x)','(x,f(x))')
title('question 2')


%% Question 3
fprintf('Question 3\n')
%steepest ascent 1 step
syms x y
f = -x.^2 - y.^2 + 2.*x -4.*y -5;
df_dx=diff(f,x);
df_dy=diff(f,y);
Xg=2.09;
Yg=-1.93;

    syms X Y h
    df_dx = subs(df_dx,x,Xg);
    df_dy = subs(df_dy,y,Yg);
    X = Xg + df_dx*h;
    Y = Yg + df_dy*h;
    g = subs(f,x,X);
    G = subs(g,y,Y);
    dG_dh = diff(G,h);
    hnew = double(solve(dG_dh==0,h));
    
    syms x y
    f = -x.^2 - y.^2 + 2.*x -4.*y -5;
    df_dx=diff(f,x);
    df_dy=diff(f,y);
    df_dx = subs(df_dx,x,Xg);
    df_dy = subs(df_dy,y,Yg);
    xstep = double(df_dx*hnew);
    ystep = double(df_dy*hnew);
    vecnorm = sqrt(xstep^2 + ystep^2);
    xunit = xstep/vecnorm;
    yunit = ystep/vecnorm;
    fprintf('First step will be in the direction of %.4fi + %.4fj\n',xunit,yunit);
   
    
    %b
syms x y
f = -x.^2 - y.^2 + 2.*x -4.*y -5;
df_dx=diff(f,x);
df_dy=diff(f,y);
Xg=2.09;
Yg=-1.93;

maxi = 100;
iter = 1;
Ea = 100;
Es = 0.05;


while(Ea > Es && iter < maxi)
    syms x y
    f = -x.^2 - y.^2 + 2.*x -4.*y -5;
    syms X Y h
    df_dx=diff(f,x);
    df_dy=diff(f,y);
    df_dx = subs(df_dx,x,Xg);
    df_dy = subs(df_dy,y,Yg);
    
    X = Xg + df_dx*h;
    Y = Yg + df_dy*h;
    g = subs(f,x,X);
    G = subs(g,y,Y);
    dG_dh = diff(G,h);
    hnew = double(solve(dG_dh==0,h));
    
   
    xNew = Xg + double(df_dx*hnew);
    yNew = Yg + double(df_dy*hnew);

    fOld = subs(f,x,Xg);
    fOld = subs(fOld,y,Yg);
    fOld = double(fOld);
    
    fNew = subs(f,x,xNew);
    fNew = subs(fNew,y,yNew);
    fNew = double(fNew);
    Ea = (fNew - fOld);
    Xg = xNew;
    Yg = yNew;
    iter = iter + 1;
end
xdist = 2.09 - xNew;
ydist = -1.93 - yNew;
totaldistance = sqrt(xdist^2 + ydist^2);
fprintf('The total distance travelled from point 1 to the max: %.4f\n',totaldistance);


%% Question 4
fprintf('Question 4\n')


% LU by hand
a = [2.5 1.1 0.92; 0.54 0.83 0.91; 0.16 1.6 0.34];
[~,n] = size(a);
L = eye(n,n);

for k = 1:1:n-1
    for i = k+1:1:n
        factor = a(i,k)/a(k,k);
        L(i,k) = factor;
        for j = k:1:n 
            a(i,j) = a(i,j) - factor*a(k,j);
        end
    end
end
fprintf('LU decomp by hand');
L
U = a

%Using lu
fprintf('LU Decomp using built in functions');
a = [2.5 1.1 0.92; 0.54 0.83 0.91; 0.16 1.6 0.34];
[L,U,P] = lu(a)

%Gauss seidel
fprintf('gauss Seidel method\n');
b = [0.75;2.8;0.79];


iter = 0;
maxi = 4;
[n,~] = size(a);
X = zeros(n,1);
T4 = zeros(3,3);
while(iter < maxi)
    iter = iter + 1;
    T4(iter,1) = X(1,1);
    T4(iter,2) = X(2,1);
    T4(iter,3) = X(3,1);
    for i = 1:n
        j = 1:n;
        j(i) = [];
        xTemp = X;
        xTemp(i) = [];
        
        X(i,1) = ( b(i,1) - sum(a(i,j)*xTemp) ) / a(i,i);
    end
    
end
T4

%% Question 5
fprintf('Question 5\n')
A = [2.5 1.1 0.92; 0.54 0.83 0.91; 0.16 1.6 0.34];
B = [0.75;2.8;0.79];

L1A = norm(A,1);
L2A = norm(A,2);
FroA = norm(A,'fro');
InfA = norm(A,'Inf');

fprintf('A norms:   L1      L2       Frobenius      Infinite\n')
fprintf('          %.4f     %.4f     %.4f       %.4f          \n',L1A,L2A,FroA,InfA);

L1B = norm(B,1);
L2B = norm(B,2);
InfB = norm(B,'Inf');

fprintf('B norms:   L1      L2       Infinite\n')
fprintf('          %.4f     %.4f     %.4f          \n',L1B,L2B,InfB);


%% Question 6
fprintf('Question 6\n')

I = [0.1, 1.3, 2.5, 3.7, 4.9, 6.1, 7.3, 8.5, 9.7, 11, 12];
V = [ 8.4, 3.6, 14, 23, 28, 43, 47, 56, 64, 70, 87];

figure(3)
plot(I,V)
hold on 
title('question 6')
xlabel('I')
ylabel('V')
hold on

sum1 = sum(I.*V); 
sum2 = sum(I);
sum3 = sum(V);
sum4 = sum(I.^2);


a1 = (11*sum1-sum2*sum3)/(11*sum4 - sum2.^2);
a0 = (sum(V)/11) - (a1*sum(I)/11);
Y_line=a1.*I+a0;
plot(I,Y_line)
fprintf('Using the slope of the regression line, resistance = %.4f ohms\n',a1);

Sr = sum((V - Y_line).^2);
Syx = sqrt(Sr/9)


%% Question 7
fprintf('Question 7\n')

x = linspace(0,10,100);
y1 = (9 - 5.5.*x)/3;
y2 = (6 - 1.1.*x)/2;
y3 = (4 - 1.*x)/2.5;

figure(4)
plot(x,y1,'r-')
hold on
plot(x,y2,'b-')
hold on
plot(x,y3,'g-')
hold on
plot([0 0],[0 20])
hold on
plot([0 20],[0 0])
xlim([0 6])
ylim([0,4])
title('question 7')
int = [5.5 3.0;1 2.5]\[9;4];
X = [0 1.636 int(1) 0];
Y = [0 0 int(2) 1.6];
patch(X,Y,'Blue')
hold on

f = -[2.2 3.3];
A = [5.5 3; 1.1 2; 1.0 2.5];
B = [9;6;4];
C = linprog(f,A,B);
F = 2.2*C(1) + 3.3*C(2);
fprintf('The maximum value of f(x,y) = %.4f is located at (%.4f,%.4f)\n',F,C(1),C(2))
plot(C(1),C(2),'co')


%% Question 8
fprintf('Question 8\n')
t1 = [0 3 6];
t2 = [7.5 8.5];
v1 = [13.698 12.358 12.109];
v2 = [13.06 12.612];
Int1 = trapz(t1,v1);
Int2 = trapz(t2,v2);
Int3 = (6-3)*(12.109 + 3*12.723 + 3*12.551 + 13.06)/8;
totD = Int1 + Int2 + Int3;
avgV = totD/8.5;
fprintf('Total distance flown: %.4f m, average velocity: %.4f m/s\n',totD,avgV)


%% Question 9
fprintf('Question 9\n')
x0 = [0.1 -0.4];
t = [0,5];
[t,x] = ode23(@myODE,t,x0);
figure(5)
plot(t,x(:,1))
hold on
plot(t,x(:,2))
hold on
plot([0 5],[0 0])
title('question 9')
xlabel('t')
ylabel('position and velocity')
legend('position (m)','velocity (m/s)')
ylim([-1.25 1.25])

%function @myODE is at EOF

%% Question 10

%1 
%a 101101 = 45
%b 101.011 = 5.375
%c 0.01101 = 0.40625

% 2. when multiplying two numbers like 0.12*0.12, a floating point will spit
% out 0.0144 while two fixed point numbers will spit out 0.014 because of
% rounding errors. Float points have much more range than a fixed point.

%3
%a m=1.5, b=2, exp=6 = 1.5*2^6 = 96
%b m=1.5, b=3.7, exp=2.5 = 1.5*3.7^2.5 = 39.49998

%% Question 11
fprintf('Question 11\n')

conductivity = 204.3;
specificHeat = 910;
Density = 2700;

Lx= 0.5;                             
Ly= 0.5;                             
Nx=25;                            
Ny=25;                             
T_initial= 0 ;                  
T_east   = 20 ;                   
T_west   = 0 ;                   
T_north  = 100 ;                   
T_south  = 0 ;                  
t_end=50 ;                        
dt=0.6 ;                           
tolerence = 0.5;                   
tolerence_ss= 0.001;      


k=1;                                              
err_SS_max(k)=1;                                   
err_SS_min(k)=1;                                          
dx=Lx/Nx;                                                                 
dy=Ly/Ny;                                                                  
n_time=round(t_end/dt);                                                    
alpha = conductivity/(specificHeat*Density);                              
T_max=max([T_east T_west T_north T_south T_initial]);                      
T_min=min([T_east T_west T_north T_south T_initial]);                      

Tss2=zeros(Nx+2,Ny+2);
Tss2(2:25,Ny+1)=T_north;
Tss2(2:25,Ny+2)=T_north;             % Redundant, it has no effect in calculations but is required in plotting section
Tss2(Nx+1,2:25)=T_east;
Tss2(Nx+2,2:25)=T_east;



T=zeros(Nx+2,Ny+2,75000);
T(2:25,Ny+1,:)= T_north;
T(2:25,Ny+2,:)= T_north;
T(Nx+1,2:25,:) = T_east;
T(Nx+2,2:25,:) = T_east;

k=1;
err_E_max(k)=100;                            
err_E_min(k)=100; 
Specnode = zeros(79135,1);
while err_E_max(k)>=tolerence
    for i=2:Nx
        for j=2:Ny
            
            if i == 2  %west
                T(i,j,k+1) =T(i,j,k)+dt*alpha*(((-2*T(i,j,k)+2*T(i+1,j,k))/dx^2)+((T(i,j-1,k)-2*T(i,j,k)+T(i,j+1,k))/dy^2));
            elseif j == 2   %south
                T(i,j,k+1) =T(i,j,k)+dt*alpha*(((T(i-1,j,k)-2*T(i,j,k)+T(i+1,j,k))/dx^2)+((-2*T(i,j,k)+2*T(i,j+1,k))/dy^2));
            else    %center nodes                                    
                T(i,j,k+1) =T(i,j,k)+dt*alpha*(((T(i-1,j,k)-2*T(i,j,k)+T(i+1,j,k))/dx^2)+((T(i,j-1,k)-2*T(i,j,k)+T(i,j+1,k))/dy^2));
                if(i==19 && j==6)
                    Specnode(k,1) = T(i,j,k+1);
                end
            end

        end
    end
    k=k+1;
    err_E_max(k)=abs(max(max(T(:,:,k)-Tss2)));        %calculate error
    err_E_min(k)=abs(min(min(T(:,:,k)-Tss2)));        %calculate error
    
    
end
T=T(:,:,1:k);                                            
SStime=k*dt;                                            
SSsteps=k; 

x=zeros(1,Nx+2);
y=zeros(1,Ny+2);
for i = 1:Nx+2
    x(i) =(i-1)*dx;
end
for i = 1:Ny+2
    y(i) =(i-1)*dy;
end

figure(6);
title('question 11 @ 50s');
surf(x,y,T(:,:,50))
colorbar
caxis([T_min T_max]);
view(90,-90);
xlim([0 Lx+dx]); xlabel('Length');
ylim([0 Ly+dy]); ylabel('Width');
zlim([T_min T_max]); zlabel('Temprature');

figure(7)
i = 1:79135;
plot(i,Specnode)
hold on
title('question 11')

%% Functions
function xd = myODE(~,x)
    k = 100; m = 1; c = 0.2;
    xd(1)=x(2);
    xd(2)=1/m*(-k.*x(1) - c.*x(2));
    xd = xd';
end