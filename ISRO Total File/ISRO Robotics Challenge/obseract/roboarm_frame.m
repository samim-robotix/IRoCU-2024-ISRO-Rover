% dhparams = [0   	pi/2	0.1   	0;
%             0.26	0       0       0;
%             0.24	0	    0  	    0;
%             0.24   	0	    0  	    0;];
        
dhparams = [0   	pi/2	0   	0;
            0.4318	0       0       0
            0.0203	-pi/2	0.15005	0;
            0   	pi/2	0.4318	0;];
   
robot = rigidBodyTree;

bodies = cell(4,1);
joints = cell(4,1);
for i = 1:4
    bodies{i} = rigidBody(['body' num2str(i)]);
    joints{i} = rigidBodyJoint(['jnt' num2str(i)],"revolute");
    setFixedTransform(joints{i},dhparams(i,:),"dh");
    bodies{i}.Joint = joints{i};
    if i == 1 % Add first body to base
        addBody(robot,bodies{i},"base")
    else % Add current body to previous body by name
        addBody(robot,bodies{i},bodies{i-1}.Name)
    end
end

showdetails(robot)

figure();
show(robot);