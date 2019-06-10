OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
U(1.570796, 0.000000, 3.141593) q[0];
U(0.000000, 0.000000, 0.785398) q[1];
U(0.000000, 0.000000, 0.785398) q[4];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, 0.785398) q[3];
CX q[3],q[4];
U(0.000000, 0.000000, 0.785398) q[0];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[0];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[1],q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
U(0.000000, 0.000000, -0.785398) q[15];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
CX q[1],q[0];
U(0.000000, 0.000000, 0.785398) q[15];
U(0.000000, 0.000000, -0.785398) q[1];
U(0.000000, 0.000000, -0.785398) q[0];
CX q[15],q[0];
CX q[15],q[2];
U(pi/2,0,pi) q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
CX q[1],q[2];
U(pi/2,0,pi) q[1];
U(1.570796, 0.000000, 3.141593) q[2];
CX q[1],q[0];
U(1.570796, 0.000000, 3.141593) q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
U(0.000000, 0.000000, 0.785398) q[2];
CX q[1],q[0];
U(pi/2,0,pi) q[2];
U(0.000000, 0.000000, 0.785398) q[0];
U(0.000000, 0.000000, 0.785398) q[1];
CX q[1],q[0];
U(pi/2,0,pi) q[1];
CX q[1],q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[1],q[0];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
CX q[1],q[2];
U(0.000000, 0.000000, -0.785398) q[0];
CX q[1],q[0];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[1];
U(0.000000, 0.000000, -0.785398) q[0];
U(pi/2,0,pi) q[2];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[1],q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[2];
U(1.570796, 0.000000, 3.141593) q[15];
CX q[1],q[2];
U(1.570796, 0.000000, 3.141593) q[15];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
U(0.000000, 0.000000, 0.785398) q[15];
U(1.570796, 0.000000, 3.141593) q[2];
U(0.000000, 0.000000, 0.785398) q[1];
U(0.000000, 0.000000, 0.785398) q[2];
U(pi/2,0,pi) q[1];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[3],q[4];
CX q[2],q[3];
U(0.000000, 0.000000, -0.785398) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[2],q[3];
U(0.000000, 0.000000, 0.785398) q[4];
U(0.000000, 0.000000, -0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[3],q[4];
CX q[2],q[3];
U(1.570796, 0.000000, 3.141593) q[4];
U(0.000000, 0.000000, 0.785398) q[4];
U(0.000000, 0.000000, 0.785398) q[3];
U(0.000000, 0.000000, 0.785398) q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
CX q[3],q[4];
CX q[1],q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
CX q[15],q[0];
U(0.000000, 0.000000, -0.785398) q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
CX q[1],q[0];
CX q[1],q[2];
U(0.000000, 0.000000, 0.785398) q[0];
U(0.000000, 0.000000, -0.785398) q[1];
U(0.000000, 0.000000, -0.785398) q[2];
U(pi/2,0,pi) q[0];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[1];
U(1.570796, 0.000000, 3.141593) q[0];
CX q[15],q[2];
U(0.000000, 0.000000, 0.785398) q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[2];
U(pi/2,0,pi) q[2];
CX q[1],q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
U(1.570796, 0.000000, 3.141593) q[2];
U(1.570796, 0.000000, 3.141593) q[1];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, 0.785398) q[1];
CX q[2],q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, -0.785398) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[3],q[4];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[3];
U(0.000000, 0.000000, -0.785398) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[3],q[4];
CX q[2],q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(1.570796, 0.000000, 3.141593) q[4];
CX q[2],q[3];
U(0.000000, 0.000000, 0.785398) q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, 0.785398) q[3];
U(0.000000, 0.000000, 0.785398) q[2];
CX q[3],q[4];
CX q[1],q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[3],q[4];
CX q[1],q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[3],q[4];
CX q[1],q[2];
CX q[3],q[4];
CX q[1],q[0];
CX q[2],q[3];
U(pi/2,0,pi) q[1];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, -0.785398) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[3],q[4];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[3];
U(0.000000, 0.000000, -0.785398) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[3],q[4];
CX q[2],q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(1.570796, 0.000000, 3.141593) q[4];
CX q[2],q[3];
U(1.570796, 0.000000, 3.141593) q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, 0.785398) q[4];
U(1.570796, 0.000000, 3.141593) q[3];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, 0.785398) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
CX q[1],q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[1],q[0];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
CX q[1],q[0];
CX q[1],q[2];
U(0.000000, 0.000000, -0.785398) q[0];
CX q[1],q[0];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[1];
U(0.000000, 0.000000, -0.785398) q[0];
U(pi/2,0,pi) q[2];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[15],q[0];
U(pi/2,0,pi) q[15];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[1],q[2];
CX q[1],q[0];
U(1.570796, 0.000000, 3.141593) q[2];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
U(0.000000, 0.000000, 0.785398) q[2];
CX q[1],q[0];
CX q[2],q[3];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[0];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
CX q[1],q[0];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[15],q[0];
CX q[3],q[4];
U(0.000000, 0.000000, 0.785398) q[0];
U(0.000000, 0.000000, 0.785398) q[15];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[15],q[0];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[15],q[14];
CX q[2],q[3];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[15],q[14];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, -0.785398) q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
CX q[3],q[4];
CX q[15],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[15],q[0];
CX q[2],q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[15],q[0];
CX q[2],q[3];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[15],q[0];
CX q[2],q[3];
U(pi/2,0,pi) q[3];
U(0.000000, 0.000000, 0.785398) q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(0.000000, 0.000000, -0.785398) q[4];
U(0.000000, 0.000000, -0.785398) q[3];
CX q[2],q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[3];
U(1.570796, 0.000000, 3.141593) q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(1.570796, 0.000000, 3.141593) q[4];
U(0.000000, 0.000000, 0.785398) q[3];
U(0.000000, 0.000000, 0.785398) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[3],q[14];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(0.000000, 0.000000, -0.785398) q[14];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[15],q[2];
CX q[15],q[14];
U(0.000000, 0.000000, 0.785398) q[2];
U(0.000000, 0.000000, -0.785398) q[15];
U(0.000000, 0.000000, -0.785398) q[14];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
CX q[2],q[3];
CX q[15],q[2];
CX q[15],q[14];
U(1.570796, 0.000000, 3.141593) q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
CX q[15],q[14];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
CX q[15],q[14];
CX q[3],q[14];
U(1.570796, 0.000000, 3.141593) q[3];
U(0.000000, 0.000000, 0.785398) q[14];
CX q[13],q[14];
U(0.000000, 0.000000, 0.785398) q[3];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[14];
CX q[13],q[14];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[14];
CX q[13],q[14];
U(pi/2,0,pi) q[13];
CX q[13],q[4];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[3],q[14];
U(0.000000, 0.000000, -0.785398) q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
CX q[13],q[14];
CX q[13],q[4];
U(0.000000, 0.000000, 0.785398) q[14];
U(0.000000, 0.000000, -0.785398) q[13];
U(0.000000, 0.000000, -0.785398) q[4];
U(pi/2,0,pi) q[14];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[13],q[14];
CX q[13],q[4];
U(1.570796, 0.000000, 3.141593) q[14];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[4];
CX q[13],q[4];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[4];
CX q[13],q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
