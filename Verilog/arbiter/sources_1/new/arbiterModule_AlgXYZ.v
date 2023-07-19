`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/18 21:00:37
// Design Name: 
// Module Name: arbiterModule_AlgXYZ
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 根据XYZ路由策略，确定数据包的转发方向，未考虑fifo状态
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "design_params.vh "

module arbiterModule_AlgXYZ(
    input wire [6 : 0] AddrDiff,
    output wire [6 : 0] Forward_direction
    );
        
    assign Forward_direction[`IDX_IP] = AddrDiff[`IDX_IP];
    
    assign Forward_direction[`IDX_W] = AddrDiff[`IDX_W];
    assign Forward_direction[`IDX_E] = AddrDiff[`IDX_E];
    
    assign Forward_direction[`IDX_S] = ( (~Forward_direction[`IDX_W]) & (~Forward_direction[`IDX_E]) & (AddrDiff[`IDX_S]) );
    assign Forward_direction[`IDX_N] = ( (~Forward_direction[`IDX_W]) & (~Forward_direction[`IDX_E]) & (AddrDiff[`IDX_N]) );
    
    assign Forward_direction[`IDX_D] = ( (~Forward_direction[`IDX_W]) & (~Forward_direction[`IDX_E]) & (~Forward_direction[`IDX_S]) & (~Forward_direction[`IDX_N]) & (AddrDiff[`IDX_D]) );
    assign Forward_direction[`IDX_U] = ( (~Forward_direction[`IDX_W]) & (~Forward_direction[`IDX_E]) & (~Forward_direction[`IDX_S]) & (~Forward_direction[`IDX_N]) & (AddrDiff[`IDX_U]) );
    
endmodule
