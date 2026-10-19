import pickle

with open('new_inv32.pkl', 'rb') as f:
    clf = pickle.load(f)

def joint_angles(x,y,z):
    return clf.predict([[x,y,z]])

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def inv_kine(X,Y,Z):
    angles = joint_angles(X,Y,Z)
    #print("Mapped Angles")
    J1 = translate(angles[0][0],-90,90,0,180)
    J2 = angles[0][1]
    J3 = translate(angles[0][2],-90,0,0,90)
    J4 = translate(angles[0][3],-90,0,90,180)
    J5 = 0

    return [J1,J2,J3,J4,J5]