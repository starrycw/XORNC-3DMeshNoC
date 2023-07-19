`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/18 21:24:26
// Design Name: 
// Module Name: arbiterNCModule_FwEncoded
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 用于判断已编码数据包的转发方向
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "design_params.vh "

module arbiterNCModule_FwEncoded_Win(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
        
    // Forward to W
    assign Forward_directions[`IDX_W] = 1'b0;
    
    // Forward to E
    assign Forward_directions[`IDX_E] = ( AddrCompare_P1[`IDX_E] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_E] & P2_YEqual & P2_ZEqual );
        
    // Forward to S
    assign Forward_directions[`IDX_S] = 1'b0;
    
    // Forward to N
    assign Forward_directions[`IDX_N] = 1'b0;
    
    // Forward to D
    assign Forward_directions[`IDX_D] = 1'b0;
    
    // Forward to U
    assign Forward_directions[`IDX_U] = 1'b0;
    
endmodule

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_FwEncoded_Ein(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
      
    // Forward to W
    assign Forward_directions[`IDX_W] = ( AddrCompare_P1[`IDX_W] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_W] & P2_YEqual & P2_ZEqual );
    
    // Forward to E
    assign Forward_directions[`IDX_E] = 1'b0;
        
    // Forward to S
    assign Forward_directions[`IDX_S] = 1'b0;
    
    // Forward to N
    assign Forward_directions[`IDX_N] = 1'b0;
    
    // Forward to D
    assign Forward_directions[`IDX_D] = 1'b0;
    
    // Forward to U
    assign Forward_directions[`IDX_U] = 1'b0;
    
endmodule

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_FwEncoded_Sin(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
      
    // Forward to W
    assign Forward_directions[`IDX_W] = ( AddrCompare_P1[`IDX_W] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_W] & P2_YEqual & P2_ZEqual );
    
    // Forward to E
    assign Forward_directions[`IDX_E] = ( AddrCompare_P1[`IDX_E] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_E] & P2_YEqual & P2_ZEqual );
        
    // Forward to S
    assign Forward_directions[`IDX_S] = 1'b0;
    
    // Forward to N
    assign Forward_directions[`IDX_N] = ( AddrCompare_P1[`IDX_N] ) | ( AddrCompare_P2[`IDX_N] );
    
    // Forward to D
    assign Forward_directions[`IDX_D] = ( P1_YEqual & AddrCompare_P1[`IDX_D] ) | ( P2_YEqual & AddrCompare_P2[`IDX_D] );
    
    // Forward to U
    assign Forward_directions[`IDX_U] = ( P1_YEqual & AddrCompare_P1[`IDX_U] ) | ( P2_YEqual & AddrCompare_P2[`IDX_U] );
    
endmodule

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_FwEncoded_Nin(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
      
    // Forward to W
    assign Forward_directions[`IDX_W] = ( AddrCompare_P1[`IDX_W] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_W] & P2_YEqual & P2_ZEqual );
    
    // Forward to E
    assign Forward_directions[`IDX_E] = ( AddrCompare_P1[`IDX_E] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_E] & P2_YEqual & P2_ZEqual );
        
    // Forward to S
    assign Forward_directions[`IDX_S] = ( AddrCompare_P1[`IDX_S] ) | ( AddrCompare_P2[`IDX_S] );
    
    // Forward to N
    assign Forward_directions[`IDX_N] = 1'b0;
    
    // Forward to D
    assign Forward_directions[`IDX_D] = ( P1_YEqual & AddrCompare_P1[`IDX_D] ) | ( P2_YEqual & AddrCompare_P2[`IDX_D] );
    
    // Forward to U
    assign Forward_directions[`IDX_U] = ( P1_YEqual & AddrCompare_P1[`IDX_U] ) | ( P2_YEqual & AddrCompare_P2[`IDX_U] );
    
endmodule

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_FwEncoded_Din(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
      
    // Forward to W
    assign Forward_directions[`IDX_W] = ( AddrCompare_P1[`IDX_W] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_W] & P2_YEqual & P2_ZEqual );
    
    // Forward to E
    assign Forward_directions[`IDX_E] = ( AddrCompare_P1[`IDX_E] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_E] & P2_YEqual & P2_ZEqual );
        
    // Forward to S
    assign Forward_directions[`IDX_S] = ( P1_ZEqual & AddrCompare_P1[`IDX_S] & AddrCompare_P2[`IDX_N] ) | ( P2_ZEqual & AddrCompare_P2[`IDX_S] & AddrCompare_P1[`IDX_N] );
    
    // Forward to N
    assign Forward_directions[`IDX_N] = ( P1_ZEqual & AddrCompare_P1[`IDX_N] & AddrCompare_P2[`IDX_S] ) | ( P2_ZEqual & AddrCompare_P2[`IDX_N] & AddrCompare_P1[`IDX_S] );
    
    // Forward to D
    assign Forward_directions[`IDX_D] = 1'b0 ;
    
    // Forward to U
    assign Forward_directions[`IDX_U] = ( AddrCompare_P1[`IDX_U] ) | ( AddrCompare_P2[`IDX_U] );
    
endmodule

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_FwEncoded_Uin(
    input wire [6 : 0] AddrCompare_P1, AddrCompare_P2,
    output wire [6 : 0] Forward_directions
    );
    
    wire P1_YEqual = (~AddrCompare_P1[`IDX_S]) & (~AddrCompare_P1[`IDX_N]);
    wire P2_YEqual = (~AddrCompare_P2[`IDX_S]) & (~AddrCompare_P2[`IDX_N]);
    wire P1_ZEqual = (~AddrCompare_P1[`IDX_D]) & (~AddrCompare_P1[`IDX_U]);
    wire P2_ZEqual = (~AddrCompare_P2[`IDX_D]) & (~AddrCompare_P2[`IDX_U]);
    
    // Forward to IP 
    assign Forward_directions[`IDX_IP] = ( AddrCompare_P1[`IDX_IP] ) | ( AddrCompare_P2[`IDX_IP] );
      
    // Forward to W
    assign Forward_directions[`IDX_W] = ( AddrCompare_P1[`IDX_W] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_W] & P2_YEqual & P2_ZEqual );
    
    // Forward to E
    assign Forward_directions[`IDX_E] = ( AddrCompare_P1[`IDX_E] & P1_YEqual & P1_ZEqual ) | ( AddrCompare_P2[`IDX_E] & P2_YEqual & P2_ZEqual );
        
    // Forward to S
    assign Forward_directions[`IDX_S] = ( P1_ZEqual & AddrCompare_P1[`IDX_S] & AddrCompare_P2[`IDX_N] ) | ( P2_ZEqual & AddrCompare_P2[`IDX_S] & AddrCompare_P1[`IDX_N] );
    
    // Forward to N
    assign Forward_directions[`IDX_N] = ( P1_ZEqual & AddrCompare_P1[`IDX_N] & AddrCompare_P2[`IDX_S] ) | ( P2_ZEqual & AddrCompare_P2[`IDX_N] & AddrCompare_P1[`IDX_S] );
    
    // Forward to D
    assign Forward_directions[`IDX_D] = ( AddrCompare_P1[`IDX_D] ) | ( AddrCompare_P2[`IDX_D] );
    
    // Forward to U
    assign Forward_directions[`IDX_U] = 1'b0;
    
endmodule
