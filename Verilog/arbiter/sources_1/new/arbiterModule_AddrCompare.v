`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/18 15:15:20
// Design Name: 
// Module Name: arbiterModule_AddrCompare
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "design_params.vh "

module arbiterModule_AddrCompare(
    input wire [`FLIT_AddressLenX -1 : 0] Local_AddrX, Desti_AddrX,
    input wire [`FLIT_AddressLenY -1 : 0] Local_AddrY, Desti_AddrY,
    input wire [`FLIT_AddressLenZ -1 : 0] Local_AddrZ, Desti_AddrZ,
    output wire [6 : 0] AddrDiff   
    );
    
    // Addr X
    assign AddrDiff[`IDX_E] = (Desti_AddrX > Local_AddrX) ? (1'b1) : (1'b0);  // E
    assign AddrDiff[`IDX_W] = (Desti_AddrX < Local_AddrX) ? (1'b1) : (1'b0);  // W
     
     // Addr Y
    assign AddrDiff[`IDX_N] = (Desti_AddrY > Local_AddrY) ? (1'b1) : (1'b0);  // N
    assign AddrDiff[`IDX_S] = (Desti_AddrY < Local_AddrY) ? (1'b1) : (1'b0);  // S
    
    // Addr Z
    assign AddrDiff[`IDX_U] = (Desti_AddrZ > Local_AddrZ) ? (1'b1) : (1'b0);  // U
    assign AddrDiff[`IDX_D] = (Desti_AddrZ < Local_AddrZ) ? (1'b1) : (1'b0); // D
    
    // Desti = Local
    assign AddrDiff[`IDX_IP] = ~( AddrDiff[`IDX_E] | AddrDiff[`IDX_W] | AddrDiff[`IDX_N] | AddrDiff[`IDX_S] | AddrDiff[`IDX_U] | AddrDiff[`IDX_D] );
    
    
endmodule
