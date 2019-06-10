OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
CX q[1],q[0];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[1],q[2];
CX q[15],q[0];
CX q[6],q[5];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[1],q[2];
CX q[15],q[0];
CX q[6],q[5];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[0];
CX q[1],q[2];
CX q[5],q[4];
CX q[15],q[0];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[7];
CX q[2],q[3];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[5];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[13],q[4];
CX q[6],q[5];
CX q[8],q[7];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[9],q[8];
CX q[13],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[9],q[8];
CX q[13],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[8];
CX q[13],q[14];
CX q[6],q[7];
CX q[9],q[8];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[9];
CX q[13],q[14];
U(pi/2,0,pi) q[13];
U(pi/2,0,pi) q[14];
CX q[13],q[14];
CX q[15],q[14];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[3],q[14];
CX q[15],q[14];
CX q[3],q[14];
CX q[2],q[3];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
CX q[15],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[15],q[14];
CX q[1],q[2];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[2],q[3];
CX q[15],q[14];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
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
CX q[5],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[5],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[5],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
CX q[1],q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[5],q[4];
CX q[1],q[2];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[1];
U(pi/2,0,pi) q[2];
CX q[5],q[4];
CX q[1],q[2];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[2];
CX q[5],q[4];
CX q[3],q[4];
CX q[5],q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
CX q[3],q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[3];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[5],q[4];
CX q[3],q[14];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[14];
CX q[5],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
CX q[5],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[5];
CX q[2],q[3];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[2],q[3];
CX q[5],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[3];
CX q[5],q[4];
CX q[3],q[14];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[6],q[5];
CX q[2],q[3];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[5],q[4];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[5];
CX q[2],q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[5];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[3],q[14];
CX q[6],q[5];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[14];
CX q[5],q[4];
CX q[2],q[3];
CX q[15],q[14];
CX q[6],q[5];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[4];
CX q[15],q[14];
CX q[6],q[5];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[14];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[15],q[14];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[15],q[2];
CX q[6],q[5];
CX q[2],q[3];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[5];
CX q[6],q[7];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[5],q[4];
CX q[2],q[3];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[2],q[3];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[2];
CX q[5],q[4];
CX q[6],q[7];
CX q[15],q[2];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[15];
U(pi/2,0,pi) q[2];
CX q[5],q[4];
CX q[8],q[7];
CX q[15],q[2];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[3],q[4];
CX q[8],q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[5],q[4];
CX q[8],q[7];
CX q[3],q[4];
CX q[8],q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[5],q[4];
CX q[6],q[7];
CX q[3],q[4];
CX q[6],q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
CX q[3],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[2],q[3];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[2],q[3];
CX q[6],q[5];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[7];
CX q[2],q[3];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[2],q[3];
CX q[6],q[7];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[8],q[7];
CX q[2],q[3];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[8],q[7];
CX q[2],q[3];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[2],q[3];
CX q[8],q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[2],q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
CX q[6],q[7];
CX q[3],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
CX q[6],q[7];
CX q[2],q[3];
CX q[8],q[7];
U(pi/2,0,pi) q[6];
CX q[3],q[4];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[9],q[8];
CX q[2],q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[2];
U(pi/2,0,pi) q[3];
CX q[6],q[5];
U(pi/2,0,pi) q[8];
CX q[2],q[3];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[5];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[6],q[7];
U(pi/2,0,pi) q[7];
CX q[6],q[5];
CX q[8],q[7];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[7],q[10];
CX q[6],q[5];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[10];
CX q[7],q[10];
CX q[5],q[4];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[10];
CX q[6],q[5];
CX q[7],q[10];
CX q[5],q[4];
CX q[9],q[10];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[9],q[8];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[9],q[10];
CX q[5],q[4];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[10];
CX q[9],q[10];
CX q[6],q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[10];
U(pi/2,0,pi) q[5];
CX q[9],q[10];
CX q[5],q[4];
CX q[9],q[8];
U(pi/2,0,pi) q[10];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[9];
CX q[5],q[4];
CX q[9],q[10];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[10];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[7],q[10];
CX q[5],q[4];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[10];
CX q[7],q[10];
CX q[6],q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[10];
CX q[6],q[5];
CX q[7],q[10];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[8],q[7];
CX q[6],q[5];
CX q[9],q[10];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[10];
CX q[6],q[5];
CX q[9],q[10];
U(pi/2,0,pi) q[5];
CX q[6],q[7];
U(pi/2,0,pi) q[9];
U(pi/2,0,pi) q[10];
CX q[5],q[4];
CX q[6],q[7];
CX q[9],q[10];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
CX q[8],q[7];
CX q[5],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[5],q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[8],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[6],q[7];
CX q[3],q[4];
CX q[8],q[7];
CX q[5],q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[8];
U(pi/2,0,pi) q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[3],q[4];
CX q[6],q[7];
CX q[5],q[4];
CX q[6],q[7];
CX q[3],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[8],q[7];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[3],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[7];
CX q[5],q[4];
CX q[6],q[7];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
CX q[3],q[4];
U(pi/2,0,pi) q[3];
U(pi/2,0,pi) q[4];
CX q[3],q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[5];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[5];
U(pi/2,0,pi) q[5];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
CX q[5],q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[5],q[4];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
CX q[6],q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[5];
CX q[6],q[11];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[11];
CX q[5],q[4];
CX q[6],q[11];
U(pi/2,0,pi) q[5];
U(pi/2,0,pi) q[4];
U(pi/2,0,pi) q[6];
U(pi/2,0,pi) q[11];
CX q[5],q[4];
CX q[6],q[11];
CX q[11],q[10];
CX q[7],q[10];
