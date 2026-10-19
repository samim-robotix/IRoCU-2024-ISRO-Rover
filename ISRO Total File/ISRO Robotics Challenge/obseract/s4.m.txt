%it has been considered that the initial position of the end effector
% is (0.01,0.01,0.01)m and final psition of the end effector is 
% (10,10,10)m. the code is written in such a way that when the 
% end effector reaches around (10,10,10) the code stops. 

clear all;
clc;

%step size
h = 0.001;

%final time in seconds
t_final = 20; %should not be considered as ultimate time of motion

%length of the link in m
l1=0.22839; %L1
l2=0.248; %L2

%value initialize
th4 = 0.17; %10 degree
th5 = 0.26; %15 degree

%iteration counter
iter=0;

%initial position of the end effector has been considered as (0,0,0)
qx = 0.001; %x co-ordinate of the end effector
qy = 0.001; %y co-ordinate of the end effector
qz = 0.001; %z co-ordinate of the end effector

%the initial value of the th1, th2, th3, th4 and th5 when end effector is at (0,0,0)
th1 = atan(qy / qx);
th3 = acos((qx^2+qy^2+qz^2 - l1^2 - l2^2)/(2*l1*l2));
th2 = atan((l1+l2*cos(th3))/(l2*sin(th3)))+atan((qx*cos(th1)+qy*sin(th1))/qz);
th4 = atan(((cos(th1)*sin(th2+th3+th4))*cos(th1) + (sin(th1)*sin(th2+th3+th4))*sin(th1))/(cos(th2+th3+th4))) - th2 - th3;
th5 = ((-cos(th1)*cos(th2+th3+th4)*sin(5)-sin(th1)*cos(th5))*cos(th1) - (cos(th1)*cos(th2+th3+th4)*cos(5)-sin(th1)*sin(th5))*sin(th1))/((-sin(th1)*cos(th2+th3+th4)*sin(th5) + cos(th1)*cos(th5))*cos(th1) - (sin(th1)*cos(th2+th3+th4)*cos(th5) + cos(th1)*sin(th5))*sin(th1));

for i = 0 : h : t_final

    iter = iter + 1; %updating the counter

    r11 = cos(th1)*cos(th2+th3+th4)*cos(5)-sin(th1)*sin(th5);
    r12 = -cos(th1)*cos(th2+th3+th4)*sin(5)-sin(th1)*cos(th5);
    r13 = cos(th1)*sin(th2+th3+th4);
    r21 = sin(th1)*cos(th2+th3+th4)*cos(th5) + cos(th1)*sin(th5);
    r22 = -sin(th1)*cos(th2+th3+th4)*sin(th5) + cos(th1)*cos(th5);
    r23 = sin(th1)*sin(th2+th3+th4);
    r23 = -sin(th2+th3+th4)*cos(th5);
    r31 = -sin(th2+th3+th4)*cos(th5);
    r32 = sin(th2+th3+th4)*sin(th5);
    r33 = cos(th2+th3+th4);

    %position of the end effector
    qx = qx+i/6000; %updating the position of the end effector
    qy = qy+i/6000; %divided by 6000 for slow increment
    qz = qz+i/6000; 

    th1 = atan(qy / qx);
    th2 = atan((l1+l2*cos(th3))/(l2*sin(th3)))+atan((qx*cos(th1)+qy*sin(th1))/qz);
    th3 = acos((qx^2+qy^2+qz^2 - l1^2 - l2^2)/(2*l1*l2));
    th4 = atan((r13*cos(th1) + r23*sin(th1))/r33) - th2 - th3;
    th5 = (r12*cos(th1) - r11*sin(th1))/(r22*cos(th1) - r21*sin(th1));

    %store the angle values in a column array
    th_1(iter,1) = rad2deg(th1); %rad2deg radian to degree converter
    th_2(iter,1) = rad2deg(th2);
    th_3(iter,1) = rad2deg(th3);
    th_4(iter,1) = rad2deg(th4);
    th_5(iter,1) = rad2deg(th5);

    %position of tne end effector
    q_x(iter, 1) = qx;
    q_y(iter, 1) = qy;
    q_z(iter, 1) = qz;

    total_time(iter,1) = i; %store the total time of the simulation

    if qx >= 10 %when the qx become 10m the simulation will stop
        break;
    end
end

disp("final simulation time=");
disp(i);

%plot the first joint angle behaviour
figure('Name','Th1','NumberTitle','off',"Color","white");
plot(total_time, th_1);
xlabel('Time (s)'); 
ylabel('Th1 (degree)');

%plot the second joint angle behaviour
figure('Name','Th2','NumberTitle','off',"Color","white");
plot(total_time, th_2);
xlabel('Time (s)');
ylabel('Th2 (degree)');

%plot the third joint angle behaviour
figure('Name','Th3','NumberTitle','off',"Color","white");
plot(total_time, th_3);
xlabel('Time (s)'); 
ylabel('Th3 (degree)');

%plot the fourth joint angle behaviour
figure('Name','Th4','NumberTitle','off',"Color","white");
plot(total_time, th_4);
xlabel('Time (s)'); 
ylabel('Th4 (degree)');

%plot the fifth joint angle behaviour
figure('Name','Th5','NumberTitle','off',"Color","white");
plot(total_time, th_5);
xlabel('Time (s)');
ylabel('Th5 (degree)');

%3D plot of the end effector position
figure('Name','End effector position','NumberTitle','off',"Color","white");
plot3(q_x, q_y, q_z);
xlabel('x-axis positioni'); 
ylabel('y-axis positioni');
zlabel('z-axis positioni');
