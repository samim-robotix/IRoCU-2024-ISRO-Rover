#include <stdio.h>
#include <math.h>

#define PI 3.14159265359

int main() {
    double h = 0.001;
    double t_final = 20;
    double l1 = 0.22839;
    double l2 = 0.248;
    double th4 = 0.17; // 10 degrees
    double th5 = 0.26; // 15 degrees

    int iter = 0;

    double qx = 0.001;
    double qy = 0.001;
    double qz = 0.001;

    double th1 = atan(qy / qx);
    double th3 = acos((pow(qx, 2) + pow(qy, 2) + pow(qz, 2) - pow(l1, 2) - pow(l2, 2)) / (2 * l1 * l2));
    double th2 = atan((l1 + l2 * cos(th3)) / (l2 * sin(th3))) + atan((qx * cos(th1) + qy * sin(th1)) / qz);
    th4 = atan(((cos(th1) * sin(th2 + th3 + th4)) * cos(th1) + (sin(th1) * sin(th2 + th3 + th4)) * sin(th1)) / (cos(th2 + th3 + th4))) - th2 - th3;
    th5 = ((-cos(th1) * cos(th2 + th3 + th4) * sin(th5) - sin(th1) * cos(th5)) * cos(th1) - (cos(th1) * cos(th2 + th3 + th4) * cos(th5) - sin(th1) * sin(th5)) * sin(th1)) / ((-sin(th1) * cos(th2 + th3 + th4) * sin(th5) + cos(th1) * cos(th5)) * cos(th1) - (sin(th1) * cos(th2 + th3 + th4) * cos(th5) + cos(th1) * sin(th5)) * sin(th1));

    double r11, r12, r13, r21, r22, r23, r31, r32, r33;

    for (double i = 0; i <= t_final; i += h) {
        iter++;

        r11 = cos(th1) * cos(th2 + th3 + th4) * cos(5) - sin(th1) * sin(th5);
        r12 = -cos(th1) * cos(th2 + th3 + th4) * sin(5) - sin(th1) * cos(th5);
        r13 = cos(th1) * sin(th2 + th3 + th4);
        r21 = sin(th1) * cos(th2 + th3 + th4) * cos(th5) + cos(th1) * sin(th5);
        r22 = -sin(th1) * cos(th2 + th3 + th4) * sin(th5) + cos(th1) * cos(th5);
        r23 = sin(th1) * sin(th2 + th3 + th4);
        r23 = -sin(th2 + th3 + th4) * cos(th5);
        r31 = -sin(th2 + th3 + th4) * cos(th5);
        r32 = sin(th2 + th3 + th4) * sin(th5);
        r33 = cos(th2 + th3 + th4);

        qx = qx + i / 6000.0;
        qy = qy + i / 6000.0;
        qz = qz + i / 6000.0;

        th1 = atan(qy / qx);
        th2 = atan((l1 + l2 * cos(th3)) / (l2 * sin(th3))) + atan((qx * cos(th1) + qy * sin(th1)) / qz);
        th3 = acos((pow(qx, 2) + pow(qy, 2) + pow(qz, 2) - pow(l1, 2) - pow(l2, 2)) / (2 * l1 * l2));
        th4 = atan((r13 * cos(th1) + r23 * sin(th1)) / r33) - th2 - th3;
        th5 = (r12 * cos(th1) - r11 * sin(th1)) / (r22 * cos(th1) - r21 * sin(th1));

        // Print or store values as needed

        if (qx >= 10 && qy >= 10 && qz >= 10)
            break;
    }

    printf("final simulation time = %.2f\n", t_final);

    // Plotting code can be implemented using libraries like OpenGL or plotting libraries in C

    return 0;
}
